import time
import uuid

import structlog
from fastapi import FastAPI, Request


# Здесь описаны middleware для FastAPI приложения, которые будут обрабатывать HTTP запросы.
# В данном случае это middleware для генерации и передачи request_id, а также middleware для лог
def register_http_middleware(app: FastAPI) -> None:
    # request_id_middleware - это middleware, который генерирует уникальный request_id для каждого HTTP запроса,
    # который может быть передан в заголовке X-Request-ID. Если заголов
    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        # генерируем новый request_id, если его нет в заголовке
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        # очищаем contextvars, чтобы не было утечки данных между запросами
        structlog.contextvars.clear_contextvars()
        # добавляем request_id в contextvars, чтобы он был доступен во всех логах, которые будут создаваться в рамках этого запроса
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    # access_log_middleware - это middleware, который логирует каждый HTTP запрос с его методом, путем, статус кодом
    # и временем обработки запроса (latency).
    @app.middleware("http")
    # Здесь мы проверяем, нужно ли логировать запросы, так как иногда может быть полезно отключить логирование
    # для снижения нагрузки на систему логирования.
    async def access_log_middleware(request: Request, call_next):
        from app.core.settings import settings  # чтобы не было циклических импортов

        # если логирование запросов отключено в настройках, просто передаем запрос дальше без логирования
        if not settings.log_requests:
            return await call_next(request)

        # замеряем время обработки запроса, чтобы потом логировать latency (время обработки запроса в миллисекундах)
        start = time.perf_counter()
        response = None
        # используем try/finally, чтобы гарантировать, что логирование произойдет даже если в процессе обработки
        # запроса возникнет исключение.
        try:
            response = await call_next(request)
            return response
        finally:
            elapsed_ms = int((time.perf_counter() - start) * 1000)  # latency в миллисекундах
            status_code = getattr(
                response, "status_code", 500
            )  # если response нет (например, при исключении), считаем статус код 500

            # логируем HTTP запрос с его методом, путем, статус кодом и latency.
            # Это поможет нам анализировать производительность
            structlog.get_logger().info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                latency_ms=elapsed_ms,
            )
