from typing import List
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import StaffORM
from app.repository.admin import AdminRepository
from app.repository.auth import get_current_active_administrator, get_user_from_database
from app.schemas import AddStaff, ReadStaff, UpdateStaff
from app.utils.enums import Role
from app import http_exceptions as http_e

router = APIRouter()

# Получение информации о текущем активном администраторе
@router.get(
        path="/admin/pc/",
        response_model=ReadStaff
        )
async def read_current_admin_pc(current_admin: StaffORM = Depends(get_current_active_administrator)):
    return current_admin

# Получение всего списка сотрудников из БД
@router.get(
        path="/admin/actions/read_staff",
        dependencies=[Depends(get_current_active_administrator)],
        response_model=List[ReadStaff]
        )
async def read_staff(session: AsyncSession = Depends(get_async_session)):
    staff_list = await AdminRepository.GetStaff(session)
    if staff_list is None: raise http_e.NoStaffInTheDatabaseException
    return staff_list

# Получение сотрудника из БД по ID
@router.get(
        path="/admin/actions/read_staff/{id}",
        dependencies=[Depends(get_current_active_administrator)],
        response_model=ReadStaff
        )
async def read_staff_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    staff = await AdminRepository.GetStaffById(session, id)
    if staff is None:
        raise http_e.UserNotFoundException
    return staff

# Добавление сотрудника в БД
@router.post(
        path="/admin/actions/add_staff",
        dependencies=[Depends(get_current_active_administrator)],
        response_model=ReadStaff
        )
async def add_staff(
    user_type: Role = Form(),
    email: EmailStr = Form(),
    password: str = Form(min_length=8, max_length=32),
    first_name: str = Form(min_length=2, max_length=32),
    last_name: str = Form(min_length=2, max_length=32),
    patronymic: str = Form(min_length=2, max_length=32),
    session: AsyncSession = Depends(get_async_session)
    ):
    
    is_user_already_exist = await get_user_from_database(session, email)
    if is_user_already_exist is not None: raise http_e.UserAlreadyExistsException
    
    staff_data = AddStaff(
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        patronymic = patronymic
    )
    
    if user_type == Role.Admin: staff_data.is_admin = True
    elif user_type == Role.Manager: staff_data.is_manager = True
    else: raise http_e.InvalidUserTypeException
    
    staff = await AdminRepository.AddStaff(staff_data, session)
    return staff

# Удаление сотрудника из БД по ID
@router.delete(
        path="/admin/actions/delete_staff/{id}"
        )
async def delete_staff_by_id(
    id: int,
    current_user: StaffORM = Depends(get_current_active_administrator),
    session: AsyncSession = Depends(get_async_session)
    ):
    if id == current_user.id:
        raise http_e.CannotDeleteCurrentUserException
    
    deleted = await AdminRepository.DeleteStaffByID(id, session)
    if deleted is None:
        raise http_e.UserNotFoundException

@router.put(
    path="/admin/actions/update_staff/{id}",
    dependencies=[Depends(get_current_active_administrator)],
    response_model=ReadStaff
)
async def update_staff_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    email: EmailStr = Form(default=None),
    password: str = Form(default=None, min_length=8, max_length=32),
    first_name: str = Form(default=None, min_length=2, max_length=32),
    last_name: str = Form(default=None, min_length=2, max_length=32),
    patronymic: str = Form(default=None, min_length=2, max_length=32)
):  
    update_info = UpdateStaff(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic
    )

    if email is not None:
        staff_with_similar_email = (
        await session.execute(select(StaffORM).where(StaffORM.email == email))
        ).scalars().first()
        if staff_with_similar_email is not None:
            raise http_e.UserAlreadyExistsException

    staff_updated = await AdminRepository.UpdateStaffByID(id, session, update_info)

    if staff_updated is None:
        raise http_e.UserNotFoundException
    return staff_updated