import uvicorn
from logging.config import dictConfig
from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.core import settings, LogConfig
from app.api import api_router


dictConfig(LogConfig().dict())


origins = [
    "https://www.incedo.me",
    "http://localhost:3000",
    "http://192.168.2.56:3000"
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"])
]

app = FastAPI(title=settings.PROJECT_NAME, middleware=middleware)

app.include_router(api_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

from app.workers import user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
