from fastapi import APIRouter

from app.repository.manager import ManagerRepository
from app.database import async_session

router = APIRouter()

@router.post("/actions/add_reply")
async def create_manager_reply(id: int, reply_text: str, manager_id: int):
    async with async_session() as session:
        review_reply = await ManagerRepository.add_reply(id, reply_text, manager_id)
        return {"Review with reply": review_reply}

@router.get("/reviews/{id}")
async def get_review(id: int):
    async with async_session() as session:
        review = await ManagerRepository.see_Review(id)
        return {"Review": review}

@router.get("/reviews")
async def get_reviews_on_page(limit: int, page: int):
    async with async_session() as session:
        page_reviews = await ManagerRepository.get_replied_on_page(limit, page-1)
        return {"Reviews on page": page_reviews}

