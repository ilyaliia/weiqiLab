from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from database import get_session
from models.users import User
from schemas.users.base import UserBaseSchema
from schemas.users.update import UserUpdateSchema

router = APIRouter()


@router.get(
    "/users/{username}",
    response_model=UserBaseSchema,
    summary="Get user profile by username",
    description="Returns public user profile by username",
    tags=["Users 👤"]
)
async def get_user_by_name(
    username: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user


@router.post(
    "/profile",
    # response_model=UserBaseSchema,
    summary="Update user profile",
    description="Update bio, avatar, country, language.",
    tags=["Users 👤"])
async def update_profile(
        update_data: UserUpdateSchema,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    if update_data.avatar_url is not None:
        current_user.avatar_url = update_data.avatar_url
    if update_data.bio is not None:
        current_user.bio = update_data.bio
    if update_data.country is not None:
        current_user.country = update_data.country
    if update_data.language is not None:
        current_user.language = update_data.language

    await session.commit()
    return {"updated": True}

