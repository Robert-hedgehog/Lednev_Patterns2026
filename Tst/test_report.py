import pytest
from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_enum import report_type_enum
from Src.Models.settings_model import settings_model


@pytest.fixture(autouse=True)
def prepare_storage():
    """Фикстура подготовки хранилища."""
    manager = storage_manager()
    manager.clear()
    manager.first_start()
    yield manager


def test_success_report_factory_create_all_formats():
    """
    <summary>Проверка создания всех зарегистрированных типов отчетов через фабрику.</summary>
    <description>Запрашиваются отчеты TXT, CSV, Markdown, XML, HTML.</description>
    <expected>Каждый генератор успешно создается.</expected>
    """
    factory = report_factory()

    for format_type in [
        report_type_enum.TXT,
        report_type_enum.CSV,
        report_type_enum.MARKDOWN,
        report_type_enum.XML,
        report_type_enum.HTML,
    ]:
        reporter = factory.create(format_type)
        assert reporter is not None


def test_success_report_factory_create_default():
    """
    <summary>Проверка работы метода create_default.</summary>
    <description>Проверяется создание отчета на основе формата из настроек (Markdown и HTML).</description>
    <expected>create_default создает генератор отчета согласно настройкам.</expected>
    """
    custom_settings = settings_model()
    custom_settings.response_format = report_type_enum.MARKDOWN

    factory_md = report_factory(custom_settings)
    reporter_md = factory_md.create_default()
    assert reporter_md.__class__.__name__ == "markdown_report"

    custom_settings.response_format = report_type_enum.HTML
    factory_html = report_factory(custom_settings)
    reporter_html = factory_html.create_default()
    assert reporter_html.__class__.__name__ == "html_report"


def test_success_csv_report_binary_content_and_structure():
    """
    <summary>Проверка генерации CSV отчета в бинарном представлении.</summary>
    <description>Формируется CSV для рецепта, проверяется наличие колонок и бинарных байтов.</description>
    <expected>Поле binary заполнено, декодированный текст содержит id, name, brutto, netto.</expected>
    """
    manager = storage_manager()
    recipe = manager.recipes[0]

    factory = report_factory()
    reporter = factory.create(report_type_enum.CSV)
    dto = reporter.build(recipe)

    assert len(dto.binary) > 0
    assert dto.text == ""

    decoded = bytes(dto.binary).decode("utf-8")
    assert "id;name;brutto;netto" in decoded
    assert str(recipe.ingredients[0].name) in decoded


def test_success_markdown_report_binary_content():
    """
    <summary>Проверка генерации Markdown отчета в бинарном представлении.</summary>
    <description>Формируется Markdown таблица для рецепта.</description>
    <expected>Поле binary заполнено, таблица содержит markdown разметку.</expected>
    """
    manager = storage_manager()
    recipe = manager.recipes[0]

    factory = report_factory()
    reporter = factory.create(report_type_enum.MARKDOWN)
    dto = reporter.build(recipe)

    assert len(dto.binary) > 0
    decoded = bytes(dto.binary).decode("utf-8")
    assert "# Отчет:" in decoded
    assert recipe.name in decoded
    assert "| id | name | brutto | netto |" in decoded


def test_success_xml_and_html_reports_structured_text():
    """
    <summary>Проверка генерации XML и HTML отчетов в виде структурированного текста.</summary>
    <description>Формируются отчеты для номенклатуры и единицы измерения.</description>
    <expected>Поле text заполнено соответствующими тегами, поле binary пустое.</expected>
    """
    manager = storage_manager()
    nom = manager.nomenclatures[0]
    unit = manager.units[0]
    factory = report_factory()

    xml_reporter = factory.create(report_type_enum.XML)
    xml_dto = xml_reporter.build(nom)
    assert "<nomenclature>" in xml_dto.text
    assert f"<name>{nom.name}</name>" in xml_dto.text
    assert len(xml_dto.binary) == 0

    html_reporter = factory.create(report_type_enum.HTML)
    html_dto = html_reporter.build(unit)
    assert "<!DOCTYPE html>" in html_dto.text
    assert f"<h2>{unit.name}</h2>" in html_dto.text
    assert len(html_dto.binary) == 0