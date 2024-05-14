from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr, UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repository.reviewer import ReviewerRepository
from app.schemas import AddReview, Review
from app.utils.enums import Status
from app import http_exceptions as http_e


router = APIRouter()

@router.post(
        path="/reviews/actions/create_review",
        response_model=str
        )
async def create_review(
    review_text: str = Form(min_length=16, max_length=255),
    # Опциональные для заполнения заявителем поля
    email: EmailStr = Form(default=None),
    first_name: str = Form(default=None, min_length=2, max_length=32),
    last_name: str = Form(default=None, min_length=2, max_length=32),
    patronymic: str = Form(default=None, min_length=2, max_length=32),
    department: str = Form(default=None, min_length=2, max_length=64, description="Department of... "),
    session: AsyncSession = Depends(get_async_session)
    ):

    review = AddReview(
        # Красивый вывод: datetime.now(timezone.utc).strftime('%d.%m.%Y - %H:%M')
        review_creation_date = datetime.utcnow(),
        review_status = Status.Created,
        review_text = review_text,
        email = email,
        first_name = first_name,
        last_name = last_name,
        patronymic = patronymic,
        department = department
    )

    review_uuid = await ReviewerRepository.AddReview(session, review)
    return str(review_uuid)

@router.get(
        path="/reviews/actions/see_review/{id}",
        response_model=Review
        )
async def see_review_by_uuid(
    uuid: UUID4,
    session: AsyncSession = Depends(get_async_session)
    ):

    review = await ReviewerRepository.GetReviewByUUID(session, uuid)
    if review is None:
        raise http_e.ReviewNotFoundException
    return review