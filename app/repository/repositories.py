# Здесь будет описываться логика для взаимодействия с БД
from sqlalchemy import select
from app.database import new_session
import app.schemas as schemas
import app.models as models

class AdminRepository:

    @classmethod
    async def GetStaff(cls):
        async with new_session() as session:
            query = select(models.StaffORM)
            result = await session.execute(query)
            staff = result.scalars().all()
            if not staff:
                return "No data"
            return staff
    
    @classmethod
    async def GetStaffById(cls, id):
        async with new_session() as session:
            query = select(models.StaffORM).where(models.StaffORM.id == id)
            result = await session.execute(query)
            staff = result.scalars().first()
            if staff is None:
                return "Not found"
            return staff
    
    @classmethod
    async def AddStaff(cls, data: schemas.AddStaff):
        async with new_session() as session:
            staff_dict = data.model_dump()
            staff = models.StaffORM(**staff_dict)
            session.add(staff)
            await session.flush()
            await session.commit()
            return staff.id
        
    @classmethod
    async def DeleteStaff(cls, id):
        async with new_session() as session:
            query = select(models.StaffORM).where(models.StaffORM.id == id)
            result = await session.execute(query)
            staff = result.scalars().first()
            if staff is None:
                return "Not found"
            await session.delete(staff)
            await session.commit()
            return "Success"

#todo: реализовать функционал менеджера для взаимодействия с БД
class ManagerRepository:
    pass

class ReviewerRepository:

    @classmethod
    async def AddReview(cls, data: schemas.AddReview):
        async with new_session() as session:
            review_dict = data.model_dump()
            review = models.ReviewsRegistryORM(**review_dict)
            session.add(review)
            await session.flush()
            await session.commit()
            return review.id

#todo: реализовать функционал для аутентификации
class AuthRepository:
    pass