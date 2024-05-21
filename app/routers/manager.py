from datetime import datetime
from typing import List
from pydantic import UUID4
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StaffORM
from app.repository.auth import get_current_active_manager
from app.repository.manager import ManagerRepository
from app.database import get_async_session
from app.schemas import ManagerReply, ReadStaff, Review
from app import http_exceptions as http_e
from app.utils.enums import Status

router = APIRouter()

@router.get(
        path="/manager/pc/",
        response_model=ReadStaff
        )
async def read_current_manager_pc(current_manager: StaffORM = Depends(get_current_active_manager)):
    return current_manager

@router.get(
        path="/manager/actions/see_reviews",
        dependencies=[Depends(get_current_active_manager)],
        # response_model=List[Review]
        )
async def see_reviews_on_page(
    # page: int | None = 1,
    session: AsyncSession = Depends(get_async_session)
    ):
    reviews_on_page = await ManagerRepository.GetReviewsOnPage(session)
    return {"reviews": reviews_on_page}

@router.get(
        path="/manager/actions/see_reviews/{id}",
        dependencies=[Depends(get_current_active_manager)],
        response_model=Review
        )
async def see_review_by_uuid(
    uuid: UUID4,
    session: AsyncSession = Depends(get_async_session)
    ):
    review = await ManagerRepository.GetReviewByUUID(session, uuid)
    if review is None:
        raise http_e.ReviewNotFoundException
    return review

@router.post(
        path="/manager/actions/add_reply",
        response_model=Review
        )
async def create_manager_reply(
    review_uuid: UUID4,
    reply_text: str = Form(min_length=16, max_length=4000),
    current_user: StaffORM = Depends(get_current_active_manager),
    session: AsyncSession = Depends(get_async_session)
    ):

    manager_reply = ManagerReply(
        review_status = Status.Replied,
        replied_manager_id = current_user.id,
        manager_reply_text = reply_text,
        manager_reply_datetime = datetime.utcnow()
    )

    review_updated = await ManagerRepository.AddReplyOnReviewByUUID(session, review_uuid, manager_reply)
    if review_updated is None:
        raise http_e.ReviewNotFoundException
    return review_updated

