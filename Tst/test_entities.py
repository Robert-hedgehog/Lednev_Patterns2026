# Необходимо установить pip install pytest в терминале с подключенным Environment
# Далее, настройки
# {
#    "python.testing.pytestArgs": [
#        "Tst"
#    ],
#    "python.testing.unittestEnabled": false,
#    "python.testing.pytestEnabled": true
#}
from Src.Core.class_abstract import abstract
from Src.Core.exception import arguments_exception

import pytest

#Тестовая сущность
class test_entity(abstract):
    pass

# Пример простого теста
def test_abstract_get_id_not_null():
    #Подготовка
    entity = test_entity()

    # Действие
    result = entity.id

    # Проверка
    assert result != ""

# Тест на проверку не повторяющихся id
def test_abstract_get_id_do_not_repeat():
    # Подготовка
    entity_1 = test_entity()
    entity_2 = test_entity()

    # Проверка
    assert entity_1 != entity_2

# Тест на проверку равенства по признаку одиннакового уникального кода
def test_abstract_get_equal_id():
    # Подготовка
    entity_1 = test_entity()
    entity_2 = test_entity()

    # Действие
    entity_1.id = "fff"
    entity_2.id = "fff"

    # Проверка
    assert entity_1 == entity_2

# Тест на проверку на формировании исключения при формировании name
def test_abstract_setter_name():
    # Подготовка
    entity = abstract()

    # Проверка

    # 1. Проверка TypeError (передача не строковых типов)
    with pytest.raises(TypeError, match="Наименование должно быть строкой."):
        entity.name = 123

    with pytest.raises(TypeError, match="Наименование должно быть строкой."):
        entity.name = None

    # 2. Проверка ValueError (пустая строка)
    with pytest.raises(ValueError, match="Наименование не может быть пустым."):
        entity.name = ""

# Тест на проверку на формировании исключения при формировании name с моим сообщением
def test_abstract_setter_name_message():
    # Подготовка
    entity = abstract()

    # Действие и Проверка перехвата                        
    with pytest.raises(arguments_exception) as exc_info:                     
        entity.name = ""                                                    
        print(f"Полный текст ошибки:\n{exc_info.value}")
