from typing import List, Optional
from Src.Core.class_abstract import abstract
from Src.Core.validator import validator
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model


class recipe_model(abstract):
    """Модель технологической карты (рецепта блюда или полуфабриката)."""

    def __init__(
        self,
        name: str = "",
        dish: Optional[nomenclature_model] = None,
        ingredients: Optional[List[ingredient_model]] = None
    ) -> None:
        """
        Инициализация технологической карты.

        Параметры:
            name: Наименование рецепта.
            dish: Выходная номенклатура (блюдо или полуфабрикат).
            ingredients: Список ингредиентов.
        """
        super().__init__()
        self._dish: Optional[nomenclature_model] = None
        self._ingredients: List[ingredient_model] = []

        if name:
            self.name = name
        elif dish:
            self.name = dish.name

        if dish is not None:
            self.dish = dish

        if ingredients:
            for item in ingredients:
                self.add_ingredient(item)

    @property
    def dish(self) -> Optional[nomenclature_model]:
        """Выходная номенклатура по рецепту."""
        return self._dish

    @dish.setter
    def dish(self, value: Optional[nomenclature_model]) -> None:
        if value is not None:
            validator.validate(value, nomenclature_model)
        self._dish = value

    @property
    def ingredients(self) -> List[ingredient_model]:
        """Список ингредиентов."""
        return self._ingredients

    def add_ingredient(self, item: ingredient_model) -> None:
        """Добавить ингредиент в рецепт."""
        validator.validate(item, ingredient_model)
        self._ingredients.append(item)

    def remove_ingredient(self, item: ingredient_model) -> bool:
        """Удалить ингредиент из рецепта."""
        if item in self._ingredients:
            self._ingredients.remove(item)
            return True
        return False

    @property
    def brutto(self) -> float:
        """Общий вес брутто рецепта."""
        return sum(item.brutto for item in self._ingredients)

    @property
    def netto(self) -> float:
        """Общий вес нетто рецепта."""
        return sum(item.netto for item in self._ingredients)

    @staticmethod
    def create(
        name: str,
        dish: nomenclature_model,
        ingredients: Optional[List[ingredient_model]] = None
    ) -> "recipe_model":
        """Фабричный метод создания рецепта."""
        return recipe_model(name=name, dish=dish, ingredients=ingredients)
    
    @property
    def items(self) -> List[ingredient_model]:
        """Синоним ingredients для совместимости с отчетами."""
        return self.ingredients

technological_card_model = recipe_model