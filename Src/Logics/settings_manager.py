import json
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, operation_exception
from Src.Models.settings_model import settings_model
from Src.Models.organization_model import organization_model


class settings_manager(abstract_manager):
    """
    Менеджер настроек приложения (Singleton).
    Загружает конфигурационные данные и формирует модель settings_model.
    """

    __default_file_name: str = "settings.json"
    __settings: settings_model = None
    __is_loaded: bool = False
    __data: dict = {}

    def __new__(cls):
        """Реализация шаблона Singleton для возврата единственного экземпляра."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Инициализация менеджера настроек."""
        super().__init__()
        if self.__settings is None:
            self.__settings = settings_model()

    def load(self, file_name: str = "") -> None:
        """
        Загрузка данных из конфигурационного файла.

        Параметры:
            file_name (str): Путь к файлу настроек.
        """
        inner_file_name = file_name if file_name and file_name.strip() != "" else self.__default_file_name
        validator.validate(inner_file_name, str)

        try:
            with open(inner_file_name, "r", encoding="utf-8") as file:
                self.__data = json.load(file)
                self.__is_loaded = self.convert()
        except Exception as ex:
            raise operation_exception(f"Ошибка при загрузке и обработке файла: {inner_file_name}. Детали: {ex}")

    def convert(self) -> bool:
        """
        Конвертация загруженных сырых данных JSON в доменные модели.

        Возвращает:
            bool: True в случае успешной конвертации, иначе False.
        """
        if not self.__data or not isinstance(self.__data, dict):
            return False

        company_data = self.__data.get("company")
        if company_data and isinstance(company_data, dict):
            org = organization_model(
                name=company_data.get("name", ""),
                inn=company_data.get("inn", ""),
                bik=company_data.get("bik", ""),
                account=company_data.get("account", ""),
                ownership_type=company_data.get("ownership_type", "")
            )
            self.__settings.company = org

        if "boss_name" in self.__data:
            self.__settings.boss_name = self.__data["boss_name"]

        if "account_name" in self.__data:
            self.__settings.account_name = self.__data["account_name"]

        return True

    @property
    def is_loaded(self) -> bool:
        """Флаг успешной загрузки и конвертации настроек."""
        return self.__is_loaded

    @property
    def settings(self) -> settings_model:
        """Модель настроек приложения."""
        return self.__settings