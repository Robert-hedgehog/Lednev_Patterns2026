import json
import pydoc
from typing import Dict, Type, Callable
from Src.Core.abstract_deserializer import abstract_deserializer
from Src.Core.class_abstract import abstract
from Src.Core.validator import argument_exception
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Models.nomenclature_model import nomenclature_model, group_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Models.organization_model import organization_model
from Src.Models.settings_model import settings_model


class deserialize_factory(abstract_deserializer):
    """Фабрика десериализации данных."""

    def __init__(self) -> None:
        """Инициализация словарей диспетчеризации."""
        super().__init__()
        self.__mapping: Dict[str, Type[abstract]] = {
            "range_model": range_model,
            "storage_model": storage_model,
            "group_model": group_model,
            "nomenclature_model": nomenclature_model,
            "ingredient_model": ingredient_model,
            "recipe_model": recipe_model,
            "organization_model": organization_model,
            "settings_model": settings_model,
            "company": organization_model,
        }
        self.__handlers: Dict[type, Callable] = {
            str: self.__handle_string,
            list: self.__handle_list,
            dict: self.__handle_dict,
        }

    def deserialize(self, data: object) -> object:
        """Полиморфная диспетчеризация десериализации по типу объекта."""
        handler = self.__handlers.get(type(data), lambda val: val)
        return handler(data)

    def __handle_string(self, text: str) -> object:
        """Обработка JSON строки."""
        try:
            parsed = json.loads(text)
            return self.deserialize(parsed)
        except Exception as ex:
            raise argument_exception("text", f"Некорректный JSON: {ex}")

    def __handle_list(self, items: list) -> list:
        """Рекурсивная обработка списков."""
        return [self.deserialize(item) for item in items]

    def __handle_dict(self, data: dict) -> object:
        """Обработка словаря через сопоставление моделей."""
        if "type" in data:
            target_class = pydoc.locate(data["type"])
            if target_class and issubclass(target_class, abstract):
                return self.deserialize_entity(target_class, data)

        registered_keys = set(data.keys()) & set(self.__mapping.keys())
        return self.__dispatch_dict(registered_keys, data)

    def __dispatch_dict(self, registered_keys: set, data: dict) -> object:
        """Маршрутизация словаря: хранилище либо одиночная сущность."""
        actions = {
            True: lambda: {
                k: [self.deserialize_entity(self.__mapping[k], item) for item in data[k]]
                if isinstance(data[k], list) else self.deserialize(data[k])
                for k in data
            },
            False: lambda: data
        }
        has_keys = len(registered_keys) > 0
        return actions[has_keys]()

    def deserialize_entity(self, target_class: Type[abstract], data: dict) -> abstract:
        """Рекурсивная сборка сущности."""
        prepared_data = {
            key: self.deserialize_type(key, value)
            if isinstance(value, dict) and key in self.__mapping
            else (self.deserialize(value) if isinstance(value, (dict, list)) else value)
            for key, value in data.items()
            if key != "type"
        }
        return target_class.from_dict(prepared_data)

    def deserialize_type(self, type_name: str, data: dict) -> abstract:
        """Точечная десериализация конкретной сущности."""
        target_class = self.__mapping.get(type_name)
        if not target_class:
            raise argument_exception("type_name", f"Неизвестный тип: {type_name}")

        return self.deserialize_entity(target_class, data)