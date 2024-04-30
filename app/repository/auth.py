from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StaffORM
from app.schemas import StaffAuth
from app.utils.password_helper import verify_password
from app.utils import jwt_helper
from app import http_exceptions

class AuthRepository:
    # Учётные данные верны - вернёт токен, где будет указан ID пользователя
    # Иначе вызовет исключение.
    async def UserAuthenticate(user_credentials: StaffAuth, session: AsyncSession) -> str:
        query = select(StaffORM).where(StaffORM.email == user_credentials.email)
        user = (await session.execute(query)).scalars().first()

        # Проверяем, есть ли вообще пользователь с введенными учетными данными в БД
        if not user:
            raise http_exceptions.UserNotFoundException
        if not verify_password(user_credentials.password, user.hashed_password):
            raise http_exceptions.InvalidCredentialsException
        
        token = jwt_helper.create_access_token({"id": user.id})
        return token