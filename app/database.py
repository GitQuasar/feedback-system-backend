from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.configs.config import settings

async_engine = create_async_engine(
    url = settings.DATABASE_URL_async,
    # Дебаг: вывод всех запросов алхимии к БД
    # echo=True
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False)

# Базовая модель, от которой наследуются остальные модели
class Base(DeclarativeBase):
    pass

# Асинхронная функция для СОЗДАНИЯ таблиц
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Асинхронная функция для УДАЛЕНИЯ таблиц
async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)