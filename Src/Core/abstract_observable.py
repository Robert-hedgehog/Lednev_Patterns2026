from abc import ABC, abstractmethod


class abstract_observable(ABC):
    """Абстрактный элемент наблюдения."""

    @abstractmethod
    def handler(self, event_type: str, params: object = None) -> None:
        """Выполнить обработку полученного события."""
        pass