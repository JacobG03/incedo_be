from fastapi import APIRouter

from app.api import me, auth, users, settings


api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['Authenticate'])
api_router.include_router(me.router, prefix='/me', tags=['Current User'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(
    settings.router, prefix='/settings', tags=['Settings'])
