from abc import ABC, abstractmethod
from Src.Core.abstract_convertor import abstract_convertor


class abstract_convert_factory(ABC):
    """Абстрактная фабрика конверторов."""

    @abstractmethod
    def create(self, value: object) -> abstract_convertor:
        """Подбор и создание конвертора для переданного значения."""
        pass

    @abstractmethod
    def convert(self, source: object) -> object:
        """Конвертация структуры данных."""
        pass