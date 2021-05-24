"""

"""
import itertools
import gc
import time

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
            Timer.exec_time[stored_func.name]= str(time)
            
        if print_results:
            print(Timer._format_report(compare))
        else:
            return Timer.exec_time

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

        return end-start

    @staticmethod
    def _format_report(compare=False)->str:
        def normal_report():
            report = f"name{(space_for_name-4)*space_char} | Execution time\n" # 4 is the lenght of name
            for name, time in Timer.exec_time.items():
                report += f"{name}{(space_for_name-len(name))*space_char} | {time}\n"      
            return report
        
        def ranked_report():
            report = f"rank | name{(space_for_name-4)*space_char} | Execution time\n" # 4 is the lenght of name
            rank = 1
            for name, time in sorted(Timer.exec_time.items(), key=lambda items:items[1]): # sort by fastest executing function
                report += f"{rank}{(4-len(str(rank)))*space_char} | {name}{(space_for_name-len(name))*space_char} | {time}\n"
                rank +=1
            return report

        space_for_name = max(map(len, Timer.exec_time.keys())) # find length of longest function name
        space_char=" "
        if compare:
            return ranked_report()
        else:
            return normal_report()

def timethis(params:list=None, name:str=None):
    """Decorator that will stores the function in Timer.functions_to_be_timed.

    Args:
        params: a list that stores arguments that the user wishes to pass
            to the function. The list can also contain a dictionary at the 
            end to hold keyword arguments.
        
        name: a descriptive name for the function. 
            defaults to the name of the function.

    """
    if not isinstance(params, list):
        raise TypeError(f"Expected a list but got {type(params).__name__}. Did you forget To put the arguments in the list?")

    def inner_decorator(func):
        f = StoredFunction(func, params, name)
        Timer.functions_to_be_timed.append(f)

        def wrapped(*args, **kwargs):
            return func

        return wrapped    

    return inner_decorator

# @timethis()
# def my_func():
#     l = [i for i in range(100)]

# @timethis()
# def my_func2():
#     l = [i for i in range(10)]
# Timer.run(10000,compare=True)
