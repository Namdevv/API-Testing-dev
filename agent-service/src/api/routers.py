from .agent.agent_api import router as agent_router
from .common.common_api import router as common_router
from .document.document_api import router as document_router
from .file.file import router as router_file
from .project.project import router as project_router
from .test_entities.test_entities_api import (
    router as test_entities_router,
)

all_routers = [
    common_router,
    agent_router,
    router_file,
    document_router,
    project_router,
    test_entities_router,
]
