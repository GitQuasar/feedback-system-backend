from fastapi import APIRouter
import app.schemas as schemas

# добавляем тег для отображения в Swagger UI
router = APIRouter(
    tags=["Authentication"]
)

@router.post("/auth")
async def staff_login():
    pass

@router.get("/admin_lk/logout")
async def admin_logout():
    pass

@router.get("/manager_lk/logout")
async def manager_logout():
    pass