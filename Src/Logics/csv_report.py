from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto


class csv_report(abstract_report):
    """CSV представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        validator.validate(source, abstract)
        result = report_result_dto()
        result.mime_type = "text/csv; charset=utf-8"
        result.file_extension = "csv"
        result.is_attachment = True

        if hasattr(source, "get_report_items"):
            items = source.get_report_items()
            if items:
                headers = list(items[0].keys())
                lines = [";".join(headers)]
                for row in items:
                    lines.append(";".join(str(row[h]) for h in headers))
                content = "\n".join(lines)
            else:
                content = "id;name\n" f"{source.id};{source.name}"
        else:
            fields = source.get_report_fields()
            headers = list(fields.keys())
            values = [str(fields[h]) for h in headers]
            content = ";".join(headers) + "\n" + ";".join(values)

        result.binary = list(content.encode("utf-8"))
        return result