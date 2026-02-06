from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from api.security import hash_password, verify_password
from models.users import User
from schemas.auth.login import UserLoginSchema
from schemas.auth.register import UserRegisterSchema
from database import engine, Base, get_session
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

router = APIRouter()

# JWT AuthX settings
config = AuthXConfig()
config.JWT_SECRET_KEY = "super_secret_key_min_32_chars_long_here!!!"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = "HS256"

security = AuthX(config=config)


# database setup
@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}


@router.get("/profile")
async def get_profile(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    user_id_str = current_user.sub  # user_id from token
    user_id = int(user_id_str)

    # search user by id
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one()  # user obj

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


# Auth
@router.post("/reg")
async def reg(
        user_data: UserRegisterSchema,
        session: AsyncSession = Depends(get_session)
):
    # check user exist
    result = await session.execute(
        select(User).where(
            (User.username == user_data.username) |
            (User.email == user_data.email)
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем или email уже существует"
        )

    # check password
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Пароли не совпадают"
        )

    # hash password
    password_hash = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
    )

    # db refresh
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {
        "message": "Пользователь создан",
        "user_id": new_user.id,
        "username": new_user.username,
    }


@router.post("/login")
async def login(creds: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_session)):
    # find user
    result = await session.execute(
        select(User).where(User.username == creds.username)
    )
    user = result.scalar_one_or_none()

    # check password
    if not user or not verify_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = security.create_access_token(uid=str(user.id))

    response.set_cookie(
        key="my_access_token",
        value=token,
        httponly=True
    )

    # last_seen
    user.last_seen = datetime.utcnow()
    await session.commit()

    return {
        "access_token": token,
        "user_id": user.id,
        "username": user.username
    }
