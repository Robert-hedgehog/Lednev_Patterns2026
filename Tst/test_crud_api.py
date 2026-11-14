import pytest
from main import api, storage


@pytest.fixture(autouse=True)
def reset_storage():
    """Сброс хранилища перед каждым интеграционным тестом."""
    storage.clear()
    storage.first_start()
    yield storage


@pytest.fixture
def client():
    """Тестовый HTTP-клиент приложения."""
    with api.test_client() as test_client:
        yield test_client


def test_success_get_report_formats_returns_json_list(client):
    """
    <summary>Проверка получения списка всех форматов отчетов через API.</summary>
    <description>Выполняется GET запрос к /api/report/formats.</description>
    <expected>Возвращается HTTP 200 и JSON-список со всеми 5 форматами.</expected>
    """
    # Подготовка
    expected_formats = {"TXT", "CSV", "MARKDOWN", "XML", "HTML"}

    # Действие
    response = client.get("/api/report/formats")

    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert expected_formats.issubset(set(data))


def test_success_crud_lifecycle_for_storage_entity(client):
    """
    <summary>Проверка полного цикла CRUD для сущности склада через API.</summary>
    <description>Последовательно выполняются POST, GET, PUT и DELETE для нового склада.</description>
    <expected>Склад создается, читается, обновляется и удаляется со статусами 201/200.</expected>
    """
    # Подготовка
    payload = {"name": "Новый склад", "address": "ул. Тестовая, д. 5"}

    # Действие
    create_resp = client.post("/api/entities/storage", json=payload)

    # Проверки
    assert create_resp.status_code == 201
    created = create_resp.json()
    entity_id = created["id"]
    assert created["name"] == "Новый склад"

    # Действие
    get_resp = client.get(f"/api/entities/storage/{entity_id}")

    # Проверки
    assert get_resp.status_code == 200
    assert get_resp.json()["address"] == "ул. Тестовая, д. 5"

    # Действие
    update_resp = client.put(
        f"/api/entities/storage/{entity_id}",
        json={"name": "Обновленный склад", "address": "ул. Новая, д. 10"}
    )

    # Проверки
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Обновленный склад"

    # Действие
    delete_resp = client.delete(f"/api/entities/storage/{entity_id}")

    # Проверки
    assert delete_resp.status_code == 200
    assert client.get(f"/api/entities/storage/{entity_id}").status_code == 404


def test_conflict_delete_linked_group_returns_409(client):
    """
    <summary>Проверка запрета удаления сущности, связанной с другой сущностью.</summary>
    <description>Попытка удалить группу номенклатуры, на которую ссылаются товары.</description>
    <expected>API возвращает статус 409 и сущность остается в хранилище.</expected>
    """
    # Подготовка
    linked_group = storage.groups[0]

    # Действие
    response = client.delete(f"/api/entities/group/{linked_group.id}")

    # Проверки
    assert response.status_code == 409
    assert client.get(f"/api/entities/group/{linked_group.id}").status_code == 200


def test_conflict_change_id_of_linked_unit_returns_409(client):
    """
    <summary>Проверка запрета изменения кода (id) связанной сущности.</summary>
    <description>Попытка изменить id единицы измерения, используемой в номенклатуре или рецептах.</description>
    <expected>API возвращает статус 409, id сущности не изменяется.</expected>
    """
    # Подготовка
    linked_unit = storage.units[0]
    payload = {
        "id": "99999999-9999-9999-9999-999999999999",
        "name": linked_unit.name,
        "conversion_factor": linked_unit.conversion_factor
    }

    # Действие
    response = client.put(f"/api/entities/range/{linked_unit.id}", json=payload)

    # Проверки
    assert response.status_code == 409
    assert client.get(f"/api/entities/range/{linked_unit.id}").status_code == 200