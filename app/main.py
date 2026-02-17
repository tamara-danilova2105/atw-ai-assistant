from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.core.logging import configure_logging, get_logger
from app.core.settings import settings
from app.core.http import register_http_middleware
from app.core.errors import register_exception_handlers

# Инициализация логирования. Это нужно делать до всего остального, чтобы все логи были в нужном формате и с нужными полями.
configure_logging()
log = get_logger()

# функция, которая описывает жизненный цикл приложения, которая будет вызываться при запуске и остановке приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup - приложение запускается
    # здесь можно выполнять любые действия, которые нужны при запуске приложения, 
    # например, подключаться к базе данных, инициализировать какие-то ресурсы и т.д.
    log.info(
        "app_start",
        app=settings.app_name,
        env=settings.env,
        log_level=settings.log_level,
    )

    yield

    # shutdown - приложение останавливается
    log.info("app_shutdown")

# функция для создания экземпляра FastAPI приложения, которая будет использоваться в main.py для запуска приложения
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    # регистрация middleware для обработки HTTP запросов и логирования
    register_http_middleware(app)
    # регистрация обработчиков исключений, чтобы все необработанные исключения логировались и возвращали корректный HTTP ответ
    register_exception_handlers(app)

    # регистрация роутов из api_router, который описан в app/api/routes.py
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()

