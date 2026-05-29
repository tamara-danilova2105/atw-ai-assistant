class TourContextBuilder:
    def build(self, tour, user_message: str | None = None) -> str:
        message = (user_message or "").lower()

        if self._is_not_included_question(message):
            return self._build_not_included_context(tour)

        if self._is_included_question(message):
            return self._build_included_context(tour)

        if self._is_dates_question(message):
            return self._build_dates_context(tour)

        if self._is_hotel_question(message):
            return self._build_hotels_context(tour)

        return self._build_full_context(tour)

    def _is_included_question(self, message: str) -> bool:
        return "включено" in message or "входит" in message or "стоимость" in message

    def _is_not_included_question(self, message: str) -> bool:
        return "не включено" in message or "не входит" in message or "дополнительно" in message

    def _is_dates_question(self, message: str) -> bool:
        return "даты" in message or "когда" in message or "выезд" in message

    def _is_hotel_question(self, message: str) -> bool:
        return (
            "размещение" in message
            or "отель" in message
            or "жилье" in message
            or "жильё" in message
        )

    def _build_included_context(self, tour) -> str:
        included = tour.details.included if tour.details else ""

        return (
            f"В стоимость тура «{tour.tour}» включено:\n\n"
            f"{included or 'Информация о том, что включено в стоимость, не указана.'}"
        )

    def _build_not_included_context(self, tour) -> str:
        not_included = tour.details.notIncluded if tour.details else ""

        return (
            f"В стоимость тура «{tour.tour}» не включено:\n\n"
            f"{not_included or 'Информация о том, что не включено в стоимость, не указана.'}"
        )

    def _build_dates_context(self, tour) -> str:
        if not tour.dates:
            return "Нет доступных дат."

        dates = "\n".join(
            (
                f"- {tour_date.date_start:%d.%m.%Y} — "
                f"{tour_date.date_finish:%d.%m.%Y}, "
                f"дней: {tour_date.days_count}, "
                f"свободных мест: {tour_date.spots}, "
                f"статус: {tour_date.status}"
            )
            for tour_date in tour.dates
        )

        return f"Даты тура «{tour.tour}»:\n\n{dates}"

    def _build_hotels_context(self, tour) -> str:
        description = (
            tour.hotels.description
            if tour.hotels and tour.hotels.description
            else "Информация о размещении не указана."
        )

        return f"Размещение в туре «{tour.tour}»:\n\n{description}"

    def _build_program_context(self, tour) -> str:
        if not tour.program:
            return "Программа тура не указана."

        return "\n\n".join(
            f"{index + 1}. {day.title}\n{day.details}" for index, day in enumerate(tour.program)
        )

    def _build_must_know_context(self, tour) -> str:
        if not tour.mustKnow:
            return "Дополнительная информация не указана."

        return "\n\n".join(
            f"Вопрос: {item.question}\nОтвет: {item.answer}" for item in tour.mustKnow
        )

    def _build_full_context(self, tour) -> str:
        included = tour.details.included if tour.details else ""
        not_included = tour.details.notIncluded if tour.details else ""

        hotel_description = (
            tour.hotels.description
            if tour.hotels and tour.hotels.description
            else "Информация о размещении не указана."
        )

        return f"""
Тур: {tour.tour}
Slug: {tour.slug}

Описание:
{tour.description or "Описание тура не указано."}

Что включено:
{included or "Информация о том, что включено в стоимость, не указана."}

Что не включено:
{not_included or "Информация о том, что не включено в стоимость, не указана."}

Даты:
{self._build_dates_context(tour)}

Программа:
{self._build_program_context(tour)}

Размещение:
{hotel_description}

Важно знать:
{self._build_must_know_context(tour)}
""".strip()
