from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import StaffORM
from app.utils.jwt_helper import decode_jwt
from app.utils.pswd_helper import verify_password
from app import http_exceptions as http_e


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/token"
)

# Функция-помощник, возвращает пользователя из БД по email (иначе None)
async def get_user_from_database(session: AsyncSession, email: EmailStr):
    query = select(StaffORM).where(StaffORM.email == email)
    result = await session.execute(query)
    user = result.scalars().first()
    return user if user else None

# Аутентификация пользователя
# Проверка на наличие пользователя с введенными учетными данными в БД
async def authenticate_user(session: AsyncSession, email: EmailStr, password: str):
    user = await get_user_from_database(session, email)
    # Возвращаем пользователя, если он существует и ввёл верные данные
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# Зависимость для получения текущего пользователя из БД по полученному токену
async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme)
    ):
    payload: dict
    email: EmailStr
    try:
        payload = decode_jwt(token)
        email = payload.get("email")
        if email is None:
            raise http_e.InvalidCredentialsException
    except JWTError:
        raise http_e.InvalidTokenException
    
    current_user = await get_user_from_database(session, email=email)
    if current_user is None:
        raise http_e.InvalidCredentialsException
    return current_user

# Получение текущего активного пользователя из БД по токену
async def get_current_active_user(current_user: StaffORM = Depends(get_current_user)):
    if not current_user.is_active:
        raise http_e.InactiveUserException
    return current_user

# Получение текущего активного админа
async def get_current_active_administrator(
    current_active_user: StaffORM = Depends(get_current_active_user)
    ):
    if not current_active_user.is_admin:
        raise http_e.UnauthorizedException
    return current_active_user

# Получение текущего активного менеджера
async def get_current_active_manager(
    current_active_user: StaffORM = Depends(get_current_active_user)
    ):
    if not current_active_user.is_manager:
        raise http_e.UnauthorizedException
    return current_active_user