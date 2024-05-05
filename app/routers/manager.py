from datetime import datetime
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StaffORM
from app.repository.auth import get_current_active_manager
from app.repository.manager import ManagerRepository
from app.database import get_async_session
from app.schemas import ManagerReply, ReadStaff
from app import http_exceptions as http_e
from app.utils.enums import Status

router = APIRouter()

@router.get("/manager/pc/", response_model=ReadStaff)
async def read_current_manager_pc(current_manager: StaffORM = Depends(get_current_active_manager)):
    return current_manager

@router.get("/manager/actions/see_reviews", dependencies=[Depends(get_current_active_manager)])
async def see_reviews_on_page(
    limit: int,
    page: int,
    session: AsyncSession = Depends(get_async_session)
    ):

    reviews_on_page = await ManagerRepository.GetReviewsOnPage(session, limit, page-1)
    return {"reviews_on_page": reviews_on_page}

@router.get("/manager/actions/see_reviews/{id}", dependencies=[Depends(get_current_active_manager)])
async def see_review_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
    ):

    review = await ManagerRepository.GetReviewByID(session, id)
    if review is None:
        raise http_e.ReviewNotFoundException
    return {"review": review}

@router.post("/manager/actions/add_reply")
async def create_manager_reply(
    reply_text: str = Form(min_length=16, max_length=255),
    review_id: int = Form(),
    current_user: StaffORM = Depends(get_current_active_manager),
    session: AsyncSession = Depends(get_async_session)
    ):

    manager_reply = ManagerReply(
        review_status = Status.Replied,
        replied_manager_id = current_user.id,
        manager_reply_text = reply_text,
        manager_reply_datetime = datetime.utcnow()
    )

    review_updated = await ManagerRepository.AddReplyOnReviewByID(session, review_id, manager_reply)
    if review_updated is None:
        return {"message" : "Review was not changed due to similar reply text"}
    return {"review_updated": review_updated}

