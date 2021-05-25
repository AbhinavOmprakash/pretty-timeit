import itertools
import gc
import time
from functools import wraps
from typing import Union, Iterable
from .helpers import StoredFunction


class Timer:
    """Class that handles executing the stored functions and timing them.

    Instance Attributes:
        functions_to_be_timed: A list that contains the StoredFunction object.
            The timethis decorator will "collect" functions in this list.

        exec_time: A dictionary that will contain the name of the function,
            and the time it took to execute.
            This will be used for printing out or generating a string
    """

    functions_to_be_timed = []
    exec_time = {}

    @staticmethod
    def run(repeat=1000000, compare=False, print_results=True):
        """calls the _timeit method on stored functions and returns/prints a report.

        Args:
            repeat: The number of times each function will be run.

            compare: If you wish to compare multiple algorithms,
                this flag tells the report to order
                the functions from fastest to slowest.

            print_results: Flag that determines whether the report
                will be returned as a string or be printed."""

        for stored_func in Timer.functions_to_be_timed:
            time = Timer._timeit(repeat, stored_func)
            Timer.exec_time[stored_func.name] = str(time)

        if print_results:
            print(Timer._format_report(compare))
        else:
            return Timer._format_report(compare)

    @staticmethod
    def _timeit(repeat, stored_func):
        func = stored_func.function
        args = stored_func.args
        kwargs = stored_func.kwargs

        gcold = gc.isenabled()
        gc.disable()

        try:
            start = time.perf_counter()
            for _ in itertools.repeat(None, repeat):
                func(*args, **kwargs)
            end = time.perf_counter()

        finally:
            if gcold:
                gc.enable()

        return end - start

    @staticmethod
    def _format_report(compare=False) -> str:
        def normal_report():
            report = f"name{(space_for_name-4)*space_char} | Execution time\n"  # 4 is the lenght of name
            for name, time in Timer.exec_time.items():
                report += f"{name}{(space_for_name-len(name))*space_char} | {time}\n"
            return report

        def ranked_report():
            report = f"rank | name{(space_for_name-4)*space_char} | Execution time\n"  # 4 is the lenght of name
            rank = 1
            for name, time in sorted(
                Timer.exec_time.items(), key=lambda items: items[1]
            ):  # sort by fastest executing function
                report += f"{rank}{(4-len(str(rank)))*space_char} | {name}{(space_for_name-len(name))*space_char} | {time}\n"
                rank += 1
            return report

        space_for_name = max(
            map(len, Timer.exec_time.keys())
        )  # find length of longest function name
        space_char = " "
        if compare:
            return ranked_report()
        else:
            return normal_report()


def timethis(args: Union[list, dict] = None, kwargs: dict = None, name: str = None):
    """Decorator that will stores the function in Timer.functions_to_be_timed.

    Args:
        args: A list that will contain positional arguments.
            In case the function only contains keyword arguments,
            This lets the user pass in a dictionary without passing in an empty list.
            So the user doesn't have to do this @timethis([], {"keyword":" argument"})
            And instead can do this @timethis({"keyword":" argument"}).

        kwargs: a dictionary that will contain keyword arguments
            that will be passed to the function.

        name: a descriptive name for the function.

    """
    if args and not isinstance(args, list) and not isinstance(args, dict):
        raise TypeError(
            f"Expected a List or Dict but got {type(args).__name__}. Did you forget To put the arguments in a list?"
        )

    if kwargs and not isinstance(kwargs, dict):
        if isinstance(kwargs, str):
            raise TypeError(
                f"Expected a Dictionary but got {type(args).__name__}. Did mean to use name={kwargs}?"
            )
        else:
            raise TypeError(f"Expected a Dictionary but got {type(args).__name__}.")

    def inner_decorator(func):
        f = StoredFunction(func, args, kwargs, name)
        Timer.functions_to_be_timed.append(f)

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return inner_decorator
