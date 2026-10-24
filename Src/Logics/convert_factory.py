from datetime import datetime, date
import uuid
from Src.Core.class_abstract import abstract
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor


class convert_factory:
    """Фабрика конвертации произвольных объектов и структур данных в словари."""

    def __init__(self) -> None:
        self.__basic = basic_convertor()
        self.__datetime = datetime_convertor()
        self.__reference = reference_convertor(self)

    def convert(self, source: object) -> object:
        """Преобразование переданного объекта в структуру словарей и списков."""

        if source is None:
            return None

        if isinstance(source, (int, float, str, bool)):
            return source

        if isinstance(source, uuid.UUID):
            return str(source)

        if isinstance(source, (datetime, date)):
            res = self.__datetime.convert("value", source)
            return res["value"]

        if isinstance(source, (list, tuple, set)):
            return [self.convert(item) for item in source]

        if isinstance(source, dict):
            return {str(k): self.convert(v) for k, v in source.items()}

        if isinstance(source, abstract):
            result = {}
            for key, val in self.__extract_attributes(source).items():
                converted_val = self.__convert_field(key, val)
                result[key] = converted_val
            return result

        return str(source)

    def __convert_field(self, field_name: str, value: object) -> object:
        """Маршрутизация значения поля на соответствующий конвертор."""
        if value is None:
            return None

        if isinstance(value, (int, float, str, bool)):
            res = self.__basic.convert(field_name, value)
            return res[field_name]

        if isinstance(value, uuid.UUID):
            res = self.__basic.convert(field_name, str(value))
            return res[field_name]

        if isinstance(value, (datetime, date)):
            res = self.__datetime.convert(field_name, value)
            return res[field_name]

        if isinstance(value, abstract):
            res = self.__reference.convert(field_name, value)
            return res[field_name]

        if isinstance(value, (list, tuple, set)):
            return [self.convert(item) for item in value]

        if isinstance(value, dict):
            return {str(k): self.convert(v) for k, v in value.items()}

        return str(value)
    
    def __extract_attributes(self, entity: abstract) -> dict:
        """Извлечение публичных свойств и приватных полей доменной модели."""
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

    def serialize(self, source: object) -> object:
        """Алиас для метода convert."""
        return self.convert(source)