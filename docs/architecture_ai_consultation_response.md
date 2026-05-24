# Архитектура ответа AI-консультанта

## Статус

Proposed

---

# Решение

AI-консультант использует гибридную модель ответа (hybrid response model), а не обычный текстовый ответ.

```python
class ConsultationResponse(BaseModel):
    answer: str

    extracted_filters: SearchFilters | None = None

    matched_tours: list[MatchedTour] = Field(default_factory=list)

    suggested_questions: list[str] = Field(default_factory=list)

    needs_clarification: bool = False
```

---

# Архитектурная идея

AI является частью продуктовой архитектуры (product architecture), а не изолированным чат-ботом.

Ответ разделяется на:

- диалоговый слой (conversational layer)
- слой извлечения данных из текста (NLP extraction layer)
- слой рекомендаций (recommendation layer)
- слой интеграции с интерфейсом (UI integration layer)
- поток уточнения запроса (clarification flow)

---

# Слой извлечения данных из текста

## Ответственность

Извлечение структурированных данных (structured data) из естественного языка (natural language).

Пример:

```python
SearchFilters(
    region="Байкал",
    max_price=150000,
    activity="hiking"
)
```

---

## Инженерная ценность

Extraction позволяет:

- делать поиск по БД (DB search)
- запускать пайплайн рекомендаций (recommendation pipeline)
- сохранять предпочтения пользователя (user preferences)
- использовать данные в CRM
- строить аналитику (analytics)
- поддерживать память AI (AI memory)

AI становится семантическим парсером (semantic parser), а не только генератором текста.

---

# Диалоговый слой

## Ответственность

Взаимодействие через естественный язык.

```python
answer: str
```

AI остаётся диалоговым интерфейсом (conversational interface), а не просто формой фильтров.

---

# Слой рекомендаций

## Ответственность

Возврат ранжированных рекомендаций туров (ranked recommendations).

```python
matched_tours: list[MatchedTour]
```

---

## Дополнительный сигнал

```python
reason: str | None
```

Explanation-based recommendation — рекомендация с объяснением причины:

```python
"Подходит по бюджету и активности"
```

Это делает поток рекомендаций (recommendation flow) более прозрачным и вызывающим доверие.

---

# Слой интеграции с интерфейсом

Response содержит данные, готовые для интерфейса (UI-ready data).

Frontend может:

- рендерить карточки туров
- строить carousel — карусель рекомендаций
- генерировать ссылки через slug
- показывать quick actions/chips — быстрые действия
- отображать explanation — объяснение рекомендации

```python
suggested_questions: list[str]
```

AI становится частью пользовательского сценария (UX flow).

---

# Поток уточнения запроса

## Ответственность

Определение недостаточности пользовательского ввода (insufficient user input).

```python
needs_clarification: bool
```

Пример:

```python
needs_clarification=True
```

AI может запускать:

- многошаговую консультацию (multi-step consultation)
- управляемый диалог (guided dialog)
- диалоговый онбординг (conversational onboarding)

---

# Почему гибридный ответ важен

## Плохой вариант

```json
{
  "answer": "..."
}
```

Проблемы:

- скрытое извлечение данных (hidden extraction)
- нет переиспользуемых данных (reusable data)
- нет интеграции с UI
- логика рекомендаций скрыта внутри LLM

---

## Хороший вариант

```json
{
  "answer": "...",
  "filters": {...},
  "matched_tours": [...],
  "suggested_questions": [...],
  "needs_clarification": false
}
```

AI становится частью backend architecture — серверной архитектуры.

---

# Продуктовая ценность

Архитектура позволяет реализовать:

- диалоговый поиск (conversational search)
- AI-помощь в подборе (AI-assisted discovery)
- систему рекомендаций (recommendation system)
- интеграцию с CRM
- аналитический пайплайн (analytics pipeline)
- персонализацию (personalization)
- память AI
- управляемый пользовательский опыт (guided UX)

---

# Инженерная ценность

Подход показывает:

- разделение ответственности (separation of concerns)
- структурированные AI-контракты (structured AI contracts)
- доменно-ориентированную AI-интеграцию (domain-oriented AI integration)
- production-подход к архитектуре
- AI как инфраструктурный компонент

---

# Заключение

AI интегрируется:

- в recommendation engine — движок рекомендаций
- в search layer — поисковый слой
- в UX layer — слой пользовательского опыта
- в CRM и доменную логику

Это production-oriented AI architecture — production-подход к AI-архитектуре, а не обычная GPT integration.
