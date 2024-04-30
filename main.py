from fastapi import FastAPI
import uvicorn

# Подключение всех необходимых роутеров
# from app.routers.frontend import router as frontend_router
from app.routers.auth import router as auth_router
# from app.routers.register import router as register_router
from app.routers.admin import router as admin_router
# from app.routers.manager import router as manager_router
# from app.routers.reveiwer import router as reviewer_router

# Точка взаимодействия с приложением
app = FastAPI(
    title="ITeam Feedback System"
)

# Включение всех роутеров в приложение
# app.include_router(frontend_router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication Router"])
# app.include_router(register_router, prefix="/auth", tags=["Registration Router"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Router"])
# app.include_router(manager_router, prefix="/manager", tags=["Manager Router"])
# app.include_router(reviewer_router, tags=["Reviewer Router"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)