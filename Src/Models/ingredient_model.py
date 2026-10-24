from typing import Optional
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class ingredient_model(abstract):
    """
    Модель ингредиента технологической карты.
    Может представлять как отдельный продукт, так и полуфабрикат.
    """

    def __init__(
        self,
        name: str = "",
        nomenclature: Optional[nomenclature_model] = None,
        brutto: float = 0.0,
        netto: float = 0.0,
        unit: Optional[range_model] = None,
        recipe: Optional["recipe_model"] = None
    ) -> None:
        """
        Инициализация ингредиента.

        Параметры:
            name: Наименование позиции.
            nomenclature: Номенклатура ингредиента.
            brutto: Вес брутто.
            netto: Вес нетто.
            unit: Единица измерения.
            recipe: Рецепт полуфабриката (если ингредиент составной).
        """
        super().__init__()
        self._nomenclature: Optional[nomenclature_model] = None
        self._brutto: float = 0.0
        self._netto: float = 0.0
        self._unit: Optional[range_model] = None
        self._recipe: Optional[object] = None

        if name:
            self.name = name
        elif nomenclature:
            self.name = nomenclature.name

        if nomenclature is not None:
            self.nomenclature = nomenclature
        if unit is not None:
            self.unit = unit
        elif nomenclature and nomenclature.unit:
            self.unit = nomenclature.unit

        self._recipe = recipe

        if recipe is not None:
            self._brutto = brutto if brutto > 0 else getattr(recipe, "brutto", 0.0)
            self._netto = netto if netto > 0 else getattr(recipe, "netto", 0.0)
        else:
            self.brutto = brutto
            self.netto = netto

    @property
    def nomenclature(self) -> Optional[nomenclature_model]:
        """Номенклатура ингредиента."""
        return self._nomenclature

    @nomenclature.setter
    def nomenclature(self, value: Optional[nomenclature_model]) -> None:
        if value is not None:
            validator.validate(value, nomenclature_model)
        self._nomenclature = value

    @property
    def unit(self) -> Optional[range_model]:
        """Единица измерения ингредиента."""
        return self._unit

    @unit.setter
    def unit(self, value: Optional[range_model]) -> None:
        if value is not None:
            validator.validate(value, range_model)
        self._unit = value

    @property
    def recipe(self) -> Optional["recipe_model"]:
        """Вложенный рецепт полуфабриката."""
        return self._recipe

    @recipe.setter
    def recipe(self, value: Optional["recipe_model"]) -> None:
        """Установка рецепта с проверкой типа."""
        if value is not None:
            from Src.Models.recipe_model import recipe_model
            validator.validate(value, recipe_model)
        self._recipe = value

    @property
    def brutto(self) -> float:
        """Вес брутто с учетом вложенного полуфабриката."""
        if self._recipe is not None and hasattr(self._recipe, "brutto"):
            return float(self._recipe.brutto)
        return self._brutto

    @brutto.setter
    def brutto(self, value: float) -> None:
        validator.validate(value, (int, float))
        if value < 0:
            raise ValueError("Вес не может быть отрицательным.")
        self._brutto = float(value)

    @property
    def netto(self) -> float:
        """Вес нетто с учетом вложенного полуфабриката."""
        if self._recipe is not None and hasattr(self._recipe, "netto"):
            return float(self._recipe.netto)
        return self._netto

    @netto.setter
    def netto(self, value: float) -> None:
        validator.validate(value, (int, float))
        if value < 0:
            raise ValueError("Вес не может быть отрицательным.")
        self._netto = float(value)

    @staticmethod
    def create(
        nomenclature: nomenclature_model,
        brutto: float,
        netto: float,
        unit: Optional[range_model] = None
    ) -> "ingredient_model":
        """Фабричный метод создания ингредиента из номенклатуры."""
        return ingredient_model(
            name=nomenclature.name,
            nomenclature=nomenclature,
            brutto=brutto,
            netto=netto,
            unit=unit or nomenclature.unit
        )

    @staticmethod
    def create_from_recipe(
        recipe: "recipe_model",
        nomenclature: Optional[nomenclature_model] = None,
        unit: Optional[range_model] = None
    ) -> "ingredient_model":
        """Фабричный метод создания ингредиента из полуфабриката."""
        from Src.Models.recipe_model import recipe_model
        validator.validate(recipe, recipe_model)

        nom = nomenclature or getattr(recipe, "dish", None)
        name = getattr(recipe, "name", "Полуфабрикат")
        return ingredient_model(
            name=name,
            nomenclature=nom,
            recipe=recipe,
            unit=unit or (nom.unit if nom else None)
        )
    
    @property
    def unique_code(self) -> str:
        """Уникальный код ингредиента."""
        return str(self.id)