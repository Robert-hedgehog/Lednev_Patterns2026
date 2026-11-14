import io
import urllib.parse
from flask import Response, send_file, abort, jsonify
import connexion

from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Logics.convert_factory import convert_factory
from Src.Dtos.report_type_enum import report_type_enum
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.validator import argument_exception, operation_exception

storage = storage_manager()
factory = report_factory()
converter = convert_factory()

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


def get_default_report(entity_type: str, entity_id: str):
    """Формирование отчета через create_default."""
    decoded_id = urllib.parse.unquote(entity_id)
    data_dto = storage.get_report_data(entity_type, decoded_id)
    if not data_dto:
        abort(404, f"Сущность {entity_type} с кодом {entity_id} не найдена.")

    reporter = factory.create_default()
    result = reporter.build(data_dto)
    return build_http_response(result)


def get_report_formats():
    """Получение списка всех поддерживаемых форматов отчетов."""
    formats = [fmt.name for fmt in report_type_enum]
    return jsonify(formats), 200


def get_entities(entity_type: str):
    """Получение списка доменных сущностей указанного типа."""
    try:
        items = storage.get_entities(entity_type)
        return jsonify(converter.convert(items)), 200
    except argument_exception as ex:
        return jsonify({"detail": str(ex)}), 400


def get_entity(entity_type: str, entity_id: str):
    """Получение доменной сущности по идентификатору."""
    try:
        decoded_id = urllib.parse.unquote(entity_id)
        item = storage.get_entity(entity_type, decoded_id)
        return jsonify(converter.convert(item)), 200
    except argument_exception as ex:
        return jsonify({"detail": str(ex)}), 400
    except operation_exception as ex:
        return jsonify({"detail": str(ex)}), 404


def create_entity(entity_type: str, body: dict):
    """Создание новой доменной сущности."""
    try:
        created = storage.add_entity(entity_type, body)
        return jsonify(converter.convert(created)), 201
    except (argument_exception, operation_exception) as ex:
        return jsonify({"detail": str(ex)}), 400


def update_entity(entity_type: str, entity_id: str, body: dict):
    """Обновление существующей доменной сущности."""
    try:
        decoded_id = urllib.parse.unquote(entity_id)
        updated = storage.update_entity(entity_type, decoded_id, body)
        return jsonify(converter.convert(updated)), 200
    except argument_exception as ex:
        return jsonify({"detail": str(ex)}), 400
    except operation_exception as ex:
        status = 404 if "не найдена" in str(ex) else 409
        return jsonify({"detail": str(ex)}), status


def delete_entity(entity_type: str, entity_id: str):
    """Удаление доменной сущности."""
    try:
        decoded_id = urllib.parse.unquote(entity_id)
        storage.delete_entity(entity_type, decoded_id)
        return jsonify({"status": "deleted"}), 200
    except argument_exception as ex:
        return jsonify({"detail": str(ex)}), 400
    except operation_exception as ex:
        status = 404 if "не найдена" in str(ex) else 409
        return jsonify({"detail": str(ex)}), status


api.add_api("openapi.yaml")

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)