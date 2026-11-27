from typing import List
from Src.Core.abstract_observable import abstract_observable
from Src.Core.validator import validator


class observer:
    """Реализация шаблона наблюдатель для рассылки системных событий."""

    handlers: List[abstract_observable] = []

    @staticmethod
    def add(source: abstract_observable) -> None:
        """Добавить подписчика под наблюдение."""
        validator.validate(source, abstract_observable)
        if source not in observer.handlers:
            observer.handlers.append(source)

    @staticmethod
    def delete(source: abstract_observable) -> None:
        """Удалить подписчика из наблюдения."""
        validator.validate(source, abstract_observable)
        if source in observer.handlers:
            observer.handlers.remove(source)

    @staticmethod
    def clear() -> None:
        """Очистить список всех подписчиков."""
        observer.handlers.clear()

    @staticmethod
    def create(event: str, params: object = None) -> None:
        """Вызвать событие и уведомить всех подписчиков."""
        validator.validate(event, str)
        for handler in list(observer.handlers):
            handler.handler(event, params)