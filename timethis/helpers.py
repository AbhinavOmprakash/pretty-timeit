from typing import Callable
import re

class StoredFunction:
    """Class that is used to store a function, its arguments, and a name.
        """
    def __init__(self, function:Callable, arguments:list, name:list):
        """inits a StoredFunction Class.
        
        Args:
            argument: A list of objects, and possibly a dictionary for keyword args.
                This contains arguments that will be passed to the function when it is called."""

        self.function = function
        self.args = self._get_args(arguments)
        self.kwargs = self._get_kwargs(arguments)
        self.name = self._create_name(name)
        
    def _get_args(self, arguments):
        if arguments:
            if isinstance(arguments[-1], dict):
                return arguments[:-1]
            else:
                return arguments
        else:
            return []

    def _get_kwargs(self, arguments):
        if arguments:
            if isinstance(arguments[-1], dict):
                return arguments[-1]
            else:
                return {}
        else:
            return {}

    def _create_name(self, name:str):
        """ If name is not specified by the user, 
        then the name defaults to the name of the function.
        For e.g. 
        def my_func():
            l = [i for i in range(100)]
        
        Defaults to my_func
        """
        if not name:
            # Extract name from function representation
            # <function my_func at 0x00000190CC976160> -> my_func
            match = re.search(r"(?<=<function )[\w]+?(?= at)", str(self.function))
            return match.group(0)
        else:
            return name
