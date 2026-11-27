from datetime import datetime
from typing import Dict, List, Optional
from Src.Core.abstract_observable import abstract_observable
from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Dtos.log_entry_dto import log_entry_dto
from Src.Logics.observer import observer


class log_service(abstract_observable):
    """Сервис логирования системных событий на базе шаблона наблюдатель."""

    def __init__(self, log_file: Optional[str] = "app.log") -> None:
        """Инициализация логгера и подписка на события."""
        if log_file is not None:
            validator.validate(log_file, str)
        self.__log_file: Optional[str] = log_file
        self.__records: List[log_entry_dto] = []
        self.__descriptions: Dict[str, str] = event_type.events()
        observer.add(self)

    @property
    def records(self) -> List[log_entry_dto]:
        """Список зафиксированных записей лога."""
        return list(self.__records)

    def clear(self) -> None:
        """Очистка буфера записей лога в памяти."""
        self.__records.clear()

    def handler(self, event: str, params: object = None) -> None:
        """Обработка входящего события и запись в журнал."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        description = self.__descriptions.get(event, event)
        entry = log_entry_dto.create(timestamp, event, description, params)
        self.__records.append(entry)

        if self.__log_file:
            line = f"{entry.timestamp} | [{entry.event}] {entry.description} | {entry.params}\n"
            with open(self.__log_file, "a", encoding="utf-8") as file:
                file.write(line)