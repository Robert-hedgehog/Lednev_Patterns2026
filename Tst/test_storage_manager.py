# Tst/test_storage_manager.py

import pytest
from Src.Logics.storage_manager import storage_manager
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Core.validator import argument_exception


@pytest.fixture(autouse=True)
def reset_storage_manager():
    """Фикстура для сброса и первоначального наполнения хранилища перед каждым тестом."""
    manager = storage_manager()
    manager.clear()
    manager.first_start()
    yield manager


def test_success_storage_manager_singleton_same_instance():
    """
    <summary>Проверка реализации паттерна Singleton для storage_manager.</summary>
    <description>Создаются два экземпляра storage_manager в разные моменты времени.</description>
    <expected>Обе переменные ссылаются на один и тот же объект в памяти.</expected>
    """
    manager1 = storage_manager()
    manager2 = storage_manager()

    assert manager1 is manager2
    assert manager1 == manager2


def test_success_storage_manager_first_start_seeded_units():
    """
    <summary>Проверка формирования единиц измерения при первом старте.</summary>
    <description>Проверяется наличие базовых единиц 'грамм', 'кг', 'литр' в storage_manager.</description>
    <expected>Коллекция units содержит созданные единицы измерения.</expected>
    """
    manager = storage_manager()
    unit_names = [u.name for u in manager.units]

    assert len(manager.units) >= 5
    assert "грамм" in unit_names
    assert "киллограмм" in unit_names
    assert "литр" in unit_names


def test_success_storage_manager_first_start_seeded_groups():
    """
    <summary>Проверка формирования групп номенклатуры при первом старте.</summary>
    <description>Проверяется наличие групп сырья, полуфабрикатов и горячих блюд.</description>
    <expected>Все ключевые группы присутствуют в коллекции groups.</expected>
    """
    manager = storage_manager()
    group_names = [g.name for g in manager.groups]

    assert "Сырье и мясная продукция" in group_names
    assert "Кулинарные полуфабрикаты" in group_names
    assert "Авторские горячие блюда" in group_names


def test_success_storage_manager_first_start_seeded_storages():
    """
    <summary>Проверка формирования складов при первом старте.</summary>
    <description>Проверяется создание производственного цеха и складов ресторанов.</description>
    <expected>Склады успешно созданы, цех и склады ресторанов присутствуют.</expected>
    """
    manager = storage_manager()
    storage_names = [s.name for s in manager.storages]

    assert len(manager.storages) >= 3
    assert "Производственный цех" in storage_names


def test_success_storage_manager_first_start_seeded_nomenclatures():
    """
    <summary>Проверка формирования позиций номенклатуры при первом старте.</summary>
    <description>Проверяются ингредиенты и блюдо 'Дождевая каша со щекой'.</description>
    <expected>Номенклатура содержит говяжьи щеки, крупу и готовое фирменное блюдо.</expected>
    """
    manager = storage_manager()
    item_names = [item.name for item in manager.nomenclatures]

    assert "Говяжьи щеки" in item_names
    assert "Крупа дождевая" in item_names
    assert "Дождевая каша со щекой" in item_names


def test_success_storage_manager_item_uniqueness():
    """
    <summary>Проверка обеспечения уникальности объектов в хранилище.</summary>
    <description>Повторно добавляется один и тот же объект склада.</description>
    <expected>Количество складов не увеличивается, дубликаты отсутствуют.</expected>
    """
    manager = storage_manager()
    custom_storage = storage_model("Дополнительный склад", "ул. Южная, 12")

    initial_count = len(manager.storages)
    manager.add_storage(custom_storage)
    manager.add_storage(custom_storage)

    assert len(manager.storages) == initial_count + 1


def test_exception_storage_manager_add_invalid_type():
    """
    <summary>Проверка валидации типа при добавлении в хранилище.</summary>
    <description>Попытка передать строку вместо объекта range_model в add_unit.</description>
    <expected>Выбрасывается argument_exception.</expected>
    """
    manager = storage_manager()
    with pytest.raises(argument_exception):
        manager.add_unit("не_модель_единицы")


def test_success_storage_manager_convert():
    """
    <summary>Проверка вызова метода convert.</summary>
    <description>Вызов метода convert и проверка флага is_loaded.</description>
    <expected>Метод возвращает True, свойство is_loaded равно True.</expected>
    """
    manager = storage_manager()
    assert manager.convert() is True
    assert manager.is_loaded is True