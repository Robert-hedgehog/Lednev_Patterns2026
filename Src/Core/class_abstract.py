from abc import ABC
import uuid

class abstract(ABC):
    """Абстрактный базовый класс для доменных сущностей."""

    def __init__(self) -> None:
        """Создаёт сущность с уникальным идентификатором и валидным именем."""

        self._id = uuid.uuid4()
        self._name = ""
        
    @property
    def id(self) -> uuid.UUID:
        """Уникальный идентификатор сущности."""
        return self._id
    
    @property
    def name(self) -> str:
        """Наименование сущности."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливаем наименование сущности с предварительной валидацией.
        
        Raises:
            TypeError: Если переданное значение не является строкой.
            ValueError: Если переданное значение пустое или состоит только из пробелов.
        """
        if not isinstance(value, str):
            raise TypeError("Наименование должно быть строкой.")

        normalized_name = value.strip()
        if not normalized_name:
            raise ValueError("Наименование не может быть пустым.")

        self._name = normalized_name