import re

from app.modules.assistant.schemas import SearchFilters

MONTHS: dict[str, int] = {
    "январ": 1,
    "феврал": 2,
    "март": 3,
    "апрел": 4,
    "ма": 5,
    "июн": 6,
    "июл": 7,
    "август": 8,
    "сентябр": 9,
    "октябр": 10,
    "ноябр": 11,
    "декабр": 12,
}

REGIONS = [
    "Дагестан",
    "Камчатка",
    "Алтай",
    "Байкал",
    "Карелия",
    "Кавказ",
]


class FilterExtractor:
    def extract(self, message: str) -> SearchFilters:
        text = message.lower()

        return SearchFilters(
            region=self._extract_region(text),
            month=self._extract_month(text),
            max_price=self._extract_max_price(text),
            days_count=self._extract_days_count(text),
        )

    def _extract_region(self, text: str) -> str | None:
        for region in REGIONS:
            if region.lower() in text:
                return region

        return None

    def _extract_month(self, text: str) -> int | None:
        for month_name, month_number in MONTHS.items():
            if month_name in text:
                return month_number

        return None

    def _extract_max_price(self, text: str) -> int | None:
        match = re.search(r"(?:до|не дороже|меньше|максимум)\s*(\d+)", text)

        if not match:
            return None

        value = int(match.group(1))

        if value < 1000:
            value *= 1000

        return value

    def _extract_days_count(self, text: str) -> int | None:
        match = re.search(r"(\d+)\s*(?:дн|день|дня|дней)", text)

        if not match:
            return None

        return int(match.group(1))
