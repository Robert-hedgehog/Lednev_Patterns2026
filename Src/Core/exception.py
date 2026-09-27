class arguments_exception(ValueError, TypeError):
    """Исключение, возникающее при передаче некорректных аргументов."""
    __stack_trace: str = ""
    __message: str = ""
    __field: str = ""

    def __init__(self, arg1: str = "", arg2: str = "", stack_trace: str = "") -> None:
        """
        Инициализирует исключение некорректного аргумента с гибким разбором входных данных.

        Параметры:
            arg1 (str): Имя проверяемого поля или текст сообщения об ошибке.
            arg2 (str): Текст сообщения об ошибке или имя поля (опционально).
            stack_trace (str): Стек вызова ошибки (опционально).
        """
        str1 = str(arg1).strip()
        str2 = str(arg2).strip()

        if not str2:
            self.__message = str1
            self.__field = "argument"
        elif " " in str1 and " " not in str2:
            self.__message = str1
            self.__field = str2
        else:
            self.__field = str1
            self.__message = str2

        self.__stack_trace = str(stack_trace).strip()
        super().__init__(self.__str__())

    def __str__(self) -> str:
        """
        Формирует строковое представление ошибки для вывода и логирования.

        Возвращает:
            str: Форматированный текст с описанием некорректного аргумента.
        """
        return f"Ошибка. Некорректный аргумент!\nПоле: {self.__field}\nСообщение: {self.__message}\n{self.__stack_trace}".strip()