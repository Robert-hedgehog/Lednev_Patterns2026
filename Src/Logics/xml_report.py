from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto


class xml_report(abstract_report):
    """XML представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        validator.validate(source, abstract)
        result = report_result_dto()
        result.mime_type = "application/xml; charset=utf-8"
        result.file_extension = "xml"
        result.is_attachment = False

        tag_name = source.__class__.__name__.replace("_model", "")
        if hasattr(source, "get_report_items"):
            items = source.get_report_items()
            items_xml = "".join(
                "<item>" + "".join(f"<{k}>{v}</{k}>" for k, v in row.items()) + "</item>"
                for row in items
            )
            inner = f"<id>{source.id}</id><name>{source.name}</name><items>{items_xml}</items>"
        else:
            fields = source.get_report_fields()
            inner = "".join(f"<{k}>{v}</{k}>" for k, v in fields.items())

        result.text = f'<?xml version="1.0" encoding="UTF-8"?><{tag_name}>{inner}</{tag_name}>'
        return result