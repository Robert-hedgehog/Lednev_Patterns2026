from typing import Callable, Dict, List, Set, Tuple, Type
from Src.Core.class_abstract import abstract
from Src.Core.common import common
from Src.Core.validator import validator, argument_exception, operation_exception
from Src.Logics.storage_manager import storage_manager
from Src.Logics.deserialize_factory import deserialize_factory
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Models.transaction_model import transaction_model
from Src.Core.event_type import event_type
from Src.Logics.observer import observer


class reference_service:
    """Сервисный слой для CRUD-операций и контроля ссылочной целостности."""

    def __init__(self, storage: storage_manager = None) -> None:
        """Инициализация сервиса с хранилищем и обратным индексом ссылок."""
        self.__storage = storage or storage_manager()
        self.__ref_index: Dict[str, Set[str]] = {}
        self.__entity_refs: Dict[str, Set[str]] = {}
        self.__indexed_version: int = -1
        self.__extractors: Dict[type, Callable[[abstract], List[object]]] = {
            range_model: lambda x: [x.base_range],
            nomenclature_model: lambda x: [x.group, x.unit],
            ingredient_model: lambda x: [x.nomenclature, x.unit, x.recipe],
            recipe_model: lambda x: [x.dish, *x.ingredients],
            transaction_model: lambda x: [x.storage, x.nomenclature, x.unit],
        }

    def __resolve_meta(self, entity_type: str) -> Tuple[str, Type[abstract]]:
        """Поиск ключа коллекции и класса модели."""
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

    def __extract_ref_ids(self, entity: abstract) -> Set[str]:
        """Извлечение идентификаторов связанных сущностей без рефлексии."""
        refs: Set[str] = set()
        root_id = str(entity.id)
        queue: List[abstract] = [entity]
        visited: Set[int] = set()

        while queue:
            current = queue.pop()
            ptr = id(current)
            if ptr in visited:
                continue
            visited.add(ptr)

            extractor = self.__extractors.get(type(current))
            if not extractor:
                continue

            for linked in extractor(current):
                if linked is None:
                    continue
                linked_id = str(linked.id)
                if linked_id != root_id:
                    refs.add(linked_id)
                if type(linked) in self.__extractors:
                    queue.append(linked)

        return refs

    def __index_entity(self, entity: abstract) -> None:
        """Добавление связей сущности в обратный индекс."""
        owner_id = str(entity.id)
        refs = self.__extract_ref_ids(entity)
        self.__entity_refs[owner_id] = refs
        for ref_id in refs:
            self.__ref_index.setdefault(ref_id, set()).add(owner_id)

    def __unindex_entity(self, entity: abstract) -> None:
        """Удаление связей сущности из обратного индекса."""
        owner_id = str(entity.id)
        for ref_id in self.__entity_refs.pop(owner_id, ()):
            owners = self.__ref_index.get(ref_id)
            if owners:
                owners.discard(owner_id)
                if not owners:
                    del self.__ref_index[ref_id]

    def __rebuild_index(self) -> None:
        """Построение обратного индекса по текущему состоянию хранилища."""
        self.__ref_index.clear()
        self.__entity_refs.clear()
        for collection in self.__storage.data.values():
            for item in collection:
                self.__index_entity(item)
        self.__indexed_version = self.__storage.version

    def __sync_index(self) -> None:
        """Синхронизация индекса при изменении версии хранилища."""
        if self.__indexed_version != self.__storage.version:
            self.__rebuild_index()

    def has_references(self, target: abstract) -> bool:
        """Проверка наличия связей сущности по обратному индексу."""
        self.__sync_index()
        return bool(self.__ref_index.get(str(target.id)))

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
        """Создать и добавить новую сущность с обновлением индекса."""
        self.__sync_index()
        validator.validate(data, dict)
        key, model_cls = self.__resolve_meta(entity_type)
        entity = deserialize_factory().deserialize_entity(model_cls, data)

        items = self.__storage.data.setdefault(key, [])
        if any(str(x.id) == str(entity.id) for x in items):
            raise operation_exception(f"Сущность с кодом {entity.id} уже существует.")

        items.append(entity)
        self.__index_entity(entity)
        observer.create(event_type.crud_create(), {"entity_type": entity_type, "id": str(entity.id)})
        return entity

    def update(self, entity_type: str, entity_id: str, data: dict) -> abstract:
        """Обновить существующую сущность с проверкой целостности кода."""
        self.__sync_index()
        validator.validate(data, dict)
        key, model_cls = self.__resolve_meta(entity_type)
        existing = self.get_by_id(entity_type, entity_id)

        new_id = str(data.get("id", existing.id)).strip()
        if new_id != str(existing.id) and self.has_references(existing):
            raise operation_exception("Запрещено менять код сущности, связанной с другими сущностями.")

        payload = dict(data)
        payload.setdefault("id", str(existing.id))
        updated = deserialize_factory().deserialize_entity(model_cls, payload)

        self.__unindex_entity(existing)
        items = self.__storage.data[key]
        items[items.index(existing)] = updated
        self.__index_entity(updated)
        observer.create(event_type.crud_update(), {"entity_type": entity_type, "id": str(updated.id)})
        return updated

    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Удалить сущность после проверки отсутствия связей."""
        self.__sync_index()
        key, _ = self.__resolve_meta(entity_type)
        existing = self.get_by_id(entity_type, entity_id)

        if self.has_references(existing):
            raise operation_exception("Запрещено удалять сущность, связанную с другими сущностями.")

        self.__unindex_entity(existing)
        self.__storage.data[key].remove(existing)
        observer.create(event_type.crud_delete(), {"entity_type": entity_type, "id": str(existing.id)})
        return True