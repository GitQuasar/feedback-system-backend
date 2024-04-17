from fastapi import APIRouter

# добавляем тег для отображения в Swagger UI
router = APIRouter(
    tags=["Manager"]
)

@router.post("/manager/actions/add_reply")
async def create_manager_reply():
    pass

@router.get("/manager/actions/see_review/{id}")
async def get_review(id: int):
    pass

