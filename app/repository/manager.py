from sqlalchemy import select, desc, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ReviewsRegistryORM
from app.schemas import ManagerReply
from app.configs.config import settings

class ManagerRepository:
    @classmethod
    async def GetReviewsOnPage(
        cls,
        session: AsyncSession,
        # page: int,
        # limit: int | None = settings.REVIEWS_ON_PAGE_LIMIT
        ):
        query = select(ReviewsRegistryORM).order_by(desc(ReviewsRegistryORM.review_creation_date))
        result = await session.execute(query)
        # reviews_on_page = result.scalars().all()[page*limit:][:limit]
        reviews_on_page = result.scalars().all()
        return reviews_on_page
    
    @classmethod
    async def GetReviewByUUID(cls, session: AsyncSession, uuid: UUID):
        review = await session.get(ReviewsRegistryORM, uuid)
        return review
    
    @classmethod
    async def AddReplyOnReviewByUUID(
        cls,
        session: AsyncSession,
        review_uuid: UUID,
        manager_reply: ManagerReply
        ):

        review_in_db = await session.get(ReviewsRegistryORM, review_uuid)
        if review_in_db is None: return None
        
        reply_data = manager_reply.model_dump()

        for key, value in reply_data.items():
            setattr(review_in_db, key, value)
        
        await session.commit()
        
        return review_in_db
