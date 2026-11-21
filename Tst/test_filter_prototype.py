from datetime import datetime
import pytest
from main import api, storage
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_type_enum import filter_type_enum
from Src.Logics.domain_prototype import domain_prototype
from Src.Logics.tbs_prototype import tbs_prototype


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


def test_success_domain_prototype_nested_search_and_chaining():
    """
    <summary>Проверка поиска во вложенных структурах и цепочки клонирования прототипа.</summary>
    <description>Поиск по базовой единице 'грамм' и по пути 'base_range.name', а также цепочка фильтров.</description>
    <expected>Поиск по 'name' находит грамм и килограмм, а по 'base_range.name' только килограмм.</expected>
    """
    # Подготовка
    proto = domain_prototype(storage.units)
    nested_any = filter_dto.create("name", "грамм", filter_type_enum.EQUALS)
    nested_path = filter_dto.create("base_range.name", "грамм", filter_type_enum.EQUALS)

    # Действие
    res_any = proto.filter(nested_any)
    res_path = res_any.filter(nested_path)

    # Проверки
    names_any = [u.name for u in res_any.data]
    assert "грамм" in names_any
    assert "киллограмм" in names_any
    assert len(res_path.data) == 1
    assert res_path.data[0].name == "киллограмм"


def test_success_tbs_prototype_build_with_filter_and_period():
    """
    <summary>Проверка расчета ОСВ через прототип с периодом и фильтрацией.</summary>
    <description>Рассчитывается ОСВ по 'Говяжьи щеки' за период с 9 по 31 января.</description>
    <expected>Начальный остаток 10000 г, приход 5000 г, расход 2500 г, конечный остаток 12500 г.</expected>
    """
    # Подготовка
    dto = filter_dto.create("nomenclature.name", "Говяжьи щеки", filter_type_enum.EQUALS)
    start = datetime(2026, 1, 9, 0, 0)
    end = datetime(2026, 1, 31, 23, 59)

    # Действие
    rows = tbs_prototype(storage.transactions).build(dto=dto, start_date=start, end_date=end)

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
        "field_name": "group.name",
        "value": "Авторские горячие блюда",
        "filter_type": "EQUALS",
    }
    tbs_payload = {
        "field_name": "nomenclature.name",
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