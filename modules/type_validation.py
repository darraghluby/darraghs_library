""" type_validation.py module for __init__.py """

# For type hinting
from typing import (
    Any,
    Callable,
    Container,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    NoReturn,
    Optional,
    Reversible,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)


def require_type(value: Any,
                 _type: Optional[type],
                 *types: Optional[type],
                 arg: str = "",
                 func: str = "",
                 error: str = "",
                 accepted: Optional[List] = None,
                 **kwargs) -> None:

    """
    Raises TypeError if type(value) is not a permitted type

    Can be used in functions to verify that an argument (of that function)
    is of the correct type(s), and displays an appropriate error otherwise

    Arguments:
        value (Any): The value whose type is being checked
        types (type): The allowed type(s) (can be 1 or more arguments)

    Optional keyword arguments:
        arg (str): The name of the value / argument
        func (str): The name of the function that the value is in
        error (str): The error to be shown when not of a valid type
        accepted (list): A list of the values that can be accepted
        
    Returns:
        None
        
    Raises:
        If not valid type, or not an acceptable value, the function 
        will raise a TypeError, or a ValueError, respectively

    Example uses:
        require_type(age, int, arg="age", func="age_function()")
        require_type(name, str, None, arg="name", func="print_name()")
    """

    # Remove duplicate types
    types: set = set([_type, *types])

    # Check this function's own arguments (inner use only)
    checkargs: list = kwargs.get("check_own_args", [1, 2, 3, 4, 5])

    if 1 in checkargs:
        require_type(*types, type, None,
                     arg="types",
                     func="require_type()",
                     check_own_args=[2, 3, 4, 5])

    if 2 in checkargs:
        require_type(arg, str,
                     arg="arg",
                     func="require_type()",
                     check_own_args=[3, 4, 5])

    if 3 in checkargs:
        require_type(func, str,
                     arg="arg",
                     func="require_type()",
                     check_own_args=[4, 5])

    if 4 in checkargs:
        require_type(error, str,
                     arg="error",
                     func="require_type()",
                     check_own_args=[5])

    if 5 in checkargs:
        require_type(accepted, list, None, tuple,
                     arg="accepted",
                     func="require_type()",
                     check_own_args=[])

    # None is not considered to be a type, it is it's own type
    checknone = True if None in types else False

    if arg:
        arg = f" '{arg}'"

    if func:
        func = f" to {func}"

    if error == "":
        # If the type is considered to be a regular type, use .__name__
        # but if the type is None, then just use 'None'

        types2 = []
        for t in types:
            if isinstance(t, type):
                types2.append(f"'{t.__name__}'")
            else:
                types2.append(f"'{t}'")

        required_types = ""
        
        if len(types2) == 1:
            required_types = f"{types2[0]}"
        else:
            for index, t in enumerate(types2):
                if index == len(types2) - 1:
                    required_types += f"or {t}"
                elif index == len(types2) - 2:
                    required_types += f"{t} "
                else:
                    required_types += f"{t}, "

        current_type = value.__class__.__name__ if value is not None else None

        error = f"Argument{arg}{func} must be type " \
                f"{required_types}, not '{current_type}'"

    if not isinstance(value, tuple(t for t in types if t is not None)):
        if checknone:
            if value is not None:
                raise TypeError(error)
        else:
            raise TypeError(error)

    if accepted:
        if value not in accepted:
            raise ValueError(f"Argument{arg}{func} not accepted - "
                             f"Value must be in: {accepted}")


if __name__ == "__main__":

    var = 3.4
    require_type(var, int, arg="var")

