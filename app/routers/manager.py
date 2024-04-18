from fastapi import APIRouter

from app.repository.repositories import ManagerRepository
from app.database import new_session

# добавляем тег для отображения в Swagger UI
router = APIRouter(
    tags=["Manager"]
)

@router.post("/manager/actions/add_reply")
async def create_manager_reply(id: int, reply_text: str, manager_id: int):
    async with new_session() as session:
        review_reply = await ManagerRepository.add_reply(id, reply_text, manager_id)
        return {"review": review_reply}

@router.get("/manager/actions/see_review/{id}")
async def get_review(id: int):
    async with new_session() as session:
        review = await ManagerRepository.see_Review(id)
        return {"review": review}

@router.get("/manager/actions/get_reviews")
async def get_reviews_on_page(limit: int, page: int):
    async with new_session() as session:
        page_reviews = await ManagerRepository.get_replied_on_page(limit, page-1)
        return {"reviews on page": page_reviews}

