from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import all_routers
from src.settings import setup_logging

setup_logging()

app = FastAPI(
    docs_url="/agent-service/agent/api/docs",
    redoc_url="/agent-service/agent/api/redoc",
    openapi_url="/agent-service/agent/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc list domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router, prefix="/agent-service/agent/api")
