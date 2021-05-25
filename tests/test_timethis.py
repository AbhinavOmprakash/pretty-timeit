from ptimeit import timethis, Timer
import pytest
from unittest.mock import Mock, patch


@pytest.fixture(autouse=True)
def clear_stored_functions():
    yield
    Timer.functions_to_be_timed = []
    Timer.exec_time = {}


@pytest.fixture
def dummy():
    return lambda: 1  # . return a function that takes no arguments


def test_the_decorator_adds_functions_to_the_list_of_functions(dummy):
    fun_decorator = timethis()
    dummy = fun_decorator(dummy)
    stored_fn = Timer.functions_to_be_timed[0].function
    assert dummy.__name__ == stored_fn.__name__


def test_timer_returns_none_by_default(dummy):
    fun_decorator = timethis()
    dummy = fun_decorator(dummy)
    assert None == Timer.run(repeat=10)


def test_timer_returns_str_when_print_results_is_false(dummy):
    fun_decorator = timethis()
    dummy = fun_decorator(dummy)
    timer_result = Timer.run(repeat=10, print_results=False)
    assert True == isinstance(timer_result, str)


def test_timer_returns_different_string_when_compare_is_true(dummy):
    fun_decorator = timethis()
    dummy = fun_decorator(dummy)
    normal_result = Timer.run(repeat=10, print_results=False)
    compare_result = Timer.run(repeat=10, print_results=False, compare=True)
    assert normal_result != compare_result


def test_timethis_throws_an_error_when_args_is_not_list():
    with pytest.raises(TypeError):
        fun_decorator = timethis("pos_arg")


def test_timethis_throws_an_error_when_args_is_not_a_dict():
    with pytest.raises(TypeError):
        fun_decorator = timethis("pos_arg")


def test_timethis_throws_an_error_when_kwargs_is_not_a_dict_nor_a_string():
    with pytest.raises(TypeError):
        fun_decorator = timethis(["pos_arg"], 1)


# TODO find a better name for this function
def test_timethis_throws_an_error_when_name_is_passed_as_a_positional_argument():
    with pytest.raises(TypeError):
        fun_decorator = timethis(["pos_arg"], " Name without keyword")


@pytest.fixture
def dummy_2():
    return (
        lambda x: x
    )  # . return a function that takes Takes an argument and returns it


def test_timethis_does_not_modify_wrapped_function(dummy_2):
    original = dummy_2
    fun_decorator = timethis()
    dummy_2 = fun_decorator(dummy_2)
    assert original(1) == dummy_2(1)  # Check of both of them return  the same value
