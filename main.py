import io
from flask import Response, send_file, abort
import connexion

from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_enum import report_type_enum

storage = storage_manager()
factory = report_factory()

api = connexion.FlaskApp(__name__, specification_dir="./")
app = api.app


def find_entity(entity_type: str, entity_id: str):
    """Поиск сущности в хранилище по типу и идентификатору."""
    normalized_type = entity_type.strip().lower()

    if normalized_type in ("nomenclature", "номенклатура"):
        collection = storage.nomenclatures
    elif normalized_type in ("range", "unit", "единица"):
        collection = storage.units
    elif normalized_type in ("recipe", "receipt", "рецепт"):
        collection = storage.recipes
    else:
        return None

    for item in collection:
        if str(item.id) == entity_id or getattr(item, "name", "") == entity_id:
            return item
    return None


@app.route("/api/report/<entity_type>/<entity_id>/<format_name>", methods=["GET"])
def get_custom_report(entity_type: str, entity_id: str, format_name: str):
    """Формирование отчета в указанном формате."""
    entity = find_entity(entity_type, entity_id)
    if entity is None:
        abort(404, description=f"Сущность {entity_type} с ID {entity_id} не найдена.")

    try:
        report_format = report_type_enum.from_string(format_name)
    except ValueError:
        abort(400, description=f"Формат {format_name} не поддерживается.")

    reporter = factory.create(report_format)
    report_dto = reporter.build(entity)

    if report_format in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        ext = "csv" if report_format == report_type_enum.CSV else "md"
        binary_data = bytes(report_dto.binary)
        return send_file(
            io.BytesIO(binary_data),
            as_attachment=True,
            download_name=f"report_{entity_type}_{entity_id}.{ext}",
            mimetype="application/octet-stream",
        )

    if report_format == report_type_enum.HTML:
        mimetype = "text/html; charset=utf-8"
    elif report_format == report_type_enum.XML:
        mimetype = "application/xml; charset=utf-8"
    else:
        mimetype = "text/plain; charset=utf-8"

    return Response(report_dto.text, mimetype=mimetype)


@app.route("/api/report/default/<entity_type>/<entity_id>", methods=["GET"])
def get_default_report(entity_type: str, entity_id: str):
    """Формирование отчета с использованием формата по умолчанию (create_default)."""
    entity = find_entity(entity_type, entity_id)
    if entity is None:
        abort(404, description=f"Сущность {entity_type} с ID {entity_id} не найдена.")

    reporter = factory.create_default()
    report_dto = reporter.build(entity)

    default_format = factory._report_factory__settings.response_format
    if default_format in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        ext = "csv" if default_format == report_type_enum.CSV else "md"
        binary_data = bytes(report_dto.binary)
        return send_file(
            io.BytesIO(binary_data),
            as_attachment=True,
            download_name=f"report_default_{entity_id}.{ext}",
            mimetype="application/octet-stream",
        )

    if default_format == report_type_enum.HTML:
        mimetype = "text/html; charset=utf-8"
    elif default_format == report_type_enum.XML:
        mimetype = "application/xml; charset=utf-8"
    else:
        mimetype = "text/plain; charset=utf-8"

    return Response(report_dto.text, mimetype=mimetype)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)