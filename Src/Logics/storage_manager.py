from typing import Dict, List
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model, group_model
from Src.Models.storage_model import storage_model


class storage_manager(abstract_manager):
    """Централизованное хранилище доменных объектов сети ресторанов."""

    __storages: Dict[str, storage_model] = {}
    __units: Dict[str, range_model] = {}
    __groups: Dict[str, group_model] = {}
    __nomenclatures: Dict[str, nomenclature_model] = {}
    __is_initialized: bool = False
    __is_loaded: bool = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage_manager, cls).__new__(cls)
            cls.instance.__storages = {}
            cls.instance.__units = {}
            cls.instance.__groups = {}
            cls.instance.__nomenclatures = {}
            cls.instance.__is_initialized = False
            cls.instance.__is_loaded = False
        return cls.instance

    def __init__(self) -> None:
        super().__init__()
        if not self.__is_initialized:
            self.first_start()
            self.__is_initialized = True

    def first_start(self) -> None:
        """Формирование начального набора данных при первом запуске."""
        gram = range_model("грамм", 1.0)
        kg = range_model("кг", 1000.0, gram)
        ml = range_model("миллилитр", 1.0)
        liter = range_model("литр", 1000.0, ml)
        piece = range_model("штука", 1.0)

        for unit in [gram, kg, ml, liter, piece]:
            self.add_unit(unit)

        main_warehouse = storage_model("Производственный цех", "ул. Производственная, д. 1")
        rest_warehouse_1 = storage_model("Склад Ресторана №1", "ул. Ленина, д. 10")
        rest_warehouse_2 = storage_model("Склад Ресторана №2 (Доставка)", "пр. Мира, д. 25")

        for storage in [main_warehouse, rest_warehouse_1, rest_warehouse_2]:
            self.add_storage(storage)

        raw_group = group_model("Сырье и мясная продукция")
        semi_group = group_model("Кулинарные полуфабрикаты")
        dish_group = group_model("Авторские горячие блюда")
        pack_group = group_model("Фирменная упаковка")

        for grp in [raw_group, semi_group, dish_group, pack_group]:
            self.add_group(grp)

        beef_cheeks = nomenclature_model("Говяжьи щеки", "Щеки говяжьи зачищенные охлажденные", raw_group, kg)
        grain = nomenclature_model("Крупа дождевая", "Крупа пшеничная птитим отборная", raw_group, kg)
        butter = nomenclature_model("Сливочное масло", "Масло сливочное крестьянское 82.5%", raw_group, kg)
        meat_sauce = nomenclature_model("Мясной соус", "Соус демигляс концентрированный", semi_group, liter)
        braised_cheeks = nomenclature_model("Томленые щеки", "Щеки говяжьи длительного томления су-вид", semi_group, kg)
        rain_porridge_dish = nomenclature_model(
            "Дождевая каша со щекой",
            "Дождевая каша с томленной говяжьей щекой в мясном соусе",
            dish_group,
            piece
        )

        for item in [beef_cheeks, grain, butter, meat_sauce, braised_cheeks, rain_porridge_dish]:
            self.add_nomenclature(item)

        self.__is_loaded = True

    def convert(self) -> bool:
        """Конвертация и актуализация состояния хранилища."""
        if not self.__is_initialized:
            self.first_start()
            self.__is_initialized = True

        self.__is_loaded = True
        return self.__is_loaded

    def add_storage(self, item: storage_model) -> None:
        """Добавить склад в хранилище."""
        validator.validate(item, storage_model)
        self.__storages[str(item.id)] = item

    def add_unit(self, item: range_model) -> None:
        """Добавить единицу измерения в хранилище."""
        validator.validate(item, range_model)
        self.__units[str(item.id)] = item

    def add_group(self, item: group_model) -> None:
        """Добавить группу номенклатуры в хранилище."""
        validator.validate(item, group_model)
        self.__groups[str(item.id)] = item

    def add_nomenclature(self, item: nomenclature_model) -> None:
        """Добавить номенклатуру в хранилище."""
        validator.validate(item, nomenclature_model)
        self.__nomenclatures[str(item.id)] = item

    def load(self, file_name: str = "") -> None:
        """Загрузка данных."""
        self.convert()

    @property
    def storages(self) -> List[storage_model]:
        """Список складов."""
        return list(self.__storages.values())

    @property
    def units(self) -> List[range_model]:
        """Список единиц измерения."""
        return list(self.__units.values())

    @property
    def groups(self) -> List[group_model]:
        """Список групп номенклатуры."""
        return list(self.__groups.values())

    @property
    def nomenclatures(self) -> List[nomenclature_model]:
        """Список позиций номенклатуры."""
        return list(self.__nomenclatures.values())

    @property
    def is_loaded(self) -> bool:
        """Флаг готовности данных."""
        return self.__is_loaded

    def clear(self) -> None:
        """Очистить коллекции (для тестов)."""
        self.__storages.clear()
        self.__units.clear()
        self.__groups.clear()
        self.__nomenclatures.clear()
        self.__is_initialized = False
        self.__is_loaded = False