from abc import ABC
import uuid
from Src.Core.exception import arguments_exception

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
        
        Параметры:
            value (str): Новое наименование сущности (до 50 символов).

        Raises:
            arguments_exception: Если переданное значение не является строкой.
            arguments_exception: Если переданное значение пустое или состоит только из пробелов.
            arguments_exception: Если длина наименования превышает 50 символов.
        """
        if not isinstance(value, str):
            raise arguments_exception("Наименование должно быть строкой.")

        normalized_name = value.strip()
        if not normalized_name:
            raise arguments_exception("name", "Наименование не может быть пустым.")
        
        if len(normalized_name) > 50:
            raise arguments_exception("name", "Длина наименования не может превышать 50 символов.")

        self._name = normalized_name

    def __eq__(self, other: object) -> bool:
        """Сравнение двух сущностей по id"""
        if isinstance(other, abstract):
            return str(self.id) == str(other.id)
        return False
    
    @id.setter
    def id(self, value:str):
        if value.strip() == "":
            raise arguments_exception("value", "Некорректно передан параметр")
        
        self._id = value.strip()