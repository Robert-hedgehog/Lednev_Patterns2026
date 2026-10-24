import io
import urllib.parse
from flask import Response, send_file, abort
import connexion

from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_enum import report_type_enum
from Src.Dtos.report_result_dto import report_result_dto

storage = storage_manager()
factory = report_factory()

api = connexion.FlaskApp(__name__, specification_dir="./")
app = api.app


def build_http_response(dto: report_result_dto):
    """Полиморфное формирование ответа из DTO без условий."""
    if dto.is_attachment:
        return send_file(
            io.BytesIO(bytes(dto.binary)),
            as_attachment=True,
            download_name=f"report.{dto.file_extension}",
            mimetype=dto.mime_type,
        )
    return Response(dto.text, mimetype=dto.mime_type)


@app.route("/api/report/<entity_type>/<entity_id>/<format_name>", methods=["GET"])
def get_report(entity_type: str, entity_id: str, format_name: str):
    """Формирование отчета в указанном формате."""
    decoded_id = urllib.parse.unquote(entity_id)
    data_dto = storage.get_report_data(entity_type, decoded_id)
    if not data_dto:
        abort(404, f"Сущность {entity_type} с кодом {entity_id} не найдена.")

    try:
        fmt = report_type_enum.from_string(format_name)
    except ValueError:
        abort(400, f"Формат {format_name} не поддерживается.")

    reporter = factory.create(fmt)
    result = reporter.build(data_dto)
    return build_http_response(result)


@app.route("/api/report/default/<entity_type>/<entity_id>", methods=["GET"])
def get_default_report(entity_type: str, entity_id: str):
    """Формирование отчета через create_default."""
    decoded_id = urllib.parse.unquote(entity_id)
    data_dto = storage.get_report_data(entity_type, decoded_id)
    if not data_dto:
        abort(404, f"Сущность {entity_type} с кодом {entity_id} не найдена.")

    reporter = factory.create_default()
    result = reporter.build(data_dto)
    return build_http_response(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)