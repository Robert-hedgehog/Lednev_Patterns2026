from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.class_abstract import abstract
from Src.Core.validator import argument_exception


class reference_convertor(abstract_convertor):
    """Конвертор ссылочных типов данных (доменных сущностей)."""

    def __init__(self, factory: object = None) -> None:
        super().__init__()
        self.__factory = factory

    def convert(self, field_name: str, value: object) -> dict:
        """Конвертация доменной сущности в словарь."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise argument_exception("field_name", "Имя поля должно быть непустой строкой.")

        if value is None:
            return {field_name.strip(): None}

        if not isinstance(value, abstract):
            raise argument_exception(
                "value",
                f"Ожидается доменная сущность abstract, получен {type(value).__name__}."
            )

        if self.__factory is not None and hasattr(self.__factory, "convert"):
            serialized = self.__factory.convert(value)
        else:
            serialized = {"id": str(value.id), "name": value.name}

        return {field_name.strip(): serialized}