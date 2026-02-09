from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security
from database import get_session
from models.users import User


async def get_current_user(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
) -> User:
    user_id = int(current_user.sub)

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()  # User type
    return user
