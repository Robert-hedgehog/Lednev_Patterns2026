from typing import Dict


class event_type:
    """Справочник типов системных событий."""

    @staticmethod
    def change_settings() -> str:
        """Событие изменения параметров настроек."""
        return "change_settings"

    @staticmethod
    def load_settings() -> str:
        """Событие загрузки настроек."""
        return "load_settings"

    @staticmethod
    def crud_create() -> str:
        """Событие создания сущности."""
        return "crud_create"

    @staticmethod
    def crud_update() -> str:
        """Событие обновления сущности."""
        return "crud_update"

    @staticmethod
    def crud_delete() -> str:
        """Событие удаления сущности."""
        return "crud_delete"

    @staticmethod
    def storage_operation() -> str:
        """Событие складской операции."""
        return "storage_operation"

    @staticmethod
    def tbs_build() -> str:
        """Событие формирования ОСВ."""
        return "tbs_build"

    @staticmethod
    def web_request() -> str:
        """Событие вызова Web-метода."""
        return "web_request"

    @staticmethod
    def events() -> Dict[str, str]:
        """Получить словарь всех зарегистрированных событий и их описаний."""
        result: Dict[str, str] = {}
        for name in dir(event_type):
            if name.startswith("_") or name == "events":
                continue
            method = getattr(event_type, name)
            if callable(method):
                doc = method.__doc__.strip().split("\n")[0] if method.__doc__ else name
                result[method()] = doc
        return result