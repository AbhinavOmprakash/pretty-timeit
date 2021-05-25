from typing import Callable, Union


class StoredFunction:
    """Class that is used to store a function, its arguments, and a name."""

    def __init__(
        self, function: Callable, args: Union[list, dict], kwargs: dict, name: str
    ):
        """inits a StoredFunction Class.

        Args:
           args: A list that will contain positional arguments.
               In case the function only contains keyword arguments,
               This will be dictionary.

           kwargs: a dictionary that will contain keyword arguments
               that will be passed to the function.

           name: a descriptive name for the function.
               defaults to the name of the function.
        """

        self.function = function
        self.args = self._get_args(args)
        self.kwargs = self._get_kwargs(args, kwargs)
        self.name = self._create_name(name)

    def _get_args(self, args):
        if args and not isinstance(args, dict):
            return args
        else:
            return []

    def _get_kwargs(self, args, kwargs):
        # In case only keyword arguments are passed,
        # they are likely to be passed to args.
        if args and isinstance(args, dict):
            return args
        elif kwargs and isinstance(kwargs, dict):
            return kwargs
        else:
            return {}

    def _create_name(self, name: str):
        """If name is not specified by the user,
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
