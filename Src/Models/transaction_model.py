from datetime import datetime
from typing import Optional
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator, argument_exception
from Src.Models.storage_model import storage_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class transaction_model(abstract):
    """Модель складской транзакции для формирования ОСВ."""

    def __init__(
        self,
        period: Optional[datetime] = None,
        storage: Optional[storage_model] = None,
        nomenclature: Optional[nomenclature_model] = None,
        unit: Optional[range_model] = None,
        quantity: float = 0.0,
    ) -> None:
        """Инициализация складской транзакции."""
        super().__init__()
        self.__period: datetime = datetime.now()
        self.__storage: Optional[storage_model] = None
        self.__nomenclature: Optional[nomenclature_model] = None
        self.__unit: Optional[range_model] = None
        self.__quantity: float = 0.0

        if period is not None:
            self.period = period
        if storage is not None:
            self.storage = storage
        if nomenclature is not None:
            self.nomenclature = nomenclature
        if unit is not None:
            self.unit = unit
        elif nomenclature is not None and nomenclature.unit is not None:
            self.unit = nomenclature.unit
        self.quantity = quantity

    @property
    def period(self) -> datetime:
        """Дата и время проведения операции."""
        return self.__period

    @period.setter
    def period(self, value: datetime) -> None:
        """Установка даты и времени операции."""
        validator.validate(value, datetime)
        self.__period = value

    @property
    def storage(self) -> Optional[storage_model]:
        """Склад операции."""
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model) -> None:
        """Установка склада операции."""
        validator.validate(value, storage_model)
        self.__storage = value

    @property
    def nomenclature(self) -> Optional[nomenclature_model]:
        """Номенклатура операции."""
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model) -> None:
        """Установка номенклатуры операции."""
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def unit(self) -> Optional[range_model]:
        """Единица измерения операции."""
        return self.__unit

    @unit.setter
    def unit(self, value: range_model) -> None:
        """Установка единицы измерения операции."""
        validator.validate(value, range_model)
        self.__unit = value

    @property
    def quantity(self) -> float:
        """Количество товара (положительное — приход, отрицательное — расход)."""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        """Установка количества товара."""
        validator.validate(value, (int, float))
        self.__quantity = float(value)

    @staticmethod
    def create(
        period: datetime,
        storage: storage_model,
        nomenclature: nomenclature_model,
        quantity: float,
        unit: Optional[range_model] = None,
    ) -> "transaction_model":
        """Фабричный метод создания складской транзакции."""
        item = transaction_model(
            period=period,
            storage=storage,
            nomenclature=nomenclature,
            unit=unit or nomenclature.unit,
            quantity=quantity,
        )
        item.name = f"{nomenclature.name} ({storage.name})"[:50]
        return item

    @classmethod
    def from_dict(cls, data: dict) -> "transaction_model":
        """Фабричный метод создания транзакции из словаря."""
        validator.validate(data, dict)
        raw_period = data.get("period")
        parsers = {
            str: datetime.fromisoformat,
            datetime: lambda val: val,
        }
        parser = parsers.get(type(raw_period))
        try:
            period = parser(raw_period) if parser is not None else None
        except ValueError:
            raise argument_exception("period", f"Некорректный формат даты: {raw_period}")

        instance = cls(
            period=period,
            storage=data.get("storage"),
            nomenclature=data.get("nomenclature"),
            unit=data.get("unit"),
            quantity=float(data.get("quantity", 0.0)),
        )
        instance.id = data.get("id", str(instance.id))
        if data.get("name"):
            instance.name = data["name"]
        return instance