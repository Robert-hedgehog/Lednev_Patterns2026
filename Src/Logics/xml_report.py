from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_data_dto import report_data_dto
from Src.Dtos.report_result_dto import report_result_dto


class xml_report(abstract_report):
    """XML представление отчета."""

    def build(self, source: report_data_dto) -> report_result_dto:
        result = report_result_dto()
        result.mime_type = "application/xml; charset=utf-8"
        result.file_extension = "xml"
        result.is_attachment = False

        items_xml = ""
        for row in source.rows:
            item_tags = "".join(
                f"<{source.headers[i]}>{row[i]}</{source.headers[i]}>"
                for i in range(len(source.headers))
            )
            items_xml += f"<item>{item_tags}</item>"

        result.text = f'<?xml version="1.0" encoding="UTF-8"?><report><title>{source.title}</title><items>{items_xml}</items></report>'
        return result