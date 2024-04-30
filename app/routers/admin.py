from fastapi import APIRouter
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.admin import AdminRepository
from app.repository.auth import AuthRepository
from app.schemas import AddStaff, ReadStaff
from app.utils.enums import Role
from app import http_exceptions

router = APIRouter()

# Получение всего списка сотрудников
#todo: изменить для возможности пагинации 
@router.get("/staff")
async def get_staff():
    staff = await AdminRepository.GetStaff()
    return {"staff": staff}

# Получение сотрудника по ID
@router.get("/staff/{id}")
async def get_staff_by_id(id: int):
    result = await AdminRepository.GetStaffById(id)
    return {"staff": result}

# Добавление сотрудника
@router.post("/actions/add_staff")
async def add_staff(user_type: Role, email: EmailStr, password: str, name: str, lastname: str):
    staff = AddStaff(email=email, password=password, name=name, lastname=lastname)
    
    if user_type == Role.Admin: staff.is_admin = True
    elif user_type == Role.Manager: staff.is_manager = True
    else: raise http_exceptions.InvalidUserType
    
    await AdminRepository.AddStaff(staff)
    return {"message": f"{user_type} {staff.name} {staff.lastname} was added succesfully."}

# Удаление сотрудника из БД по ID
@router.delete("/actions/delete_staff/{id}")
async def delete_staff(id: int):
    result = await AdminRepository.DeleteStaff(id)
    return {"message": result}