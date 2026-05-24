# Установка зависимостей и запуск

## Требования

- Python 3.11+
- Poetry 1.8+

Проверка:

```bash
python --version
poetry --version
```

---

## Установка зависимостей

В корне проекта выполните:

```bash
poetry install
```

Poetry:

- создаст виртуальное окружение `.venv`
- установит все зависимости из `poetry.lock`

Проверить окружение:

```bash
poetry env info
```

---

## Запуск сервера

Запуск FastAPI сервиса:

```bash
poetry run uvicorn app.main:app --reload
```

Сервер будет доступен по адресу:

```
http://127.0.0.1:8000
```


Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Полезные команды

Добавить зависимость:

```bash
poetry add package-name
```

Добавить dev-зависимость:

```bash
poetry add --group dev package-name
```

Запуск любого скрипта:

```bash
poetry run python script.py
```
