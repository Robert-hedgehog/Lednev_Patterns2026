from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_data_dto import report_data_dto
from Src.Dtos.report_result_dto import report_result_dto


class text_report(abstract_report):
    """Текстовое представление отчета."""

    def build(self, source: report_data_dto) -> report_result_dto:
        result = report_result_dto()
        result.mime_type = "text/plain; charset=utf-8"
        result.file_extension = "txt"
        result.is_attachment = False

        head_line = " | ".join(source.headers)
        rows_lines = [" | ".join(str(val) for val in row) for row in source.rows]
        result.text = f"{source.title}\n{head_line}\n" + "\n".join(rows_lines)

        return result