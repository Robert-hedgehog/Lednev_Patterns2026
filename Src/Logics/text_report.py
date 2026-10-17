from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class text_report(abstract_report):
    """Текстовое представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        """Построение текстового отчета."""
        validator.validate(source, abstract)
        result = report_result_dto()

        if isinstance(source, recipe_model):
            header = "Код | Наименование | Брутто | Нетто"
            rows = [f"{i.id} | {i.name} | {i.brutto} | {i.netto}" for i in source.ingredients]
            result.text = f"{source.name}\n{header}\n" + "\n".join(rows)
        elif isinstance(source, nomenclature_model):
            unit_name = source.unit.name if source.unit else ""
            result.text = f"Код: {source.id}\nНаименование: {source.name}\nПолное наименование: {source.full_name}\nЕдиница: {unit_name}"
        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            result.text = f"Код: {source.id}\nНаименование: {source.name}\nКоэффициент: {source.conversion_factor}\nБазовая: {base_name}"
        else:
            result.text = f"Код: {source.id}\nНаименование: {source.name}"

        return result