from app.models import StaffORM
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StaffORM
from app.utils import jwt_helper
from app import http_exceptions

async def GetCurrentUser(
        token: str,
        session: AsyncSession
        ):
        payload = jwt_helper.decode_and_verify_token(token)
        user_id = payload.get("id")
        if user_id is None:
            raise http_exceptions.InvalidCredentialsException
        user = await session.get(StaffORM, user_id)
        if user is None:
            raise http_exceptions.UserNotFoundException
        return user