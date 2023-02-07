""" type_validation.py module for main.py """

# For type hinting
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    Union,
    Tuple,
)


# For checking types in run-time
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
      of said function

    Arguments:
        obj (Any): The object to be checked

    Positional Arguments:
        types (type): The types that are required.
                      (All remaining positional arguments)

    Optional Keyword Arguments:
        arg (str): The name of the argument/variable being validated
        func (str): The name of the function (if any) that the argument is in
        type_errmsg (str): The error message to be shown if the object
                           is of an incorrect type
        accepted (tuple): A tuple containing all values (not types) that the
                          object can be (each value must be any of the types
                          that were previously provided)

    Returns:
        None (may raise TypeError or ValueError)

    Example use:
        x = 5
        require_type(x, int, arg="x")         -> checks if x is int
        require_type(x, int, float, str, arg="x")  -> checks if x is int OR float OR str
    """

    # Arguments to validate in this (require_type()) function
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
        
    arg = "" if arg is None or arg == "" else f"{arg} "
    func = "" if func is None or func == "" else f"to {func} "

    obj_type_name = repr(None) if obj is None else repr(obj.__class__.__name__)

    # Compares type names, instead of comparing directly, to avoid errors
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


def require_types(*args: Tuple[Any, ...],
                  argnames: Optional[Tuple[str]] = None,
                  func: Optional[str] = None) -> None:

    """
    Validate multiple variable types at once and raise appropriate error(s) if the type(s)
    is/are not accepted (instead of separate require_type() calls)
    This function has more limitations than require_type()
    
    - Mainly intended for use inside functions, to verify numerous arguments
      of that function

    Positional Arguments:
        *args (tuple): A tuple containing the object and its required type

    Optional Keyword Arguments:
        argnames (tuple): A tuple containing all of the argument names
                          (relative to the order that the tuple arguments were given in)
        func (str): The name of the function (if any)

    Returns:
        None (may raise TypeError or ValueError)

    Example use:
        x = 5
        y = "hi"
        
        require_types(
            (x, int),
            (y, str),
            argnames=("x", "y")
        )
    """

    require_type(func, str, None, arg="func", func="require_types()")

    arg_names: list = ["" for i in args] if argnames is None else [*argnames]
    func_name: str = "" if func is None else func

    if len(args) != len(arg_names):
        raise ValueError(f"{len(arg_names)} argument names given, expected {len(args)}")

    for arg in args:
        require_type(arg, tuple, arg="args", func="require_types()")
        giventype = arg[1]
        if type(giventype) != type and giventype is not None:
            raise ValueError(f"Each type given must be type 'type' or 'None', "
                             f"not '{giventype.__class__.__name__}'")

    for argname in arg_names:
        if not isinstance(argname, str):
            raise ValueError(f"Each argument name given must be type 'str',"
                             f"not '{type(argname).__name__}'")

    for argname, arg in zip(arg_names, args):
        _types = arg[1:]
        require_type(arg[0], *_types, arg=argname, func=func_name)


if __name__ == "__main__":

    pass
