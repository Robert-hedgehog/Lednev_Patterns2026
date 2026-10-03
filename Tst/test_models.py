import pytest
from Src.Core.exception import arguments_exception
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model, group_model
from Src.Models.organization_model import organization_model
from Src.Models.storage_model import storage_model


def test_success_range_model_init_default():
    """
    <summary>Проверка создания единицы измерения по умолчанию.</summary>
    <description>Создается range_model без аргументов.</description>
    <expected>Коэффициент равен 1.0, базовая единица None.</expected>
    """
    unit = range_model()
    assert unit.conversion_factor == 1.0
    assert unit.base_range is None


def test_success_range_model_conversion_hierarchy():
    """
    <summary>Демонстрация работы с моделью единица измерения.</summary>
    <description>Создается базовая единица 'грамм' и производная 'кг' с коэффициентом 1000.</description>
    <expected>new_range имеет коэффициент 1000 и ссылается на base_range.</expected>
    """
    base_range = range_model("грамм", 1)
    new_range = range_model("кг", 1000, base_range)

    assert base_range.name == "грамм"
    assert new_range.name == "кг"
    assert new_range.conversion_factor == 1000.0
    assert new_range.base_range == base_range


def test_success_range_model_set_base_range_none():
    """
    <summary>Проверка сброса базовой единицы в None.</summary>
    <description>Присваивание None свойству base_range.</description>
    <expected>Свойство base_range равно None.</expected>
    """
    unit = range_model("кг", 1000)
    unit.base_range = None
    assert unit.base_range is None


def test_exception_range_model_conversion_factor_not_number():
    """
    <summary>Проверка передачи нечислового коэффициента пересчета.</summary>
    <description>В conversion_factor передается строка.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    with pytest.raises(arguments_exception):
        range_model("литр", "не_число")


def test_exception_range_model_conversion_factor_non_positive():
    """
    <summary>Проверка передачи нулевого или отрицательного коэффициента.</summary>
    <description>Проверяются значения 0 и -15.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    with pytest.raises(arguments_exception):
        range_model("кг", 0)

    with pytest.raises(arguments_exception):
        range_model("кг", -15)


def test_exception_range_model_invalid_base_range_type():
    """
    <summary>Проверка установки некорректного типа в base_range.</summary>
    <description>В свойство base_range передается строка вместо объекта range_model.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    unit = range_model("кг", 1)
    with pytest.raises(arguments_exception):
        unit.base_range = "не_range_model"


def test_success_group_model_init_default():
    """
    <summary>Проверка создания группы по умолчанию.</summary>
    <description>Создается group_model без аргументов.</description>
    <expected>Объект успешно создан.</expected>
    """
    group = group_model()
    assert group.id is not None


def test_success_group_model_init_valid():
    """
    <summary>Проверка успешного создания группы номенклатуры с именем.</summary>
    <description>Создается group_model с наименованием 'Мясо'.</description>
    <expected>Имя установлено, id сгенерирован.</expected>
    """
    group = group_model("Мясо")
    assert group.name == "Мясо"
    assert group.id is not None


def test_exception_group_model_empty_name():
    """
    <summary>Проверка ошибки при передаче пустого имени группы.</summary>
    <description>Передается пустая строка в наименование группы.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    with pytest.raises(arguments_exception):
        group_model("")


def test_exception_group_model_name_too_long():
    """
    <summary>Проверка лимита длины имени группы (> 50 символов).</summary>
    <description>Передается строка длиной 51 символ.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    with pytest.raises(arguments_exception):
        group_model("Г" * 51)


def test_success_nomenclature_model_full_init():
    """
    <summary>Проверка создания номенклатуры со всеми параметрами.</summary>
    <description>Заполняются краткое имя, полное имя, group и unit.</description>
    <expected>Все поля и связи сохранены.</expected>
    """
    group = group_model("Сырье")
    unit = range_model("кг", 1)
    item = nomenclature_model(
        name="Говядина",
        full_name="Говядина бескостная высший сорт",
        group=group,
        unit=unit
    )
    assert item.name == "Говядина"
    assert item.full_name == "Говядина бескостная высший сорт"
    assert item.group == group
    assert item.unit == unit


def test_success_nomenclature_model_default_full_name():
    """
    <summary>Проверка подстановки краткого имени в полное, если full_name не передан.</summary>
    <description>Передается только name='Сахар'.</description>
    <expected>full_name автоматически становится равен 'Сахар'.</expected>
    """
    item = nomenclature_model(name="Сахар")
    assert item.full_name == "Сахар"


def test_success_nomenclature_model_set_group_and_unit_none():
    """
    <summary>Проверка установки None в свойства group и unit номенклатуры.</summary>
    <description>Сброс ссылок на группу и единицу измерения.</description>
    <expected>Свойства становятся None без ошибок.</expected>
    """
    item = nomenclature_model(name="Тест")
    item.group = None
    item.unit = None
    assert item.group is None
    assert item.unit is None


def test_exception_nomenclature_model_full_name_empty():
    """
    <summary>Проверка валидации пустого full_name.</summary>
    <description>Устанавливается пустая строка в full_name.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    item = nomenclature_model(name="Товар")
    with pytest.raises(arguments_exception):
        item.full_name = "   "


def test_exception_nomenclature_model_full_name_too_long():
    """
    <summary>Проверка лимита длины full_name (> 255 символов).</summary>
    <description>Передается строка длиной 256 символов.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    item = nomenclature_model(name="Товар")
    with pytest.raises(arguments_exception):
        item.full_name = "А" * 256


def test_exception_nomenclature_model_full_name_not_string():
    """
    <summary>Проверка передачи нестрокового типа в full_name.</summary>
    <description>В full_name передается число 12345.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    item = nomenclature_model(name="Товар")
    with pytest.raises(arguments_exception):
        item.full_name = 12345


