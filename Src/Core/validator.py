from Src.Core.exception import arguments_exception


class argument_exception(arguments_exception):
    """Исключение при проверке аргумента (наследуется от базового arguments_exception)."""
    pass


class operation_exception(Exception):
    """Исключение при выполнении бизнес-операции."""
    pass


class validator:
    """Централизованный набор проверок данных."""

    @staticmethod
    def validate(value, type_, len_=None):
        """
        Валидация аргумента по типу и максимальной длине.

        Args:
            value: Проверяемое значение.
            type_: Ожидаемый тип данных.
            len_ (int, optional): Максимально допустимая длина строки.

        Raises:
            argument_exception: Если передан None, неверный тип, пустая строка или превышена длина.

        Returns:
            bool: True, если валидация пройдена.
        """
        if value is None:
            raise argument_exception("value", "Пустой аргумент")

        if not isinstance(value, type_):
            raise argument_exception(
                "type",
                f"Некорректный тип! Ожидается {type_}. Текущий тип: {type(value)}"
            )

        if isinstance(value, str):
            cleaned = value.strip()
            if len(cleaned) == 0:
                raise argument_exception("value", "Пустой строковый аргумент")

            if len_ is not None and len(cleaned) > len_:
                raise argument_exception("len", f"Некорректная длина аргумента. Максимум: {len_}")

        return True