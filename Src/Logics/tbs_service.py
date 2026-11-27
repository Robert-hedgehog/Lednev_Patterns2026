from datetime import datetime
from typing import Dict, List, Optional, Tuple
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_type_enum import filter_type_enum
from Src.Dtos.tbs_row_dto import tbs_row_dto
from Src.Logics.domain_prototype import domain_prototype
from Src.Logics.storage_manager import storage_manager
from Src.Models.range_model import range_model
from Src.Models.transaction_model import transaction_model


class tbs_service:
    """Сервис формирования оборотно-сальдовой ведомости (ОСВ)."""

    def __init__(self, storage: storage_manager = None) -> None:
        """Инициализация сервиса с хранилищем данных."""
        self.__storage = storage or storage_manager()

    def build(
        self,
        dto: Optional[filter_dto] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[tbs_row_dto]:
        """Расчет ОСВ с использованием прототипа для фильтрации транзакций."""
        source_proto = domain_prototype(self.__storage.transactions)
        if dto is not None:
            source_proto = source_proto.filter(dto)

        opening_rows: Dict[Tuple[str, str], tbs_row_dto] = {}
        if start_date is not None:
            opening_filter = filter_dto.create("period", start_date, filter_type_enum.LESS_OR_EQUAL)
            opening_proto = source_proto.filter(opening_filter)
            opening_rows = self.__calculate_opening(opening_proto.data)

        turnover_proto = source_proto
        if start_date is not None:
            from_filter = filter_dto.create("period", start_date, filter_type_enum.GREATER)
            turnover_proto = turnover_proto.filter(from_filter)
        if end_date is not None:
            to_filter = filter_dto.create("period", end_date, filter_type_enum.LESS_OR_EQUAL)
            turnover_proto = turnover_proto.filter(to_filter)

        turnover_rows = self.__calculate_turnover(turnover_proto.data)
        return self.__merge_results(opening_rows, turnover_rows)

    def __create_row(self, tx: transaction_model, base_unit: Optional[range_model]) -> tbs_row_dto:
        """Создание DTO строки ОСВ для пары склад и номенклатура."""
        return tbs_row_dto.create(
            storage_id=str(tx.storage.id),
            storage_name=tx.storage.name,
            nomenclature_id=str(tx.nomenclature.id),
            nomenclature_name=tx.nomenclature.name,
            unit_name=base_unit.name if base_unit else "-",
        )

    def __calculate_opening(self, items: List[transaction_model]) -> Dict[Tuple[str, str], tbs_row_dto]:
        """Расчет начальных остатков по транзакциям до даты начала периода."""
        rows: Dict[Tuple[str, str], tbs_row_dto] = {}
        for tx in items:
            base_unit, qty = self.__to_base_unit(tx.unit, tx.quantity)
            key = (str(tx.storage.id), str(tx.nomenclature.id))
            row = rows.setdefault(key, self.__create_row(tx, base_unit))
            row.opening_balance += qty
        return rows

    def __calculate_turnover(self, items: List[transaction_model]) -> Dict[Tuple[str, str], tbs_row_dto]:
        """Расчет прихода и расхода по транзакциям за выбранный период."""
        rows: Dict[Tuple[str, str], tbs_row_dto] = {}
        for tx in items:
            base_unit, qty = self.__to_base_unit(tx.unit, tx.quantity)
            key = (str(tx.storage.id), str(tx.nomenclature.id))
            row = rows.setdefault(key, self.__create_row(tx, base_unit))
            row.income += max(qty, 0.0)
            row.outcome += abs(min(qty, 0.0))
        return rows

    def __merge_results(
        self,
        opening_rows: Dict[Tuple[str, str], tbs_row_dto],
        turnover_rows: Dict[Tuple[str, str], tbs_row_dto],
    ) -> List[tbs_row_dto]:
        """Объединение начальных остатков и оборотов с расчетом конечных остатков."""
        result: List[tbs_row_dto] = []
        for key in set(opening_rows.keys()) | set(turnover_rows.keys()):
            source = opening_rows.get(key) or turnover_rows[key]
            opening = opening_rows[key].opening_balance if key in opening_rows else 0.0
            income = turnover_rows[key].income if key in turnover_rows else 0.0
            outcome = turnover_rows[key].outcome if key in turnover_rows else 0.0

            merged = tbs_row_dto.create(
                storage_id=source.storage_id,
                storage_name=source.storage_name,
                nomenclature_id=source.nomenclature_id,
                nomenclature_name=source.nomenclature_name,
                unit_name=source.unit_name,
            )
            merged.opening_balance = round(opening, 4)
            merged.income = round(income, 4)
            merged.outcome = round(outcome, 4)
            merged.closing_balance = round(opening + income - outcome, 4)
            result.append(merged)
        return result

    def __to_base_unit(self, unit: Optional[range_model], quantity: float) -> Tuple[Optional[range_model], float]:
        """Приведение количества к базовой единице измерения."""
        current = unit
        total = float(quantity)
        while current is not None and current.base_range is not None:
            total *= current.conversion_factor
            current = current.base_range
        return current, total