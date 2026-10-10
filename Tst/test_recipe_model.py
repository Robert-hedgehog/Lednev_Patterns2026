import pytest
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model, group_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model


@pytest.fixture(autouse=True)
def init_storage():
    """Фикстура подготовки хранилища."""
    manager = storage_manager()
    manager.clear()
    manager.first_start()
    yield manager


def test_success_recipe_presence_in_storage_manager():
    """
    <summary>Проверка наличия рецептов в хранилище при первом старте.</summary>
    <description>Проверяется наличие полуфабриката и основного блюда в коллекции recipes.</description>
    <expected>Оба рецепта присутствуют в хранилище.</expected>
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    recipe_names = [r.name for r in manager.recipes]

    # Проверки
    assert len(manager.recipes) >= 2
    assert "Томленые говяжьи щеки (полуфабрикат)" in recipe_names
    assert "Дождевая каша с томленной щекой в мясном соусе" in recipe_names


def test_success_recipe_nested_brutto_and_netto_calculation():
    """
    <summary>Проверка расчета веса Брутто и Нетто для составного рецепта.</summary>
    <description>Главное блюдо включает полуфабрикат, вес которого суммируется автоматически.</description>
    <expected>Вес блюда равен сумме обычных ингредиентов плюс вес полуфабриката.</expected>
    """
    # Подготовка
    manager = storage_manager()
    main_recipe = next(r for r in manager.recipes if "Дождевая каша" in r.name)
    semi_recipe = next(r for r in manager.recipes if "полуфабрикат" in r.name)

    # Действие
    semi_brutto = semi_recipe.brutto
    semi_netto = semi_recipe.netto
    main_brutto = main_recipe.brutto
    main_netto = main_recipe.netto

    # Проверки
    # Полуфабрикат: щеки (180/150) + соус (50/50) = 230 брутто / 200 нетто
    assert semi_brutto == 230.0
    assert semi_netto == 200.0

    # Главное блюдо включает полуфабрикат (230/200) + 290 г остальных ингредиентов
    assert main_brutto == 230.0 + 290.0
    assert main_netto == 200.0 + 290.0


def test_success_recipe_recalculate_on_add_and_remove_ingredient():
    """
    <summary>Проверка пересчета веса при добавлении и удалении ингредиента.</summary>
    <description>В рецепт добавляется новый ингредиент, а затем удаляется.</description>
    <expected>Вес корректно увеличивается при добавлении и уменьшается при удалении.</expected>
    """
    # Подготовка
    dish = nomenclature_model.create("Тестовое блюдо")
    salt_nom = nomenclature_model.create("Соль")
    pepper_nom = nomenclature_model.create("Перец")

    ing_salt = ingredient_model.create(salt_nom, brutto=10.0, netto=10.0)
    ing_pepper = ingredient_model.create(pepper_nom, brutto=5.0, netto=5.0)
    recipe = recipe_model.create("Тестовый рецепт", dish, [ing_salt])

    initial_brutto = recipe.brutto
    initial_netto = recipe.netto

    # Действие
    recipe.add_ingredient(ing_pepper)

    # Проверки
    assert recipe.brutto == initial_brutto + 5.0
    assert recipe.netto == initial_netto + 5.0

    # Действие
    is_removed = recipe.remove_ingredient(ing_pepper)

    # Проверки
    assert is_removed is True
    assert recipe.brutto == initial_brutto
    assert recipe.netto == initial_netto

def test_ingredient_model_setters_and_negative_validation():
    """
    <summary>Проверка сеттеров и валидации отрицательного веса ингредиента.</summary>
    <description>Проверяются свойства nomenclature, unit, recipe и ошибки при весе меньше 0.</description>
    <expected>Свойства устанавливаются, на отрицательный вес выбрасывается ValueError.</expected>
    """
    # Подготовка
    nom = nomenclature_model.create("Тест")
    ing = ingredient_model.create(nom, brutto=10.0, netto=10.0)

    # Действие и проверки
    ing.unit = None
    ing.recipe = None
    assert ing.unit is None
    assert ing.recipe is None

    with pytest.raises(ValueError):
        ing.brutto = -5.0

    with pytest.raises(ValueError):
        ing.netto = -1.0


def test_recipe_model_dish_setter_and_remove_missing_ingredient():
    """
    <summary>Проверка сеттера блюда и удаления отсутствующего ингредиента.</summary>
    <description>Установка dish и попытка удалить ингредиент, которого нет в рецепте.</description>
    <expected>dish обновляется, удаление несуществующего возвращает False.</expected>
    """
    # Подготовка
    nom1 = nomenclature_model.create("Блюдо 1")
    nom2 = nomenclature_model.create("Блюдо 2")
    recipe = recipe_model.create("Рецепт", nom1, [])
    missing_ing = ingredient_model.create(nom2, 10.0, 10.0)

    # Действие
    recipe.dish = nom2
    result = recipe.remove_ingredient(missing_ing)

    # Проверки
    assert recipe.dish == nom2
    assert result is False


def test_storage_manager_add_all_types_and_load_call():
    """
    <summary>Проверка методов добавления всех сущностей в storage_manager и вызова load.</summary>
    <description>Вызов add_group, add_nomenclature, add_recipe и load для покрытия методов.</description>
    <expected>Элементы добавляются в соответствующие коллекции, load выполняется успешно.</expected>
    """
    # Подготовка
    manager = storage_manager()
    grp = group_model.create("Новая группа")
    nom = nomenclature_model.create("Новая номенклатура", group=grp)
    rec = recipe_model.create("Новый рецепт", nom, [])

    # Действие
    manager.add_group(grp)
    manager.add_nomenclature(nom)
    manager.add_recipe(rec)
    manager.load()

    # Проверки
    assert grp in manager.groups
    assert nom in manager.nomenclatures
    assert rec in manager.recipes