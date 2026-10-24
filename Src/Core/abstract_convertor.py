from abc import ABC, abstractmethod


class abstract_convertor(ABC):
    """Абстрактный класс конвертора данных в словарь."""

    @abstractmethod
    def convert(self, field_name: str, value: object) -> dict:
        """Преобразование переданного поля и значения в словарь."""
        pass

    def Convert(self, field_name: str, value: object) -> dict:
        """Алиас метода convert для совместимости."""
        return self.convert(field_name, value)