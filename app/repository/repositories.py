# Здесь будет описываться логика для взаимодействия с БД
from datetime import datetime
from sqlalchemy import select
from app.database import new_session
import app.schemas as schemas
import app.models as models
from sqlalchemy import desc

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
    @classmethod
    async def see_Review(cls, id: int):
        async with new_session() as session:
            query = select(models.ReviewsRegistryORM).where(models.ReviewsRegistryORM.id == id)
            result = await session.execute(query)
            review = result.scalars().all()

            if not review:
                return "Review not found"
            return review
    
    @classmethod
    async def add_reply(cls, id: int, reply_text: str, manager_id: int):
        async with new_session() as session:
            reply = await session.get(models.ReviewsRegistryORM, id)
            check_reply = reply.manager_reply_text
            reply.manager_reply_text = reply_text
            reply.replied_manager_id = manager_id
            reply.manager_reply_datetime = datetime.now()
            reply.review_status = 3
            await session.commit()
            
            if check_reply == reply.manager_reply_text:
                return "Error! Replay was not published"
            return reply.review_status
        
    @classmethod
    async def get_replied_on_page(cls, limit: int, page: int):
        async with new_session() as session:
            query = select(models.ReviewsRegistryORM).order_by(desc(models.ReviewsRegistryORM.id))
            result = await session.execute(query)
            page_reviews = result.scalars().all()[page*limit:][:limit]
            return page_reviews

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