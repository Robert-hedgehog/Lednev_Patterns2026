from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class html_report(abstract_report):
    """HTML представление отчета."""

    def build(self, source: abstract) -> report_result_dto:
        """Построение HTML отчета."""
        validator.validate(source, abstract)
        result = report_result_dto()

        if isinstance(source, recipe_model):
            rows = "".join(
                f"<tr><td>{i.id}</td><td>{i.name}</td><td>{i.brutto}</td><td>{i.netto}</td></tr>"
                for i in source.ingredients
            )
            result.text = (
                f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{source.name}</title></head><body>"
                f"<h2>Рецепт: {source.name}</h2>"
                f"<table border='1'><thead><tr><th>Код</th><th>Ингредиент</th><th>Брутто</th><th>Нетто</th></tr></thead>"
                f"<tbody>{rows}</tbody></table></body></html>"
            )
        elif isinstance(source, nomenclature_model):
            unit_name = source.unit.name if source.unit else ""
            result.text = (
                f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{source.name}</title></head><body>"
                f"<h2>Номенклатура: {source.name}</h2>"
                f"<p><strong>ID:</strong> {source.id}</p>"
                f"<p><strong>Полное наименование:</strong> {source.full_name}</p>"
                f"<p><strong>Единица:</strong> {unit_name}</p></body></html>"
            )
        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            result.text = (
                f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{source.name}</title></head><body>"
                f"<h2>Единица измерения: {source.name}</h2>"
                f"<p><strong>ID:</strong> {source.id}</p>"
                f"<p><strong>Коэффициент:</strong> {source.conversion_factor}</p>"
                f"<p><strong>Базовая единица:</strong> {base_name}</p></body></html>"
            )
        else:
            result.text = f"<!DOCTYPE html><html><body><h2>{source.name}</h2><p>{source.id}</p></body></html>"

        return result