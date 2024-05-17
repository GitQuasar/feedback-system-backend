from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from app.routers.login import router as login_router
from app.routers.admin import router as admin_router
from app.routers.manager import router as manager_router
from app.routers.reveiwer import router as reviewer_router


# Точка взаимодействия с приложением
app = FastAPI(
    title="ITeam Feedback System API"
)

app.include_router(login_router, prefix="/api", tags=["Login Router"])
app.include_router(admin_router, prefix="/api", tags=["Admin Router"])
app.include_router(manager_router, prefix="/api", tags=["Manager Router"])
app.include_router(reviewer_router, prefix="/api", tags=["Reviewer Router"])

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)