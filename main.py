from fastapi import FastAPI
import uvicorn

# Подключение всех необходимых роутеров
# from app.routers.frontend import router as frontend_router
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router
from app.routers.manager import router as manager_router
from app.routers.reveiwer import router as reviewer_router

# Точка взаимодействия с приложением
app = FastAPI(
    title="ITeam Feedback System"
)
# Включение всех роутеров в приложение
# app.include_router(frontend_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(reviewer_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)