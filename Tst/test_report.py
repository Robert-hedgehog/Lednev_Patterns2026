import pytest
from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_enum import report_type_enum
from Src.Dtos.report_data_dto import report_data_dto
from Src.Models.settings_model import settings_model
from Src.Core.validator import argument_exception


@pytest.fixture(autouse=True)
def init_storage():
    """Подготовка хранилища."""
    # Подготовка
    manager = storage_manager()
    manager.clear()
    manager.first_start()
    yield manager


def test_success_report_factory_create_all_five_formats():
    """
    <summary>Проверка создания всех 5 форматов через фабрику.</summary>
    <description>Запрашиваются отчеты TXT, CSV, Markdown, XML, HTML.</description>
    <expected>Для каждого типа возвращается соответствующий объект отчета.</expected>
    """
    # Подготовка
    factory = report_factory()
    formats = [
        report_type_enum.TXT,
        report_type_enum.CSV,
        report_type_enum.MARKDOWN,
        report_type_enum.XML,
        report_type_enum.HTML,
    ]

    # Действие и Проверки
    for fmt in formats:
        # Действие
        reporter = factory.create(fmt)

        # Проверки
        assert reporter is not None


def test_success_report_factory_create_default():
    """
    <summary>Проверка создания отчета через метод create_default.</summary>
    <description>Задаются форматы HTML и CSV в настройках, вызывается create_default.</description>
    <expected>Фабрика создает генератор согласно переданным настройкам.</expected>
    """
    # Подготовка
    custom_settings = settings_model()

    # Действие 1 (HTML)
    custom_settings.response_format = report_type_enum.HTML
    factory_html = report_factory(custom_settings)
    reporter_html = factory_html.create_default()

    # Проверки 1
    assert reporter_html.__class__.__name__ == "html_report"

    # Действие 2 (CSV)
    custom_settings.response_format = report_type_enum.CSV
    factory_csv = report_factory(custom_settings)
    reporter_csv = factory_csv.create_default()

    # Проверки 2
    assert reporter_csv.__class__.__name__ == "csv_report"


def test_success_build_all_five_formats_with_report_data_dto():
    """
    <summary>Проверка формирования данных во всех 5 форматах через универсальный report_data_dto.</summary>
    <description>Формируются отчеты TXT, CSV, Markdown, XML, HTML для рецепта.</description>
    <expected>Каждый генератор корректно заполняет DTO данными рецепта.</expected>
    """
    # Подготовка
    manager = storage_manager()
    recipe = manager.recipes[0]
    data_dto = manager.get_report_data("recipe", recipe.name)
    factory = report_factory()

    # Действие 1: TXT
    txt_reporter = factory.create(report_type_enum.TXT)
    txt_result = txt_reporter.build(data_dto)

    # Проверки 1
    assert len(txt_result.text) > 0
    assert recipe.name in txt_result.text

    # Действие 2: CSV
    csv_reporter = factory.create(report_type_enum.CSV)
    csv_result = csv_reporter.build(data_dto)

    # Проверки 2
    assert len(csv_result.binary) > 0
    csv_decoded = bytes(csv_result.binary).decode("utf-8")
    assert "id;name;brutto;netto" in csv_decoded
    assert recipe.ingredients[0].name in csv_decoded

    # Действие 3: Markdown
    md_reporter = factory.create(report_type_enum.MARKDOWN)
    md_result = md_reporter.build(data_dto)

    # Проверки 3
    assert len(md_result.binary) > 0
    md_decoded = bytes(md_result.binary).decode("utf-8")
    assert f"# Отчет: {recipe.name}" in md_decoded

    # Действие 4: XML
    xml_reporter = factory.create(report_type_enum.XML)
    xml_result = xml_reporter.build(data_dto)

    # Проверки 4
    assert len(xml_result.text) > 0
    assert "<report>" in xml_result.text
    assert f"<title>{recipe.name}</title>" in xml_result.text

    # Действие 5: HTML
    html_reporter = factory.create(report_type_enum.HTML)
    html_result = html_reporter.build(data_dto)

    # Проверки 5
    assert len(html_result.text) > 0
    assert "<!DOCTYPE html>" in html_result.text
    assert f"<h2>{recipe.name}</h2>" in html_result.text


def test_success_get_report_data_for_nomenclature_and_range():
    """
    <summary>Проверка формирования report_data_dto для номенклатуры и единицы измерения.</summary>
    <description>Запрашиваются данные номенклатуры и единицы через хранилище.</description>
    <expected>Формируются валидные объекты report_data_dto с соответствующими колонками.</expected>
    """
    # Подготовка
    manager = storage_manager()
    nom = manager.nomenclatures[0]
    unit = manager.units[0]

    # Действие 1: Номенклатура
    nom_dto = manager.get_report_data("nomenclature", nom.name)

    # Проверки 1
    assert nom_dto is not None
    assert nom_dto.title == nom.name
    assert "full_name" in nom_dto.headers

    # Действие 2: Единица измерения
    unit_dto = manager.get_report_data("range", unit.name)

    # Проверки 2
    assert unit_dto is not None
    assert unit_dto.title == unit.name
    assert "conversion_factor" in unit_dto.headers


def test_exception_report_factory_unsupported_format():
    """
    <summary>Проверка исключения при запросе неподдерживаемого формата.</summary>
    <description>В фабрику передается несуществующий строковый тип.</description>
    <expected>Выбрасывается argument_exception.</expected>
    """
    # Подготовка
    factory = report_factory()

    # Действие и Проверки
    with pytest.raises(argument_exception):
        factory.create("UNKNOWN_FORMAT")