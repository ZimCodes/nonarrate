"""Provides a UniqueConst class for managing unique constant values.

UniqueConst ensures duplicate values are not added to the collection.
This is useful to prevent flags from producing the same value.

"""
import argparse
from abc import ABC, abstractmethod

class UniqueConst(argparse.Action, ABC):
    """Represents a parser action to enforce an option to have unique values.

    UniqueConst behaves the same as the 'append_const' parser action except it places the 'const' value in a set() to prevent duplicate values.

    Attributes:
        _shared_list: A set of 'const' values
    """

    def __init__(self, option_strings, dest, const=None, default=None, type=None, choices=None,
                 required=False, help=None, metavar=None, deprecated=False):
        self._shared_list = None
        if const is None:
            raise ValueError(f'{self.__class__.__name__} requires "const" to have a value!')
        super().__init__(option_strings, dest, 0, const, default, type, choices, required, help, metavar, deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle new 'const' value introduced by an argument.

        When an argument with this action is used, this method is called.
        The method makes sure new unique 'const' values are added to the 
        collection.
        
        Args:
            parser: The parser used to extract values from arguments.
            namespace: The current namespace object holding all parsed values.
            values: A sequence of values supplied with the argument
            option_string: the argument string used to invoke this action

        """
        self.__init_set(namespace)
        self._modify_set(option_string)
        self.__apply_namespace(namespace)

    def __init_set(self, namespace):
        self._shared_list = getattr(namespace, self.dest, None)
        if self._shared_list is not None and not isinstance(self._shared_list, set):
            self._shared_list = set(self._shared_list)

    @abstractmethod
    def _modify_set(self, option_string: str):
        """Manage a set of constant values.

        Args:
            option_string: the name of the argument used to call this action
        """
        pass

    def __apply_namespace(self, namespace: argparse.Namespace):
        setattr(namespace, self.dest, self._shared_list)
