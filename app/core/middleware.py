import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import structlog

from app.core.settings import settings


log = structlog.get_logger()

# Здесь описаны middleware для FastAPI приложения, которые будут обрабатывать HTTP запросы.
# В данном случае это middleware для генерации и передачи request_id, а также middleware для лог
class RequestIdMiddleware(BaseHTTPMiddleware):
    # request_id_middleware - это middleware, который генерирует уникальный request_id для каждого HTTP запроса,
    # который может быть передан в заголовке X-Request-ID. Если заголовка нет, то генерируется новый request_id с помощью uuid4. 
    # Этот request_id затем добавляется в contextvars,
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # прокидываем в контекст логов
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# access_log_middleware - это middleware, который логирует каждый HTTP запрос с его методом, путем, статус кодом 
# и временем обработки запроса (latency). Это поможет нам анализировать производительность нашего приложения
class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not settings.log_requests:
            return await call_next(request)

        start = time.perf_counter()
        response = None
        try:
            response = await call_next(request)
            return response
        finally:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            status = getattr(response, "status_code", 500)

            # Не логируем query string целиком (там может быть PII)
            log.info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status_code=status,
                latency_ms=elapsed_ms,
            )
