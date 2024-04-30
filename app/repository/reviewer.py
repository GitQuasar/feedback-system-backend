from app.database import async_session
from app.models import ReviewsRegistryORM
from app.schemas import AddReview

class ReviewerRepository:
    @classmethod
    async def AddReview(cls, data: AddReview):
        async with async_session() as session:
            review_dict = data.model_dump()
            review = ReviewsRegistryORM(**review_dict)
            session.add(review)
            await session.flush()
            await session.commit()
            return review.id