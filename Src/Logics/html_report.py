from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_data_dto import report_data_dto
from Src.Dtos.report_result_dto import report_result_dto


class html_report(abstract_report):
    """HTML представление отчета."""

    def build(self, source: report_data_dto) -> report_result_dto:
        result = report_result_dto()
        result.mime_type = "text/html; charset=utf-8"
        result.file_extension = "html"
        result.is_attachment = False

        th = "".join(f"<th>{h}</th>" for h in source.headers)
        tr = "".join(
            "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
            for row in source.rows
        )
        table = f"<table border='1'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

        result.text = (
            f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{source.title}</title></head>"
            f"<body><h2>{source.title}</h2>{table}</body></html>"
        )
        return result