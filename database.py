from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from typing import Annotated

# database
engine = create_async_engine("sqlite+aiosqlite:///weiqi.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    session = new_session()
    try:
        yield session
    finally:
        await session.close()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Base (SQLAlchemy)
class Base(DeclarativeBase):
    pass
