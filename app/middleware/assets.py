import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Response, status
from starlette.requests import Request
from starlette.types import ASGIApp

logger = logging.getLogger('main')

# Credit - https://github.com/tiangolo/fastapi/issues/362#issuecomment-508274824


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.info('Middleware start')
        if request.method in ['PUT', 'POST']:
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                logger.info('413 response')
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        logger.info('Middleware end')
        return await call_next(request)
