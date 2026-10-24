from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_data_dto import report_data_dto
from Src.Dtos.report_result_dto import report_result_dto


class markdown_report(abstract_report):
    """Markdown представление отчета."""

    def build(self, source: report_data_dto) -> report_result_dto:
        result = report_result_dto()
        result.mime_type = "text/markdown; charset=utf-8"
        result.file_extension = "md"
        result.is_attachment = True

        title = f"# Отчет: {source.title}\n\n"
        head_line = "| " + " | ".join(source.headers) + " |"
        sep_line = "| " + " | ".join(["---"] * len(source.headers)) + " |"
        rows_lines = ["| " + " | ".join(str(val) for val in row) + " |" for row in source.rows]
        content = title + head_line + "\n" + sep_line + "\n" + "\n".join(rows_lines)

        result.binary = list(content.encode("utf-8"))
        return result