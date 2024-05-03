from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.models import StaffORM
from app.schemas import AddStaff
from app.utils.pswd_helper import hash_password

class AdminRepository:
    @classmethod
    async def GetStaff(cls):
        async with async_session() as session:
            query = select(StaffORM)
            result = await session.execute(query)
            staff = result.scalars().all()
            if not staff:
                return "No data"
            return staff
    
    @classmethod
    async def GetStaffById(cls, id):
        async with async_session() as session:
            query = select(StaffORM).where(StaffORM.id == id)
            result = await session.execute(query)
            staff = result.scalars().first()
            if staff is None:
                return "Not found"
            return staff
    
    @classmethod
    async def AddStaff(cls, data: AddStaff, session: AsyncSession):
        staff_dict = data.model_dump()
        password = staff_dict.pop("password")
        staff_dict["hashed_password"] = hash_password(password)

        staff = StaffORM(**staff_dict)
        session.add(staff)
        await session.flush()
        await session.commit()
        return staff.id
        
    @classmethod
    async def DeleteStaff(cls, id):
        async with async_session() as session:
            query = select(StaffORM).where(StaffORM.id == id)
            result = await session.execute(query)
            staff = result.scalars().first()
            if staff is None:
                return "Not found"
            await session.delete(staff)
            await session.commit()
            return "Success"