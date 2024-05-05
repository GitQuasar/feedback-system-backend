from datetime import datetime
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repository.reviewer import ReviewerRepository
from app.schemas import AddReview
from app.utils.enums import Status


router = APIRouter()

@router.post("/reviews/actions/create_review")
async def create_review(
    review_text: str = Form(min_length=16, max_length=255),
    # Опциональные для заполнения заявителем поля
    email: Optional[EmailStr] = Form(default=None),
    name: Optional[str] = Form(default=None, min_length=2, max_length=32),
    lastname: Optional[str] = Form(default=None, min_length=2, max_length=32),
    session: AsyncSession = Depends(get_async_session)
    ):

    review = AddReview(
        # Красивый вывод: datetime.now(timezone.utc).strftime('%d.%m.%Y - %H:%M')
        review_creation_date = datetime.utcnow(),
        review_status = Status.Created,
        review_text = review_text,
        email = email,
        name = name,
        lastname = lastname
    )

    review = await ReviewerRepository.AddReview(session, review)
    return {"id": f"{review.id}"}