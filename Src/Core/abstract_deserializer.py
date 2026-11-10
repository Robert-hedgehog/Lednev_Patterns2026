from abc import ABC, abstractmethod


class abstract_deserializer(ABC):
    """Абстрактный класс десериализатора данных."""

    @abstractmethod
    def deserialize(self, data: object) -> object:
        """Преобразование переданной структуры данных в доменные модели."""
        pass