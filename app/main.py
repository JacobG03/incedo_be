import uvicorn
from logging.config import dictConfig
from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

from app.core import settings, LogConfig
from app.middleware import LimitUploadSize
from app.api import api_router


dictConfig(LogConfig().dict())

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(LimitUploadSize, max_upload_size=settings.MAX_AVATAR_SIZE)

app.include_router(api_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

from app import workers

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
