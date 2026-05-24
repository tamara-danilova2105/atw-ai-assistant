# AI Consultation Response Architecture

## Status

Proposed

---

# Decision

AI-консультант использует hybrid response model вместо обычного text response.

```python
class ConsultationResponse(BaseModel):
    answer: str

    extracted_filters: SearchFilters | None = None

    matched_tours: list[MatchedTour] = Field(default_factory=list)

    suggested_questions: list[str] = Field(default_factory=list)

    needs_clarification: bool = False
```

---

# Architectural Idea

AI является частью product architecture, а не isolated chatbot.

Response разделяется на:

- conversational layer
- NLP extraction layer
- recommendation layer
- UI integration layer
- clarification flow

---

# NLP Extraction Layer

## Responsibility

Извлечение structured data из natural language.

Пример:

```python
SearchFilters(
    region="Байкал",
    max_price=150000,
    activity="hiking"
)
```

## Engineering Value

Extraction позволяет:

- делать DB search
- запускать recommendation pipeline
- сохранять user preferences
- использовать данные в CRM
- строить analytics
- поддерживать AI memory

AI становится semantic parser, а не только text generator.

---

# Conversational Layer

## Responsibility

Human-friendly interaction через natural language.

```python
answer: str
```

AI остаётся conversational interface вместо обычной filter form.

---

# Recommendation Layer

## Responsibility

Возврат ranked tour recommendations.

```python
matched_tours: list[MatchedTour]
```

## Additional Signal

```python
reason: str | None
```

Explanation-based recommendation:

```python
"Подходит по бюджету и активности"
```

Это делает recommendation flow более transparent и trustworthy.

---

# UI Integration Layer

Response содержит UI-ready data.

Frontend может:

- render tour cards
- build carousel
- generate links через slug
- render quick actions/chips
- показывать recommendation explanations

```python
suggested_questions: list[str]
```

AI становится частью UX flow.

---

# Clarification Flow

## Responsibility

Определение insufficient user input.

```python
needs_clarification: bool
```

Пример:

```python
needs_clarification=True
```

AI может запускать:

- multi-step consultation
- guided dialog
- conversational onboarding

---

# Why Hybrid Response Matters

## Bad

```json
{
  "answer": "..."
}
```

Проблемы:

- hidden extraction
- нет reusable data
- нет UI integration
- recommendation logic скрыта внутри LLM

---

## Good

```json
{
  "answer": "...",
  "filters": {...},
  "matched_tours": [...],
  "suggested_questions": [...],
  "needs_clarification": false
}
```

AI становится частью backend architecture.

---

# Product Value

Архитура позволяет реализовать:

- conversational search
- AI-assisted discovery
- recommendation system
- CRM integration
- analytics pipeline
- personalization
- AI memory
- guided UX

---

# Engineering Value

Подход показывает:

- separation of concerns
- structured AI contracts
- domain-oriented AI integration
- production-oriented architecture
- AI as infrastructure component

---

# Conclusion

AI интегрируется:

- в recommendation engine
- search layer
- UX layer
- CRM/domain logic

Это production-oriented AI architecture, а не обычная GPT integration.
