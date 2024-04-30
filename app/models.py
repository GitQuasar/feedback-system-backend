from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base

"""
Здесь описываются МОДЕЛИ - то, на основе чего будут создаваться таблицы в БД. Модели наследуются от базовой модели Base.
Отдельная модель соответствует определенной таблице в БД. Объекты моделей соответствуют столбцам таблицы
"""
# Сюда запоминается вся информация о моделях
metadata = MetaData()

# # Перечисление всех возможных статусов отзывов
# class ReviewsStatusesORM(Base):
#     __tablename__ = "reviews_statuses"
#     metadata

#     id: Mapped[int] = mapped_column(primary_key=True)
#     status: Mapped[str]

class StaffORM(Base):
    __tablename__ = "staff"
    metadata
    
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    lastname: Mapped[str]

    email: Mapped[str]
    # Хэшированный пароль хранится с типом bytes, а не str
    hashed_password: Mapped[bytes]

    is_admin: Mapped[bool]
    is_manager: Mapped[bool]
    is_verified: Mapped[bool]
    is_active: Mapped[bool]

class ReviewsRegistryORM(Base):
    __tablename__ = "reviews_registry"
    metadata

    id: Mapped[int] = mapped_column(primary_key=True)

    review_creation_date: Mapped[datetime]
    review_status: Mapped[str]
    review_text: Mapped[str]

    # опциональные для заполнения заявителем поля
    email: Mapped[str | None]
    name: Mapped[str | None]
    lastname: Mapped[str | None]

    # поля, заполняемые в момент ответа менеджера на отзыв
    manager_reply_text: Mapped[str | None]
    replied_manager_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id"))
    manager_reply_datetime: Mapped[datetime | None]