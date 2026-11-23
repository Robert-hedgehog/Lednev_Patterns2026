from datetime import datetime
import pytest
from main import api, storage
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_type_enum import filter_type_enum
from Src.Logics.domain_prototype import domain_prototype
from Src.Logics.tbs_service import tbs_service


@pytest.fixture(autouse=True)
def reset_storage():
    """Сброс хранилища перед каждым тестом."""
    storage.clear()
    storage.first_start()
    yield storage


@pytest.fixture
def client():
    """Тестовый HTTP-клиент приложения."""
    with api.test_client() as test_client:
        yield test_client


def test_success_domain_prototype_filter_equals_by_name_and_id():
    """
    <summary>Проверка фильтрации EQUALS по наименованию и уникальному коду.</summary>
    <description>Фильтруется номенклатура по точному имени и по точному id.</description>
    <expected>Прототип возвращает ровно одну совпадающую сущность в каждом случае.</expected>
    """
    # Подготовка
    target = storage.nomenclatures[0]
    proto = domain_prototype(storage.nomenclatures)
    dto_name = filter_dto.create("name", target.name, filter_type_enum.EQUALS)
    dto_id = filter_dto.create("id", str(target.id), filter_type_enum.EQUALS)

    # Действие
    res_name = proto.filter(dto_name)
    res_id = proto.filter(dto_id)

    # Проверки
    assert len(res_name.data) == 1
    assert res_name.data[0] == target
    assert len(res_id.data) == 1
    assert res_id.data[0] == target


def test_success_domain_prototype_filter_like_for_all_domains():
    """
    <summary>Проверка фильтрации LIKE для номенклатуры, групп, единиц и рецептов.</summary>
    <description>Применяется один и тот же класс domain_prototype к разным коллекциям.</description>
    <expected>Для каждой коллекции найдены объекты с вхождением подстроки.</expected>
    """
    # Подготовка
    nom_dto = filter_dto.create("name", "щек", filter_type_enum.LIKE)
    grp_dto = filter_dto.create("name", "полуфабрикат", filter_type_enum.LIKE)
    rec_dto = filter_dto.create("name", "каша", filter_type_enum.LIKE)

    # Действие
    nom_res = domain_prototype(storage.nomenclatures).filter(nom_dto)
    grp_res = domain_prototype(storage.groups).filter(grp_dto)
    rec_res = domain_prototype(storage.recipes).filter(rec_dto)

    # Проверки
    assert len(nom_res.data) >= 2
    assert len(grp_res.data) == 1
    assert len(rec_res.data) == 1


def test_success_domain_prototype_nested_model_name_and_chaining():
    """
    <summary>Проверка поиска во вложенных структурах через model_name и цепочки прототипа.</summary>
    <description>Фильтруются единицы измерения по model_name='base_range' и номенклатура по model_name='group'.</description>
    <expected>Найдена производная единица 'киллограмм' и номенклатура нужной группы.</expected>
    """
    # Подготовка
    unit_dto = filter_dto.create("name", "грамм", filter_type_enum.EQUALS, model_name="base_range")
    nom_dto = filter_dto.create("name", "Авторские горячие блюда", filter_type_enum.EQUALS, model_name="group")
    unit_proto = domain_prototype(storage.units)
    nom_proto = domain_prototype(storage.nomenclatures)

    # Действие
    res_units = unit_proto.filter(unit_dto)
    res_noms = nom_proto.filter(nom_dto)

    # Проверки
    assert len(res_units.data) == 1
    assert res_units.data[0].name == "киллограмм"
    assert len(res_noms.data) == 1
    assert res_noms.data[0].name == "Дождевая каша со щекой"


def test_success_tbs_service_build_with_filter_and_period():
    """
    <summary>Проверка расчета ОСВ через tbs_service с периодом и фильтрацией.</summary>
    <description>Рассчитывается ОСВ по 'Говяжьи щеки' за период с 9 по 31 января.</description>
    <expected>Начальный остаток 10000 г, приход 5000 г, расход 2500 г, конечный остаток 12500 г.</expected>
    """
    # Подготовка
    service = tbs_service(storage)
    dto = filter_dto.create("name", "Говяжьи щеки", filter_type_enum.EQUALS, model_name="nomenclature")
    start = datetime(2026, 1, 9, 0, 0)
    end = datetime(2026, 1, 31, 23, 59)

    # Действие
    rows = service.build(dto=dto, start_date=start, end_date=end)

    # Проверки
    assert len(rows) == 1
    row = rows[0]
    assert row["unit_name"] == "грамм"
    assert row["opening_balance"] == 10000.0
    assert row["income"] == 5000.0
    assert row["outcome"] == 2500.0
    assert row["closing_balance"] == 12500.0


def test_success_api_post_filter_and_tbs_endpoints(client):
    """
    <summary>Проверка POST-эндпоинтов /api/filter/{entity_type} и /api/tbs.</summary>
    <description>Отправляются POST-запросы с DTO фильтрации к новым маршрутам REST API.</description>
    <expected>Оба эндпоинта возвращают HTTP 200 и корректно отфильтрованные данные.</expected>
    """
    # Подготовка
    filter_payload = {
        "model_name": "group",
        "field_name": "name",
        "value": "Авторские горячие блюда",
        "filter_type": "EQUALS",
    }
    tbs_payload = {
        "model_name": "nomenclature",
        "field_name": "name",
        "value": "Крупа дождевая",
        "filter_type": "LIKE",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-31T23:59:59",
    }

    # Действие
    filter_resp = client.post("/api/filter/nomenclature", json=filter_payload)
    tbs_resp = client.post("/api/tbs", json=tbs_payload)

    # Проверки
    assert filter_resp.status_code == 200
    filtered_items = filter_resp.json()
    assert len(filtered_items) == 1
    assert filtered_items[0]["name"] == "Дождевая каша со щекой"

    assert tbs_resp.status_code == 200
    tbs_rows = tbs_resp.json()
    assert len(tbs_rows) == 1
    assert tbs_rows[0]["nomenclature_name"] == "Крупа дождевая"
    assert tbs_rows[0]["closing_balance"] == 2500.0