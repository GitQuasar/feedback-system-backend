from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ReviewsRegistryORM
from app.schemas import AddReview


class ReviewerRepository:
    @classmethod
    async def AddReview(cls, session: AsyncSession, data: AddReview):
        review_dict = data.model_dump()
        review = ReviewsRegistryORM(**review_dict)
        session.add(review)
        await session.flush()
        await session.commit()
        return review