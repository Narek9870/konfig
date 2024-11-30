import pytest
import io
from config_parser import ConfigParser

def test_transform_value_number():
    transformer = ConfigParser()
    assert transformer.transform_value('42') == 42
    assert transformer.transform_value('3.14') == 3.14

def test_transform_value_string():
    transformer = ConfigParser()
    assert transformer.transform_value('"Name"') == 'Name'
    assert transformer.transform_value('"Hello World"') == 'Hello World'

def test_transform_value_boolean():
    transformer = ConfigParser()
    assert transformer.transform_value('true') is True
    assert transformer.transform_value('false') is False

def test_transform_value_none():
    transformer = ConfigParser()
    assert transformer.transform_value('None') == 'None'  # Строковое значение "None"

def test_handle_variable_declaration():
    transformer = ConfigParser()
    transformer.handle_variable_declaration('var a := 5')
    assert transformer.variables['a'] == 5

def test_handle_list_declaration():
    transformer = ConfigParser()
    transformer.variables = {'a': 5, 'b': 10}
    transformer.handle_list_declaration('list(${a}, ${b}, ${a} + ${b})')
    assert transformer.variables['list'] == [5, 10, 15]

def test_evaluate_expression():
    transformer = ConfigParser()
    transformer.variables = {'a': 5, 'b': 10}
    assert transformer.evaluate_expression('5 + 10') == 15
    assert transformer.evaluate_expression('abs(-10)') == 10
    assert transformer.evaluate_expression('invalid + 5') == 'invalid + 5'  # Оставляем строку на ошибку


def test_parse_file(monkeypatch):
    test_config = """
    var a := 5
    var b := 10
    list(${a}, ${b}, ${a} + ${b})
    """

    # Патчим open, чтобы возвращать поток данных (StringIO), а не файл
    monkeypatch.setattr('builtins.open', lambda file, mode, **kwargs: io.StringIO(test_config))

    transformer = ConfigParser()

    # Теперь передаем поток данных в parse
    transformer.parse(io.StringIO(test_config))  # Путь заменен на сам поток данных

    # Проверяем результат
    assert 'a' in transformer.variables
    assert 'b' in transformer.variables
    assert 'list' in transformer.variables
    assert transformer.variables['list'] == [5, 10, 15]



def test_invalid_syntax():
    transformer = ConfigParser()
    with pytest.raises(Exception):
        transformer.handle_variable_declaration('var c := ${undefined_variable}')

def test_expression_with_variables():
    transformer = ConfigParser()
    transformer.variables = {'a': 5, 'b': 10}
    assert transformer.evaluate_expression('${a} + ${b}') == 15
