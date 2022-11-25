"""
'darraghs_library.py'

Darragh's Library is a Python module containing various functions,
classes, etc. It contains bundles of code that can be used repeatedly
in many different programs, and it makes working with Python simpler and
more efficient.
"""

from __future__ import annotations

__all__ = [
    "Lorem", "StringMethods", "Xrange", "as_price", "colors", "countdown",
    "dice_roll", "errmsg", "file_exists", "for_each", "get_input", "helpme",
    "huge_text", "install_module", "int_to_roman", "menu", "multiline_input",
    "printf", "require_type", "roman_to_int", "successmsg", "timethis",
]

__author__ = "Darragh Luby"
__email__ = "darraghluby@gmail.com"
__version__ = "0.0.1"

# Modules below are in the Python standard library
import os
import random
import re
import time
from subprocess import CalledProcessError, check_call
from sys import executable, stderr
from functools import wraps
from collections import UserString

# Related modules
from modules.colors_class import colors
from modules.huge_letters_dict import HUGE_LETTERS
from modules.type_validation import (  # pylint: disable=unused-import
    require_type,
    Any,
    Callable,
    Container,
    Dict,
    FrozenSet,
    Iterable,
    List,
    NoReturn,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

# System call - Activate ANSI codes in terminal
os.system("")


def printf(*arguments,
           showerror: bool = True,
           showexamples: bool = False,
           **kwargs) -> None:

    """
    Print colored/decorated text

    Optional keyword arguments:
        showerror (bool): Display an error when unmatched tags are detected
        showexamples (bool): Display example of every tag name

    Other keyword arguments are passed to print()

    Below are all the available tag names
    (use printf(showexamples=True) for examples)

    COLOR TAG NAMES:

        FOREGROUND COLORS:

            Light colors:
                grey (or gray), red, green, yellow, blue, magenta, cyan, white

            Dark colors:
                darkgrey (or darkgray), darkred, darkgreen, darkyellow,
                darkblue, darkmagenta, darkcyan, darkwhite

        BACKGROUND COLORS:

            To apply background colors, the tag names are the same as the
            foreground colors, except the prefix for all background colors
            is "bg" e.g. "bgred" or "bgdarkred"

    TEXT DECORATION TAG NAMES:
        bold (or b), italic (or i), underlined (or u), reversed (or r)

    How to use printf():

    Using printf() is the same as if you are using the built-in print()
    function, with all the same keyword arguments.

    To use a tag, you wrap your chosen color or formatting option
    with less-than (<) and greater-than (>) signs. Then, that style
    will be applied to anything following, until you use a closing tag.

    You can think of this like using HTML tags; first use the
    opening tag, then the closing tag (with a "/"), for example:

    printf("<blue>This is blue</blue>")
              ^                  ^
           opening            closing
             tag                tag

    The text inside the tags will be decorated with the style(s) you choose.
    Opening tags that don't have a matching closing tag will not be applied,
    and vise versa.

    If you don't have a closing tag, an error will be raised, unless the
    optional argument is manually set to False.

    Unrecognised tags will be treated as text.

    The <none> tag does not require a closing tag. It will just reset all
    formatting and colors to the default.

    HINT: If you use Visual Studio Code, there is an extension named
    "Auto Rename Tag", which may be useful as it works while using this
    function
    """

    # Get all variables from the "colors" class
    color_vars = {
        f"<{key}>": value for key, value in
        vars(colors).items() if "__" not in key
        and key != "none" and key != "reset"
    }

    # Create a copy
    formatting = color_vars.copy()

    for index, (key, value) in enumerate(color_vars.items()):
        closing_tag = "</" + key[1:]

        # If foreground color
        if index < 18:
            formatting[closing_tag] = "\033[39m"

        # If background color
        elif index >= 18:
            formatting[closing_tag] = "\033[49m"

    # Set the rest of the keys manually
    formatting["</bold>"] = "\033[22m"
    formatting["</b>"] = "\033[22m"

    formatting["</italic>"] = "\033[23m"
    formatting["</i>"] = "\033[23m"

    formatting["</underlined>"] = "\033[24m"
    formatting["</u>"] = "\033[24m"

    formatting["</reverse>"] = "\033[27m"
    formatting["</r>"] = "\033[27m"

    formatting["<none>"] = "\033[0;0m"

    args = list(arguments)

    # The point in the dictionary at which the opening tags end
    halfway = (len(formatting) - 1) // 2

    # Iterable list of all the dictionary keys
    key_list = list(formatting.keys())

    # Show example for each option
    if showexamples:
        printf("<bold>Available tags:\n"
               "---------------</bold>")
        for index, i in enumerate(key_list[:halfway], 1):
            printf(
                f"<blue>{str(index).zfill(len(str(halfway)))}</blue> ->",
                end=""
            )
            print(f"{formatting[i]}{i}{formatting['</' + i[1:]]}")

        return

    try:
        mainerrors = []
        raiseerr = False

        # Repeat for each separate argument given
        for arg in args:

            errors = []
            errnum = 0

            for key in key_list[:halfway]:

                opening = key
                closing = "</" + key[1:]

                opening_count = arg.count(opening)
                closing_count = arg.count(closing)

                if opening_count != closing_count:

                    errnum += 1

                    if opening_count > closing_count:
                        raiseerr = True
                        errors.append(
                            f"{errnum}) Opening '{opening}' tag does "
                            f"not have a matching closing '{closing}' tag"
                        )

                    elif closing_count > opening_count:
                        raiseerr = True
                        errors.append(
                            f"{errnum}) Closing '{closing}' tag does "
                            f"not have a matching opening '{opening}' tag"
                        )

            if raiseerr:
                mainerrors.append(f"\n\nArgument: \"{arg}\"\n\n"
                                  + "\n".join(errors))

        if raiseerr:
            raise ValueError("\n".join(mainerrors))

    except ValueError as errormsg:
        if showerror:
            raise errormsg

    else:

        for index, arg in enumerate(args):
            original_arg = arg

            for key in formatting:
                if key in key_list[:halfway]:
                    if "</" + key[1:] in arg:
                        arg = arg.replace(key, formatting[key])
                elif key in key_list[halfway:]:
                    if "<" + key[2:] in original_arg:
                        arg = arg.replace(key, formatting[key])

            arg = arg.replace("<none>", formatting["<none>"]
                              ).replace("</none>", formatting["<none>"])

            args[index] = arg

    print(*args, **kwargs)


def errmsg(*args, **kwargs) -> None:
    """
    Prints a red error message (to sys.stderr)
    Arguments are passed to printf()

    Example use:
        errmsg("Invalid input, please try again")
    """

    args = tuple(f"{colors.red}{arg}{colors.none}" for arg in args)

    # Attempts to print to sys.stderr, otherwise it just displays as red
    printf(*args, file=stderr, **kwargs)


def successmsg(*args, **kwargs) -> None:
    """
    Prints a green success message
    Arguments are passed to printf()

    Example use:
        successmsg("Downloaded successfully")
    """

    args = tuple(f"{colors.green}{arg}{colors.none}" for arg in args)

    # Displays as green
    printf(*args, **kwargs)


def install_module(module_name: str) -> None:
    """
    Import a python module using pip

    Arguments:
        module_name (str): The name of the module

    Example use:
        install_module("some_module")
    """

    require_type(module_name, str,
                 arg="module_name",
                 func="install_module()")

    # For aesthetics (loading... animation)
    for i in range(2):
        for j in range(4):
            print(f"Attempting installation: '{module_name}'"
                  + ("." * j), end="\r")
            time.sleep(0.4)
        if i != 1:
            print(f"Attempting installation: '{module_name}'", end="   \r")

    print("\n")

    try:
        check_call([
            executable,
            "-m",
            "pip",
            "install",
            module_name,
        ])
    except CalledProcessError:
        errmsg(f"\nModule: '{module_name}' could not be installed")
    else:
        successmsg(f"\nModule: '{module_name}' installed successfully")


def get_input(prompt: str = "",
              inputtype: type = str,
              *,
              accepted: Optional[Any] = None,
              exitinput: Optional[Any] = None,
              showaccepted: bool = False,
              wrongtypemsg: Optional[str] = None,
              unacceptedmsg: Optional[str] = None,
              defaultvalue: Any = None) -> Any:

    """
    Repeats input prompt until an input can be casted to the correct type,
    and (if 'accepted' argument is set) can be accepted;

    Optional arguments:
        prompt (str): The prompt
        inputtype (type): The required type of the input

    Optional keyword arguments:
        accepted (Any): A single value, or a tuple/list/range
                        of values that can be accepted
        defaultvalue (Any): Value to return if exit input is given
        exitinput (str): A single string, or a tuple/list of strings,
                         that when given as an input, exit the loop
                         (returns defaultvalue)
        showaccepted (bool): Shows the acceptable values when an unacceptable
                             value is given
        wrongtypemsg (str): The message to be shown when the input cannot be
                            casted to the correct type ('inputtype')
        unacceptedmsg (str): The message to be shown when the input is casted
                             to the correct type, but is not an accepted value

    Returns:
        specified type (inputtype) (or -1 if exitinput is given)

    Example use:
        number = get_input(
            "Enter a number: ",
            int,
            accepted=range(1, 6),
            exitinput=("exit", "stop", "-1"),
            showaccepted=True,
        )
    """

    require_type(prompt, str, arg="prompt", func="get_input()")
    require_type(inputtype, type, arg="inputtype", func="get_input()")
    require_type(showaccepted, bool, arg="showaccepted", func="get_input()")

    require_type(wrongtypemsg,
                 str,
                 None,
                 arg="wrongtypemsg",
                 func="get_input()")

    require_type(unacceptedmsg,
                 str,
                 None,
                 arg="unacceptedmsg",
                 func="get_input()")

    _type = inputtype()

    require_type(_type, str, int, float, complex, bool, list, tuple,
                 arg="inputtype", func="get_inputs()")

    check_accepted = False
    if accepted is not None:

        if isinstance(accepted, (list, tuple, range, Xrange)):

            accepted = list(accepted)
            for index, i in enumerate(accepted):
                if not isinstance(i, inputtype):

                    if isinstance(i, int) and inputtype is float:
                        accepted[index] = float(i)

                    elif isinstance(i, float) and inputtype is int:
                        accepted[index] = int(i)

                    else:
                        raise TypeError("All values in 'accepted' sequence "
                                        "must be same type as inputtype")

            accepted_list = accepted
            check_accepted = True

        elif isinstance(accepted, int) and inputtype is float:
            accepted_list = [float(accepted)]
            check_accepted = True

        elif isinstance(accepted, float) and inputtype is int:
            accepted_list = [int(accepted)]
            check_accepted = True

        elif isinstance(accepted, inputtype):
            accepted_list = [accepted]
            check_accepted = True

        else:
            raise TypeError("'accepted' value must be same type as inputtype "
                            "or a sequence of values of the same type")

    check_exit = False
    if exitinput is not None:

        if isinstance(exitinput, (list, tuple, range)):
            for i in exitinput:
                if not isinstance(i, str):
                    raise TypeError("All values in 'exitinput' sequence "
                                    "must be type 'str'")

            exitinputs = list(exitinput)
            check_exit = True

        else:
            if isinstance(exitinput, str):
                exitinputs = [exitinput]
            else:
                raise TypeError("'exitinput' value must be type 'str', or "
                                "a sequence of type 'str'")

            check_exit = True

    while True:
        userinput = input(prompt)
        if check_exit:
            if userinput in exitinputs:
                return defaultvalue
        try:
            userinput = inputtype(userinput)
        except ValueError:
            if wrongtypemsg is None:
                errmsg("Invalid input")
            else:
                errmsg(wrongtypemsg)
        else:
            if not check_accepted:
                return userinput

            if userinput in accepted_list:
                return userinput

            if showaccepted:
                errmsg(f"Value must be in list: {accepted_list}")
            else:
                if unacceptedmsg is None:
                    errmsg("Value not accepted")
                else:
                    errmsg(unacceptedmsg)


def as_price(number: Union[int, float], *, currency: str = "€") -> str:

    """
    Displays an integer or float as a price (price tag & 2 decimal places)

    Arguments:
        number (float, int): The number (price) to be displayed

    Optional keyword arguments:
        currency (str): The currency symbol to be shown (e.g. "$")

    Returns:
        new formatted string (str)

    Example use:
        print(as_price(19.99))
    """

    require_type(number, int, float, arg="number", func="as_price()")
    require_type(currency, str, arg="currency", func="as_price()")

    return f"{currency}{number:.2f}"


def multiline_input(msg: str = "Enter/Paste your content."
                               "Ctrl-Z (or Ctrl-D) to save.") -> str:

    """
    Gets a multi-line input from the user and returns a list

    Optional arguments:
        msg (str): The prompt

    Returns:
        users input (str)

    Example use:
    input_list = multiline_input("Type a paragraph: ")
    """

    require_type(msg, str, arg="msg", func="multiline_input")

    print(msg)
    inputs = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        inputs.append(line)

    return "\n".join(inputs)


def dice_roll(*, animation: bool = True) -> int:

    """
    Simulate rolling a dice

    Optional keyword arguments:
        animation (bool): Choose whether the animation should be shown or not

    Returns:
        The random number 1-6 (int)

    Example use:
        outcome = dice_roll()
    """

    require_type(animation, bool,
                 arg="animation", func="dice_roll()")

    if animation:
        dice = ["□", "◇"]
        text = "rolling..."
        for i in range(15):
            print(text[:i] + " "*i, dice[i % 2], end="\r", flush=True)
            time.sleep(0.06)

        print(text + " "*(i+1), end="")

    print(r := random.randint(1, 6))
    time.sleep(0.05)

    return r


class Lorem:
    """
    Lorem Ipsum Generator - Generate random dummy text.

    My take on the various types of "Lipsum" generators used to get dummy text.
    Inspiration / External Links:

    [1]: https://www.lipsum.com/
    [2]: https://loremipsum.io/
    [3]: https://en.wikipedia.org/wiki/Lorem_ipsum
    """

    WORDS = [
        "a", "ac", "accumsan", "ad", "adipiscing", "aenean", "aliquam",
        "amet", "ante", "aptent", "arcu", "at", "auctor", "augue", "bibendum",
        "class", "commodo", "condimentum", "congue", "consectetur",
        "conubia", "convallis", "cras", "cubilia", "curabitur", "curae",
        "dapibus", "diam", "dictum", "dictumst", "dignissim", "dis", "dolor",
        "dui", "duis", "efficitur", "egestas", "eget", "eleifend",
        "elit", "enim", "erat", "eros", "est", "et", "etiam", "eu", "euismod",
        "facilisi", "facilisis", "fames", "faucibus", "felis", "fermentum",
        "finibus", "fringilla", "fusce", "gravida", "habitant", "habitasse",
        "hendrerit", "himenaeos", "iaculis", "id", "imperdiet", "in",
        "integer", "interdum", "ipsum", "justo", "lacinia", "lacus",
        "lectus", "leo", "libero", "ligula", "litora", "lobortis", "lorem",
        "maecenas", "magna", "magnis", "malesuada", "massa", "mattis",
        "maximus", "metus", "mi", "molestie", "mollis", "montes", "morbi",
        "nam", "nascetur", "natoque", "nec", "neque", "netus", "nibh", "nisi",
        "non", "nostra", "nulla", "nullam", "nunc", "odio", "orci", "ornare",
        "pellentesque", "penatibus", "per", "pharetra", "phasellus",
        "platea", "porta", "porttitor", "posuere", "potenti", "praesent",
        "primis", "proin", "pulvinar", "purus", "quam", "quis", "quisque",
        "ridiculus", "risus", "rutrum", "sagittis", "sapien", "scelerisque",
        "sem", "semper", "senectus", "sit", "sociosqu", "sodales",
        "suscipit", "suspendisse", "taciti", "tellus", "tempor", "tempus",
        "torquent", "tortor", "tristique", "turpis", "ullamcorper",
        "ultricies", "urna", "ut", "varius", "vehicula", "vel", "velit",
    ]

    @classmethod
    def word(cls) -> str:
        """
        Returns a random word from the list (str)

        Example use:
            random_word = Lorem.word()
        """

        return random.choice(cls.WORDS)

    @classmethod
    def sentence(cls, *, words: Optional[int] = None) -> str:
        """
        Returns a formatted sentence with (8 to 20) words
        with punctuation marks, capitalised letters, etc. (str)

        Optional keyword arguments:
            words (int): Specify a length for the sentence

        Example use:
            random_sentence = lorem.sentence()'
        """

        require_type(words,
                     int,
                     None,
                     arg="words",
                     func="Lorem.sentence()")

        if words is None:
            sentence_len = random.randint(8, 20)
        else:
            sentence_len = words

        _sentence = [cls.word() for _ in range(sentence_len)]

        punc_marks = [
            random.choice([",", ",", ",", " -", ";", "'", "\""])
            for _ in range(random.randint(0, (sentence_len // 5)))
        ]

        for p in punc_marks:

            random_index = random.randint(1, sentence_len - 2)

            if p in ["'", "\""]:
                _sentence[random_index] = p + _sentence[random_index] + p
            else:
                _sentence[random_index] = _sentence[random_index] + p

        _sentence[0] = _sentence[0].capitalize()
        _sentence[-1] += random.choice(
            [".", ".", ".", ".", ".", ".", ".", "?", "!"]
        )

        return " ".join(_sentence)

    @classmethod
    def paragraph(cls) -> str:
        """
        Returns a paragraph with (4 to 7) sentences (str)

        Example use:
            random_paragraph = lorem.paragraph()
        """

        para_len = random.randint(4, 7)

        return " ".join(cls.sentence() for _ in range(para_len))

    @classmethod
    def text(cls) -> str:
        """
        Returns a block of (3 to 5) paragraphs (str)

        Example use:
            random_text = lorem.text()
        """

        text_len = random.randint(3, 5)

        return "\n\n".join(
            cls.paragraph() for _ in range(text_len)
        )

    @classmethod
    def getlist(cls, length: Optional[int] = None, **kwargs) -> List:
        """
        Returns a list of length (10 to 20)
        Also used for gettuple() / getset() functions (list)

        Optional arguments:
            length (int): Specify a length for the list

        Example use:
            random_word_list = lorem.getlist()
        """

        list_len = random.randint(10, 20)

        # Used for require_type() function below (inner use only)
        function_name = kwargs.get("function_name", "lorem.getlist()")

        require_type(length, int, None,
                     arg="length",
                     func=function_name)

        if length is not None:
            if length > 0:
                list_len = length

        return [cls.word() for _ in range(list_len)]

    @classmethod
    def gettuple(cls, *args, **kwargs) -> Tuple:
        """
        Returns a tuple of length (10 to 20) (tuple)
        Arguments are passed to getlist() method

        Example use:
            new_tuple = Lorem.gettuple()
        """

        return tuple(
            cls.getlist(*args, function_name="lorem.gettuple()", **kwargs)
        )

    @classmethod
    def getset(cls, *args, **kwargs) -> Set:
        """
        Returns a set of length (10 to 20) (set)
        Arguments are passed to getlist() method

        Example use:
            new_set = Lorem.getset()
        """

        return set(
            cls.getlist(*args, function_name="lorem.getset()", **kwargs)
        )


_ROMAN_NUMERALS = {
    "I": 1,
    "IV": 4,
    "V": 5,
    "IX": 9,
    "X": 10,
    "XL": 40,
    "L": 50,
    "XC": 90,
    "C": 100,
    "CD": 400,
    "D": 500,
    "CM": 900,
    "M": 1000,
    "MV̅": 4000,
    "V̅": 5000,
    "MX̅": 9000,
    "X̅": 10000,
}


def int_to_roman(num: int) -> str:

    """
    Convert a regular integer (int) to a roman numeral (str)

    Arguments:
        num (int): The integer to be converted to roman number

    Example use:
        roman_number = int_to_roman(999)
    """

    require_type(num, int, arg="num", func="int_to_roman()")

    # Lists are in descending order - highest to lowest value
    # Keys are in SYMBOLS, values are in NUMBERS

    symbols = [*_ROMAN_NUMERALS.keys()][::-1]
    numbers = [*_ROMAN_NUMERALS.values()][::-1]

    roman_num = ""

    for number, symbol in zip(numbers, symbols):
        amount = num // number
        num %= number
        roman_num += symbol * amount

    return roman_num


def roman_to_int(num: str) -> int:

    """
    Convert a roman numeral (str) to an integer (int)

    Arguments:
        num (int): The roman number to be converted to an integer

    Example use:
        int_number = roman_to_int("CMXCIX")
    """

    require_type(num, str, arg="num", func="roman_to_int()")

    symbols = [*_ROMAN_NUMERALS.keys()][::-1]
    numbers = [*_ROMAN_NUMERALS.values()][::-1]

    # Sort the symbol list by putting symbols of len(2) at start
    symbols2 = list(sorted(symbols, key=len)[::-1])
    # Sort the number list in the same order
    numbers2 = [numbers[symbols.index(i)] for i in symbols2]

    int_num = 0

    for number, symbol in zip(numbers2, symbols2):
        int_num += number * num.count(symbol)
        num = num.replace(symbol, "")

    return int_num


def file_exists(file_name: str, *, encoding: str = "utf-8") -> bool:

    """
    Returns True if the file exists, otherwise False (bool)

    Arguments:
        file_name (str): The name of the file

    Optional keyword arguments:
        encoding (str): The encoding for the open() function

    Example use:
        print(file_exists("example.csv"))
    """

    require_type(file_name, str,
                 arg="file_name", func="file_exists()")
    require_type(encoding, str,
                 arg="encoding", func="file_exists()")

    try:
        with open(file_name, "r", encoding=encoding):
            return True
    except FileNotFoundError:
        return False


def countdown(*args, **kwargs) -> None:

    """
    Counts down from a given time (hrs, mins, secs) and displays the timer

    Positional arguments:
        (float or int)

         Argument positions represent different values
         based on amount of args given:

         1 arg)  countdown(1) -> 1 second
         2 args) countdown(2, 1) -> 2 minutes, 1 second
         3 args) countdown(3, 2, 1) -> 3 hours, 2 minutes, 1 second

    Optional keyword arguments:
        position (str):
            Specify where to position the countdown on the screen
            This uses built in python string methods, so you can customize
            the position yourself, e.g. "position = 'rjust(20)'"
            Note: You must pass the method as a string

            Available positions:
            ljust(x), rjust(x), center(x), default,
            where x is the total width

        display (str):

            Customize how the countdown is displayed

            Available displays:
            default, words, letters

        blink (bool): Choose whether to display a blinking arrow or not

    Example uses:
        countdown(10) [10 seconds]
        countdown(2, 30) [2 minutes, 30 seconds]
        countdown(8, 1, 32) [8 hours, 1 minute, 32 seconds]
    """

    blinker = kwargs.get("blink", False)

    require_type(blinker, bool, arg="blink", func="countdown()")

    # 'position' kwarg - specify where to position the countdown on the console
    position = kwargs.get("position", "default").lower()

    if position != "default":
        position = position.split("(")
        position_type = position[0]
        try:
            position_value = int(position[1][:-1])
        except ValueError:
            raise ValueError(f"Invalid value for '{position_type}()' "
                             "in 'position' keyword argument to countdown()")

    else:
        position_type = position

    if position_type not in ["ljust", "rjust", "center", "default"]:
        raise ValueError("Invalid 'position' keyword argument to countdown()")

    # 'display' kwarg - specify how the countdown should be displayed
    hrsep, minsep, secsep = {
        "default": [":", ":", ""],
        "words": [" hours ", " minutes ", " seconds "],
        "letters": ["h ", "m ", "s "],
    }.get(
        kwargs.get("display", "default"),
        [":", ":", ""]
    )

    blinking_list = ["-> ", "   "]

    # args
    length = len(args)
    seconds = minutes = hours = 0

    # Argument positions represent different values
    # based on amount of args given:
    # -> countdown(1, 2, 3) -> 1 hour, 2 minutes, 3 seconds
    # -> countdown(2, 3) -> 2 minutes, 3 seconds
    # -> countdown(3) -> 3 seconds

    if length == 3:
        hours, minutes, seconds = args
    elif length == 2:
        minutes, seconds = args
    elif length == 1:
        seconds = args[0]

    else:
        if length == 0:
            raise ValueError("countdown() takes min. 1 "
                             "argument, but none were given")
        elif length > 3:
            raise ValueError("countdown() takes max. 3 arguments "
                             f"but {length} were given")

    for i in args:
        if not isinstance(i, (float, int)):
            raise ValueError("All arguments to countdown() "
                             "must be type 'float' or 'int'")

    if hours > 24:
        raise ValueError("Maximum quantity for 'hours' argument is 24")

    total_seconds = seconds + (minutes * 60) + (hours * 60 * 60)
    if total_seconds > 86400:
        raise ValueError("Max. countdown time is 24 hours")
    elif total_seconds < 0:
        raise ValueError("Min. countdown time is 0 seconds")

    # Correct all possible arguments
    hours = (total_seconds // 60 // 60)
    minutes = (total_seconds // 60) - (hours * 60)
    seconds = total_seconds - (minutes * 60) - (hours * 60 * 60)

    for count in range(total_seconds, -1, -1):

        if blinker:
            print(blinking_list[count % 2], end="")

        print_str = f"{str(hours).zfill(2)}{hrsep}" \
                    f"{str(minutes).zfill(2)}{minsep}" \
                    f"{str(seconds).zfill(2)}{secsep}"

        if position_type == "ljust":
            print(print_str.ljust(position_value), end="\r")
        elif position_type == "rjust":
            print(print_str.rjust(position_value), end="\r")
        elif position_type == "center":
            print(print_str.center(position_value), end="\r")
        else:
            print(print_str, end="\r")

        if count > 0:
            time.sleep(1)

        seconds -= 1

        if seconds == -1:

            if minutes != 0:
                minutes -= 1
                seconds = 59
            else:
                if hours != 0:
                    hours -= 1
                    minutes = 59
                    seconds = 59

    print()


def huge_text(text: str, *, spacegap: int = 3) -> str:
    """
    Returns string with large characters, where each large
    character is 6 characters tall, i.e. 6 rows
    The six rows make up the letter when separated by a newline

    Only a few characters are supported, mainly alphanumeric & some symbols,
    as well as whitespace:
    [a-z], [A-Z], [0-9], [any from "!"$%()-+=/.,<>'#:;[]?"]

    Inspiration: "https://fsymbols.com/generators/tarty/"

    Arguments:
        text (str): The text to be transformed

    Optional keyword arguments:
        spacegap (int): The gap (width) of 1 space

    Returns:
        large string (str)

    Example use:
        print(huge_text("hello world"))
    """

    require_type(text, str, arg="text", func="huge_text()")
    require_type(spacegap, int, arg="spacegap", func="huge_text()")

    text = text.lower()

    chars = HUGE_LETTERS
    chars[" "] = [" " * spacegap] * 6

    not_supported = [f"'{char}'" for char in text if char not in chars.keys()]

    if not_supported:
        raise ValueError(f"\n\nCharacter(s): {', '.join(not_supported)} "
                         "not supported in huge_text() function")

    return "\n".join(
        ["".join([chars[char][index] for char in text]) for index in range(6)]
    )


class StringMethods(UserString):

    """
    StringMethods class

    A class inheriting from the UserString class from the collections
    module. This class has extended methods for string analysis, password
    checking etc., and also has the ability to create mutable strings,
    with all the same methods as regular strings.

    Initializing StringMethods class:
        string = StringMethods("Hello world")

    Note:
    You can make the string mutable if you wish, simply use the keyword
    argument "mutable" when initializing the object, for example:
    string = StringMethods("Hello world", mutable=True)

    However, by doing this, the way you use some methods will change
    (see StringMethods.__init__ doc for more information)

    Inspiration:
    Link [1]: https://www.geeksforgeeks.org/collections-userstring-in-python/
    """

    def __init__(self, seq: str, *, inplace: bool = False) -> None:
        """
        StringMethods class constructor

        Arguments:
            string (str): The string

        Optional keyword arguments:
            inplace (bool): Choose whether to make the string mutable -
                            This will modify the string in place (returns None)

        Note:
        If you make the string mutable by using the inplace keyword argument,
        method behaviour is altered.

        Instead of the following example (a regular, immutable string):
            string = string.shuffle() -> Returns new value

        It would be (a mutable string):
            string.shuffle() -> This will change the value in place

        This would be the case with all methods that return a string;
        Other methods, such as .contains() (which returns a boolean value),
        will still work as normal.
        """

        require_type(inplace,
                     bool,
                     arg="inplace",
                     func="StringMethods.__init__()")

        # Initialize inherited class
        super().__init__(seq)

        # Check if user activated inplace / mutable string
        self.mutable = inplace

        # Instance variables
        self.length = self.len = len(self.data)
        self.charlist = [i for i in self.data]
        self.charset = set(i for i in self.data)
        self.digits = "".join(i for i in self.data if i in "0123456789")
        self.alphalower = "".join(i for i in self.data if i.islower())
        self.alphaupper = "".join(i for i in self.data if i.isupper())
        self.alpha = "".join(
            i for i in self.data if i in self.alphalower + self.alphaupper
        )
        self.alphanum = "".join(
            i for i in self.data if i in self.alpha + self.digits
        )
        self.other = "".join(i for i in self.data if i not in self.alphanum)
        self.binary = " ".join(format(ord(char), "b") for char in self.data)

    def setmutable(self) -> None:
        """
        Manually sets the string to a mutable string

        Example use:
            string.setmutable()

        See StringMethods.__init__.__doc__ for more info.
        """

        self.mutable = True

    def _mutable_check(self, new: str) -> Optional[str]:
        """
        Checks if user has enabled mutable string during initialization
        [Intended for internal use only]

        Arguments:
            new (str): The new version of "self.data" to be set or returned
        """

        if self.mutable:
            self.data = new

            # If mutable, initalized variables must be updated
            StringMethods.__init__(self, self.data, inplace=True)
            return None

        return new

    # ---------------- Bool Returns ----------------

    def contains(self, char: str, *, casesensitive: bool = True) -> bool:
        """
        Returns True if given char is in the string,
        otherwise returns False

        Arguments:
            char (str): Character to be checked

        Optional keyword arguments:
            casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
            print(string.contains("h", casesensitive=False))
        """

        require_type(char,
                     str,
                     arg="char",
                     func="StringMethods.contains()")
        require_type(casesensitive,
                     bool,
                     arg="casesensitive",
                     func="StringMethods.contains()")

        if not casesensitive:
            return char.lower() in self.data.lower()
        return str(char) in self.data

    def containsany(self,
                    chars: Iterable[str],
                    *,
                    casesensitive: bool = True) -> bool:
        """
        Returns True if any given chars are in the string,
        otherwise returns False

        Arguments:
            chars (list, str, ...): Characters to be checked (must be iterable)

        Optional keyword arguments:
            casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
            print(string.containsany("hwokdbe", casesensitive=False))
        """

        require_type(casesensitive,
                     bool,
                     arg="casesensitive",
                     func="StringMethods.containsany()")

        for char in chars:
            if casesensitive:
                if str(char) in self.data:
                    return True
            else:
                if str(char).lower() in self.data.lower():
                    return True
        return False

    def hasdigit(self) -> bool:
        """
        Returns True if string has any digits [0-9]

        Example use:
            print(string.hasdigit())
        """

        return bool(self.digits)

    def haslower(self) -> bool:
        """
        Returns True if string has any lowercase letters [a-z]

        Example use:
            print(string.haslower())
        """

        return bool(self.alphalower)

    def hasupper(self) -> bool:
        """
        Returns True if string has any uppercase letters [A-Z]

        Example use:
            print(string.hasupper())
        """

        return bool(self.alphaupper)

    def hassymbol(self) -> bool:
        """
        Returns True if string has any symbols
        [Everything but alphanumeric characters]

        Example:
            print(string.hassymbol())
        """

        return bool(self.other)

    def haswhitespace(self) -> bool:
        """
        Returns True if string has whitespace

        Example use:
            print(string.haswhitespace())
        """

        return self.contains(" ")

    def isemail(self) -> bool:
        """
        Checks if string appears to be a valid email address

        Example use:
            print(string.isemail())
        """

        pattern = re.compile(r"\"?([-a-zA-Z\d.`?{}]+@\w+\.\w+)\"?")

        if re.match(pattern, self.data):
            return True

        return False

    def isyes(self) -> bool:
        """
        Checks if string appears to be a positive response
        (Mainly intended for input validation)

        Example use:
            print(string.isyes())
        """

        if self.data.lower() in (
            "yes ye y sure mhm absolutely affirmative "
            "positive true certainly yas yup yip ok okay "
            "o.k. okie yeah yah aye alright indeed uh-huh "
            "yis sey ya ys yus yez yess k yaz yups "
        ).split(" "):
            return True

        return False

    # ---------------- String Returns ----------------

    def only(self, chars: Iterable[str], *, casesensitive: bool = True) -> Optional[str]:
        """
        Returns a new string with only these characters

        Arguments:
            chars (list, str, ...): Characters to accept

        Optional keyword arguments:
            casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
            print(string.only("abc"))
        """

        require_type(casesensitive,
                     bool,
                     arg="casesensitive",
                     func="StringMethods.containsany()")

        if not casesensitive:
            chars = "".join(i.lower() for i in chars)
            return self._mutable_check(
                "".join(i for i in self.data if i.lower() in chars)
            )

        return self._mutable_check(
            "".join(i for i in self.data if i in chars)
        )

    def shuffle(self) -> Optional[str]:
        """
        Shuffles the string in a random order and returns a new string

        Example use:
            print(string.shuffle())
        """

        return self._mutable_check(
            "".join(random.sample(self.data, self.length))
        )

    def removechars(self,
                    chars: Iterable[str],
                    *,
                    casesensitive: bool = True) -> Optional[str]:
        """
        Remove all instances of specified characters from string

        Arguments:
            chars (list, str, ...): Characters to remove (must be iterable)

        Optional keyword arguments:
            casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
            print(string.removechars("a"))
            print(string.removechars(["a", "b", "c"])
        """

        require_type(casesensitive,
                     bool,
                     arg="casesensitive",
                     func="StringMethods.removechars()")

        chars = set(str(char) for char in chars)

        if casesensitive:
            return self._mutable_check(
                "".join(i for i in self.data if i not in chars))
        else:
            return self._mutable_check(
                "".join(i for i in self.data if i.lower()
                        not in [j.lower() for j in chars])
            )

    def reverse(self) -> Optional[str]:
        """
        Reverses a string

        Example use:
            print(string.reverse())
        """

        return self._mutable_check(self.data[::-1])

    def up(self, amt: int = 1) -> Optional[str]:
        """
        Adds newlines to bottom of string (moving it "up")

        Optional arguments:
            amt (int): Amount of newlines to be added

        Example use:
            print(string.up(3))
        """

        require_type(amt, int, arg="amt", func="StringMethods.up()")

        return self._mutable_check(self.data + ("\n" * amt))

    def down(self, amt: int = 1) -> Optional[str]:
        """
        Adds newlines to top of string (moving it "down")

        Optional arguments:
            amt (int): Amount of newlines to be added

        Example use:
            print(string.down(3))
        """

        require_type(amt,
                     int,
                     arg="amt",
                     func="StringMethods.down()")

        return self._mutable_check(("\n" * amt) + self.data)

    def updown(self, amt: int = 1) -> Optional[str]:
        """
        Adds newlines to top & bottom of string (moving it "up" & "down")

        Optional arguments:
            amt (int): Amount of newlines to be added

        Example use:
            print(string.updown(3))
        """

        require_type(amt,
                     int,
                     arg="amt",
                     func="StringMethods.updown()")

        return self._mutable_check(("\n" * amt) + self.data + ("\n" * amt))

    def expand(self, spaces: int = 1, *, fill: str = " ") -> Optional[str]:
        """
        Puts specified amt. of spaces between characters

        Optional arguments:
            spaces (int): Amount of spaces between each character

        Optional keyword arguments:
            fill (str): Replace spaces with specified character

        Example use:
            print(string.expand(3, fill="-"))
        """

        require_type(spaces,
                     int,
                     arg="spaces",
                     func="StringMethods.expand()")
        require_type(fill,
                     str,
                     arg="fill",
                     func="StringMethods.expand()")

        return self._mutable_check(
            "".join(char + (fill * spaces) for char in self.data))

    def __sub__(self, n: int) -> "StringMethods":
        """
        Takes n characters from the end of the string

        Arguments:
            n (int): Number of characters

        Example use:
            string -= 1
        """

        require_type(n, int, arg="n", func="__sub__")

        # self._mutable_check is not required here
        # "string - 1" as a statement by itself doesn't really make sense
        # "string -= 1" is better

        # __sub__ Not implimented in collections.UserString, and returns the
        # incorrect value, so return StringMethods type manually

        # Compensate for mutable strings
        if self.mutable:
            return StringMethods("".join(self.data[:-n]), inplace=True)
        return StringMethods("".join(self.data[:-n]))

    def __format__(self, format_spec: str) -> str:

        """
        Return a formatted version of the string as described by
        format_spec; Added format specifiers as well as the built-in ones

        Arguments:
            format_spec (str): The format specifier

        Example use:
            print(f"{string:hide}")

        New format specifiers:
            1) "hide": Hides the string (as a password; bulletpoints)
            2) "rev": Reverses the string
        """

        string = self.data

        # Hide (like a password)
        if "hide" in format_spec.lower():
            string = "•" * len(string)
            format_spec = format_spec.replace("hide", "")

        # Reverse
        if "rev" in format_spec.lower():
            string = string[::-1]
            format_spec = format_spec.replace("rev", "")

        # __format__ must return str, not None, so self._mutable_check
        # is not required here

        if len(format_spec) > 0:
            return string.__format__(format_spec)

        return string

    # ---------------- None Returns ----------------

    def flush(self,
              *,
              timeout: float = 0.06,
              cursor: bool = True,
              **kwargs) -> None:

        """
        Prints each characters in the string one after another,
        in a smooth animation

        Optional keyword arguments:
            timeout (float): Time in seconds to wait after printing
                             last character
            cursor (bool) Display a cursor bar (like a typewriter)
            pauseatchars (list): Wait for pausetimeout at these chars
            pausetimeout (float, int): Time in seconds to wait at each pause

        Example use:
            string = StringMethods("Hello everyone, my name is Steve")
            string.flush()
        """

        # To avoid 'Dangerous default value [] as argument' warning
        pauseatchars: List = kwargs.get("pauseatchars", [])

        pausetimeout: Union[int, float] = kwargs.get("pausetimeout", 0.01)

        require_type(timeout, float, int,
                     arg="timeout",
                     func="StringMethods.flush()")
        require_type(cursor, bool,
                     arg="cursor",
                     func="StringMethods.flush()")
        require_type(pauseatchars, list,
                     arg="pauseatchar",
                     func="StringMethods.flush()")
        require_type(pausetimeout, float, int,
                     arg="pausetimeout",
                     func="StringMethods.flush()")

        cursor_bar = " "
        if cursor:
            cursor_bar = "|"

        for index in range(self.len):

            if index in pauseatchars:
                if pauseatchars:
                    print(self.data[:index], end="\r")
                    time.sleep(pausetimeout)

            print(self.data[:index], end=f"{cursor_bar}\r", flush=True)
            time.sleep(timeout)

        print(f"{self.data} \r", end="")

    def printchars(self, end: str = "\n") -> None:
        """
        Prints all characters in the string (separately)

        Optional arguments:
            end (str): Specify character at end of string

        Example use:
            string.printchars()
        """

        require_type(end,
                     str,
                     arg="end",
                     func="StringMethods.printchars()")

        for index, char in enumerate(self.data, 1):
            if index == self.len:
                end = "\n"
            print(char, end=end)

    # ---------------- Other Returns ----------------

    def splitevery(self, n: int) -> Optional[List]:
        """
        Splits a string every n characters

        Arguments:
            n (int): Number of characters

        Example use:
            print(string.splitevery(2))
        """

        require_type(n,
                     int,
                     arg="n",
                     func="StringMethods.splitevery()")

        # Returns a list, cannot change type if mutable
        # self._mutable_check not required here
        return re.findall(("." * n) + "?", self.data)

    # Methods below from the str class have already been adjusted in the
    # collections.UserString class, however, I am adjusting them again here
    # in order to carry out the correct operation based on whether the string
    # is mutable or not

    # Return type of all methods below -> Optional[str]
    def capitalize(self, *args): return self._mutable_check(self.data.capitalize(*args))
    def expandtabs(self, *args): return self._mutable_check(self.data.expandtabs(*args))
    def format_map(self, *args): return self._mutable_check(self.data.format_map(*args))
    def translate(self, *args): return self._mutable_check(self.data.translate(*args))
    def swapcase(self, *args): return self._mutable_check(self.data.swapcase(*args))
    def casefold(self, *args): return self._mutable_check(self.data.casefold(*args))
    def replace(self, *args): return self._mutable_check(self.data.replace(*args))
    def join(self, *args): return self._mutable_check(self.data.join(*args))
    def ljust(self, *args): return self._mutable_check(self.data.ljust(*args))
    def lower(self, *args): return self._mutable_check(self.data.lower(*args))
    def lstrip(self, *args): return self._mutable_check(self.data.lstrip(*args))
    def center(self, *args): return self._mutable_check(self.data.center(*args))
    def rjust(self, *args): return self._mutable_check(self.data.rjust(*args))
    def rstrip(self, *args): return self._mutable_check(self.data.rstrip(*args))
    def strip(self, *args): return self._mutable_check(self.data.strip(*args))
    def title(self, *args): return self._mutable_check(self.data.title(*args))
    def upper(self, *args): return self._mutable_check(self.data.upper(*args))
    def zfill(self, *args): return self._mutable_check(self.data.zfill(*args))


def timethis(func):
    """
    @timethis Decorator

    Calculates execution time of any function
    It will print out the result to the screen

    Example use:
        @timethis
        def some_process(...): ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Place all arguments in a list for display
        all_args = [str(arg) for arg in args]
        all_args.extend(f"{key}={val}" for key, val in kwargs.items())

        printf(f"<green>Called function '{func.__name__}'</green>")

        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = f"{time.time() - start_time:.2f}"

        # Join the all_args list with commas & spaces
        printf(f"<green>Function '{func.__name__}({', '.join(all_args)})' "
               f"took {total_time} seconds</green>")
        return result

    return wrapper


def helpme():

    """
    Interactive help module with information, instructions and more
    about all the important functions, classes and dunder variables
    in this library
    """

    print("\nWelcome to the darraghs_library interactive help function. "
          "Here are the available functions, classes, and more information "
          "that you may be interested in.\n")

    functions = [
        key for key, value in globals().items()
        if type(value).__name__ == "function"
        if key not in ("wraps", "check_call")
    ]

    dundervars = [
        key for key in globals() if key.startswith("__")
        and key.endswith("__")
    ]

    classes = ["colors", "Lorem", "StringMethods", "Xrange", "Table"]

    all_attr = functions + dundervars + classes
    all_attr_lower = [i.lower() for i in all_attr]

    func_len = len(functions)
    dund_len = len(dundervars)
    class_len = len(classes)

    longest = max(func_len, dund_len, class_len)
    total = func_len + dund_len + class_len

    functions = (
        [f"{num:02} {func}" for num, func in enumerate(functions, 1)]
        + [""] * (longest - func_len))

    dundervars = (
        [f"{num:02} {dund}" for num, dund in
         enumerate(dundervars, func_len + 1)]
        + [""] * (longest - dund_len))

    classes = (
        [f"{num:02} {clss}" for num, clss in
         enumerate(classes, func_len + dund_len + 1)]
        + [""] * (longest - class_len))

    justify = 25

    longest_func = len(max(functions, key=len))
    longest_dund = len(max(dundervars, key=len))
    longest_clss = len(max(classes, key=len))

    print(
        "Functions".ljust(justify)
        + "Dunder Variables".ljust(justify)
        + "Classes".ljust(justify)
    )

    print(
        ("-" * longest_func).ljust(justify)
        + ("-" * longest_dund).ljust(justify)
        + ("-" * longest_clss).ljust(justify)
    )

    for a, b, c in zip(functions, dundervars, classes):
        print(
            colors.green + a[:2] + colors.none + a[2:].ljust(justify - 2),
            colors.green + b[:2] + colors.none + b[2:].ljust(justify - 2),
            colors.green + c[:2] + colors.none + c[2:].ljust(justify - 2),
            sep=""
        )

    try:
        while True:

            printf(
                "\n<blue>Type 'exit' or '0' to leave interactive help</blue>"
            )

            while True:

                response = input("Enter object name or number: ").lower()

                try:
                    number = int(response)
                except ValueError:

                    if response in ("exit", "quit", "stop", "end", "break"):
                        break

                    if response in all_attr_lower:
                        number = all_attr_lower.index(response) + 1
                        break
                    else:

                        # The program will figure out what you might
                        # have meant, even if you have spelt the name
                        # wrong (not 100% accurate)

                        most_likely = -1
                        likeliness = 0

                        for lst_index, i in enumerate(all_attr_lower):
                            if i.startswith(response):
                                most_likely = lst_index + 1
                                likeliness = len(response)
                                break

                        else:
                            for lst_index, i in enumerate(all_attr_lower):
                                for index in range(len(response)):
                                    if response[:index + 1] in i:
                                        if index + 1 >= likeliness:
                                            most_likely = lst_index + 1
                                            likeliness = index + 1

                        number = most_likely

                        if most_likely == -1 or not response:
                            errmsg("Please enter a valid name or number")
                        else:
                            break
                else:
                    if number not in range(0, total + 1):
                        errmsg("Please enter a number from "
                               f"1 to {total} (or 0 to exit)")
                    else:
                        break

            if response in ("0", "exit", "quit", "stop", "end", "break"):
                break

            print()

            attr_index = number - 1
            attr = all_attr[attr_index]

            name = attr
            value = globals()[attr]
            _type = type(value).__name__

            if _type in ("ABCMeta", "type"):
                _type = "class"

            if attr_index in range(func_len, func_len + dund_len):
                print(f"| Name: {name}")

                value = str(value).splitlines()
                if len(value) == 1:
                    value = "".join(value)
                    print(f"| Value: {value}")
                else:
                    print("| Value: ")
                    for i in value:
                        print(f"| {i}")

            else:
                print(f"| Name: {name}")
                print(f"| Type: {_type}")

                print()
                help(value)

    except KeyboardInterrupt:
        print("\nNow leaving helpme() function")


def for_each(obj: Iterable, func: Callable, *args, **kwargs) -> Any:
    """
    For everything in the given object, do the specified task

    Arguments:
        obj (Iterable): The object to be iterated over
        func (Callable): The function to perform for each item in that object

    Any more arguments or keyword arguments are passed to the given function

    Pass an object & function to this function without the parenthesis,
    and specify any arguments and keyword arguments after.

    Note:
    The print function will print any other arguments before the item

    Example use:
        for_each([1, 2, 3], print, "Number:", end=" ")
        lst = for_each([4, 5, 6], pow, 3)
    """
    if func is print:
        returns = tuple(func(*args, i, **kwargs) for i in obj)
    else:
        returns = tuple(func(i, *args, **kwargs) for i in obj)

    return returns


class Xrange:

    """
    Xrange Class based on the built-in range method, but with added
    abilities and outcomes, which may be useful.

    Return object that produces numbers from start (inclusive)
    to stop (exclusive, unless argument inclusive = True), and increases,
    (or decreases) by the given value for step (positive or negative)
    """

    def __init__(self,
                 *args,
                 convertint: bool = True,
                 inclusive: bool = False) -> None:

        """
        Xrange class constructor method

        Positional arguments:

            (all can be int or float)

            Minimum: 1 argument
            Maximum: 3 arguments

            Values depend on position of arguments

            1 arg:  Xrange(stop)
            2 args: Xrange(start, stop)
            3 args: Xrange(start, stop, step)

        Optional keyword arguments:
            convertint (bool): Convert floats with finite integral
                            value to int (default: True)
            inclusive (bool):  Change the final value to the stop value,
                            instead of stop minus step (default: False)

        Returns:
            Xrange (iterator): Iterator of the values provided

        Example use:
            for i in Xrange(0, 100, 0.01, inclusive=True):
                print(i, end=", ")
        """

        require_type(convertint,
                     bool,
                     arg="convertint",
                     func="Xrange.__init__()")
        require_type(inclusive,
                     bool,
                     arg="inclusive",
                     func="Xrange.__init__()")

        for arg in args:
            argtype = type(arg).__name__
            if not isinstance(arg, (float, int)):
                raise TypeError(
                    f"Arg must be float or int, not {argtype}"
                )

        self.start: Union[int, float] = 0
        self.step: Union[int, float] = 1

        if len(args) == 1:
            self.end, = args

        elif len(args) == 2:
            self.start, self.end = args

        elif len(args) == 3:
            self.start, self.end, self.step = args

        elif len(args) > 3:
            raise ValueError(f"Xrange expected at most 3 "
                             f"positional arguments, got {len(args)}")

        else:
            raise ValueError("Xrange expected 1 positional argument, got 0")

        if not inclusive:
            self.end -= self.step

        self.first = self.start
        self.convertint = convertint

        if self.step == 0:
            raise ValueError("\n\nstep value cannot be 0")

        for i in (self.start, self.end, self.step):
            try:
                len(str(float(i)).split(".")[1])
            except IndexError:
                raise ValueError("\n\nValues cannot have more than 4 "
                                 "decimal places\nmin: 0.0001 or max: -0.0001")

    def __iter__(self):
        return self

    def __next__(self):

        # Stop iteration on these cases:

        # range(1, 10, -1) -> None
        if self.step < 0:
            if self.start < self.end:
                raise StopIteration

        # range(10, 1) -> None
        elif self.step > 0:
            if self.start > self.end:
                raise StopIteration

        if (self.start <= self.end) or (self.start >= self.end):

            previous = self.start

            if isinstance(self.step, int):
                self.start += self.step

            else:
                # For floating point rounding errors
                dec_points_first = len(str(float(self.first)).split(".")[1])
                dec_points_step = len(str(float(self.step)).split(".")[1])

                roundto = max(dec_points_first, dec_points_step)

                self.start += self.step
                self.start = round(self.start, roundto)

            if self.convertint:
                if float(previous).is_integer():
                    return int(previous)

            return previous

        raise StopIteration

    def __repr__(self):
        return f"Xrange({self.first}, {self.end}, {self.step})"


def menu(*args,
         spacing: int = 2,
         verticalspacing: int = 1,
         title: Optional[str] = " Menu ",
         label: bool = False,
         border: str = "default",
         position: str = "left",
         newline: bool = True,
         ) -> None:

    """
    Print out a nice menu with this function, with lots of customisation

    Arguments:
        Positional arguments will be printed out as an "option" in the menu

    Optional keyword arguments:
        spacing (int): The spaces on the left & right of the menu
        verticalspacing (int): The spaces on the top & bottom of the menu
        title (str): The name of the menu (displays at the top)
        label (bool): Choose to display menu option numbers
        border (str): The style of border you would like
                      border options:
                      default, clean, bold, wiggle, double
        position (str): Choose where to position the menu options
                        position options:
                        left, right, center
        newline (bool): Add a newline after printing the menu

    If you want to pass a collection (list, tuple, dict, set, etc.) into
    this function, use the built-in unpacking operator (*) before the argument

    Example use:
        lst = ["option 1", "option 2", "option 3"]
        menu(lst)
    """

    if len(args) < 1:
        raise ValueError("menu() expected 1 argument, got none")

    require_type(verticalspacing,
                 int,
                 arg="verticalspacing",
                 func="menu()")
    require_type(spacing, int, arg="spacing", func="menu()")
    require_type(title, str, None, arg="title", func="menu()")
    require_type(label, bool, arg="label", func="menu()")
    require_type(border, str, arg="border", func="menu()")
    require_type(position, str, arg="position", func="menu()")

    title = "" if title is None else title

    position = {
        "left": "ljust",
        "right": "rjust",
        "center": "center",
    }.get(position, "ljust")

    chosen = {
        "bold": 0,
        "clean": 1,
        "default": 2,
        "wiggle": 3,
        "double": 4,
    }.get(border, 1)

    horizontal = ["━", "─", "-", "~", "═"]
    vertical = ["┃", "│", "¦", "¦", "║"]
    topright = ["┓", "┐", "+", "~", "╗"]
    topleft = ["┏", "┌", "+", "~", "╔"]
    bottomright = ["┛", "┘", "+", "~", "╝"]
    bottomleft = ["┗", "└", "+", "~", "╚"]

    if label:
        args = tuple(
            f"{str(number).zfill(len(str(len(args))))}" + ") "
            + str(arg) for number, arg in enumerate(args, 1)
        )
    else:
        args = tuple(str(arg) for arg in args)

    minlen = len(max(args, key=len))

    def printverticalspaces() -> None:
        for _ in range(verticalspacing):
            print(
                vertical[chosen]
                + (" " * spacing)
                + (" " * minlen)
                + (" " * spacing)
                + vertical[chosen]
            )

    print(
        topleft[chosen]
        + f"{title}".center(minlen + spacing*2, horizontal[chosen])
        + topright[chosen]
    )

    printverticalspaces()

    for i in args:

        print(
            vertical[chosen]
            + (spacing * " ")
            + eval(f"'{i}'.{position}({minlen})")
            + (spacing * " ")
            + vertical[chosen]
        )

    printverticalspaces()

    print(
        bottomleft[chosen]
        + horizontal[chosen] * (minlen + spacing * 2)
        + bottomright[chosen]
    )

    if newline:
        print()


class Table:

    def __init__(self,
                 rownum: int,
                 colnum: int,
                 *,
                 align: str = "left",
                 justify: int = 15,
                 index: bool = False,
                 indexheader: str = "",
                 headernewline: str = "\n"):

        require_type(rownum, int, arg="rownum", func="Table.__init__()")
        require_type(colnum, int, arg="colnum", func="Table.__init__()")
        require_type(align, str, arg="colnum", func="Table.__init__()", accepted=("left", "right", "center", "centre"))
        require_type(justify, int, arg="justify", func="Table.__init__()")
        require_type(index, bool, arg="index", func="Table.__init__()")
        require_type(indexheader, str, arg="indexheader", func="Table.__init__()")
        require_type(headernewline, str, arg="headernewline", func="Table.__init__()")

        if rownum < 1:
            raise ValueError("Number of rows must be greater than 0")
        if colnum < 1:
            raise ValueError("Number of columns must be greater than 0")

        self.rownum = rownum
        self.colnum = colnum
        self.justify = justify
        self.align = align.lower()
        self.index = index
        self.indexheader = indexheader
        self.headernewline = headernewline

        self.__headers: List[List[Any]] = [None] * self.colnum
        self.__rows: List[List[Any]] = [[None] * self.colnum for i in range(self.rownum)]

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value: list):

        require_type(value, list, arg="value", func="rows")

        for i in value:
            if not isinstance(i, list) or len(i) != self.colnum:
                raise ValueError(f"Rows must be a list of length {self.rownum} containing lists of length {self.colnum}")

        if len(value) != self.rownum:
            raise ValueError(f"Rows must be a list of length {self.rownum} containing lists of length {self.colnum}")

        self.__rows = value

    @rows.deleter
    def rows(self):
        self.__rows = [[None] * self.colnum for i in range(self.rownum)]

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value: List[Any]):

        require_type(value, list, arg="value", func="headers")

        if len(value) != self.colnum:
            raise ValueError(f"Headers must be a list with {self.colnum} values")

        self.__headers = value

    @headers.deleter
    def headers(self):
        self.__headers = [None] * 6

    def get(self, row: int, col: int):
        require_type(row, int, arg="row", func="Table.getitem()")
        require_type(col, int, arg="col", func="Table.getitem()")

        try:
            returnval = self.rows[row][col]
        except IndexError:
            return None

        return returnval

    def alignitem(self, item: Any) -> str:

        """
        Aligns an item as specified by self.align
        and self.justify
        """

        if self.align == "left":
            return str(item).ljust(self.justify)

        elif self.align == "right":
            return str(item).rjust(self.justify)

        return str(item).center(self.justify)

    def __setitem__(self, key: int, value: list):

        require_type(key, int, arg="key", func="Table.__setitem__")
        require_type(value, list, arg="value", func="Table.__setitem__")

        if len(value) != self.colnum:
            raise ValueError(f"New value must contain {self.colnum} values")

        if len(self.__rows) - 1 < key:
            raise ValueError(f"Index out of range -> Key must be between 0 to {self.rownum - 1}")

        self.__rows[key] = value

    def __getitem__(self, key: int):

        require_type(key, int, arg="key", func="Table.__setitem__")

        if len(self.__rows) - 1 < key:
            raise ValueError(f"Index out of range -> Key must be between 0 to {self.rownum - 1}")

        return self.__rows[key]

    def __str__(self) -> str:

        _rows = self.__rows

        s = ""
        if self.__headers != [None] * self.colnum:
            s += "".join(self.alignitem(col) for col in self.__headers) + self.headernewline
            if self.index:
                s = self.alignitem(self.indexheader) + s

        if self.index:
            for i in range(self.rownum):
                _rows[i].insert(0, i)

        s += "\n".join(
            "".join(self.alignitem(col) for col in row) for row in _rows
        )

        return s

    def __repr__(self) -> str:
        return f"Table(rownum={self.rownum}, colnum={self.colnum}, align={self.align}, justify={self.justify})"


def as_word(num: Union[float, int], *, zero: bool = True) -> str:
    """
    Converts a word to its English word representation
    
    Arguments:
        num (int): Number to be converted
    
    Example use:
        print(as_word(123.5)) -> "one hundred twenty-three point five"
        print(as_word(3523)) -> "three thousand five hundred twenty-three"
        
    Note:
    Highest number = 10^100 (1 Googol)
    """
    
    require_type(num, float, int, arg="num", func="as_word()")
    require_type(zero, bool, arg="zero", func="as_word()", accepted=(True,))
    
    # Intended for inner use only
    if num == 0 and zero:
        return "zero"

    def formatstr(string: str) -> str:
        """
        Removes any extra spaces in given string
        and replaces with a single space
        
        Arguments:
            string (str): The string to format
        """
        
        return " ".join(string.split())
    
    numstr = str(num)
    numlen = len(numstr)
    
    # Digits & irregular numbers
    numdict = {
        0: "",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "fourty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }
    
    if num == 10**100:
        return "one googol"
    
    if num > 10**100:
        raise ValueError("Number is too large -> Max: 10^100")
    
    if num < 0:
        return formatstr("negative " + as_word(abs(num), zero=False))
    
    if "." in numstr:
        
        first, second = numstr.split(".")
        
        decimal = " point " + " ".join([as_word(int(i), zero=False) for i in second])
        
        # Common decimal place names
        if int(second) == 125: decimal = " and one eight"
        elif int(second) == 25: decimal = " and one quarter"
        elif int(second) == 33: decimal = " and one third"
        elif int(second) == 16: decimal = " and one sixth"
        elif int(second) == 75: decimal = " and three quarters"
        elif int(second) == 66: decimal = " and two thirds"
        elif int(second) == 11: decimal = " and one ninth"
        elif int(second) == 14: decimal = " and one seventh"
        elif int(second) == 1: decimal = " and one tenth"
        elif int(second) == 2: decimal = " and one fifth"
        elif int(second) == 3: decimal = " and three tenths"
        elif int(second) == 4: decimal = " and two fifths"
        elif int(second) == 5: decimal = " and a half"
        elif int(second) == 6: decimal = " and three fifths"
        elif int(second) == 7: decimal = " and seven tenths"
        elif int(second) == 8: decimal = " and four fifths"
        elif int(second) == 9: decimal = " and nine tenths"
            
        return formatstr(as_word(int(first), zero=False) + decimal)
    
    if num in numdict and num != 0:
        return formatstr(numdict[int(num)])
    
    if numlen == 2:
        return formatstr(numdict[int(numstr[0] + "0")] + "-" + numdict[int(numstr[1])])

    if numlen < 4 and num != 0:
        return formatstr(as_word(int(numstr[0]), zero=False)) + " hundred " + as_word(int(numstr[1:]), zero=False)
    
    names = [
        "thousand", "million", "billion", "trillion", "quadrillion",
        "quintillion", "sextillion", "septillion", "octillion", "nonillion",
        "decillion", "undecillion", "duodecillion", "tredecillion",
        "quattuordecillion", "quindecillion", "sexdicillion", "septendcillion",
        "octodecillion", "novemdecillion", "vigintillion", "unvigintillion",
        "duovigintillion", "trevigintillion", "quattorvingintillion",
        "quinvintillion", "sexvigintillion", "septenvigintillion", "octovigintillion",
        "novemvigintillion", "trigintillion", "untrigintillion", "duotrigintillion",
    ]
    
    if numlen in range(4, 100_000, 3):
        name = names[(numlen // 3) - 1]
        return formatstr(as_word(int(numstr[0]), zero=False) + f" {name} " + as_word(int(numstr[1:]), zero=False))
    
    if numlen in range(5, 100_000, 3):
        name = names[(numlen // 3) - 1]
        return formatstr(as_word(int(numstr[0:2]), zero=False) + f" {name} " + as_word(int(numstr[2:]), zero=False))
    
    if numlen in range(6, 100_000, 3):
        name = names[(numlen // 3) - 2]
        return formatstr(as_word(int(numstr[0:3]), zero=False) + f" {name} " + as_word(int(numstr[3:]), zero=False))
    
    return ""

if __name__ == "__main__":
    
    pass

    # TODO: Xrange testing
    # TODO: for_each testing
    # TODO: Fix countdown
