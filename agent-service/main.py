from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import all_routers
from src.registry.actions import scan_and_register_actions
from src.registry.nodes import scan_and_register_nodes
from src.registry.tools import scan_and_register_tools
from src.registry.workflows import scan_and_register_workflows

scan_and_register_tools()
scan_and_register_actions()
scan_and_register_nodes()
scan_and_register_workflows()


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc list domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router, prefix="/api")
