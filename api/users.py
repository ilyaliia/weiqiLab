from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models.users import User
from schemas.users.base import UserBaseSchema

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
