from typing import Callable, Dict, List, Set
from Src.Core.class_abstract import abstract
from Src.Core.prototype import prototype
from Src.Core.validator import validator
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_type_enum import filter_type_enum
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Models.transaction_model import transaction_model


class domain_prototype(prototype):
    """Универсальный прототип фильтрации для всех доменных моделей."""

    def __init__(self, data: List[abstract] = None) -> None:
        """Инициализация прототипа со словарями сопоставления и связей."""
        super().__init__(data)
        self.__matchers: Dict[filter_type_enum, Callable[[str, str], bool]] = {
            filter_type_enum.EQUALS: lambda actual, expected: actual == expected,
            filter_type_enum.LIKE: lambda actual, expected: expected.lower() in actual.lower(),
        }
        self.__nested_extractors: Dict[type, Callable[[abstract], List[object]]] = {
            range_model: lambda x: [x.base_range],
            nomenclature_model: lambda x: [x.group, x.unit],
            ingredient_model: lambda x: [x.nomenclature, x.unit, x.recipe],
            recipe_model: lambda x: [x.dish, *x.ingredients],
            transaction_model: lambda x: [x.storage, x.nomenclature, x.unit],
        }
        self.__path_handlers: Dict[type, Callable[[object, List[str]], List[object]]] = {
            list: self.__resolve_list_path,
        }

    def filter(self, dto: filter_dto) -> "domain_prototype":
        """Фильтрация данных по DTO с возвратом нового клона прототипа."""
        validator.validate(dto, filter_dto)
        if not dto.value:
            return self.clone(list(self.data))

        filtered = [item for item in self.data if self.__matches_entity(item, dto)]
        return self.clone(filtered)

    def __matches_entity(self, entity: abstract, dto: filter_dto) -> bool:
        """Проверка соответствия сущности и её вложенных структур условию фильтра."""
        matcher = self.__matchers[dto.filter_type]
        if "." in dto.field_name:
            values = self.__resolve_path_values(entity, dto.field_name.split("."))
            return any(matcher(str(val).strip(), dto.value) for val in values)

        queue: List[object] = [entity]
        visited: Set[int] = set()

        while queue:
            current = queue.pop(0)
            if current is None:
                continue
            ptr = id(current)
            if ptr in visited:
                continue
            visited.add(ptr)

            field_value = getattr(current, dto.field_name, None)
            if field_value is not None and matcher(str(field_value).strip(), dto.value):
                return True

            extractor = self.__nested_extractors.get(type(current))
            if extractor is not None:
                queue.extend(child for child in extractor(current) if child is not None)

        return False

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