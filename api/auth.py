from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from core.security import hash_password, verify_password
from models.users import User
from schemas.auth.login import UserLoginSchema
from schemas.auth.register import UserRegisterSchema
from database import engine, Base, get_session
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta

router = APIRouter()

# JWT AuthX settings
config = AuthXConfig()
config.JWT_SECRET_KEY = "super_secret_key_min_32_chars_long_here!!!"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_REFRESH_COOKIE_NAME = "my_refresh_token"
config.JWT_TOKEN_LOCATION = ["cookies", "headers"]
config.JWT_HEADER_NAME = "Authorization"
config.JWT_HEADER_TYPE = "Bearer"
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
config.JWT_COOKIE_CSRF_PROTECT = False  # Development mode
config.JWT_COOKIE_SECURE = False  # Use secure cookies only in production

security = AuthX(config=config)


@router.post("/refresh", summary="Refresh access token", tags=["Auth 🔐"])
async def refresh_token(response: Response, refresh_data=Depends(security.refresh_token_required)):
    new_access_token = security.create_access_token(uid=refresh_data.sub)
    security.set_access_cookies(new_access_token, response)
    return {"access_token": new_access_token}

# Dev endpoint to setup database. Drop all tables and create new ones.
@router.post(
    "/setup_database",
    summary="create database",
    description="⚠️ DELETE ALL and create new db. Use for development only",
    tags=["Development ⚙️"]
)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}


@router.post(
    "/register",
    summary="Register new user",
    description="Creates a new user account with username, email and password",
    tags=["Auth 🔐"]
)
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
            detail="User with this username or email already exists"
        )

    # check password
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
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
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username,
    }


@router.post(
    "/login",
    summary="User login",
    description="Authenticates user and returns JWT token. Sets HTTP-only cookie.",
    tags=["Auth 🔐"]
)
async def login(creds: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_session)):
    # find user
    result = await session.execute(
        select(User).where(User.username == creds.username)
    )
    user = result.scalar_one_or_none()

    # check password
    if not user or not verify_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = security.create_access_token(uid=str(user.id))
    refresh_token = security.create_refresh_token(uid=str(user.id))

    security.set_access_cookies(access_token, response)
    security.set_refresh_cookies(refresh_token, response)

    # last_seen
    user.last_seen = datetime.utcnow()
    await session.commit()

    return {
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username
    }


@router.post(
    "/logout",
    summary="User logout",
    description="Logout from user account. Delete JWT-cookie",
    tags=["Auth 🔐"]
)
async def logout(response: Response):
    security.unset_cookies(response)
    return {
        "message": "successfully logged out"
    }


