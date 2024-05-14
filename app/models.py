from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base

"""
Здесь описываются МОДЕЛИ - то, на основе чего будут создаваться таблицы в БД. Модели наследуются от базовой модели Base.
Отдельная модель соответствует определенной таблице в БД. Объекты моделей соответствуют столбцам таблицы.
"""
# Сюда запоминается вся информация о моделях
metadata = MetaData()

class StaffORM(Base):
    __tablename__ = "staff"
    metadata
    
    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]

    email: Mapped[str]
    hashed_password: Mapped[bytes]

    is_admin: Mapped[bool]
    is_manager: Mapped[bool]
    is_verified: Mapped[bool]
    is_active: Mapped[bool]

class ReviewsRegistryORM(Base):
    __tablename__ = "reviews_registry"
    metadata

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)

    review_creation_date: Mapped[datetime]
    review_status: Mapped[str]
    review_text: Mapped[str]

    # Опциональные к заполнению заявителем поля
    email: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    patronymic: Mapped[str | None]
    department: Mapped[str | None]

    # Поля, заполняемые в момент ответа менеджера на отзыв
    manager_reply_text: Mapped[str | None]
    replied_manager_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id"))
    manager_reply_datetime: Mapped[datetime | None]