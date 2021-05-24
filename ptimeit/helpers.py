from typing import Callable

class StoredFunction:
    """Class that is used to store a function, its arguments, and a name.
        """
    def __init__(self, function:Callable, arguments:list, name:str):
        """inits a StoredFunction Class.
        
        Args:
            argument: A list of objects, and possibly a dictionary for keyword args.
                This contains arguments that will be passed to the function when it is called."""

        self.function = function
        self.args = self._get_args(arguments)
        self.kwargs = self._get_kwargs(arguments)
        self.name = self._create_name(name)
        
    def _get_args(self, arguments):
        if arguments and isinstance(arguments[-1], dict):
            return arguments[:-1]
        elif not arguments:
            return []
        else:
            return arguments

    def _get_kwargs(self, arguments):
        if arguments and isinstance(arguments[-1], dict):
            return arguments[-1]
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
            return self.function.__name__
        else:
            return name
