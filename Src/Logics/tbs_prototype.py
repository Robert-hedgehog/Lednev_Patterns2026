from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple
from Src.Dtos.filter_dto import filter_dto
from Src.Logics.domain_prototype import domain_prototype
from Src.Models.range_model import range_model
from Src.Models.transaction_model import transaction_model


class tbs_prototype(domain_prototype):
    """Прототип формирования оборотно-сальдовой ведомости (ОСВ)."""

    def filter_by_predicate(self, predicate: Callable[[transaction_model], bool]) -> "tbs_prototype":
        """Клонирование прототипа с отбором транзакций по предикату."""
        return self.clone([item for item in self.data if predicate(item)])

    def build(
        self,
        dto: Optional[filter_dto] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[dict]:
        """Расчет ОСВ через цепочку клонов прототипа."""
        scoped = self.filter(dto) if dto is not None else self.clone()
        bounded = scoped.filter_by_predicate(lambda tx: end_date is None or tx.period <= end_date)

        opening_proto = bounded.filter_by_predicate(
            lambda tx: start_date is not None and tx.period < start_date
        )
        period_proto = bounded.filter_by_predicate(
            lambda tx: start_date is None or tx.period >= start_date
        )
        income_proto = period_proto.filter_by_predicate(lambda tx: tx.quantity >= 0)
        outcome_proto = period_proto.filter_by_predicate(lambda tx: tx.quantity < 0)

        rows: Dict[Tuple[str, str], dict] = {}
        self.__accumulate(rows, opening_proto.data, "opening_balance", lambda q: q)
        self.__accumulate(rows, income_proto.data, "income", lambda q: q)
        self.__accumulate(rows, outcome_proto.data, "outcome", abs)

        for row in rows.values():
            row["opening_balance"] = round(row["opening_balance"], 4)
            row["income"] = round(row["income"], 4)
            row["outcome"] = round(row["outcome"], 4)
            row["closing_balance"] = round(row["opening_balance"] + row["income"] - row["outcome"], 4)

        return list(rows.values())

    def __accumulate(
        self,
        rows: Dict[Tuple[str, str], dict],
        items: List[transaction_model],
        field: str,
        transform: Callable[[float], float],
    ) -> None:
        """Накопление сумм транзакций в указанную колонку ОСВ."""
        for tx in items:
            base_unit, qty = self.__to_base_unit(tx.unit, tx.quantity)
            key = (str(tx.storage.id), str(tx.nomenclature.id))
            row = rows.setdefault(
                key,
                {
                    "storage_id": str(tx.storage.id),
                    "storage_name": tx.storage.name,
                    "nomenclature_id": str(tx.nomenclature.id),
                    "nomenclature_name": tx.nomenclature.name,
                    "unit_name": base_unit.name if base_unit else "-",
                    "opening_balance": 0.0,
                    "income": 0.0,
                    "outcome": 0.0,
                    "closing_balance": 0.0,
                },
            )
            row[field] += transform(qty)

    def __to_base_unit(self, unit: Optional[range_model], quantity: float) -> Tuple[Optional[range_model], float]:
        """Приведение количества к базовой единице измерения."""
        current = unit
        total = float(quantity)
        while current is not None and current.base_range is not None:
            total *= current.conversion_factor
            current = current.base_range
        return current, total