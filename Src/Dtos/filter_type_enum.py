from enum import Enum
from Src.Core.validator import argument_exception


class filter_type_enum(Enum):
    """Типы операций фильтрации данных."""

    EQUALS = 1
    LIKE = 2
    LESS = 3
    LESS_OR_EQUAL = 4
    GREATER = 5
    GREATER_OR_EQUAL = 6

    @staticmethod
    def from_string(value: str) -> "filter_type_enum":
        """Преобразование строки в тип фильтрации."""
        mapping = {
            "EQUALS": filter_type_enum.EQUALS,
            "LIKE": filter_type_enum.LIKE,
            "LESS": filter_type_enum.LESS,
            "LESS_OR_EQUAL": filter_type_enum.LESS_OR_EQUAL,
            "GREATER": filter_type_enum.GREATER,
            "GREATER_OR_EQUAL": filter_type_enum.GREATER_OR_EQUAL,
        }
        normalized = str(value).strip().upper()
        result = mapping.get(normalized)
        if result is None:
            raise argument_exception("filter_type", f"Неизвестный тип фильтрации: {value}")
        return result