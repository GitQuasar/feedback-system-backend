from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ReviewsRegistryORM
from app.schemas import ManagerReply

class ManagerRepository:
    @classmethod
    async def GetReviewsOnPage(cls, session: AsyncSession, limit: int, page: int):
        query = select(ReviewsRegistryORM).order_by(desc(ReviewsRegistryORM.id))
        result = await session.execute(query)
        reviews_on_page = result.scalars().all()[page*limit:][:limit]
        return reviews_on_page
    
    @classmethod
    async def GetReviewByID(cls, session: AsyncSession, id: int):
        review = await session.get(ReviewsRegistryORM, id)
        return review
    
    @classmethod
    async def AddReplyOnReviewByID(cls, session: AsyncSession, review_id: int, manager_reply: ManagerReply):

        review_in_db = await session.get(ReviewsRegistryORM, review_id)
        if review_in_db.manager_reply_text == manager_reply.manager_reply_text:
            return None
        
        reply_data = manager_reply.model_dump()

        for key, value in reply_data.items():
            setattr(review_in_db, key, value)
        
        await session.commit()
        
        return review_in_db
