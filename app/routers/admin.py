from fastapi import APIRouter, Form, Request
from pydantic import EmailStr

from app.repository.repositories import AdminRepository
import app.schemas as schemas

# добавляем тег для отображения в Swagger UI
router = APIRouter(
    tags=["Admin"]
)

# Получение всего списка сотрудников
#todo: изменить для возможности пагинации 
@router.get("/admin/view_staff/")
async def get_staff():
    staff = await AdminRepository.GetStaff()
    return {"staff": staff}

# Добавление сотрудника
#todo: переработать на получение информации из HTTP-запроса (закомментированный код именно для этого)
@router.post("/admin/actions/add_staff")
async def add_staff(
    # request: Request,
    # email: EmailStr = Form(...),
    # password: str = Form(...),
    # name: str = Form(...),
    # lastname: str = Form(...)

    role_id: int, email: EmailStr, password: str, name: str, lastname: str):

    # В будущем ОБЯЗАТЕЛЬНО пределать так, чтобы в БД передавался ТОЛЬКО хэшированный код
    staff = schemas.AddStaff(
        role_id = role_id,
        email = email,
        password = password,
        name = name,
        lastname = lastname
    )

    await AdminRepository.AddStaff(staff)

# Получение сотрудника по ID
@router.get("/admin/staff/{id}")
async def get_staff_by_id(id: int):
    result = await AdminRepository.GetStaffById(id)
    return {"staff": result}

# Удаление сотрудника из БД по ID
@router.delete("/admin/actions/staff_delete/{id}")
async def delete_staff(id: int):
    result = await AdminRepository.DeleteStaff(id)
    return {"message": result}