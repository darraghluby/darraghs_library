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


def require_type(obj: Any,
                 type_: Optional[type],
                 *types: Optional[type],
                 arg: Optional[str] = None,
                 func: Optional[str] = None,
                 type_errmsg: Optional[str] = None,
                 accepted: Optional[Tuple[Any, ...]] = None,
                 ) -> None:

    """
    Validate variable types and raise appropriate errors if the type
    is not accepted

    - Mainly intended for use inside functions, to verify arguments
      of that function

    Arguments:
        obj (Any): The object to be checked

    Positional Arguments:
        types (type): Any types that the object must be (at least one of)
                     (These are all the remaining positional arguments)

    Optional Keyword Arguments:
        arg (str): The name of the argument/variable
        func (str): The name of the function (if any)
        type_errmsg (str): The error message to be shown if the object
                           is an incorrect type
        accepted (tuple): A tuple containing all values (not types) that the
                          object can be (each value must be any of the types
                          that werepreviously provided)

    Returns:
        None or NoReturn (may raise TypeError or ValueError

    Example use:
        x = 5
        require_type(x, int, arg="x")         -> checks if x is int
        require_type(x, int, float, arg="x")  -> checks if x is int OR float
    """

    # Arguments to check in this function (no recursion)
    arguments = [
        (arg, str, repr("arg")),
        (func, str, repr("func")),
        (type_errmsg, str, repr("type_errmsg")),
        (accepted, tuple, repr("accepted")),
    ]

    # Loop through arguments list to verify types
    for a, a_type, a_name in arguments:
        if a is not None:
            if not isinstance(a, a_type):
                raise TypeError(
                    f"Argument {a_name} to require_type() must be type "
                    f"'{a_type.__name__}' or None, "
                    f"not '{a.__class__.__name__}'"
                )

    # Remove duplicate types
    types_set: set = {type_, *types}

    # Ensure each type given is a valid type (or None)
    for t in types_set:
        if t is not None:
            if not isinstance(t, type):
                raise TypeError(
                    f"Each positional type argument to require_type() must be "
                    f"type 'type' or None, not '{t.__class__.__name__}'"
                )

    # Represent type names (e.g. str) as "'str'" instead of "'<class 'str'>'"
    types: list = [
        repr(None) if t is None else repr(t.__name__)
        for t in types_set
    ]

    # Format message appropriately, based on the amount of types
    if len(types) > 1:
        types_string = ", ".join(types[:-1]) + f" or {types[-1]}"
    else:
        types_string = ", ".join(types)

    arg = "" if arg is None else f"{arg} "
    func = "" if func is None else f"to {func} "

    obj_type_name = repr(None) if obj is None else repr(obj.__class__.__name__)

    # Compares type names, instead of comparing directly
    if obj_type_name not in types:
        if type_errmsg is None:
            type_errmsg = (
                f"Argument {arg}{func}must be type "
                f"{types_string}, not {obj_type_name}"
            )
        raise TypeError(type_errmsg)

    # Check if value can be accepted
    if accepted is not None:

        accepted = tuple(set(accepted))

        for value in accepted:

            # Ensure all 'accepted' values are the same type(s) that
            # was/were provided

            if value is None:
                value_type_name = repr(None)
            elif value is not None:
                value_type_name = repr(value.__class__.__name__)

            if value_type_name not in types:
                raise TypeError(
                    f"All accepted values must be type {types_string}, "
                    f"not {value_type_name}"
                )

            if len(accepted) >= 10:
                accepted_values_string = f"in list:\n{accepted}"
            else:
                accepted_values: List[str] = [
                    f"'{str(i)}' ({i.__class__.__name__})" for i in accepted
                ]
                
                if len(accepted_values) > 1:
                    accepted_values_string = (
                        ", ".join(accepted_values[:-1])
                        + f" or {accepted_values[-1]}"
                    )
                else:
                    accepted_values_string = ", ".join(accepted_values)

            if obj is not None:

                if obj not in accepted:
                    raise ValueError(
                        f"Argument {arg}{func}value must be "
                        f"{accepted_values_string}, not '{obj}'"
                    )


if __name__ == "__main__":

    var = 3.4
    try:
        require_type(var, int, arg="var")
    except TypeError as err:
        print(err)
