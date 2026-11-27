from datetime import datetime
import pytest
from main import api, storage, service
from Src.Core.event_type import event_type
from Src.Dtos.log_entry_dto import log_entry_dto
from Src.Logics.observer import observer
from Src.Logics.log_service import log_service
from Src.Logics.settings_manager import settings_manager
from Src.Logics.tbs_service import tbs_service
from Src.Models.transaction_model import transaction_model


@pytest.fixture
def isolated_logger(tmp_path):
    """Изолированный логгер во временном файле для каждого теста."""
    previous = list(observer.handlers)
    observer.clear()
    log_file = str(tmp_path / "test.log")
    logger = log_service(log_file)
    storage.clear()
    storage.first_start()
    yield logger, log_file
    observer.clear()
    for item in previous:
        observer.add(item)


@pytest.fixture
def client():
    """Тестовый HTTP-клиент приложения."""
    with api.test_client() as test_client:
        yield test_client


def test_success_log_service_logs_crud_operations(isolated_logger):
    """
    <summary>Проверка логирования CRUD-операций через наблюдателя.</summary>
    <description>Последовательно выполняются create, update и delete склада через reference_service.</description>
    <expected>В лог-сервисе фиксируются DTO-записи crud_create, crud_update и crud_delete и пишутся в файл.</expected>
    """
    # Подготовка
    logger, log_file = isolated_logger

    # Действие
    created = service.create("storage", {"name": "Лог склад", "address": "ул. Тестовая, 1"})
    service.update("storage", str(created.id), {"name": "Лог склад 2", "address": "ул. Тестовая, 2"})
    service.delete("storage", str(created.id))

    # Проверки
    assert all(isinstance(rec, log_entry_dto) for rec in logger.records)
    events = [rec.event for rec in logger.records]
    assert event_type.crud_create() in events
    assert event_type.crud_update() in events
    assert event_type.crud_delete() in events
    with open(log_file, "r", encoding="utf-8") as file:
        content = file.read()
    assert "crud_create" in content
    assert "crud_delete" in content


def test_success_log_service_logs_storage_and_tbs_operations(isolated_logger):
    """
    <summary>Проверка логирования складских операций и расчёта ОСВ.</summary>
    <description>Добавляется складская транзакция и формируется ОСВ через tbs_service.</description>
    <expected>Фиксируются события storage_operation и tbs_build.</expected>
    """
    # Подготовка
    logger, _ = isolated_logger
    tx = transaction_model.create(
        datetime(2026, 1, 20, 10, 0),
        storage.storages[0],
        storage.nomenclatures[0],
        2.0,
        storage.units[1],
    )
    tbs = tbs_service(storage)

    # Действие
    storage.add_transaction(tx)
    tbs.build()

    # Проверки
    events = [rec.event for rec in logger.records]
    assert event_type.storage_operation() in events
    assert event_type.tbs_build() in events


def test_success_log_service_logs_settings_load_and_change(isolated_logger):
    """
    <summary>Проверка логирования загрузки и изменения параметров настроек.</summary>
    <description>Вызывается load() и update() для изменения параметров в settings_manager.</description>
    <expected>Фиксируются события load_settings и change_settings.</expected>
    """
    # Подготовка
    logger, _ = isolated_logger
    manager = settings_manager()

    # Действие
    manager.load()
    manager.update(boss_name="Тестовый Директор")
    manager.load()

    # Проверки
    events = [rec.event for rec in logger.records]
    assert event_type.load_settings() in events
    assert event_type.change_settings() in events


def test_success_log_service_logs_web_requests(isolated_logger, client):
    """
    <summary>Проверка логирования вызовов Web-методов через REST API.</summary>
    <description>Выполняется GET запрос к /api/report/formats.</description>
    <expected>Возвращается HTTP 200 и в логе появляется событие web_request с путём запроса.</expected>
    """
    # Подготовка
    logger, _ = isolated_logger

    # Действие
    response = client.get("/api/report/formats")

    # Проверки
    assert response.status_code == 200
    web_events = [rec for rec in logger.records if rec.event == event_type.web_request()]
    assert len(web_events) >= 1
    assert any(rec.params["path"] == "/api/report/formats" for rec in web_events)