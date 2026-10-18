from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto


class text_report(abstract_report):
    """Текстовое представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        validator.validate(source, abstract)
        result = report_result_dto()
        result.mime_type = "text/plain; charset=utf-8"
        result.file_extension = "txt"
        result.is_attachment = False

        if hasattr(source, "get_report_items"):
            items = source.get_report_items()
            if items:
                headers = list(items[0].keys())
                header_line = " | ".join(headers)
                rows = [" | ".join(str(row[h]) for h in headers) for row in items]
                result.text = f"{source.name}\n{header_line}\n" + "\n".join(rows)
            else:
                result.text = f"{source.id} | {source.name}"
        else:
            fields = source.get_report_fields()
            result.text = f"Сущность: {source.name}\n" + "\n".join(f"{k}: {v}" for k, v in fields.items())

        return result
