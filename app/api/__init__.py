from fastapi import APIRouter

from app.api import me, auth


api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['Authenticate'])
api_router.include_router(me.router, prefix='/me', tags=['Current User'])
