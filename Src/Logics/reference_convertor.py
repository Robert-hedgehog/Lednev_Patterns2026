from typing import Optional
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_convert_factory import abstract_convert_factory
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator, argument_exception


class reference_convertor(abstract_convertor):
    """Конвертор ссылочных типов данных."""

    def __init__(self, factory: Optional[abstract_convert_factory] = None) -> None:
        super().__init__()
        self.__factory: Optional[abstract_convert_factory] = None
        if factory is not None:
            self.factory = factory

    @property
    def factory(self) -> Optional[abstract_convert_factory]:
        """Фабрика конвертации данных."""
        return self.__factory

    @factory.setter
    def factory(self, value: abstract_convert_factory) -> None:
        """Установка фабрики с проверкой типа."""
        validator.validate(value, abstract_convert_factory)
        self.__factory = value

    def convert(self, field_name: str, value: object) -> dict:
        """Конвертация доменной сущности в словарь."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise argument_exception("field_name", "Имя поля должно быть строкой.")

        if value is None:
            return {field_name.strip(): None}

        if not isinstance(value, abstract):
            raise argument_exception("value", "Ожидается доменная сущность.")

        if self.__factory is not None:
            serialized = self.__factory.convert(value)
        else:
            serialized = {"id": str(value.id), "name": value.name}

        return {field_name.strip(): serialized}