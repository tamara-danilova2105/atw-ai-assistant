from pydantic_settings import BaseSettings, SettingsConfigDict


# Здесь описываем все настройки приложения, которые можно конфигурировать через переменные окружения или .env файл.
class Settings(BaseSettings):
    # model_config - это новый способ в pydantic v2 задавать конфигурацию модели.
    # Здесь мы указываем, что настройки можно загружать из .env файла и что он в кодировке utf-8.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "atw-ai-assistant"
    env: str = "dev"  # dev | staging | prod
    log_level: str = "INFO"  # DEBUG/INFO/WARNING/ERROR/CRITICAL

    # Включать/выключать логирование запросов (если надо будет глушить в нагрузке)
    log_requests: bool = True


settings = Settings()
