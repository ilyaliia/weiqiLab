import asyncio
from database import engine, Base


async def init_db():
    """Создать все таблицы в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована!")


if __name__ == "__main__":
    asyncio.run(init_db())
