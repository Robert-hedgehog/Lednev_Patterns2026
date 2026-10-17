from Src.Core.abstract_report import abstract_report
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class markdown_report(abstract_report):
    """Markdown представление отчета в виде таблицы с бинарными данными."""

    def build(self, source: abstract) -> report_result_dto:
        """Построение Markdown таблицы в бинарном формате."""
        validator.validate(source, abstract)
        result = report_result_dto()

        if isinstance(source, recipe_model):
            title = f"# Технологическая карта: {source.name}\n\n"
            header = "| Идентификатор | Ингредиент | Брутто | Нетто |\n| :--- | :--- | :--- | :--- |"
            rows = [f"| {i.id} | {i.name} | {i.brutto} | {i.netto} |" for i in source.ingredients]
            content = title + header + "\n" + "\n".join(rows)
        elif isinstance(source, nomenclature_model):
            unit_name = source.unit.name if source.unit else "-"
            content = (
                f"# Номенклатура: {source.name}\n\n"
                "| Параметр | Значение |\n| :--- | :--- |\n"
                f"| Код | {source.id} |\n"
                f"| Наименование | {source.name} |\n"
                f"| Полное наименование | {source.full_name} |\n"
                f"| Единица измерения | {unit_name} |"
            )
        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else "-"
            content = (
                f"# Единица измерения: {source.name}\n\n"
                "| Параметр | Значение |\n| :--- | :--- |\n"
                f"| Код | {source.id} |\n"
                f"| Наименование | {source.name} |\n"
                f"| Коэффициент | {source.conversion_factor} |\n"
                f"| Базовая единица | {base_name} |"
            )
        else:
            content = f"# Сущность: {source.name}\n\n| Код | {source.id} |"

        raw_bytes = content.encode("utf-8")
        result.binary = list(raw_bytes)
        return result