from fastapi import APIRouter

from api.endpoints import admin, internal, public

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(internal.router, prefix="/internal", tags=["internal"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
