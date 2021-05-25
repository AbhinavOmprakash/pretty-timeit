from ptimeit.helpers import StoredFunction
import pytest


@pytest.fixture
def dummy():
    return (
        lambda pos, key="": pos
    )  # . return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly(dummy):
    args = ["pos"]
    kwargs = {"key": "keyword"}
    stored = StoredFunction(dummy, args, kwargs, None)
    assert stored.args == ["pos"]
    assert stored.kwargs == {"key": "keyword"}


@pytest.fixture
def dummy_2():
    return (
        lambda pos: pos
    )  # . return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly_when_no_keyword_args(dummy_2):
    args = ["pos"]
    stored = StoredFunction(dummy_2, args, None, None)
    assert stored.args == ["pos"]
    assert stored.kwargs == {}


@pytest.fixture
def dummy_3():
    return (
        lambda key="a": key
    )  # . return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly_when_only_keyword_args(dummy_3):
    args = {"key": "a"}
    stored = StoredFunction(dummy_3, args, None, None)
    assert stored.args == []
    assert stored.kwargs == {"key": "a"}


@pytest.fixture
def dummy_4():
    return lambda: 1  # . return a function that takes Positional and a keyword argument


def test_params_are_parsed_correctly_when_no__args_are_passed(dummy_4):
    stored = StoredFunction(dummy_4, None, None, None)
    assert stored.args == []
    assert stored.kwargs == {}


@pytest.fixture
def dummy_5():
    def named_function():
        return True

    return named_function  # . return a function that takes Positional and a keyword argument


def test_stored_function_name_is_function_name_by_default(dummy_5):
    stored = StoredFunction(dummy_5, None, None, None)
    assert stored.name == dummy_5.__name__


def test_stored_function_name_is_descriptive_name(dummy_5):
    stored = StoredFunction(dummy_5, None, None, "description")
    assert stored.name != dummy_5.__name__
    assert stored.name == "description"
