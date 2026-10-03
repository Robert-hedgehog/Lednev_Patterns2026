from Src.Core.class_abstract import abstract
from Src.Models.organization_model import organization_model
from Src.Core.validator import validator


class settings_model(abstract):
    # Карточка организации
    __company:organization_model = None
    # Наименование директора
    __boss_name:str = ""
    # Наименование главного бухгалтера
    __account_name:str = ""

    """
    Карточка организации
    """
    @property
    def company(self) -> organization_model:
        return self.__company

    @company.setter
    def company(self, value:organization_model) -> None:
        validator.validate(value, organization_model)
        self.__company = value

    """
    Наименование директора
    """
    @property
    def boss_name(self) -> str:
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value:str) -> None:
        validator.validate(value, str, 255)
        self.__boss_name = value.strip()

    """
    Главный бухгалтер
    """
    @property
    def account_name(self) -> str:
        return self.__account_name    

    @account_name.setter
    def account_name(self, value:str) -> None:
        validator.validate(value, str, 255)
        self.__account_name = value.strip()