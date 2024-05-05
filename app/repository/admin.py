from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import StaffORM
from app.schemas import AddStaff
from app.utils.pswd_helper import hash_password

class AdminRepository:
    @classmethod
    async def GetStaff(cls, session: AsyncSession):
        result = await session.execute(select(StaffORM))
        staff = result.scalars().all()
        return staff
    
    @classmethod
    async def GetStaffById(cls, session: AsyncSession, id: int):
        staff_by_id = await session.get(StaffORM, id)
        return staff_by_id
    
    @classmethod
    async def AddStaff(cls, staff_data: AddStaff, session: AsyncSession):
        staff_data_dict = staff_data.model_dump()
        password = staff_data_dict.pop("password")
        staff_data_dict["hashed_password"] = hash_password(password)

        new_staff = StaffORM(**staff_data_dict)
        session.add(new_staff)
        await session.flush()
        await session.commit()
        
    @classmethod
    async def DeleteStaffByID(cls, id: int, session: AsyncSession):
        to_delete = (await session.execute(select(StaffORM).where(StaffORM.id == id))).scalars().first()
        if to_delete is None:
            return None
        await session.delete(to_delete)
        await session.commit()
        return to_delete