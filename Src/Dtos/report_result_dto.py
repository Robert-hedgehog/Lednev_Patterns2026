from Src.Core.class_abstract import abstract
from Src.Core.validator import validator


class report_result_dto(abstract):
    """Модель для хранения результата формирования отчета."""

    def __init__(self) -> None:
        super().__init__()
        self.__text: str = ""
        self.__binary: list = []

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