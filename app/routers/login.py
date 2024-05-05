from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import get_async_session
from app import http_exceptions as http_e
from app.models import StaffORM
from app.repository.auth import authenticate_user, get_current_active_administrator, get_current_active_manager
from app.schemas import ReadStaff, TokenInfo
from app.utils.jwt_helper import create_access_token

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
    
    payload = {
        # "sub" (subject) - то, о ком этот токен (будем использовать ID пользователя)
        # "sub" обязательно должен содержать СТРОКУ
        "sub": str(user.id),
        "email" : user.email,
        "name" : user.name,
        "lastname" : user.lastname
    }

    token = create_access_token(payload)
    
    return TokenInfo(type = "Bearer", access_token = token)

@router.get("/manager/pc/", response_model=ReadStaff)
async def read_current_manager_pc(
    current_manager: StaffORM = Depends(get_current_active_manager)
    ):
    return current_manager