from abc import ABC, abstractmethod


class abstract_manager(ABC):
    """Абстрактный класс для реализации загрузки и обработки данных."""

    def __init__(self) -> None:
        self._file_name: str = ""
        self._is_loaded: bool = False
        self._data: dict | list = {}

    @abstractmethod
    def load(self, file_name: str = "") -> None:
        """Загрузить данные из файла."""
        pass

    @abstractmethod
    def convert(self) -> bool:
        """Обработать и конвертировать загруженные данные."""
        return False

    @property
    def is_loaded(self) -> bool:
        """Флаг завершения загрузки и конвертации данных."""
        return self._is_loaded