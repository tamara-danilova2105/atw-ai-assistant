# Typing Standard — ATW AI Assistant

## 1. Назначение

Статическая типизация используется как:

- контракт между слоями
- защита от регрессий
- механизм безопасного рефакторинга
- часть production-стандарта backend

---

## 2. Область обязательной типизации

Обязательно типизируются:

- публичные функции
- service/use-case слой
- FastAPI endpoints
- repository интерфейсы
- DTO и response модели

Не допускается:

- неаннотированные публичные функции
- возврат `dict[str, Any]` из сервисов
- `Any` в публичных сигнатурах без причины
- `Optional` "на всякий случай"

---

## 3. Архитектурное правило

Типы фиксируют границы:

```
API → Service → Repository → Infrastructure
```

Сырой `dict` не должен пересекать границы слоёв.

---

## 4. Инструменты

- pyright — проверка типов
- ruff — линтинг
- FastAPI + Pydantic — API контракт

---

## 5. Конфигурация

### pyrightconfig.json

```json
{
  "include": ["app"],
  "typeCheckingMode": "basic",
  "reportOptionalMemberAccess": "error",
  "reportOptionalCall": "error"
}
```

---

## 6. Инженерные команды

В проекте используется `Makefile` (в корне):

```makefile
lint:
	poetry run ruff check .

format:
	poetry run ruff format .

typecheck:
	poetry run pyright

check: lint typecheck
```

Доступные команды:

- `make lint`
- `make format`
- `make typecheck`
- `make check`

---

## 7. CI правило

PR не может быть смержен при:

- type errors
- lint errors

CI выполняет:

```
poetry run ruff check .
poetry run pyright
```

---

## 8. Эволюция

Текущий режим: `basic`

Дальнейшее усиление:

- переход к strict
- запрет неаннотированных публичных функций
- минимизация Any