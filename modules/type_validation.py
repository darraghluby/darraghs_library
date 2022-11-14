""" type_validation.py module for darraghs_library.py """

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
                 *types: type | None,
                 arg_name: str = "",
                 func_name: str = "",
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
    
    Optional arguments:
    arg_name (str): The name of the value / argument
    func_name (str): The name of the function that the value is in
    error (str): The error to be shown when not of a valid type
    accepted (list): A list of the values that can be accepted
    
    Example uses:
    require_type(age, int, arg_name="age", func_name="age_function()")
    require_type(name, str, None, arg_name="name", func_name="print_name()")
    """
    
    # Remove duplicate types
    types: set = set([*types])
    
    # Check this function's own arguments (inner use only)
    checkargs: list = kwargs.get("check_own_args", [1, 2, 3, 4, 5])
    
    if 1 in checkargs:
        require_type(*types, type, None,
                     arg_name="types",
                     func_name="require_type()",
                     check_own_args=[2, 3, 4, 5])
        
    if 2 in checkargs:
        require_type(arg_name, str,
                     arg_name="arg_name",
                     func_name="require_type()",
                     check_own_args=[3, 4, 5])
    
    if 3 in checkargs:
        require_type(func_name, str,
                     arg_name="arg_name",
                     func_name="require_type()",
                     check_own_args=[4, 5])
    
    if 4 in checkargs:
        require_type(error, str,
                     arg_name="error",
                     func_name="require_type()",
                     check_own_args=[5])
    
    if 5 in checkargs:
        require_type(accepted, list, None,
                     arg_name="accepted",
                     func_name="require_type()",
                     check_own_args=[])
                     
    
    # None is not considered to be a type, it is it's own type
    checknone = True if None in types else False
    
    if arg_name:
        arg_name = f" '{arg_name}'"
        
    if func_name:
        func_name = f" to {func_name} function"
     
    if error == "":
        # If the type is considered to be a regular type, use .__name__
        # but if the type is None, then just use 'None'
        
        types2 = []
        for t in types:
            if isinstance(t, type):
                types2.append(f"'{t.__name__}'")
            else:
                types2.append(f"{t}")
        
        required_types = ' or '.join(types2)
        current_type = value.__class__.__name__ if value is not None else None

        error = f"Argument{arg_name}{func_name} must be type " \
                f"{required_types}, not '{current_type}'"
    
    if not isinstance(value, tuple(t for t in types if t is not None)):
        if checknone:
            if value is not None:
                raise TypeError(error)
        else:
            raise TypeError(error)
    
    if accepted:
        if value not in accepted:
            raise ValueError("Argument value not accepted - "
                             f"Value must be in list: {accepted}")