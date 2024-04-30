from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

from app.utils.enums import Status

"""
Схемы - "формы", принимающие значение и передающие информацию в (из) модели (-ей) pydantic-а
"""

### СХЕМЫ ДЛЯ СОТРУДНИКОВ ###

# Авторизация сотрудника
class StaffAuth(BaseModel):
    email: EmailStr
    password: str

# Базовый класс для сотрудника
# Добавление сотрудника
class AddStaff(BaseModel):
    email: EmailStr
    password: str
    name: str
    lastname: str
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_manager: Optional[bool] = False

class ReadStaff(BaseModel):
    id: int
    email: str
    name: str
    lastname: str
    is_active: bool = True
    is_verified: bool = False
    is_admin: Optional[bool] = False
    is_manager: Optional[bool] = False

class UpdateStaff(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    name: Optional[str]
    lastname: Optional[str]
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    # is_admin: Optional[bool] = False
    # is_manager: Optional[bool] = False

# Сотрудник
class Staff(AddStaff):
    id: int
    model_config = ConfigDict(from_attributes=True)


### СХЕМЫ ДЛЯ ОТЗЫВОВ ###

# Базовый класс для отзыва
# Добавление отзыва
class AddReview(BaseModel):
    review_creation_date: datetime
    review_status: Status
    review_text: str
    # опциональные для заполнения заявителем поля
    email: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None

# Отзыв
class Review(AddReview):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Добавление ответа на отзыв
class AddManagerReply(Review):
    # Поля, заполняемые в момент ответа менеджера на отзыв
    manager_reply_text: str
    replied_manager_id: str
    manager_reply_datetime: datetime