from Src.Core.class_abstract import abstract
from Src.Core.exception import arguments_exception


class organization_model(abstract):
    """Модель организации (юридического лица ООО «Ромашка» или контрагента)."""

    def __init__(
        self,
        name: str = "",
        inn: str = "",
        bik: str = "",
        account: str = "",
        ownership_type: str = ""
    ) -> None:
        """
        Инициализирует модель организации.

        Args:
            name (str): Наименование организации (до 50 символов).
            inn (str): ИНН (10 или 12 цифр).
            bik (str): БИК (9 цифр).
            account (str): Номер расчетного счета (20 цифр).
            ownership_type (str): Форма собственности ('ООО', 'ПАО', 'ИП' и т.д.).
        """
        super().__init__()
        self._inn: str = ""
        self._bik: str = ""
        self._account: str = ""
        self._ownership_type: str = ""

        if name:
            self.name = name
        if inn:
            self.inn = inn
        if bik:
            self.bik = bik
        if account:
            self.account = account
        if ownership_type:
            self.ownership_type = ownership_type

    @property
    def inn(self) -> str:
        """ИНН организации (10 цифр для юридических лиц, 12 для ИП)."""
        return self._inn

    @inn.setter
    def inn(self, value: str) -> None:
        """
        Устанавливает ИНН.

        Raises:
            arguments_exception: Если ИНН содержит не только цифры или не равен 10/12 символам.
        """
        if not isinstance(value, str):
            raise arguments_exception("inn", "ИНН должен быть строкой.")

        clean_inn = value.strip()
        if not clean_inn.isdigit() or len(clean_inn) not in (10, 12):
            raise arguments_exception("inn", "ИНН должен состоять из 10 или 12 цифр.")

        self._inn = clean_inn

    @property
    def bik(self) -> str:
        """БИК банка (9 цифр)."""
        return self._bik

    @bik.setter
    def bik(self, value: str) -> None:
        """
        Устанавливает БИК.

        Raises:
            arguments_exception: Если БИК не состоит из ровно 9 цифр.
        """
        if not isinstance(value, str):
            raise arguments_exception("bik", "БИК должен быть строкой.")

        clean_bik = value.strip()
        if not clean_bik.isdigit() or len(clean_bik) != 9:
            raise arguments_exception("bik", "БИК должен состоять ровно из 9 цифр.")

        self._bik = clean_bik

    @property
    def account(self) -> str:
        """Расчетный счет (20 цифр)."""
        return self._account

    @account.setter
    def account(self, value: str) -> None:
        """
        Устанавливает расчетный счет.

        Raises:
            arguments_exception: Если номер счета не состоит из ровно 20 цифр.
        """
        if not isinstance(value, str):
            raise arguments_exception("account", "Счет должен быть строкой.")

        clean_account = value.strip()
        if not clean_account.isdigit() or len(clean_account) != 20:
            raise arguments_exception("account", "Номер счета должен состоять ровно из 20 цифр.")

        self._account = clean_account

    @property
    def ownership_type(self) -> str:
        """Форма собственности (ООО, АО, ИП и др.)."""
        return self._ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str) -> None:
        """
        Устанавливает форму собственности.

        Raises:
            arguments_exception: Если строка пустая или длиннее 50 символов.
        """
        if not isinstance(value, str):
            raise arguments_exception("ownership_type", "Форма собственности должна быть строкой.")

        normalized_ownership = value.strip()
        if not normalized_ownership:
            raise arguments_exception("ownership_type", "Форма собственности не может быть пустой.")

        if len(normalized_ownership) > 50:
            raise arguments_exception("ownership_type", "Форма собственности не может превышать 50 символов.")

        self._ownership_type = normalized_ownership