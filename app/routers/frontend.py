# Здесь будет описываться логика для работы с HTTP-запросами
from fastapi import APIRouter

router = APIRouter(
    tags=["Frontend"]  # добавляем тег для отображения в Swagger UI
)
