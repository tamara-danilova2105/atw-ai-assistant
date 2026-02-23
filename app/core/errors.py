from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

# Здесь описаны обработчики исключений для FastAPI приложения,
# которые будут логировать все необработанные исключения и возвращать корректный HTTP ответ с кодом 500
# и сообщением "Internal Server Error". Это нужно для того, чтобы не допустить утечки информации об ошибках
# в ответах и чтобы все ошибки были залогированы для последующего анализа.
log = get_logger()


# функция для регистрации обработчиков исключений в FastAPI приложении
def register_exception_handlers(app: FastAPI) -> None:
    # Python 3.11 / anyio может кидать ExceptionGroup
    @app.exception_handler(ExceptionGroup)  # type: ignore[name-defined]
    # обработчик для ExceptionGroup, который может содержать несколько исключений внутри себя.
    async def exception_group_handler(request: Request, exc: ExceptionGroup):
        # логируем всю группу исключений, чтобы не потерять информацию о них.
        log.exception(
            "unhandled_exception_group",
            method=request.method,
            path=request.url.path,
        )
        # возвращаем общий ответ с кодом 500, так как мы не хотим раскрывать детали ошибок в ответах,
        # но при этом все ошибки будут залогированы.
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    # обработчик для всех остальных исключений, которые не были обработаны другими обработчиками.
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        log.exception(
            "unhandled_exception",
            method=request.method,
            path=request.url.path,
        )
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
