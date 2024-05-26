from fastapi import APIRouter, Depends
from pathlib import Path

from fastapi.responses import FileResponse

from app.repository.auth import get_current_active_administrator
from app.repository.auth import get_current_active_manager

router = APIRouter()

# Путь до директории с файлами инструкций
IMAGES_DIRECTORY = Path(__file__).parent.parent.parent.parent / 'feedback-system-frontend' / 'public' / 'instructions'

# Для администратора
@router.get(
        path="/admin/download/instruction",
        dependencies=[Depends(get_current_active_administrator)]
        )
async def administrator_instruction():
    filename = 'administrator.pdf'
    file_path = f"{IMAGES_DIRECTORY / filename}"
    headers = {'Content-Disposition': f"attachment; filename=\"{filename}\""}
    return FileResponse(file_path, media_type="multipart/form-data", headers=headers)

# Для менеджера
@router.get(
        path="/manager/download/instruction",
        dependencies=[Depends(get_current_active_manager)]
        )
async def manager_instruction():
    filename = 'manager.pdf'
    file_path = f"{IMAGES_DIRECTORY / filename}"
    headers = {'Content-Disposition': f"attachment; filename=\"{filename}\""}
    return FileResponse(file_path, media_type="multipart/form-data", headers=headers)

# Для сотрудника
@router.get(
        path="/reviewer/download/instruction"
        )
async def reviewer_instruction():
    filename = 'reviewer.pdf'
    file_path = f"{IMAGES_DIRECTORY / filename}"
    headers = {'Content-Disposition': f"attachment; filename=\"{filename}\""}
    return FileResponse(file_path, media_type="multipart/form-data", headers=headers)
