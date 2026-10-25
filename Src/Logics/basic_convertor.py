import uuid
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class basic_convertor(abstract_convertor):
    """Конвертор простых типов данных."""

    def convert(self, field_name: str, value: object) -> dict:
        """Конвертация простого значения в словарь."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise argument_exception("field_name", "Имя поля должно быть строкой.")

        if value is not None and not isinstance(value, (int, float, str, bool, uuid.UUID)):
            raise argument_exception("value", "Некорректный тип данных.")
        
        serialized_value = str(value) if isinstance(value, uuid.UUID) else value

        return {field_name.strip(): serialized_value}