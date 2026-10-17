from abc import ABC, abstractmethod
from Src.Core.class_abstract import abstract
from Src.Dtos.report_result_dto import report_result_dto


class abstract_report(ABC):
    """Абстрактный класс для формирования отчета."""

    @abstractmethod
    def build(self, source: abstract) -> report_result_dto:
        """Сформировать отчет."""
        pass