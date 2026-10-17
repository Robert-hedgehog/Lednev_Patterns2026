from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class csv_report(abstract_report):
    """CSV представление отчета с формированием бинарных данных."""

    def build(self, source: abstract) -> report_result_dto:
        """Построение CSV отчета в бинарном представлении."""
        validator.validate(source, abstract)
        result = report_result_dto()

        if isinstance(source, recipe_model):
            header = "id;name;brutto;netto"
            rows = [f"{i.id};{i.name};{i.brutto};{i.netto}" for i in source.ingredients]
            content = f"{header}\n" + "\n".join(rows)
        elif isinstance(source, nomenclature_model):
            unit_name = source.unit.name if source.unit else ""
            content = "id;name;full_name;unit\n" f"{source.id};{source.name};{source.full_name};{unit_name}"
        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            content = "id;name;conversion_factor;base_range\n" f"{source.id};{source.name};{source.conversion_factor};{base_name}"
        else:
            content = "id;name\n" f"{source.id};{source.name}"

        raw_bytes = content.encode("utf-8")
        result.binary = list(raw_bytes)
        return result