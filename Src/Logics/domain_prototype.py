from typing import Callable, Dict, List
from Src.Core.class_abstract import abstract
from Src.Core.prototype import prototype
from Src.Core.validator import validator
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_type_enum import filter_type_enum


class domain_prototype(prototype):
    """Универсальный прототип фильтрации для всех доменных моделей."""

    def __init__(self, data: List[abstract] = None) -> None:
        """Инициализация прототипа со словарями сопоставления и связей."""
        super().__init__(data)
        self.__matchers: Dict[filter_type_enum, Callable[[object, object], bool]] = {
            filter_type_enum.EQUALS: self.__match_equals,
            filter_type_enum.LIKE: lambda actual, expected: str(expected).strip().lower() in str(actual).strip().lower(),
            filter_type_enum.LESS: lambda actual, expected: actual < expected,
            filter_type_enum.LESS_OR_EQUAL: lambda actual, expected: actual <= expected,
            filter_type_enum.GREATER: lambda actual, expected: actual > expected,
            filter_type_enum.GREATER_OR_EQUAL: lambda actual, expected: actual >= expected,
        }
        self.__path_handlers: Dict[type, Callable[[object, List[str]], List[object]]] = {
            list: self.__resolve_list_path,
        }

    def filter(self, dto: filter_dto) -> "domain_prototype":
        """Фильтрация данных по DTO с возвратом нового клона прототипа."""
        validator.validate(dto, filter_dto)
        if dto.value == "":
            return self.clone(list(self.data))

        filtered = [item for item in self.data if self.__matches_entity(item, dto)]
        return self.clone(filtered)

    def __match_equals(self, actual: object, expected: object) -> bool:
        """Проверка точного совпадения значений."""
        if type(actual) is type(expected):
            return actual == expected
        return str(actual).strip() == str(expected).strip()

    def __matches_entity(self, entity: abstract, dto: filter_dto) -> bool:
        """Проверка соответствия сущности и её вложенных структур условию фильтра."""
        matcher = self.__matchers[dto.filter_type]
        path = f"{dto.model_name}.{dto.field_name}" if dto.model_name else dto.field_name
        values = self.__resolve_path_values(entity, path.split("."))
        return any(matcher(val, dto.value) for val in values)

    def __resolve_list_path(self, items: list, parts: List[str]) -> List[object]:
        """Извлечение значений по пути для списка дочерних элементов."""
        result: List[object] = []
        for item in items:
            result.extend(self.__resolve_path_values(item, parts))
        return result

    def __resolve_path_values(self, current: object, parts: List[str]) -> List[object]:
        """Извлечение значений по вложенному пути атрибутов."""
        if current is None:
            return []
        if not parts:
            return [current]

        handler = self.__path_handlers.get(type(current))
        if handler is not None:
            return handler(current, parts)

        next_obj = getattr(current, parts[0], None)
        return self.__resolve_path_values(next_obj, parts[1:])