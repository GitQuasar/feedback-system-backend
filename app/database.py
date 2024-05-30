from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.configs.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_ASYNC)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# Генератор асинхронных сессий
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

# Базовая модель, от которой наследуются остальные модели
class Base(DeclarativeBase):
    pass