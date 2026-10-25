from datetime import datetime, date
import uuid
from typing import Optional
from Src.Core.abstract_convert_factory import abstract_convert_factory
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.class_abstract import abstract
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor


class convert_factory(abstract_convert_factory):
    """Фабрика конвертации объектов по схеме [Тип | Конвертор]."""

    def __init__(self) -> None:
        super().__init__()
        self.__basic = basic_convertor()
        self.__datetime = datetime_convertor()
        self.__reference = reference_convertor(self)

        self.__mapping: dict[type, abstract_convertor] = {
            int: self.__basic,
            float: self.__basic,
            str: self.__basic,
            bool: self.__basic,
            uuid.UUID: self.__basic,
            datetime: self.__datetime,
            date: self.__datetime,
            abstract: self.__reference,
        }

    def create(self, value: object) -> Optional[abstract_convertor]:
        """Классический подбор конвертора через словарь по типу данных."""
        if value is None:
            return None

        val_type = type(value)

        if val_type in self.__mapping:
            return self.__mapping[val_type]

        for base_type, convertor in self.__mapping.items():
            if issubclass(val_type, base_type):
                return convertor

        return None

    def convert(self, source: object) -> object:
        """Преобразование переданного объекта в структуру словарей и списков."""
        if source is None:
            return None

        if isinstance(source, (list, tuple, set)):
            return [self.convert(item) for item in source]

        if isinstance(source, dict):
            return {str(k): self.convert(v) for k, v in source.items()}

        if isinstance(source, abstract):
            result = {}
            for key, val in self.__extract_attributes(source).items():
                result[key] = self.__convert_field(key, val)
            return result

        convertor = self.create(source)
        if convertor is not None:
            res = convertor.convert("value", source)
            return res["value"]

        return str(source)

    def __convert_field(self, field_name: str, value: object) -> object:
        """Конвертация отдельного поля через конвертор из словаря."""
        if value is None:
            return None

        convertor = self.create(value)
        if convertor is not None:
            res = convertor.convert(field_name, value)
            return res[field_name]

        if isinstance(value, (list, tuple, set)):
            return [self.convert(item) for item in value]

        if isinstance(value, dict):
            return {str(k): self.convert(v) for k, v in value.items()}

        return str(value)

    def __extract_attributes(self, entity: abstract) -> dict:
        """Извлечение свойств сущности без синонимов и дублей."""
        fields = {}
        ignored = {"items", "unique_code", "base", "value"}

        cls = type(entity)
        for attr_name in dir(cls):
            if attr_name.startswith("_") or attr_name in ignored:
                continue
            prop = getattr(cls, attr_name, None)
            if isinstance(prop, property):
                try:
                    val = getattr(entity, attr_name)
                    if not callable(val):
                        fields[attr_name] = val
                except Exception:
                    pass

        return fields