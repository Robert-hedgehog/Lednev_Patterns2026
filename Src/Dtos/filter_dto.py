from Src.Core.class_abstract import abstract
from Src.Core.validator import validator, argument_exception
from Src.Dtos.filter_type_enum import filter_type_enum


class filter_dto(abstract):
    """DTO-модель параметров фильтрации доменных сущностей."""

    def __init__(
        self,
        field_name: str = "name",
        value: object = "",
        filter_type: filter_type_enum = filter_type_enum.EQUALS,
        model_name: str = "",
    ) -> None:
        """Инициализация параметров фильтрации."""
        super().__init__()
        self.__field_name: str = "name"
        self.__value: object = ""
        self.__filter_type: filter_type_enum = filter_type_enum.EQUALS
        self.__model_name: str = ""

        self.field_name = field_name
        if value != "":
            self.value = value
        self.filter_type = filter_type
        if model_name:
            self.model_name = model_name

    @property
    def field_name(self) -> str:
        """Наименование поля для фильтрации."""
        return self.__field_name

    @field_name.setter
    def field_name(self, value: str) -> None:
        """Установка поля фильтрации."""
        validator.validate(value, str, 100)
        self.__field_name = value.strip()

    @property
    def model_name(self) -> str:
        """Название вложенной модели для фильтрации."""
        return self.__model_name

    @model_name.setter
    def model_name(self, value: str) -> None:
        """Установка названия вложенной модели."""
        if value is None:
            self.__model_name = ""
            return
        if not isinstance(value, str):
            raise argument_exception("model_name", "Название модели должно быть строкой.")
        self.__model_name = value.strip()

    @property
    def value(self) -> object:
        """Искомое значение фильтра."""
        return self.__value

    @value.setter
    def value(self, value: object) -> None:
        """Установка искомого значения."""
        if value is None:
            raise argument_exception("value", "Значение фильтра не может быть None.")
        self.__value = value.strip() if type(value) is str else value

    @property
    def filter_type(self) -> filter_type_enum:
        """Тип сравнения фильтра."""
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, value: filter_type_enum | str) -> None:
        """Установка типа сравнения."""
        converters = {
            filter_type_enum: lambda v: v,
            str: filter_type_enum.from_string,
        }
        converter = converters.get(type(value))
        if converter is None:
            raise argument_exception("filter_type", "Некорректный тип фильтрации.")
        self.__filter_type = converter(value)

    @staticmethod
    def create(
        field_name: str,
        value: object,
        filter_type: filter_type_enum | str = filter_type_enum.EQUALS,
        model_name: str = "",
    ) -> "filter_dto":
        """Фабричный метод создания DTO фильтра."""
        dto = filter_dto()
        dto.field_name = field_name
        dto.value = value
        dto.filter_type = filter_type
        dto.model_name = model_name
        return dto

    @classmethod
    def from_dict(cls, data: dict) -> "filter_dto":
        """Фабричный метод создания DTO фильтра из словаря."""
        validator.validate(data, dict)
        dto = cls()
        dto.id = data.get("id", str(dto.id))
        if "field_name" in data:
            dto.field_name = data["field_name"]
        if "model_name" in data:
            dto.model_name = data["model_name"]
        if "value" in data:
            dto.value = data["value"]
        if "filter_type" in data:
            dto.filter_type = data["filter_type"]
        return dto