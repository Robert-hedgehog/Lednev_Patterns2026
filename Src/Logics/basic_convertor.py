from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class basic_convertor(abstract_convertor):
    """Конвертор простых типов данных (числа, строки, булевы флаги)."""

    def convert(self, field_name: str, value: object) -> dict:
        """Конвертация простого значения в словарь."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise argument_exception("field_name", "Имя поля должно быть непустой строкой.")

        if value is not None and not isinstance(value, (int, float, str, bool)):
            raise argument_exception(
                "value",
                f"Ожидается простой тип данных, получен {type(value).__name__}."
            )

        return {field_name.strip(): value}