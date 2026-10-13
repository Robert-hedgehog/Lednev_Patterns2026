from Src.Core.class_abstract import abstract
from Src.Core.exception import arguments_exception


class storage_model(abstract):
    """Модель склада (помещение для хранения сырья, заготовок и готовой продукции)."""

    def __init__(self, name: str = "", address: str = "") -> None:
        """
        Инициализирует склад.

        Args:
            name (str): Наименование склада (до 50 символов).
            address (str): Адрес или номер помещения (до 255 символов).
        """
        super().__init__()
        self._address: str = ""

        if name:
            self.name = name
        if address:
            self.address = address

    @property
    def address(self) -> str:
        """Адрес помещения склада."""
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """
        Устанавливает адрес помещения.

        Raises:
            arguments_exception: Если адрес не строка или превышает 255 символов.
        """
        if not isinstance(value, str):
            raise arguments_exception("address", "Адрес склада должен быть строкой.")

        normalized_address = value.strip()
        if len(normalized_address) > 255:
            raise arguments_exception("address", "Длина адреса не может превышать 255 символов.")

        self._address = normalized_address

    @staticmethod
    def create(name: str, address: str = "") -> "storage_model":
        """Фабричный метод создания склада."""
        storage = storage_model()
        storage.name = name
        if address:
            storage.address = address
        return storage