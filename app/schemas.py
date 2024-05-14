from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, EmailStr
from datetime import datetime

from app.utils.enums import Status

"""
Схемы используются для валидации ввода pydantic-ом
"""

### СХЕМЫ ДЛЯ СОТРУДНИКОВ ###

# Базовый класс для сотрудника
# Добавление сотрудника
class AddStaff(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    patronymic: str
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_manager: Optional[bool] = False

class ReadStaff(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    patronymic: str
    is_active: bool = True
    is_verified: bool = False
    is_admin: Optional[bool] = False
    is_manager: Optional[bool] = False
    model_config = ConfigDict(from_attributes=True)

class UpdateStaff(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    patronymic: Optional[str]

### СХЕМЫ ДЛЯ ОТЗЫВОВ ###

# Базовый класс для отзыва
# Добавление отзыва
class AddReview(BaseModel):
    review_creation_date: datetime
    review_status: Status
    review_text: str
    # опциональные для заполнения заявителем поля
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    department: Optional[str] = None

# Добавление ответа на отзыв
class ManagerReply(BaseModel):
    # Поля, заполняемые в момент ответа менеджера на отзыв
    review_status: Status
    manager_reply_text: str
    replied_manager_id: int
    manager_reply_datetime: datetime

class Review(BaseModel):
    uuid: UUID4
    review_creation_date: datetime
    review_status: Status
    review_text: str

    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    department: Optional[str] = None

    manager_reply_text: Optional[str] = None
    replied_manager_id: Optional[int] = None
    manager_reply_datetime: Optional[datetime] = None

class TokenInfo(BaseModel):
    type: str
    role: str
    access_token: str
    refresh_token: str