def test_exception_nomenclature_model_invalid_group_type():
    """
    <summary>Проверка типа поля group в номенклатуре.</summary>
    <description>В свойство group передается не group_model.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    item = nomenclature_model(name="Товар")
    with pytest.raises(arguments_exception):
        item.group = "Невалидная группа"


def test_exception_nomenclature_model_invalid_unit_type():
    """
    <summary>Проверка типа поля unit в номенклатуре.</summary>
    <description>В свойство unit передается число вместо range_model.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    item = nomenclature_model(name="Товар")
    with pytest.raises(arguments_exception):
        item.unit = 999


def test_success_organization_model_init_default():
    """
    <summary>Проверка создания организации без аргументов.</summary>
    <description>Создается organization_model по умолчанию.</description>
    <expected>Объект успешно создан.</expected>
    """
    org = organization_model()
    assert org.id is not None


def test_success_organization_model_valid_10_digits_inn():
    """
    <summary>Проверка создания организации с 10-значным ИНН (юрлицо).</summary>
    <description>Задаются валидные реквизиты: ИНН 10 цифр, БИК 9 цифр, счет 20 цифр, форма 'ООО'.</description>
    <expected>Все поля успешно сохранены.</expected>
    """
    org = organization_model(
        name="ООО Ромашка",
        inn="7701234567",
        bik="044525225",
        account="40702810900000001234",
        ownership_type="ООО"
    )
    assert org.inn == "7701234567"
    assert org.bik == "044525225"
    assert org.account == "40702810900000001234"
    assert org.ownership_type == "ООО"


def test_success_organization_model_valid_12_digits_inn():
    """
    <summary>Проверка создания организации с 12-значным ИНН (ИП).</summary>
    <description>Задается ИНН длиной 12 цифр.</description>
    <expected>ИНН успешно сохранен.</expected>
    """
    org = organization_model(name="ИП Иванов", inn="770123456789")
    assert org.inn == "770123456789"


def test_exception_organization_model_inn_not_string():
    """
    <summary>Проверка передачи нестрокового ИНН.</summary>
    <description>В поле ИНН передается целое число.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    org = organization_model(name="Тест")
    with pytest.raises(arguments_exception):
        org.inn = 7701234567


def test_exception_organization_model_inn_invalid_length_or_chars():
    """
    <summary>Проверка валидации некорректного ИНН.</summary>
    <description>Проверяются: короткий ИНН (9 цифр), длинный ИНН (13 цифр), буквы в ИНН.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    org = organization_model(name="Тест")
    with pytest.raises(arguments_exception):
        org.inn = "123456789"
    with pytest.raises(arguments_exception):
        org.inn = "1234567890123"
    with pytest.raises(arguments_exception):
        org.inn = "770123456A"


def test_exception_organization_model_bik_invalid():
    """
    <summary>Проверка валидации БИК (ровно 9 цифр).</summary>
    <description>Передаются значения БИК с длиной != 9, не строкой и с буквами.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    org = organization_model(name="Тест")
    with pytest.raises(arguments_exception):
        org.bik = 44525225  # int
    with pytest.raises(arguments_exception):
        org.bik = "04452522"  # 8 цифр
    with pytest.raises(arguments_exception):
        org.bik = "abcdefghi"  # буквы


def test_exception_organization_model_account_invalid():
    """
    <summary>Проверка валидации расчетного счета (ровно 20 цифр).</summary>
    <description>Передаются значения счета с неверной длиной, типом и с буквами.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    org = organization_model(name="Тест")
    with pytest.raises(arguments_exception):
        org.account = 40702810900000001234  # int
    with pytest.raises(arguments_exception):
        org.account = "40702810"  # короткий
    with pytest.raises(arguments_exception):
        org.account = "4070281090000000123A"  # буква


def test_exception_organization_model_ownership_type_invalid():
    """
    <summary>Проверка валидации формы собственности.</summary>
    <description>Проверяются пустая строка, не строка и строка более 50 символов.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    org = organization_model(name="Тест")
    with pytest.raises(arguments_exception):
        org.ownership_type = ""
    with pytest.raises(arguments_exception):
        org.ownership_type = 12345
    with pytest.raises(arguments_exception):
        org.ownership_type = "Ф" * 51


def test_success_storage_model_init_default():
    """
    <summary>Проверка создания склада по умолчанию.</summary>
    <description>Создается storage_model без параметров.</description>
    <expected>Склад создан, адрес пустой.</expected>
    """
    storage = storage_model()
    assert storage.id is not None
    assert storage.address == ""


def test_success_storage_model_init_valid():
    """
    <summary>Проверка корректной инициализации склада с адресом.</summary>
    <description>Создается склад с именем и адресом.</description>
    <expected>Имя и адрес сохранены.</expected>
    """
    storage = storage_model("Склад сырья", "г. Москва, ул. Заводская, д. 2")
    assert storage.name == "Склад сырья"
    assert storage.address == "г. Москва, ул. Заводская, д. 2"


def test_exception_storage_model_address_not_string():
    """
    <summary>Проверка передачи нестрокового адреса склада.</summary>
    <description>В свойство address передается число.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    storage = storage_model("Склад")
    with pytest.raises(arguments_exception):
        storage.address = 12345


def test_exception_storage_model_address_too_long():
    """
    <summary>Проверка превышения лимита длины адреса (> 255 символов).</summary>
    <description>Передается адрес длиной 256 символов.</description>
    <expected>Выбрасывается arguments_exception.</expected>
    """
    storage = storage_model("Склад")
    with pytest.raises(arguments_exception):
        storage.address = "А" * 256
