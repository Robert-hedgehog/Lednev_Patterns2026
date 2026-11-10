import json
import pytest
from Src.Logics.storage_manager import storage_manager
from Src.Logics.convert_factory import convert_factory
from Src.Logics.deserialize_factory import deserialize_factory
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model


@pytest.fixture(autouse=True)
def init_storage():
    """Подготовка хранилища."""
    # Подготовка
    manager = storage_manager()
    manager.clear()
    manager.first_start()
    yield manager


def test_success_deserialize_single_storage_model():
    """
    <summary>Проверка десериализации одиночной модели склада.</summary>
    <description>Склад сериализуется в словарь и восстанавливается через фабричный метод from_dict.</description>
    <expected>Восстановленный объект эквивалентен исходному по id и атрибутам.</expected>
    """
    # Подготовка
    original = storage_model.create("Тестовый склад", "ул. Мира, 1")
    factory = convert_factory()
    serialized = factory.convert(original)

    # Действие
    deserialized = storage_model.from_dict(serialized)

    # Проверки
    assert deserialized == original
    assert deserialized.name == original.name
    assert deserialized.address == original.address


def test_success_deserialize_single_range_model_with_base():
    """
    <summary>Проверка десериализации единицы измерения с базовой единицей через рекурсию.</summary>
    <description>Создается килограмм с базовым граммом, сериализуется и восстанавливается через фабрику.</description>
    <expected>Вложенная базовая единица измерения корректно десериализована.</expected>
    """
    # Подготовка
    original = range_model.create_killogramm()
    c_factory = convert_factory()
    d_factory = deserialize_factory()
    serialized = c_factory.convert(original)

    # Действие
    deserialized = d_factory.deserialize_entity(range_model, serialized)

    # Проверки
    assert deserialized == original
    assert deserialized.name == "киллограмм"
    assert deserialized.conversion_factor == 1000.0
    assert deserialized.base_range is not None
    assert deserialized.base_range.name == "грамм"


def test_success_deserialize_full_storage_manager_data_compare():
    """
    <summary>Сравнение десериализованных данных с моделями storage_manager.</summary>
    <description>Полный цикл: сериализация storage_manager.data в JSON и обратная рекурсивная десериализация.</description>
    <expected>Все коллекции, объекты, атрибуты и вложенные структуры совпадают с исходными.</expected>
    """
    # Подготовка
    storage = storage_manager()
    c_factory = convert_factory()
    d_factory = deserialize_factory()

    serialized_data = c_factory.convert(storage.data)
    json_text = json.dumps(serialized_data, ensure_ascii=False)

    # Действие
    restored_data = d_factory.deserialize(json_text)

    # Проверки
    assert isinstance(restored_data, dict)

    original_storages = storage.storages
    restored_storages = restored_data[storage_manager.storage_key()]
    assert len(restored_storages) == len(original_storages)
    for orig, rest in zip(original_storages, restored_storages):
        assert rest == orig
        assert rest.name == orig.name
        assert rest.address == orig.address

    original_units = storage.units
    restored_units = restored_data[storage_manager.range_key()]
    assert len(restored_units) == len(original_units)
    for orig, rest in zip(original_units, restored_units):
        assert rest == orig
        assert rest.name == orig.name
        assert rest.conversion_factor == orig.conversion_factor

    original_recipes = storage.recipes
    restored_recipes = restored_data[storage_manager.recipe_key()]
    assert len(restored_recipes) == len(original_recipes)

    orig_main = original_recipes[1]
    rest_main = restored_recipes[1]
    assert rest_main == orig_main
    assert rest_main.name == orig_main.name
    assert rest_main.brutto == orig_main.brutto
    assert rest_main.netto == orig_main.netto
    assert len(rest_main.ingredients) == len(orig_main.ingredients)

    orig_semi_ing = orig_main.ingredients[0]
    rest_semi_ing = rest_main.ingredients[0]
    assert rest_semi_ing.name == orig_semi_ing.name
    assert rest_semi_ing.recipe is not None
    assert rest_semi_ing.recipe.name == orig_semi_ing.recipe.name


def test_success_deserialize_factory_by_type_name():
    """
    <summary>Проверка десериализации одиночного объекта по наименованию типа.</summary>
    <description>Вызов метода deserialize_type для конкретной модели склада.</description>
    <expected>Возвращается валидный экземпляр storage_model.</expected>
    """
    # Подготовка
    d_factory = deserialize_factory()
    payload = {"id": "11111111-1111-1111-1111-111111111111", "name": "Цех", "address": "ул. Заводская"}

    # Действие
    result = d_factory.deserialize_type("storage_model", payload)

    # Проверки
    assert isinstance(result, storage_model)
    assert result.name == "Цех"
    assert result.address == "ул. Заводская"