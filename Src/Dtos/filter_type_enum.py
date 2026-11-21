from enum import Enum
from Src.Core.validator import argument_exception


class filter_type_enum(Enum):
    """Типы операций фильтрации данных."""

    EQUALS = 1
    LIKE = 2

    @staticmethod
    def from_string(value: str) -> "filter_type_enum":
        """Преобразование строки в тип фильтрации."""
        mapping = {
            "EQUALS": filter_type_enum.EQUALS,
            "LIKE": filter_type_enum.LIKE,
        }
        normalized = str(value).strip().upper()
        result = mapping.get(normalized)
        if result is None:
            raise argument_exception("filter_type", f"Неизвестный тип фильтрации: {value}")
        return result