from datetime import datetime, date
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception


class datetime_convertor(abstract_convertor):
    """Конвертор типов DateTime и Date в строковый формат."""

    def convert(self, field_name: str, value: object) -> dict:
        """Конвертация даты или времени в строку."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise argument_exception("field_name", "Имя поля должно быть непустой строкой.")

        if value is None:
            return {field_name.strip(): None}

        if not isinstance(value, (datetime, date)):
            raise argument_exception(
                "value",
                f"Ожидается datetime или date, получен {type(value).__name__}."
            )

        if isinstance(value, datetime):
            formatted = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted = value.strftime("%Y-%m-%d")

        return {field_name.strip(): formatted}