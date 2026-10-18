from typing import Optional
from Src.Core.class_abstract import abstract
from Src.Core.exception import arguments_exception


class range_model(abstract):
    """Модель единицы измерения (диапазон измерения)."""

    def __init__(
        self,
        name: str = "",
        conversion_factor: float = 1.0,
        base_range: Optional["range_model"] = None
    ) -> None:
        """
        Инициализирует единицу измерения.

        Args:
            name (str): Краткое наименование (до 50 символов).
            conversion_factor (float): Коэффициент пересчета относительно базовой единицы.
            base_range (Optional[range_model]): Базовая единица измерения (если есть).
        """
        super().__init__()
        self._conversion_factor: float = 1.0
        self._base_range: Optional["range_model"] = None

        if name:
            self.name = name

        self.conversion_factor = conversion_factor

        if base_range is not None:
            self.base_range = base_range

    @property
    def conversion_factor(self) -> float:
        """Коэффициент пересчета относительно базовой единицы измерения."""
        return self._conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value: float) -> None:
        """
        Устанавливает коэффициент пересчета.

        Raises:
            arguments_exception: Если значение не является числом или <= 0.
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("conversion_factor", "Коэффициент пересчета должен быть числом.")

        if value <= 0:
            raise arguments_exception("conversion_factor", "Коэффициент пересчета должен быть строго больше 0.")

        self._conversion_factor = float(value)

    @property
    def base_range(self) -> Optional["range_model"]:
        """Базовая единица измерения."""
        return self._base_range

    @base_range.setter
    def base_range(self, value: Optional["range_model"]) -> None:
        """
        Устанавливает базовую единицу измерения.

        Raises:
            arguments_exception: Если переданное значение не является range_model.
        """
        if value is not None and not isinstance(value, range_model):
            raise arguments_exception("base_range", "Базовая единица должна являться объектом range_model.")

        self._base_range = value

    """
    Фабричный метод - создать киллограмм
    """
    @staticmethod
    def create_killogramm() -> "range_model":
        gramm = range_model("грамм", 1.0)
        return range_model("киллограмм", 1000.0, gramm)
    
    def get_report_fields(self) -> dict:
        """Поля единицы измерения для отчетов."""
        data = super().get_report_fields()
        data["conversion_factor"] = self.conversion_factor
        data["base_range"] = self.base_range.name if self.base_range else "-"
        return data