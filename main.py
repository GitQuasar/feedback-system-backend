from fastapi import FastAPI
import uvicorn

from app.routers.login import router as login_router
from app.routers.admin import router as admin_router
from app.routers.manager import router as manager_router
from app.routers.reveiwer import router as reviewer_router


# Точка взаимодействия с приложением
app = FastAPI(
    title="ITeam Feedback System"
)

app.include_router(login_router, tags=["Login Router"])
app.include_router(admin_router, tags=["Admin Router"])
app.include_router(manager_router, tags=["Manager Router"])
app.include_router(reviewer_router, tags=["Reviewer Router"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)