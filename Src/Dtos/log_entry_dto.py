from Src.Core.class_abstract import abstract
from Src.Core.validator import validator


class log_entry_dto(abstract):
    """DTO-модель записи системного журнала событий."""

    def __init__(self) -> None:
        """Инициализация записи лога значениями по умолчанию."""
        super().__init__()
        self.__timestamp: str = ""
        self.__event: str = ""
        self.__description: str = ""
        self.__params: dict | str = {}

    @property
    def timestamp(self) -> str:
        """Время фиксации события."""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: str) -> None:
        """Установка времени фиксации события."""
        validator.validate(value, str)
        self.__timestamp = value.strip()

    @property
    def event(self) -> str:
        """Код системного события."""
        return self.__event

    @event.setter
    def event(self, value: str) -> None:
        """Установка кода события."""
        validator.validate(value, str)
        self.__event = value.strip()

    @property
    def description(self) -> str:
        """Описание системного события."""
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        """Установка описания события."""
        validator.validate(value, str)
        self.__description = value.strip()

    @property
    def params(self) -> dict | str:
        """Параметры события."""
        return self.__params

    @params.setter
    def params(self, value: dict | str | None) -> None:
        """Установка параметров события."""
        if value is None:
            self.__params = {}
            return
        validator.validate(value, (dict, str))
        self.__params = value

    @staticmethod
    def create(
        timestamp: str,
        event: str,
        description: str,
        params: dict | str | None = None,
    ) -> "log_entry_dto":
        """Фабричный метод создания записи журнала."""
        dto = log_entry_dto()
        dto.timestamp = timestamp
        dto.event = event
        dto.description = description
        dto.params = params
        dto.name = f"{event} ({timestamp})"[:50]
        return dto

    @classmethod
    def from_dict(cls, data: dict) -> "log_entry_dto":
        """Фабричный метод создания записи журнала из словаря."""
        validator.validate(data, dict)
        dto = cls()
        fields = ("id", "name", "timestamp", "event", "description", "params")
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(dto, field, value)
        return dto