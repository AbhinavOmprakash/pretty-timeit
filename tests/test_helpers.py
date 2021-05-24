from ptimeit.helpers import StoredFunction
import pytest

@pytest.fixture
def dummy():
    return lambda pos, key="": pos #. return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly(dummy):
    params = ["pos", {"key":"keyword"}]
    stored=StoredFunction(dummy,params, None)
    assert stored.args == ["pos"]
    assert stored.kwargs =={"key":"keyword"}


@pytest.fixture
def dummy_2():
    return lambda pos:pos #. return a function that takes Positional and a keyword argument

def test_params_are_parsed_correctly_when_no_keyword_args(dummy_2):
    params = ["pos"]
    stored=StoredFunction(dummy_2,params, None)
    assert stored.args == ["pos"]
    assert stored.kwargs =={}

@pytest.fixture
def dummy_3():
    return lambda key="a":key #. return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly_when_only_keyword_args(dummy_3):
    params = [{"key":"a"}]
    stored=StoredFunction(dummy_3,params, None)
    assert stored.args == []
    assert stored.kwargs == {"key":"a"}

@pytest.fixture
def dummy_4():
    return lambda :1 #. return a function that takes Positional and a keyword argument

def test_params_are_parsed_correctly_when_only_keyword_args(dummy_4):
    params = []
    stored=StoredFunction(dummy_4, params, None)
    assert stored.args == []
    assert stored.kwargs == {}

@pytest.fixture
def dummy_5():
    def named_function():
        return True
    return named_function#. return a function that takes Positional and a keyword argument


def test_stored_function_name_is_function_name_by_default(dummy_5):
    params = []
    stored=StoredFunction(dummy_5, params, None)
    assert stored.name == dummy_5.__name__

def test_stored_function_name_is_descriptive_name(dummy_5):
    params = []
    stored=StoredFunction(dummy_5, params, "description")
    assert stored.name != dummy_5.__name__
    assert stored.name == "description"



















