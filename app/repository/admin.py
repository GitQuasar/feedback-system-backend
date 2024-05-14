from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StaffORM
from app.schemas import AddStaff, UpdateStaff
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
    async def AddStaff(cls, staff_data: AddStaff, session: AsyncSession) -> StaffORM:
        staff_data_dict = staff_data.model_dump()
        password = staff_data_dict.pop("password")
        staff_data_dict["hashed_password"] = hash_password(password)

        new_staff = StaffORM(**staff_data_dict)
        session.add(new_staff)
        await session.flush()
        await session.commit()
        return new_staff
        
    @classmethod
    async def DeleteStaffByID(cls, id: int, session: AsyncSession):
        staff_in_db = await session.get(StaffORM, id)
        if staff_in_db is None: return None
        await session.delete(staff_in_db)
        await session.commit()
        return staff_in_db
    
    @classmethod
    async def UpdateStaffByID(
        cls,
        id: int,
        session: AsyncSession,
        update_data: UpdateStaff
        ):
        
        staff_in_db = await session.get(StaffORM, id)
        if staff_in_db is None: return None
        
        update_dict = update_data.model_dump()
        for key, value in update_dict.items():
            if value: setattr(staff_in_db, key, value)
        
        await session.commit()

        return staff_in_db
        