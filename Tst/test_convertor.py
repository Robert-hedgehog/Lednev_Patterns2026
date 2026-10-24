from datetime import datetime, date
import pytest

from Src.Core.validator import argument_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_manager import storage_manager
from Src.Models.storage_model import storage_model


def test_success_basic_convertor_numeric_and_string():
    """
    <summary>Проверка конвертации базовых типов (числа, строки, булевы).</summary>
    <description>Передаются int, float, str, bool с валидным именем поля.</description>
    <expected>Возвращается словарь с ключом и неизменным значением.</expected>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    res_str = convertor.convert("name", "Говядина")
    res_int = convertor.convert("count", 10)
    res_float = convertor.convert("weight", 12.5)
    res_bool = convertor.convert("is_active", True)

    # Проверки
    assert res_str == {"name": "Говядина"}
    assert res_int == {"count": 10}
    assert res_float == {"weight": 12.5}
    assert res_bool == {"is_active": True}


def test_exception_basic_convertor_invalid_type():
    """
    <summary>Проверка исключения basic_convertor при неверном типе значения.</summary>
    <description>Передается список вместо простого типа.</description>
    <expected>Выбрасывается argument_exception.</expected>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие и Проверки
    with pytest.raises(argument_exception):
        convertor.convert("items", [1, 2, 3])


def test_success_datetime_convertor_datetime_and_date():
    """
    <summary>Проверка конвертации DateTime и Date.</summary>
    <description>Передаются объекты datetime и date.</description>
    <expected>Возвращается словарь с форматированной датой в строковом виде.</expected>
    """
    # Подготовка
    convertor = datetime_convertor()
    dt = datetime(2026, 3, 30, 15, 30, 0)
    d = date(2026, 3, 30)

    # Действие
    res_dt = convertor.convert("created_at", dt)
    res_d = convertor.convert("date", d)

    # Проверки
    assert res_dt == {"created_at": "2026-03-30 15:30:00"}
    assert res_d == {"date": "2026-03-30"}


def test_exception_datetime_convertor_invalid_type():
    """
    <summary>Проверка исключения datetime_convertor при неверном типе.</summary>
    <description>Передается строка вместо datetime.</description>
    <expected>Выбрасывается argument_exception.</expected>
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие и Проверки
    with pytest.raises(argument_exception):
        convertor.convert("date", "2026-03-30")


def test_success_reference_convertor_domain_entity():
    """
    <summary>Проверка конвертации ссылочного типа Reference (доменной сущности).</summary>
    <description>Передается объект storage_model в reference_convertor.</description>
    <expected>Возвращается словарь с вложенными данными сущности.</expected>
    """
    # Подготовка
    convertor = reference_convertor()
    storage = storage_model.create("Основной склад", "ул. Ленина, 1")

    # Действие
    res = convertor.convert("storage", storage)

    # Проверки
    assert "storage" in res
    assert res["storage"]["name"] == "Основной склад"
    assert "id" in res["storage"]


def test_exception_reference_convertor_non_abstract_object():
    """
    <summary>Проверка исключения reference_convertor при не-доменном типе.</summary>
    <description>Передается число вместо наследника abstract.</description>
    <expected>Выбрасывается argument_exception.</expected>
    """
    # Подготовка
    convertor = reference_convertor()

    # Действие и Проверки
    with pytest.raises(argument_exception):
        convertor.convert("reference", 12345)


def test_success_convert_factory_nested_domain_structure():
    """
    <summary>Проверка работы convert_factory на сложной составной структуре.</summary>
    <description>Конвертируется рецепт с вложенными ингредиентами, единицами и полуфабрикатами.</description>
    <expected>Формируется вложенный словарь со всеми полями исходной структуры.</expected>
    """
    # Подготовка
    storage = storage_manager()
    storage.clear()
    storage.first_start()
    recipe = storage.recipes[1]
    factory = convert_factory()

    # Действие
    data = factory.convert(recipe)

    # Проверки
    assert isinstance(data, dict)
    assert data["name"] == recipe.name
    assert "ingredients" in data
    assert isinstance(data["ingredients"], list)
    assert len(data["ingredients"]) == len(recipe.ingredients)

    first_ingredient = data["ingredients"][0]
    assert "name" in first_ingredient
    assert "brutto" in first_ingredient
    assert "netto" in first_ingredient


def test_success_convert_factory_simple_types_and_lists():
    """
    <summary>Проверка convert_factory на примитивах, списках и словарях.</summary>
    <description>Передаются списки чисел, дат и вложенные словари.</description>
    <expected>Все типы корректно преобразуются в структуры данных.</expected>
    """
    # Подготовка
    factory = convert_factory()
    sample = {
        "title": "Тестовый отчет",
        "created_date": date(2026, 8, 31),
        "numbers": [1, 2, 3.5],
        "is_ready": True,
    }

    # Действие
    result = factory.convert(sample)

    # Проверки
    assert result["title"] == "Тестовый отчет"
    assert result["created_date"] == "2026-08-31"
    assert result["numbers"] == [1, 2, 3.5]
    assert result["is_ready"] is True