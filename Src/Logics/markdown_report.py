from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto


class markdown_report(abstract_report):
    """Markdown представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        validator.validate(source, abstract)
        result = report_result_dto()
        result.mime_type = "text/markdown; charset=utf-8"
        result.file_extension = "md"
        result.is_attachment = True

        if hasattr(source, "get_report_items"):
            items = source.get_report_items()
            if items:
                headers = list(items[0].keys())
                title = f"# Отчет: {source.name}\n\n"
                head_line = "| " + " | ".join(headers) + " |"
                sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
                rows = ["| " + " | ".join(str(row[h]) for h in headers) + " |" for row in items]
                content = title + head_line + "\n" + sep_line + "\n" + "\n".join(rows)
            else:
                content = f"# {source.name}\n\n| id | name |\n| --- | --- |\n| {source.id} | {source.name} |"
        else:
            fields = source.get_report_fields()
            content = f"# {source.name}\n\n| Параметр | Значение |\n| :--- | :--- |\n" + "\n".join(
                f"| {k} | {v} |" for k, v in fields.items()
            )

        result.binary = list(content.encode("utf-8"))
        return result