from enum import Enum


class report_type_enum(Enum):
    """Типы поддерживаемых форматов отчетов."""

    TXT = 1
    CSV = 2
    MARKDOWN = 3
    XML = 4
    HTML = 5

    @staticmethod
    def from_string(value: str) -> "report_type_enum":
        """Преобразование строки в элемент перечисления."""
        normalized = str(value).strip().upper()
        if normalized in ("MD", "MARKDOWN"):
            return report_type_enum.MARKDOWN
        if normalized == "CSV":
            return report_type_enum.CSV
        if normalized == "XML":
            return report_type_enum.XML
        if normalized == "HTML":
            return report_type_enum.HTML
        if normalized == "TXT":
            return report_type_enum.TXT
        raise ValueError(f"Неизвестный формат отчета: {value}")