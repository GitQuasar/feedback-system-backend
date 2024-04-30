from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from app.schemas import StaffAuth
from app.repository.auth import AuthRepository
from app.repository.dependency_injection import GetCurrentUser
from app.database import get_async_session
router = APIRouter()

@router.post("/auth")
async def staff_auth(email: EmailStr, password: str, session: AsyncSession = Depends(get_async_session)):
    credentials = StaffAuth(email=email, password=password)
    token = await AuthRepository.UserAuthenticate(credentials, session)
    return {"token": token}

@router.post("/staff/lk")
async def get_current_user(
    token: str,
    session: AsyncSession = Depends(get_async_session)
    ):
    current_user = await GetCurrentUser(token, session)
    return {"current_user": current_user}