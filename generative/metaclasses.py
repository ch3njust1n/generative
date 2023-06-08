import textwrap
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Type,
)

from .utils import (
    extract_func_name,
    is_valid_syntax,
    remove_prepended,
)

"""
This is an abstract base class that represents a database API.

Developers can extend this class to implement their own database classes
that can be used anywhere an object of type `AbstractDatabase` is expected.

Subclasses must implement the following methods:

find(self, query: str) -> Any:
    Executes a given query against the database.

add(self, data: Any) -> None:
    Adds data into the database.
"""


class AbstractDatabase(ABC):
    @abstractmethod
    def find(self, query: str) -> Any:
        """
        Executes a given query against the database.

        :param query: query to be executed.
        :return: Query results.
        """
        pass

    @abstractmethod
    def add(self, data: Any) -> None:
        """
        Inserts data into the database.

        :param data: Data to be inserted.
        """
        pass


class DatabaseException(Exception):
    """Exception raised for database-related errors."""

    pass


class BaseMetaClass(type):
    is_generative: bool = False


"""
A metaclass for dynamic class generation.

This metaclass enables dynamic generation and addition of methods to the
classes it creates, based on the provided Python code.

Attributes:
    is_generative: A boolean flag indicating whether the class is generative.
"""


class GenerativeMetaClass(BaseMetaClass):
    """
    Initialize the GenerativeMetaClass.

    Args:
        cls: The class object to be initialized.
        name: The name of the new class.
        bases: A tuple of the new class's parent classes.
        attrs: A dictionary of the new class's attributes.
    """

    def __init__(
        cls: Type[Any],
        name: str,
        bases: Tuple[Type[Any], ...],
        attrs: Dict[str, Any],
    ) -> None:
        cls.is_generative = False  # type: ignore

    """
    Generate and add a method to the class.

    This function takes Python code as input, validates its syntax,
    compiles it, and adds the resulting function as a method to the class.

    Args:
        cls: The class to which the method should be added.
        code: The Python code to compile into a function.

    Raises:
        SyntaxError: If the input code is not valid Python syntax.
    """

    @staticmethod
    def generate(
        cls: Type[Any], code: str, database: Optional[AbstractDatabase] = None
    ) -> None:
        cls.is_generative = True  # type: ignore
        local_vars: Dict[str, Any] = {}

        code = remove_prepended(code)
        code = textwrap.dedent(code)

        if not is_valid_syntax(code):
            raise SyntaxError("Invalid syntax")

        func_name = extract_func_name(code)

        if database:
            try:
                capability = {
                    "function_name": func_name,
                    "generated_code": code,
                    "args": {},
                    "kwargs": {},
                }
                database.add(capability)
            except Exception as e:
                raise DatabaseException(
                    "An error occurred while adding to the database"
                ) from e

        byte_code = compile(code, filename=func_name, mode="exec")
        exec(byte_code, {}, local_vars)
        setattr(cls, func_name, local_vars[func_name])
