# Здесь будет описываться логика для работы с HTTP-запросами
from fastapi import APIRouter
import app.schemas as schemas

router = APIRouter(
    tags=["Frontend"]  # добавляем тег для отображения в Swagger UI
)

# Аутентификация пользователя (для администраторов и менеджеров)
def check_authentication():
    pass
