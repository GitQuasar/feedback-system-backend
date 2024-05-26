from sqlalchemy import select

from app.database import async_session
from app.models import StaffORM
from app.schemas import AddStaff
from app.repository.admin import AdminRepository

async def prefill_staff_table():
    async with async_session() as session:
        staff = (await session.execute(select(StaffORM))).scalars().first()
    
        if staff is None:

            print("#(log)# (!!) Staff table is empty ###")

            test_admin_data = AddStaff(
                email = "test_admin@gmail.com",
                password = "test_password",
                first_name = "AdminName",
                last_name = "AdminLastName",
                patronymic = "AdminPatronymic",
                is_active = True,
                is_verified = False,
                is_admin = True,
                is_manager = False
            )
            test_manager_data = AddStaff(
                email = "test_manager@gmail.com",
                password = "test_password",
                first_name = "ManagerName",
                last_name = "ManagerLastName",
                patronymic = "ManagerPatronymic",
                is_active = True,
                is_verified = False,
                is_admin = False,
                is_manager = True
            )
            await AdminRepository.AddStaff(test_admin_data, session)
            await AdminRepository.AddStaff(test_manager_data, session)

            print("#(log)# (OK) Staff table was succesfully pre-filled with test admin and manager #")
            print("#(log)# (!!) It is strongly advised to change test admin's and manager's e-mails and passwords #")
        
        else:
            print("#(log)# (OK) Staff table contains data #")
