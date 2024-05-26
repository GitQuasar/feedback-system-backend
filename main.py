from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import app_startup as startup

from app.routers.login import router as login_router
from app.routers.admin import router as admin_router
from app.routers.manager import router as manager_router
from app.routers.reveiwer import router as reviewer_router
from app.routers.instructions import router as instruction_download_router


# Действия при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup.prefill_staff_table()
    yield

# Точка взаимодействия с приложением
app = FastAPI(
    lifespan=lifespan,
    title="ITeam Feedback System API"
)

app.include_router(login_router, prefix="/api", tags=["Login Router"])
app.include_router(admin_router, prefix="/api", tags=["Admin Router"])
app.include_router(manager_router, prefix="/api", tags=["Manager Router"])
app.include_router(reviewer_router, prefix="/api", tags=["Reviewer Router"])
app.include_router(instruction_download_router, prefix="/api", tags=["Instructions Router"])

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    try:
        uvicorn.run(
            app="main:app",
            host="127.0.0.1",
            port=8000,
            log_level="info",
            reload=True,
        )
    except KeyboardInterrupt:
        print("#(log)# Server stopped by keyboard interrupt #")