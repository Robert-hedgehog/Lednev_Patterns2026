from Src.Core.class_abstract import abstract
from Src.Core.validator import validator


class report_result_dto(abstract):
    """Модель для хранения результата формирования отчета."""

    def __init__(self) -> None:
        super().__init__()
        self.__text: str = ""
        self.__binary: list = []
        self.__mime_type: str = "text/plain; charset=utf-8"
        self.__file_extension: str = "txt"
        self.__is_attachment: bool = False

    @property
    def text(self) -> str:
        """Текстовый результат отчета."""
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        validator.validate(value, str)
        self.__text = value
        self.__binary = []

    @property
    def binary(self) -> list:
        """Бинарный результат отчета."""
        return self.__binary

    @binary.setter
    def binary(self, value: list) -> None:
        validator.validate(value, list)
        if len(value) > 0:
            self.__text = ""
            self.__binary = value

    @property
    def mime_type(self) -> str:
        """MIME-тип сформированного отчета."""
        return self.__mime_type

    @mime_type.setter
    def mime_type(self, value: str) -> None:
        validator.validate(value, str)
        self.__mime_type = value

    @property
    def file_extension(self) -> str:
        """Расширение файла."""
        return self.__file_extension

    @file_extension.setter
    def file_extension(self, value: str) -> None:
        validator.validate(value, str)
        self.__file_extension = value

    @property
    def is_attachment(self) -> bool:
        """Флаг необходимости скачивания файла."""
        return self.__is_attachment

    @is_attachment.setter
    def is_attachment(self, value: bool) -> None:
        validator.validate(value, bool)
        self.__is_attachment = value