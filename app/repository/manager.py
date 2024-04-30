from sqlalchemy import select
from datetime import datetime
from sqlalchemy import desc

from app.database import async_session
from app.models import ReviewsRegistryORM

class ManagerRepository:
    @classmethod
    async def GetReview(cls, id: int):
        async with async_session() as session:
            query = select(ReviewsRegistryORM).where(ReviewsRegistryORM.id == id)
            result = await session.execute(query)
            review = result.scalars().all()

            if not review:
                return "Review not found"
            return review
    
    @classmethod
    async def GetReviewsOnPage(cls, limit: int, page: int):
        async with async_session() as session:
            query = select(ReviewsRegistryORM).order_by(desc(ReviewsRegistryORM.id))
            result = await session.execute(query)
            reviews_on_page = result.scalars().all()[page*limit:][:limit]
            return reviews_on_page
    
    @classmethod
    async def AddReply(cls, id: int, reply_text: str, manager_id: int):
        async with async_session() as session:
            reply = await session.get(ReviewsRegistryORM, id)
            check_reply = reply.manager_reply_text
            reply.manager_reply_text = reply_text
            reply.replied_manager_id = manager_id
            reply.manager_reply_datetime = datetime.now()
            reply.review_status = 3
            await session.commit()
            
            # хз, что здесь вообще происходит...
            if check_reply == reply.manager_reply_text:
                return "Error! Reply was not published"
            return reply.review_status
