import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog

from app.core.settings import settings


def _drop_sensitive_fields(_, __, event_dict: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    # На будущее: сюда можно добавлять редактирование полей.
    # Пример: если случайно передали "authorization", "cookie", "token", "password" и т.п.
    sensitive_keys = {"password", "token", "authorization", "cookie", "set-cookie"}
    for k in list(event_dict.keys()):
        if k.lower() in sensitive_keys:
            event_dict[k] = "***redacted***"
    return event_dict


def configure_logging() -> None:
    # настройка стандартного python logging, на который опирается structlog
    logging.basicConfig(
        format="%(message)s",  # structlog уже форматирует лог в JSON, поэтому просто выводим его без дополнительного форматирования
        stream=sys.stdout,  # логируем в stdout, чтобы docker и kubernetes могли собирать логи
        level=getattr(
            logging, settings.log_level.upper(), logging.INFO
        ),  # уровень логирования из настроек, по умолчанию INFO
    )

    # настройка structlog, который будет использоваться для структурированного логирования
    structlog.configure(
        # процессоры, которые будут обрабатывать каждый лог. Они выполняются в порядке перечисления.
        processors=[
            structlog.contextvars.merge_contextvars,  # добавляем в лог все переменные из contextvars (например, request_id)
            structlog.processors.add_log_level,  # добавляем уровень логирования в поле "level"
            structlog.processors.TimeStamper(
                fmt="iso"
            ),  # добавляем timestamp в поле "timestamp" в формате ISO 8601
            _drop_sensitive_fields,  # удаляем или маскируем чувствительные поля
            structlog.processors.format_exc_info,  # traceback в поле exception
            structlog.processors.JSONRenderer(),  # рендерим лог в JSON, чтобы его было удобно парсить и анализировать в системах логирования
        ],
        # wrapper_class - класс логгера, который будет использоваться.
        # Мы используем фильтрующий логгер, который позволяет задавать уровень логирования для каждого логгера отдельно.
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper(), logging.INFO)
        ),
        # logger_factory - фабрика для создания логгеров.
        # Мы используем стандартную фабрику, которая создает логгеры на основе стандартного python logging.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # cache_logger_on_first_use - кэшировать ли логгеры после первого использования.
        # Обычно рекомендуется включать, чтобы не создавать новый логгер при каждом вызове get_logger.
        cache_logger_on_first_use=True,
    )


# функция для получения логгера, который уже будет иметь в своем контексте имя приложения и окружение
def get_logger():
    return structlog.get_logger(settings.app_name).bind(env=settings.env)
