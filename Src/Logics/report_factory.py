from typing import Optional
from Src.Core.abstract_report_factory import abstract_report_factory
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_enum import report_type_enum
from Src.Logics.settings_manager import settings_manager
from Src.Models.settings_model import settings_model
from Src.Logics.text_report import text_report
from Src.Logics.csv_report import csv_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.xml_report import xml_report
from Src.Logics.html_report import html_report
from Src.Core.validator import argument_exception


class report_factory(abstract_report_factory):
    """Фабрика отчетов с инкапсулированными настройками приложения."""

    def __init__(self, settings: Optional[settings_model] = None) -> None:
        super().__init__()
        self.__settings: settings_model = settings if settings is not None else settings_manager().settings

        self.__mapping = {
            report_type_enum.TXT: text_report,
            report_type_enum.CSV: csv_report,
            report_type_enum.MARKDOWN: markdown_report,
            report_type_enum.XML: xml_report,
            report_type_enum.HTML: html_report,
        }

    def create(self, report_type: report_type_enum) -> abstract_report:
        """Создает генератор отчета указанного типа."""
        if report_type not in self.__mapping:
            raise argument_exception(f"Указанный тип отчета {report_type} не реализован!")

        report_class = self.__mapping[report_type]
        return report_class()

    def create_default(self) -> abstract_report:
        """Создает генератор отчета на основе настроек приложения."""
        default_format = self.__settings.response_format
        return self.create(default_format)