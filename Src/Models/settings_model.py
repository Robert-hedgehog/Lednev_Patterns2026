from Src.Core.class_abstract import abstract
from Src.Models.organization_model import organization_model
from Src.Core.validator import validator
from Src.Dtos.report_type_enum import report_type_enum


class settings_model(abstract):
    """Модель глобальных настроек приложения."""

    def __init__(self) -> None:
        super().__init__()
        self.__company: organization_model = None
        self.__boss_name: str = ""
        self.__account_name: str = ""
        self.__response_format: report_type_enum = report_type_enum.TXT

    @property
    def company(self) -> organization_model:
        """Карточка организации сети."""
        return self.__company

    @company.setter
    def company(self, value: organization_model) -> None:
        validator.validate(value, organization_model)
        self.__company = value

    @property
    def boss_name(self) -> str:
        """ФИО генерального директора."""
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__boss_name = value.strip()

    @property
    def account_name(self) -> str:
        """ФИО главного бухгалтера."""
        return self.__account_name

    @account_name.setter
    def account_name(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__account_name = value.strip()

    @property
    def response_format(self) -> report_type_enum:
        """Формат вывода отчетов по умолчанию."""
        return self.__response_format

    @response_format.setter
    def response_format(self, value: report_type_enum | str) -> None:
        if isinstance(value, str):
            self.__response_format = report_type_enum.from_string(value)
        elif isinstance(value, report_type_enum):
            self.__response_format = value
        else:
            raise ValueError("Некорректный тип для response_format.")