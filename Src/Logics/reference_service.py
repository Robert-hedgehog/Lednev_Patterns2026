from typing import Callable, Dict, List, Tuple, Type
from Src.Core.class_abstract import abstract
from Src.Core.common import common
from Src.Core.validator import validator, argument_exception, operation_exception
from Src.Logics.storage_manager import storage_manager
from Src.Logics.deserialize_factory import deserialize_factory


class reference_service:
    """Сервисный слой для CRUD-операций и контроля ссылочной целостности."""

    def __init__(self, storage: storage_manager = None) -> None:
        """Инициализация сервиса с хранилищем данных."""
        self.__storage = storage or storage_manager()
        self.__checkers: Dict[type, Callable] = {
            abstract: self.__check_abstract_ref,
            list: self.__check_iterable_ref,
            tuple: self.__check_iterable_ref,
            set: self.__check_iterable_ref,
        }

    def __resolve_meta(self, entity_type: str) -> Tuple[str, Type[abstract]]:
        """Поиск ключа коллекции и класса модели через рефлексию доменов."""
        normalized = str(entity_type).strip().lower()
        domains = common.domain_models(storage_manager)
        aliases = {key: key for key in domains}
        aliases.update({key.removesuffix("_model"): key for key in domains})
        aliases.update({
            "unit": storage_manager.range_key(),
            "receipt": storage_manager.recipe_key(),
        })

        target_key = aliases.get(normalized)
        if not target_key:
            raise argument_exception("entity_type", f"Неизвестный тип сущности: {entity_type}")
        return target_key, domains[target_key]

    def __check_abstract_ref(self, val: abstract, target_id: str, visited: set) -> bool:
        """Проверка ссылки внутри доменной сущности."""
        return str(val.id) == target_id or self.__contains_reference(val, target_id, visited)

    def __check_iterable_ref(self, val: object, target_id: str, visited: set) -> bool:
        """Проверка ссылок внутри коллекции элементов."""
        return any(self.__check_value_reference(item, target_id, visited) for item in val)

    def __check_value_reference(self, val: object, target_id: str, visited: set) -> bool:
        """Диспетчеризация проверки значения на ссылку по типу."""
        handler = next((fn for cls, fn in self.__checkers.items() if isinstance(val, cls)), None)
        return handler(val, target_id, visited) if handler else False

    def __contains_reference(self, obj: abstract, target_id: str, visited: set) -> bool:
        """Рекурсивный поиск ссылки на target_id в свойствах объекта."""
        obj_ptr = id(obj)
        if obj_ptr in visited:
            return False
        visited.add(obj_ptr)
        return any(
            self.__check_value_reference(getattr(obj, attr, None), target_id, visited)
            for attr in common.get_fields(obj)
        )

    def has_references(self, target: abstract) -> bool:
        """Универсальная проверка связей сущности со всеми объектами хранилища."""
        target_id = str(target.id)
        visited: set = set()
        items = (
            item for collection in self.__storage.data.values()
            for item in collection if str(item.id) != target_id
        )
        return any(self.__contains_reference(item, target_id, visited) for item in items)

    def get_all(self, entity_type: str) -> List[abstract]:
        """Получить список всех сущностей указанного типа."""
        key, _ = self.__resolve_meta(entity_type)
        return self.__storage.data.get(key, [])

    def get_by_id(self, entity_type: str, entity_id: str) -> abstract:
        """Найти сущность по типу и идентификатору."""
        search_id = str(entity_id).strip()
        found = next((item for item in self.get_all(entity_type) if str(item.id) == search_id), None)
        if not found:
            raise operation_exception(f"Сущность {entity_type} с кодом {entity_id} не найдена.")
        return found

    def create(self, entity_type: str, data: dict) -> abstract:
        """Создать и добавить новую сущность с валидацией."""
        validator.validate(data, dict)
        key, model_cls = self.__resolve_meta(entity_type)
        entity = deserialize_factory().deserialize_entity(model_cls, data)

        items = self.__storage.data.setdefault(key, [])
        if any(str(x.id) == str(entity.id) for x in items):
            raise operation_exception(f"Сущность с кодом {entity.id} уже существует.")

        items.append(entity)
        return entity

    def update(self, entity_type: str, entity_id: str, data: dict) -> abstract:
        """Обновить существующую сущность с проверкой целостности кода."""
        validator.validate(data, dict)
        key, model_cls = self.__resolve_meta(entity_type)
        existing = self.get_by_id(entity_type, entity_id)

        new_id = str(data.get("id", existing.id)).strip()
        if new_id != str(existing.id) and self.has_references(existing):
            raise operation_exception("Запрещено менять код сущности, связанной с другими сущностями.")

        payload = dict(data)
        payload.setdefault("id", str(existing.id))
        updated = deserialize_factory().deserialize_entity(model_cls, payload)

        items = self.__storage.data[key]
        items[items.index(existing)] = updated
        return updated

    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Удалить сущность после проверки отсутствия связей."""
        key, _ = self.__resolve_meta(entity_type)
        existing = self.get_by_id(entity_type, entity_id)

        if self.has_references(existing):
            raise operation_exception("Запрещено удалять сущность, связанную с другими сущностями.")

        self.__storage.data[key].remove(existing)
        return True