from Src.Core.class_abstract import abstract
from Src.Core.validator import validator


class tbs_row_dto(abstract):
    """DTO-модель строки оборотно-сальдовой ведомости (ОСВ)."""

    def __init__(self) -> None:
        """Инициализация строки ОСВ значениями по умолчанию."""
        super().__init__()
        self.__storage_id: str = ""
        self.__storage_name: str = ""
        self.__nomenclature_id: str = ""
        self.__nomenclature_name: str = ""
        self.__unit_name: str = "-"
        self.__opening_balance: float = 0.0
        self.__income: float = 0.0
        self.__outcome: float = 0.0
        self.__closing_balance: float = 0.0

    @property
    def storage_id(self) -> str:
        """Идентификатор склада."""
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value: str) -> None:
        """Установка идентификатора склада."""
        validator.validate(value, str)
        self.__storage_id = value.strip()

    @property
    def storage_name(self) -> str:
        """Наименование склада."""
        return self.__storage_name

    @storage_name.setter
    def storage_name(self, value: str) -> None:
        """Установка наименования склада."""
        validator.validate(value, str)
        self.__storage_name = value.strip()

    @property
    def nomenclature_id(self) -> str:
        """Идентификатор номенклатуры."""
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str) -> None:
        """Установка идентификатора номенклатуры."""
        validator.validate(value, str)
        self.__nomenclature_id = value.strip()

    @property
    def nomenclature_name(self) -> str:
        """Наименование номенклатуры."""
        return self.__nomenclature_name

    @nomenclature_name.setter
    def nomenclature_name(self, value: str) -> None:
        """Установка наименования номенклатуры."""
        validator.validate(value, str)
        self.__nomenclature_name = value.strip()

    @property
    def unit_name(self) -> str:
        """Наименование базовой единицы измерения."""
        return self.__unit_name

    @unit_name.setter
    def unit_name(self, value: str) -> None:
        """Установка наименования единицы измерения."""
        validator.validate(value, str)
        self.__unit_name = value.strip()

    @property
    def opening_balance(self) -> float:
        """Начальный остаток."""
        return self.__opening_balance

    @opening_balance.setter
    def opening_balance(self, value: float) -> None:
        """Установка начального остатка."""
        validator.validate(value, (int, float))
        self.__opening_balance = float(value)

    @property
    def income(self) -> float:
        """Приход за период."""
        return self.__income

    @income.setter
    def income(self, value: float) -> None:
        """Установка прихода за период."""
        validator.validate(value, (int, float))
        self.__income = float(value)

    @property
    def outcome(self) -> float:
        """Расход за период."""
        return self.__outcome

    @outcome.setter
    def outcome(self, value: float) -> None:
        """Установка расхода за период."""
        validator.validate(value, (int, float))
        self.__outcome = float(value)

    @property
    def closing_balance(self) -> float:
        """Конечный остаток."""
        return self.__closing_balance

    @closing_balance.setter
    def closing_balance(self, value: float) -> None:
        """Установка конечного остатка."""
        validator.validate(value, (int, float))
        self.__closing_balance = float(value)

    @staticmethod
    def create(
        storage_id: str,
        storage_name: str,
        nomenclature_id: str,
        nomenclature_name: str,
        unit_name: str = "-",
    ) -> "tbs_row_dto":
        """Фабричный метод создания строки ОСВ."""
        dto = tbs_row_dto()
        dto.storage_id = storage_id
        dto.storage_name = storage_name
        dto.nomenclature_id = nomenclature_id
        dto.nomenclature_name = nomenclature_name
        dto.unit_name = unit_name
        dto.name = f"{nomenclature_name} ({storage_name})"[:50]
        return dto

    @classmethod
    def from_dict(cls, data: dict) -> "tbs_row_dto":
        """Фабричный метод создания строки ОСВ из словаря."""
        validator.validate(data, dict)
        dto = cls()
        fields = (
            "id", "name", "storage_id", "storage_name",
            "nomenclature_id", "nomenclature_name", "unit_name",
            "opening_balance", "income", "outcome", "closing_balance",
        )
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(dto, field, value)
        return dto