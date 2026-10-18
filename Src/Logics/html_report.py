from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto


class html_report(abstract_report):
    """HTML представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        validator.validate(source, abstract)
        result = report_result_dto()
        result.mime_type = "text/html; charset=utf-8"
        result.file_extension = "html"
        result.is_attachment = False

        if hasattr(source, "get_report_items"):
            items = source.get_report_items()
            if items:
                headers = list(items[0].keys())
                th = "".join(f"<th>{h}</th>" for h in headers)
                tr = "".join(
                    "<tr>" + "".join(f"<td>{row[h]}</td>" for h in headers) + "</tr>"
                    for row in items
                )
                body = f"<table border='1'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"
            else:
                body = f"<p>{source.id}: {source.name}</p>"
        else:
            fields = source.get_report_fields()
            tr = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in fields.items())
            body = f"<table border='1'><tbody>{tr}</tbody></table>"

        result.text = (
            f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{source.name}</title></head>"
            f"<body><h2>{source.name}</h2>{body}</body></html>"
        )
        return result