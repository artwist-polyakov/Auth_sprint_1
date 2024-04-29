import logging
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_ID_KEY = "X-Request-Id"


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get(REQUEST_ID_KEY, uuid.uuid4())
        logging.info(f"Request started. "
                     f"Method: {request.method}, "
                     f"URL: {request.url}, "
                     f"X-Request-Id: {request_id}")
        response = await call_next(request)
        logging.info(f"Request finished. "
                     f"Method: {request.method}, "
                     f"URL: {request.url}, "
                     f"X-Request-Id: {request_id}")
        return response
