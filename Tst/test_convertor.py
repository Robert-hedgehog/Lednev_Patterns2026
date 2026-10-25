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


def test_success_reference_convertor_with_factory_property():
    """
    <summary>Проверка reference_convertor и его свойства factory.</summary>
    <description>Проверяется геттер, сеттер factory и сериализация сущности.</description>
    <expected>Свойство factory устанавливается с валидацией, сущность сериализуется.</expected>
    """
    # Подготовка
    factory = convert_factory()
    convertor = reference_convertor()
    convertor.factory = factory
    storage = storage_model.create("Основной склад", "ул. Ленина, 1")

    # Действие
    res = convertor.convert("storage", storage)

    # Проверки
    assert convertor.factory == factory
    assert "storage" in res
    assert res["storage"]["name"] == "Основной склад"


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


def test_success_convert_factory_create_by_type_mapping():
    """
    <summary>Проверка подбора конвертора через словарь типов в convert_factory.</summary>
    <description>Вызывается create для чисел, дат и сущностей.</description>
    <expected>Метод create возвращает нужный конвертор из словаря __mapping.</expected>
    """
    # Подготовка
    factory = convert_factory()
    storage = storage_model.create("Склад")

    # Действие
    conv_int = factory.create(100)
    conv_str = factory.create("текст")
    conv_date = factory.create(date.today())
    conv_ref = factory.create(storage)

    # Проверки
    assert conv_int.__class__.__name__ == "basic_convertor"
    assert conv_str.__class__.__name__ == "basic_convertor"
    assert conv_date.__class__.__name__ == "datetime_convertor"
    assert conv_ref.__class__.__name__ == "reference_convertor"


def test_success_convert_factory_full_storage_dump():
    """
    <summary>Проверка полной сериализации всех данных storage_manager в единую структуру.</summary>
    <description>Конвертируется весь словарь storage.data с коллекциями складов, единиц и рецептов.</description>
    <expected>Формируется словарь, содержащий все зарегистрированные доменные коллекции.</expected>
    """
    # Подготовка
    storage = storage_manager()
    storage.clear()
    storage.first_start()
    factory = convert_factory()

    # Действие
    data = factory.convert(storage.data)

    # Проверки
    assert isinstance(data, dict)
    assert storage_manager.range_key() in data
    assert storage_manager.storage_key() in data
    assert storage_manager.nomenclature_key() in data
    assert storage_manager.recipe_key() in data
    assert len(data[storage_manager.recipe_key()]) >= 2