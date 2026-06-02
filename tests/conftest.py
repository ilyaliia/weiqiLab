import asyncio

import pytest
from database import engine, Base


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create tables for tests before any requests run."""

    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_create())
    yield

    async def _drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(_drop())
