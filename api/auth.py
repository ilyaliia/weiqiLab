from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from models.users import User
from schemas.users import UserLoginSchema
from database import engine, Base, get_session
from sqlalchemy.ext.asyncio import AsyncSession

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
async def reg(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password  # No hash
    )

    # save in db
    session.add(new_user)
    await session.commit()

    return {"message": "User created", "username": user_data.username}


@router.post("/login")
async def login(creds: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.username == creds.username)
    )
    user = result.scalar_one_or_none()

    if user and user.password == creds.password:
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token, "user_id": user.id}

    raise HTTPException(status_code=401, detail="Incorrect username or password")
