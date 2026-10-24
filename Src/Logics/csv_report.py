from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_data_dto import report_data_dto
from Src.Dtos.report_result_dto import report_result_dto


class csv_report(abstract_report):
    """CSV представление отчета."""

    def build(self, source: report_data_dto) -> report_result_dto:
        result = report_result_dto()
        result.mime_type = "text/csv; charset=utf-8"
        result.file_extension = "csv"
        result.is_attachment = True

        lines = [";".join(source.headers)]
        for row in source.rows:
            lines.append(";".join(str(val) for val in row))
        content = "\n".join(lines)

        result.binary = list(content.encode("utf-8"))
        return result