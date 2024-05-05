from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import StaffORM
from app.repository.admin import AdminRepository
from app.repository.auth import get_current_active_administrator, get_user_from_database
from app.schemas import AddStaff, ReadStaff
from app.utils.enums import Role
from app import http_exceptions as http_e

router = APIRouter()

# Получение информации о текущем активном администраторе
@router.get("/admin/pc/", response_model=ReadStaff)
async def read_current_admin_pc(current_admin: StaffORM = Depends(get_current_active_administrator)):
    return current_admin

# Получение всего списка сотрудников
@router.get("/admin/actions/read_staff", dependencies=[Depends(get_current_active_administrator)])
async def read_staff(session: AsyncSession = Depends(get_async_session)):
    staff = await AdminRepository.GetStaff(session)
    if staff is None:
        raise http_e.NoStaffInTheDatabaseException
    return {"staff": staff}

# Получение сотрудника из БД по ID
@router.get("/admin/actions/read_staff/{id}", dependencies=[Depends(get_current_active_administrator)])
async def read_staff_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    staff_by_id = await AdminRepository.GetStaffById(session, id)
    if staff_by_id is None:
        raise http_e.UserNotFoundException
    return {"staff_by_id": staff_by_id}

# Добавление сотрудника в БД
@router.post("/admin/actions/add_staff", dependencies=[Depends(get_current_active_administrator)])
async def add_staff(
    user_type: Role,
    email: EmailStr,
    password: str,
    name: str,
    lastname: str,
    session: AsyncSession = Depends(get_async_session)
    ):
    
    is_user_already_exist = await get_user_from_database(session, email)
    if is_user_already_exist is not None:
        raise http_e.UserAlreadyExistsException
    
    staff_data = AddStaff(
        email=email,
        password=password,
        name=name,
        lastname=lastname
    )
    
    if user_type == Role.Admin: staff_data.is_admin = True
    elif user_type == Role.Manager: staff_data.is_manager = True
    else:
        raise http_e.InvalidUserTypeException
    
    await AdminRepository.AddStaff(staff_data, session)
    return {"message": f"{user_type} {staff_data.name} {staff_data.lastname} was added successfully."}

# Удаление сотрудника из БД по ID
@router.delete("/admin/actions/delete_staff/{id}")
async def delete_staff_by_id(
    id: int,
    current_user: StaffORM = Depends(get_current_active_administrator),
    session: AsyncSession = Depends(get_async_session)
    ):
    if id == current_user.id:
        raise http_e.CannotDeleteCurrentUserException
    else:
        deleted = await AdminRepository.DeleteStaffByID(id, session)
        if deleted is None:
            raise http_e.UserNotFoundException
        return {"message": f"User with ID {id} was deleted successfully."}
