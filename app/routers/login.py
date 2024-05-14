from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_async_session
from app import http_exceptions as http_e
from app.repository.auth import authenticate_user
from app.schemas import TokenInfo
from app.utils.enums import Role
from app.utils.jwt_helper import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/token", response_model=TokenInfo)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session)
    ):
    user = await authenticate_user(session, email=form_data.username, password=form_data.password)

    # Бросаем исключение, если (либо...либо):
    # Пользователя нет в БД, введённые данные неверны
    if not user: raise http_e.InvalidCredentialsException
    role: str = Role.Admin if user.is_admin == True else Role.Manager 

    token_payload = {
        # "sub" (subject) - то, о ком этот токен (будем использовать ID пользователя)
        "sub": str(user.id),
        "email": user.email
    }

    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)
    
    return TokenInfo(type="Bearer", role=role, access_token=access_token, refresh_token=refresh_token)