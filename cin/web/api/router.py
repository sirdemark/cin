from fastapi.routing import APIRouter

from cin.web.api import monitoring, search

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(search.router)
