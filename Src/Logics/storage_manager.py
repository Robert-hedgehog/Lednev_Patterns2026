from typing import Dict, List
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model, group_model
from Src.Models.storage_model import storage_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model


class storage_manager(abstract_manager):
    """Централизованное хранилище доменных объектов сети ресторанов."""

    __data: Dict[str, list] = {}
    __is_initialized: bool = False
    __is_loaded: bool = False

    def __new__(cls):
        """Реализация паттерна Singleton."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Инициализация данных в конструкторе."""
        super().__init__()
        if not hasattr(self, '_storage_manager__is_initialized') or not self.__is_initialized:
            self.__data = {}
            self.__is_initialized = False
            self.__is_loaded = False
            self.first_start()
            self.__is_initialized = True

    @staticmethod
    def range_key() -> str:
        """Ключ коллекции единиц измерения."""
        return "range_model"

    @staticmethod
    def storage_key() -> str:
        """Ключ коллекции складов."""
        return "storage_model"

    @staticmethod
    def group_key() -> str:
        """Ключ коллекции групп номенклатуры."""
        return "group_model"

    @staticmethod
    def nomenclature_key() -> str:
        """Ключ коллекции номенклатуры."""
        return "nomenclature_model"

    @staticmethod
    def recipe_key() -> str:
        """Ключ коллекции технологических карт."""
        return "recipe_model"

    def first_start(self) -> None:
        """Формирование начального набора данных через фабричные методы."""
        kg = range_model.create_killogramm()
        gram = kg.base_range
        ml = range_model("миллилитр", 1.0)
        liter = range_model("литр", 1000.0, ml)
        piece = range_model("штука", 1.0)

        self.__data[storage_manager.range_key()] = [gram, kg, ml, liter, piece]

        warehouse_main = storage_model.create("Производственный цех", "ул. Производственная, д. 1")
        warehouse_rest1 = storage_model.create("Склад Ресторана №1", "ул. Ленина, д. 10")
        warehouse_rest2 = storage_model.create("Склад Ресторана №2 (Доставка)", "пр. Мира, д. 25")

        self.__data[storage_manager.storage_key()] = [warehouse_main, warehouse_rest1, warehouse_rest2]

        raw_group = group_model.create("Сырье и мясная продукция")
        semi_group = group_model.create("Кулинарные полуфабрикаты")
        dish_group = group_model.create("Авторские горячие блюда")
        pack_group = group_model.create("Фирменная упаковка")

        self.__data[storage_manager.group_key()] = [raw_group, semi_group, dish_group, pack_group]

        beef_cheeks = nomenclature_model.create("Говяжьи щеки", "Щеки говяжьи зачищенные", raw_group, kg)
        grain = nomenclature_model.create("Крупа дождевая", "Крупа пшеничная птитим отборная", raw_group, kg)
        butter = nomenclature_model.create("Сливочное масло", "Масло сливочное крестьянское 82.5%", raw_group, kg)
        cheese = nomenclature_model.create("Сыр Пармезан", "Сыр твердый выдержанный пармезан", raw_group, kg)
        broth = nomenclature_model.create("Бульон мясной", "Бульон говяжий концентрированный", raw_group, liter)
        meat_sauce = nomenclature_model.create("Мясной соус", "Соус демигляс", semi_group, liter)
        greens = nomenclature_model.create("Микрозелень", "Микрозелень кресс-салат", raw_group, gram)

        braised_cheeks_semi = nomenclature_model.create(
            "Томленые щеки", "Щеки говяжьи длительного томления су-вид", semi_group, kg
        )
        rain_porridge_dish = nomenclature_model.create(
            "Дождевая каша со щекой", "Дождевая каша с томленной говяжьей щекой в мясном соусе", dish_group, piece
        )

        self.__data[storage_manager.nomenclature_key()] = [
            beef_cheeks, grain, butter, cheese, broth, meat_sauce, greens,
            braised_cheeks_semi, rain_porridge_dish
        ]

        ing_cheeks = ingredient_model.create(beef_cheeks, brutto=180.0, netto=150.0, unit=gram)
        ing_sauce_semi = ingredient_model.create(meat_sauce, brutto=50.0, netto=50.0, unit=ml)

        semi_recipe = recipe_model.create(
            name="Томленые говяжьи щеки (полуфабрикат)",
            dish=braised_cheeks_semi,
            ingredients=[ing_cheeks, ing_sauce_semi]
        )

        ing_semi = ingredient_model.create_from_recipe(
            recipe=semi_recipe,
            nomenclature=braised_cheeks_semi,
            unit=gram
        )
        ing_grain = ingredient_model.create(grain, brutto=75.0, netto=75.0, unit=gram)
        ing_broth = ingredient_model.create(broth, brutto=140.0, netto=140.0, unit=ml)
        ing_sauce_glaze = ingredient_model.create(meat_sauce, brutto=40.0, netto=40.0, unit=ml)
        ing_butter = ingredient_model.create(butter, brutto=20.0, netto=20.0, unit=gram)
        ing_cheese = ingredient_model.create(cheese, brutto=10.0, netto=10.0, unit=gram)
        ing_greens = ingredient_model.create(greens, brutto=5.0, netto=5.0, unit=gram)

        main_recipe = recipe_model.create(
            name="Дождевая каша с томленной щекой в мясном соусе",
            dish=rain_porridge_dish,
            ingredients=[
                ing_semi, ing_grain, ing_broth,
                ing_sauce_glaze, ing_butter, ing_cheese, ing_greens
            ]
        )

        self.__data[storage_manager.recipe_key()] = [semi_recipe, main_recipe]
        self.__is_loaded = True

    def convert(self) -> bool:
        """Конвертация и подготовка данных хранилища."""
        if not self.__is_initialized:
            self.first_start()
            self.__is_initialized = True
        self.__is_loaded = True
        return self.__is_loaded

    def add_storage(self, item: storage_model) -> None:
        """Добавить склад в хранилище с контролем уникальности."""
        validator.validate(item, storage_model)
        items = self.__data.setdefault(storage_manager.storage_key(), [])
        if not any(str(x.id) == str(item.id) for x in items):
            items.append(item)

    def add_unit(self, item: range_model) -> None:
        """Добавить единицу измерения в хранилище с контролем уникальности."""
        validator.validate(item, range_model)
        items = self.__data.setdefault(storage_manager.range_key(), [])
        if not any(str(x.id) == str(item.id) for x in items):
            items.append(item)

    def add_group(self, item: group_model) -> None:
        """Добавить группу номенклатуры в хранилище с контролем уникальности."""
        validator.validate(item, group_model)
        items = self.__data.setdefault(storage_manager.group_key(), [])
        if not any(str(x.id) == str(item.id) for x in items):
            items.append(item)

    def add_nomenclature(self, item: nomenclature_model) -> None:
        """Добавить позицию номенклатуры в хранилище с контролем уникальности."""
        validator.validate(item, nomenclature_model)
        items = self.__data.setdefault(storage_manager.nomenclature_key(), [])
        if not any(str(x.id) == str(item.id) for x in items):
            items.append(item)

    def add_recipe(self, item: recipe_model) -> None:
        """Добавить технологическую карту в хранилище с контролем уникальности."""
        validator.validate(item, recipe_model)
        items = self.__data.setdefault(storage_manager.recipe_key(), [])
        if not any(str(x.id) == str(item.id) for x in items):
            items.append(item)

    def load(self, file_name: str = "") -> None:
        """Загрузка данных."""
        self.convert()

    @property
    def data(self) -> Dict[str, list]:
        """Словарь всех зарегистрированных данных."""
        return self.__data

    @property
    def storages(self) -> List[storage_model]:
        """Список складов."""
        return self.__data.get(storage_manager.storage_key(), [])

    @property
    def units(self) -> List[range_model]:
        """Список единиц измерения."""
        return self.__data.get(storage_manager.range_key(), [])

    @property
    def groups(self) -> List[group_model]:
        """Список групп номенклатуры."""
        return self.__data.get(storage_manager.group_key(), [])

    @property
    def nomenclatures(self) -> List[nomenclature_model]:
        """Список позиций номенклатуры."""
        return self.__data.get(storage_manager.nomenclature_key(), [])

    @property
    def recipes(self) -> List[recipe_model]:
        """Список технологических карт."""
        return self.__data.get(storage_manager.recipe_key(), [])

    @property
    def is_loaded(self) -> bool:
        """Флаг готовности данных."""
        return self.__is_loaded

    def clear(self) -> None:
        """Очистка всех коллекций хранилища."""
        self.__data.clear()
        self.__is_initialized = False
        self.__is_loaded = False

    def get_by_type_and_id(self, entity_type: str, entity_id: str) -> object:
        """Поиск сущности в хранилище по типу и идентификатору или имени."""
        normalized_type = str(entity_type).strip().lower()
        search = str(entity_id).strip()

        if normalized_type in ("nomenclature", "номенклатура"):
            collection = self.nomenclatures
        elif normalized_type in ("range", "unit", "единица"):
            collection = self.units
        elif normalized_type in ("recipe", "receipt", "рецепт"):
            collection = self.recipes
        else:
            return None

        for item in collection:
            item_name = getattr(item, "name", "").strip()
            item_id = str(getattr(item, "id", "")).strip()
            if item_id == search or item_name == search or search in item_name:
                return item

        return None
    
    def get_report_data(self, entity_type: str, entity_id: str):
        """Формирует и возвращает report_data_dto для запрашиваемой сущности."""
        from Src.Dtos.report_data_dto import report_data_dto

        t = str(entity_type).strip().lower()
        search = str(entity_id).strip()

        if t in ("recipe", "receipt", "рецепт"):
            for item in self.recipes:
                if str(item.id) == search or item.name == search or search in item.name:
                    headers = ["id", "name", "brutto", "netto"]
                    rows = [[str(ing.id), ing.name, ing.brutto, ing.netto] for ing in item.ingredients]
                    return report_data_dto(item.name, headers, rows)

        elif t in ("nomenclature", "номенклатура"):
            for item in self.nomenclatures:
                if str(item.id) == search or item.name == search or search in item.name:
                    headers = ["id", "name", "full_name", "group", "unit"]
                    grp = item.group.name if item.group else "-"
                    u = item.unit.name if item.unit else "-"
                    rows = [[str(item.id), item.name, item.full_name, grp, u]]
                    return report_data_dto(item.name, headers, rows)

        elif t in ("range", "unit", "единица"):
            for item in self.units:
                if str(item.id) == search or item.name == search or search in item.name:
                    headers = ["id", "name", "conversion_factor", "base_range"]
                    base_name = item.base_range.name if item.base_range else "-"
                    rows = [[str(item.id), item.name, item.conversion_factor, base_name]]
                    return report_data_dto(item.name, headers, rows)

        return None