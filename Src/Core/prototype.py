from typing import List
from Src.Core.validator import validator


class prototype:
    """Базовый класс паттерна Прототип для клонирования наборов данных."""

    def __init__(self, data: List[object] = None) -> None:
        """Инициализация прототипа исходным списком данных."""
        self.__data: List[object] = []
        if data is not None:
            self.data = data

    @property
    def data(self) -> List[object]:
        """Текущий набор данных прототипа."""
        return self.__data

    @data.setter
    def data(self, value: List[object]) -> None:
        """Установка набора данных."""
        validator.validate(value, list)
        self.__data = value

    def clone(self, data: List[object] = None) -> "prototype":
        """Создание нового экземпляра прототипа с переданным или текущим набором данных."""
        inner_data = data if data is not None else list(self.__data)
        return self.__class__(inner_data)