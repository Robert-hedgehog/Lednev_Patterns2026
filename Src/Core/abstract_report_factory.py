from abc import ABC, abstractmethod
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_enum import report_type_enum

class abstract_report_factory(ABC):
    """Абстрактная фабрика отчетов."""

    @abstractmethod
    def create(self, report_type: report_type_enum) -> abstract_report:
        """Подобрать и создать инстанс нужного отчета."""
        pass

    @abstractmethod
    def create_default(self) -> abstract_report:
        """Создать инстанс отчета по умолчанию из настроек."""
        pass