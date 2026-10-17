from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class xml_report(abstract_report):
    """XML представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        """Построение XML отчета."""
        validator.validate(source, abstract)
        result = report_result_dto()

        if isinstance(source, recipe_model):
            items_xml = "".join(
                f"<ingredient><id>{i.id}</id><name>{i.name}</name><brutto>{i.brutto}</brutto><netto>{i.netto}</netto></ingredient>"
                for i in source.ingredients
            )
            result.text = f'<?xml version="1.0" encoding="UTF-8"?><recipe><id>{source.id}</id><name>{source.name}</name><ingredients>{items_xml}</ingredients></recipe>'
        elif isinstance(source, nomenclature_model):
            unit_name = source.unit.name if source.unit else ""
            result.text = f'<?xml version="1.0" encoding="UTF-8"?><nomenclature><id>{source.id}</id><name>{source.name}</name><full_name>{source.full_name}</full_name><unit>{unit_name}</unit></nomenclature>'
        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            result.text = f'<?xml version="1.0" encoding="UTF-8"?><range><id>{source.id}</id><name>{source.name}</name><conversion_factor>{source.conversion_factor}</conversion_factor><base>{base_name}</base></range>'
        else:
            result.text = f'<?xml version="1.0" encoding="UTF-8"?><entity><id>{source.id}</id><name>{source.name}</name></entity>'

        return result