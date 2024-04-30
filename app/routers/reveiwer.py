from datetime import datetime
from fastapi import APIRouter, Form, Request
from pydantic import EmailStr

from app.repository.reviewer import ReviewerRepository
import app.schemas as schemas
from app.utils.enums import Status

router = APIRouter()

#todo: переработать на получение информации из HTTP-запроса (закомментированный код именно для этого)
@router.post("/reviews/actions/create_review")
async def create_review(
    # request: Request,
    # Данные, передаваемые пользователем
    # review_text: str = Form(...),
    # email: EmailStr = Form(None),
    # name: str = Form(None),
    # lastname: str = Form(None)

    review_text: str,
    email: EmailStr,
    name: str,
    lastname: str
    ):

    new_review = schemas.AddReview(
        # datetime.now(timezone.utc).strftime('%d.%m.%Y - %H:%M')
        review_creation_date = datetime.now(),
        review_status = Status.Created,
        review_text = review_text,
        email = email,
        name = name,
        lastname = lastname
    )

    await ReviewerRepository.AddReview(new_review)