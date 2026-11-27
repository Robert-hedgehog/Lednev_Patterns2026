import json
import os
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import operation_exception
from Src.Models.settings_model import settings_model
from Src.Logics.deserialize_factory import deserialize_factory
from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Logics.observer import observer


class settings_manager(abstract_manager):
    """Менеджер глобальных настроек приложения."""

    __default_file_name: str = "settings.json"
    __settings: settings_model = None
    __is_initialized: bool = False

    def __new__(cls):
        """Реализация паттерна Singleton."""
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Инициализация менеджера настроек."""
        super().__init__()
        if not hasattr(self, "_settings_manager__is_initialized") or not self.__is_initialized:
            self.__settings = settings_model()
            self._file_name = self.__default_file_name
            self.__is_initialized = True
            self.load()

    def load(self, file_name: str = "") -> None:
        """Загрузка настроек из JSON-файла."""
        target_file = file_name.strip() if file_name else self.__default_file_name
        if not os.path.exists(target_file):
            raise operation_exception(f"Файл настроек {target_file} не найден.")

        try:
            with open(target_file, "r", encoding="utf-8") as file:
                self._data = json.load(file)
            self._file_name = target_file
            self._is_loaded = self.convert()
            observer.create(event_type.load_settings(), {"file_name": target_file})
        except Exception as ex:
            raise operation_exception(f"Ошибка загрузки настроек: {ex}")

    def convert(self) -> bool:
        """Десериализация настроек через общую фабрику десериализации."""
        if not isinstance(self._data, dict):
            return False

        factory = deserialize_factory()
        self.__settings = factory.deserialize_type("settings_model", self._data)
        return True

    @property
    def settings(self) -> settings_model:
        """Текущие настройки приложения."""
        return self.__settings
    
    @settings.setter
    def settings(self, value: settings_model) -> None:
        """Установка новых настроек приложения."""
        validator.validate(value, settings_model)
        self.__settings = value
        observer.create(
            event_type.change_settings(),
            {"boss_name": value.boss_name, "response_format": value.response_format.name},
        )

    def update(self, **kwargs) -> None:
        """Изменение параметров настроек с уведомлением наблюдателей."""
        for field, value in kwargs.items():
            setattr(self.__settings, field, value)
        observer.create(event_type.change_settings(), kwargs)