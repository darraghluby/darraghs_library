"""
'darraghs_library.py'

Darragh's Library is a Python module containing various functions,
classes, etc. It contains bundles of code that can be used repeatedly
in many different programs, and it makes working with Python simpler and
more efficient.
"""

__author__ = "Darragh Luby"
__email__ = "darraghluby@gmail.com"
__version__ = "0.0.1"

# All modules below are in the Python standard library
import time
import random
import os
import re
import sys

from functools import wraps

# For 'install_module()' function (see line 270)
from subprocess import check_call, CalledProcessError

# System call - Activate ANSI codes in terminal
os.system("")  

# Related module              
from modules.type_validation import (
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

# Related modules
from modules.colors_class import colors
from modules.huge_letters_dict import HUGE_LETTERS
    
          
def printf(*arguments,
           showerror: bool = True,
           showexamples: bool = False,
           **kwargs) -> None:
    
    """
    Print colored/decorated text
    
    Optional arguments:
    showerror (bool): Display an error when unmatched tags are detected
    showexamples (bool): Display example of every tag name

    Optional keyword arguments are passed to print()
    
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
            foreground colors, except the prefix for all background colors is "bg"
            e.g. "bgred" or "bgdarkred"
    
    TEXT DECORATION TAG NAMES:
        bold (or b), italic (or i), underlined (or u), reversed (or r)
    
    How to use printf():
    
    Using printf() is the same as if you are using the built-in print() function,
    with all the same keyword arguments.
    
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
    "Auto Rename Tag", which may be useful as it works while using this function
    """
    
    # Get all variables from the "colors" class
    color_vars = {
        f"<{key}>" : value for key, value in
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
            printf(f"<blue>{str(index).zfill(len(str(halfway)))}</blue> -> ", end="")
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
                            f"{errnum}) Opening '{opening}' tag does not have a matching "
                            f"closing '{closing}' tag"
                        )
                    
                    elif closing_count > opening_count:
                        raiseerr = True
                        errors.append(
                            f"{errnum}) Closing '{closing}' tag does not have a matching "
                            f"opening '{opening}' tag"
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
    printf(*args, file=sys.stderr, **kwargs)
    

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
                 arg_name="module_name",
                 func_name="install_module()")
    
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
            sys.executable,
            "-m",
            "pip",
            "install",
            module_name,
        ])
    except CalledProcessError:
        errmsg(f"\nModule: '{module_name}' could not be installed")
    else:
        successmsg(f"\nModule: '{module_name}' installed successfully")


def get_input(msg: str,
              inputtype: type = str,
              required: Optional[Any] = None,
              stopatinput: Optional[Any] = None,
              error: str = "Invalid input") -> Any:
    
    """
    Repeats input prompt until given value can be casted to the correct type
    
    Arguments:
    msg (str): The prompt
    
    Optional arguments:
    inputtype: The required type of the input
    required: The required value of the input, can
              be one of many, i.e. a range, list, etc.
    stopatinput: Stops looping when that input is given
    error: Error message to display when invalid input is given
    
    Example use:
    get_input("Enter a number: ", int, required=range(0, 101))
    """
    
    require_type(msg, str, arg_name="msg", func_name="get_input()")
    require_type(inputtype, type, arg_name="_type", func_name="get_input()")
    require_type(error, str, arg_name="error", func_name="get_input()")
    
    # The following must be the same type as the type of the input
    require_type(stopatinput, inputtype, None,
                 arg_name="stopatinput", func_name="get_input()")

    while True:
        try:
            x = inputtype(input(msg))
        except ValueError:
            errmsg(error)
        else:
            if stopatinput is not None:
                if x == inputtype(stopatinput):
                    break
            if required is not None:
                if isinstance(required, (range, list, tuple, set)):
                    if x in required:
                        break
                    else:
                        if isinstance(required, range):
                            errmsg(f"Value must be between {required[0]} " \
                                   "to {required[-1]}")
                        else:
                            errmsg(f"Value must be in {required}")
                        continue
                else:
                    if x == required:
                        break
                    else:
                        errmsg(error)
                        continue
            else:
                break
            
    return x


def as_price(number: Union[int, float], currency: str = "€") -> str:
    
    """
    Displays an integer or float as a price (price tag & 2 decimal places)
    
    Arguments:
    number (float, int): The number (price) to be displayed
    
    Optional arguments:
    currency: The currency symbol to be shown (e.g. "$")
    
    Example use:
    print(as_price(19.99))
    """
    
    require_type(number, int, float, arg_name="number", func_name="as_price()")
    require_type(currency, str, arg_name="currency", func_name="as_price()")
    
    return f"{currency}{number:.2f}"


def multiline_input(msg: str = "Enter/Paste your content." \
                               "Ctrl-Z (or Ctrl-D) to save.") -> str:
    
    """
    Gets a multi-line input from the user and returns a list
    
    Optional arguments:
    msg (str): The prompt
    
    Example use:
    input_list = multiline_input("Type a paragraph: ")
    """
    
    require_type(msg, str, arg_name="msg", func_name="multiline_input")
    
    print(msg)
    inputs = []
    
    while True:
        try:
            line = input()
        except EOFError:
            break
        inputs.append(line)
        
    return "\n".join(inputs)


def dice_roll(animation: bool = True) -> int:
    
    """
    Simulate rolling a dice
    
    Optional arguments:
    animation (bool): Choose whether the animation should be shown or not
    
    Example use:
    outcome = dice_roll()
    """
    
    require_type(animation, bool,
                 arg_name="animation", func_name="dice_roll()")
    
    if animation:
        dice = ["□", "◇"]
        text = "rolling..."
        for i in range(15):
            print(text[:i] + " "*i, dice[i % 2], end="\r", flush=True)
            time.sleep(0.06)
        else:
            print(text + " "*(i+1), end="")
            
    print(r := random.randint(1, 6))
    time.sleep(0.05)
    
    return r
    

def read_csv(file_name: str, delimiter: str = ",",
             encoding: str = "utf-8") -> List:
    
    """
    Read & split each line in a csv file
    
    Arguments:
    file_name (str): The name of the file to be read
    
    Optional arguments:
    delimiter (str): The separator of the csv file
    encoding (str): Specify an encoding for the open() function
    
    Example use:
    csv_lines = read_csv("example.csv")
    """
    
    require_type(file_name, str, arg_name="file_name", func_name="read_csv()")
    require_type(delimiter, str, arg_name="delimiter", func_name="read_csv()")
    require_type(encoding, str, arg_name="encoding", func_name="read_csv()")
    
    try:
        with open(file_name, "r", encoding=encoding) as file:
            lines = file.read().split("\n")
            contents = [line.split(delimiter) for line in lines]
            
    except FileNotFoundError:
        raise FileNotFoundError(f"\n\nFile '{file_name}' not found")
    
    return contents
        
        
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
        Returns a random word from the list
        
        Example use:
        random_word = Lorem.word()
        """
        
        return random.choice(cls.WORDS)

    @classmethod
    def sentence(cls) -> str:
        """
        Returns a formatted sentence with (8 to 20) words
        with punctuation marks, capitalised letters, etc.

        Example use: random_sentence = lorem.sentence()'
        """
        
        sentence_len = random.randint(8, 20)
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
        Returns a paragraph with (4 to 7) sentences
        
        Example use:
        random_paragraph = lorem.paragraph()
        """
        
        para_len = random.randint(4, 7)
        
        return " ".join(cls.sentence() for _ in range(para_len))

    @classmethod
    def text(cls) -> str:
        """
        Returns a block of (3 to 5) paragraphs
        
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
        Also used for gettuple() / getset() functions
        
        Optional arguments:
        length: Specify a length for the list

        Example use:
        random_word_list = lorem.getlist()
        """
        
        list_len = random.randint(10, 20)
        
        # Used for require_type() function below (inner use only)
        function_name = kwargs.get("function_name", "lorem.getlist()")

        require_type(length, int, None,
                     arg_name="length",
                     func_name=function_name)
        
        if length is not None:
            if length > 0:
                list_len = length
            
        return [cls.word() for _ in range(list_len)]

    @classmethod
    def gettuple(cls, *args, **kwargs) -> Tuple:
        """
        Returns a tuple of length (10 to 20)
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
        Returns a set of length (10 to 20)
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
    
    require_type(num, int, arg_name="num", func_name="int_to_roman()")
    
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
    
    require_type(num, str, arg_name="num", func_name="roman_to_int()")
    
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


def file_exists(file_name: str, encoding: str = "utf-8") -> bool:
    
    """
    Returns True if the file exists, otherwise False

    Arguments:
    file_name (str): The name of the file
    
    Optional arguments:
    encoding (str): The encoding for the open() function
    
    Example use:
    print(file_exists("example.csv"))
    """
    
    require_type(file_name, str,
                 arg_name="file_name", func_name="file_exists()")
    require_type(encoding, str,
                 arg_name="encoding", func_name="file_exists()")
    
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
        This uses built in python functions, so you can customize
        the position yourself, e.g. "position = rjust(20)"
        
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
    
    require_type(blinker, bool, arg_name="blink", func_name="countdown()")
    
    # 'position' kwarg - specify where to position the countdown on the console
    position = kwargs.get("position", "default").lower()

    if position != "default":
        position = position.split("(")
        position_type = position[0]
        try:
            position_value = int(position[1][:-1])
        except ValueError:
            raise ValueError(f"Invalid value for '{position_type}()' " \
                             "in 'position' keyword argument to countdown()")

    else:
        position_type = position

    if position_type not in ["ljust", "rjust", "center", "default"]:
        raise ValueError("Invalid 'position' keyword argument to countdown()")
    
    # 'display' kwarg - specify how the countdown should be displayed
    hrsep, minsep, secsep = {
        "default": [":", ":", ""],
        "words": ["hours", "minutes", "seconds"],
        "letters": ["h", "m", "s"],
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
            raise ValueError("countdown() takes min. 1 " \
                             "argument, but none were given")
        elif length > 3:
            raise ValueError("countdown() takes max. 3 arguments " \
                             "but {length} were given")
    
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


def huge_text(text: str, spacegap: int = 3) -> str:
    """
    Returns string with large characters, where each large
    character is 6 characters tall, i.e. 6 rows
    The six rows make up the letter when separated by a newline
    
    Only a few characters are supported, mainly alphanumeric & some symbols,
    as well as whitespace
    [a-z], [A-Z], [0-9], [ !"$%()-+=/.,<>'#:;[]?]
    
    Inspiration: "https://fsymbols.com/generators/tarty/"
    
    Arguments:
    text (str): The text to be transformed
    
    Optional arguments:
    spacegap (int): The gap (width) of 1 space
    
    Example use:
    print(huge_text("hello world"))
    """
    
    require_type(text, str, arg_name="text", func_name="huge_text()")
    require_type(spacegap, int, arg_name="spacegap", func_name="huge_text()")
    
    text = text.lower()
    
    chars = HUGE_LETTERS
    chars[" "] = [" " * spacegap] * 6
    
    not_supported = [f"'{char}'" for char in text if char not in chars.keys()]
    
    if not_supported:
        raise ValueError(f"\n\nCharacter(s): {', '.join(not_supported)} " \
                         "not supported in huge_text() function")
    
    return "\n".join(
        ["".join([chars[char][index] for char in text]) for index in range(6)]
    )      

class StringMethods(str):

    """
    StringMethods class

    A class inheriting from the built in python 'str' class,
    but with extended methods for string analysis, password checking etc.
    
    Initializing StringMethods class:
    
    Example:
    string = StringMethods("Hello world")
    """

    def __init__(self, string: str):

        """
        StringMethods class constructor

        Arguments:
        string (str): The string

        See help(type(self)) for accurate signature.
        """
        
        # Initialize inherited class
        super().__init__()
        
        self.string = str(string)
        self.length = len(self)
        self.chars = [i for i in self]
        self.digits = "".join(i for i in self if i in "0123456789")
        
        self.alphalower = "".join(i for i in self if i.islower())
        self.alphaupper = "".join(i for i in self if i.isupper())
        
        self.alpha = "".join(
            i for i in self if i in self.alphalower + self.alphaupper
        )
        
        self.alphanum = "".join(
            i for i in self if i in self.alpha + self.digits
        )
        
        self.symbols = "".join(i for i in self if i not in self.alphanum)
        self.binary = " ".join(format(ord(char), "b") for char in self)
        
    def shuffle(self) -> "StringMethods":
        """ 
        Shuffles the string in a random order and returns a new string

        Example use:
        print(string.shuffle())
        """
        
        return StringMethods("".join(random.sample(self, self.length)))
    
    def contains(self, char: str, casesensitive: bool = True) -> bool:
        """ 
        Returns True if given char is in the string,
        otherwise returns False

        Arguments:
        char (str): Character to be checked

        Optional arguments:
        casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
        print(string.contains("h", casesensitive=False))
        """
        
        require_type(casesensitive, bool,
                     arg_name="casesensitive",
                     func_name="StringMethods.contains()")
        
        if not casesensitive:
            return str(char).lower() in self.lower()
        return str(char) in self

    def containsany(self, chars: Iterable, casesensitive: bool = True) -> bool:
        """ 
        Returns True if any given chars are in the string,
        otherwise returns False

        Arguments:
        chars (str): Characters to be checked (must be iterable)

        Optional arguments:
        casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
        print(string.containsany("hwokdbe", casesensitive=False))
        """
        
        require_type(casesensitive, bool,
                     arg_name="casesensitive",
                     func_name="StringMethods.containsany()")
        
        for char in chars:
            if casesensitive:
                if str(char) in self:
                    return True
            else:
                if str(char).lower() in self.lower():
                    return True
        return False

    def hasdigit(self) -> bool: 
        """ 
        Returns True if string has any digits [0-9]
        
        Example use:
        print(string.hasdigit())
        """
        return (self.containsany("0123456789"))
    
    def haslower(self) -> bool: 
        """ 
        Returns True if string has any lowercase letters [a-z] 
        
        Example use:
        print(string.haslower())
        """

        return (self.containsany("abcdefghijklmnopqrstuvwxyz"))
    
    def hasupper(self) -> bool: 
        """ 
        Returns True if string has any uppercase letters [A-Z] 
        
        Example use:
        print(string.hasupper())
        """
        
        return (self.containsany("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    
    def hassymbol(self) -> bool:
        """ 
        Returns True if string has any symbols
        [Everything but digits or lowercase / uppercase letters]
        
        Example:
        print(string.hassymbol())
        """

        return (True if len(self.symbols) > 0 else False)
    
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
        
        if re.match(pattern, self):
            return True
        
        return False
    
    def isyes(self) -> bool:
        """ 
        Checks if string appears to be a positive response
        Mainly intended for input validation

        Example use:
        print(string.isyes())
        """
        
        if self.lower() in (
            "yes ye y sure mhm absolutely affirmative "
            "positive true certainly yas yup yip ok okay "
            "o.k. okie yeah yah aye alright indeed uh-huh "
            "yis sey"
        ).split(" "):
            return True
        
        return False
    
    def removechar(self, char: str, casesensitive: bool = True) -> "StringMethods":
        """ 
        Remove all instances of specified character from string 
        
        Arguments:
        char (str): Character to remove

        Optional arguments:
        casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
        print(string.removechar("w"))
        """
        
        char = str(char)

        if casesensitive:
            return StringMethods("".join(i for i in self if i != char))
        else:
            return StringMethods(
                "".join(i for i in self if i.lower() != char.lower())
            )
        
    def removechars(self, chars: Iterable, casesensitive: bool = True) -> "StringMethods":
        """
        Remove all instances of specified characters from string 
        
        Arguments:
        chars (list, string, ...): Characters to remove (must be iterable)

        Optional arguments:
        casesensitive (bool): Specify if uppercase and lowercase matters

        Example use:
        print(string.removechars("wol"))
        """

        chars = [str(char) for char in chars]

        if casesensitive:
            return StringMethods("".join(i for i in self if i not in chars))
        else:
            return StringMethods(
                "".join(i for i in self if i.lower() not in 
                [j.lower() for j in chars])
            ) 
    
    def reverse(self) -> "StringMethods":
        """ 
        Reverses a string 
        
        Example use:
        print(string.reverse())
        """
        
        return StringMethods(self[::-1])
    
    def up(self, amt: int = 1) -> "StringMethods":
        """ 
        Adds newlines to bottom of string 
        
        Optional arguments:
        amt (int): Amount of newlines to be added

        Example use:
        print(string.up(3))
        """
        
        require_type(amt, int, arg_name="amt", func_name="StringMethods.up()")
        
        return StringMethods(self + ("\n" * amt))
    
    def down(self, amt: int = 1) -> "StringMethods":
        """ 
        Adds newlines to top of string 
        
        Optional arguments:
        amt (int): Amount of newlines to be added

        Example use:
        print(string.down(3))
        """
        
        require_type(amt, int,
                     arg_name="amt",
                     func_name="StringMethods.down()")
        
        return StringMethods(("\n" * amt) + self)
    
    def updown(self, amt: int = 1) -> "StringMethods":
        """ 
        Adds newlines to top & bottom of string 
        
        Optional arguments:
        amt (int): Amount of newlines to be added

        Example use:
        print(string.updown(3))
        """
        
        require_type(amt, int,
                     arg_name="amt",
                     func_name="StringMethods.updown()")
        
        return StringMethods(("\n" * amt) + self + ("\n" * amt))
    
    def printchars(self, end: str = "\n") -> None:
        """ 
        Prints all characters in the string

        Optional arguments:
        end (str): Specify character at end of string

        Example use:
        string.printchars()
        """
        
        require_type(end, str,
                     arg_name="end",
                     func_name="StringMethods.printchars()")
        
        for index, char in enumerate(self, 1):
            if index == len(self):
                end = "\n"
            print(char, end=end)
            
    def expand(self, spaces: int = 1, fill: str = " ") -> "StringMethods":
        """ 
        Puts specified amt. of spaces between characters 
        
        Optional arguments:
        spaces (int): Amount of spaces between each character
        fill (str): Replace spaces with specified character

        Example use:
        print(string.expand(3))
        """
        
        require_type(spaces, int,
                     arg_name="spaces",
                     func_name="StringMethods.expand()")
        require_type(fill, str,
                     arg_name="fill",
                     func_name="StringMethods.expand()")
        
        return StringMethods("".join(char + (fill * spaces) for char in self))
    
    def printstring(self, *args, **kwargs) -> None:
        """ 
        Prints the string and passes arguments to print function

        Example use:
        string = StringMethods("Hello world")
        string.printstring() # same as print(string)
        """
        
        print(self, *args, **kwargs)
    
    def flush(self,
              timeout: float = 0.06,
              cursor: bool = True,
              **kwargs) -> None:

        """
        Prints each characters in the string one after another
        in a smooth animation

        Optional arguments:
        timeout (float): Time in seconds to wait after printing last character
        cursor (bool) Display a cursor bar as if somebody is manually typing
        
        Optional keyword arguments:
        pauseatchars (list): Wait for pausetimeout at these chars (see below)
        pausetimeout (float, int): Time in seconds to wait at each pause

        Example use:
        string = StringMethods("Hello everyone, my name is Steve")
        string.flush()
        """
        
        # To avoid 'Dangerous default value [] as argument' warning
        pauseatchars: List = kwargs.get("pauseatchars", [])
        pausetimeout: Union[int, float] = kwargs.get("pausetimeout", 0.01)
        
        require_type(timeout, float, int,
                     arg_name="timeout",
                     func_name="StringMethods.flush()")
        require_type(cursor, bool,
                     arg_name="cursor",
                     func_name="StringMethods.flush()")
        require_type(pauseatchars, list,
                     arg_name="pauseatchar",
                     func_name="StringMethods.flush()")
        require_type(pausetimeout, float, int,
                     arg_name="pausetimeout",
                     func_name="StringMethods.flush()")
        
        cursor_bar = " "
        if cursor:
            cursor_bar = "|"
        
        for index in range(len(self)):
            
            if index in pauseatchars:
                if pauseatchars:
                    print(self[:index], end="\r")
                    time.sleep(pausetimeout)
                
            print(self[:index], end=f"{cursor_bar}\r", flush=True)
            time.sleep(timeout)
            
        print(self, end=f"{cursor_bar}\r")
        
        if cursor:
            time.sleep(0.25)
            print(self, end=" \n")
            time.sleep(0.25)
        
    def __sub__(self, n: int) -> "StringMethods":
        """
        Takes n characters from the end of the string

        Arguments:
        n (int): Number of characters

        Example use:
        string -= 1
        """
        
        return StringMethods("".join(self[:-n]))
    
    def huge(self) -> "StringMethods":
        """ 
        Impliments the huge_text() function

        Example use:
        print(string.huge())
        """
        
        return StringMethods(huge_text(self))
    
    def splitevery(self, n: int) -> List:
        """ 
        Splits a string every n characters 

        Arguments:
        n (int): Number of characters

        Example use:
        print(string.splitevery(2))
        """
        
        require_type(n, int, arg_name="n", func_name="StringMethods.sep()")
        
        return re.findall(("." * n) + "?", self)

    """
    Here, I am adjusting methods from the 'str' class which
    would normally return type 'str'.
    
    I changed each one to correctly return type 'StringMethods' instead,
    so the instance's type is not changed after using one of these methods.
    
    All other methods from the 'str' class return a different type,
    such as str.count(), which returns type 'int', or str.isupper(),
    which return type 'bool', so I don't need to change the return type for them.
    """
    
    # Return type of all methods below -> "StringMethods"
    def capitalize(self, *args): return (
        StringMethods(super().capitalize(*args))
    )

    def expandtabs(self, *args): return (
        StringMethods(super().expandtabs(*args))
    )
    def format_map(self, *args): return (
        StringMethods(super().format_map(*args))
    )

    def removeprefix(self, *args): return (
        StringMethods(super().removeprefix(*args))
    )
    def removesuffix(self, *args): return (
        StringMethods(super().removesuffix(*args))
    )
    
    def __getitem__(self, *args): return (
        StringMethods(super().__getitem__(*args))
    )

    def __format__(self, format_spec: str) -> str:
        
        string = str(self)

        # Hide (like a password)
        if "hide" in format_spec.lower():
            string = "•" * len(string)
            format_spec = format_spec.replace("hide", "")

        # Reverse
        if "rev" in format_spec.lower():
            string = string[::-1]
            format_spec = format_spec.replace("rev", "")
        
        # Variable name
        if "name" in format_spec.lower():
            string = f"{string=}".split("=")[0]
            format_spec = format_spec.replace("name", "")
        
        if len(format_spec) > 0:
            return StringMethods(string.__format__(format_spec))

        return StringMethods(string)

    def __mod__(self, *args): return StringMethods(super().__mod__(*args))
    def __mul__(self, *args): return StringMethods(super().__mul__(*args))
    def __repr__(self, *args): return StringMethods(super().__repr__(*args))
    def __rmul__(self, *args): return StringMethods(super().__rmul__(*args))
    def join(self, *args): return StringMethods(super().join(*args))
    def ljust(self, *args): return StringMethods(super().ljust(*args))
    def lower(self, *args): return StringMethods(super().lower(*args))
    def lstrip(self, *args): return StringMethods(super().lstrip(*args))
    def replace(self, *args): return StringMethods(super().replace(*args))
    def casefold(self, *args): return StringMethods(super().casefold(*args))
    def center(self, *args): return StringMethods(super().center(*args))
    def rjust(self, *args): return StringMethods(super().rjust(*args))
    def rstrip(self, *args): return StringMethods(super().rstrip(*args))
    def strip(self, *args): return StringMethods(super().strip(*args))
    def swapcase(self, *args): return StringMethods(super().swapcase(*args))
    def title(self, *args): return StringMethods(super().title(*args))
    def translate(self, *args): return StringMethods(super().translate(*args))
    def upper(self, *args): return StringMethods(super().upper(*args))
    def zfill(self, *args): return StringMethods(super().zfill(*args))
    def __add__(self, *args): return StringMethods(super().__add__(*args))


def timethis(func):
    """ 
    @timethis Decorator

    Calculates execution time of any function
    It will print out the result to the screen

    Example use:

    @timethis
    some_calculation(1, 3, 5, 2)
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
    about all the important functions, classes and dunder variables in this library
    """

    print("\nWelcome to the darraghs_library interactive help function. Here are the available "
          "functions, classes, and more information that you may be interested in.\n")

    functions = [i for i in globals() if type(eval(i)).__name__ == "function" if i not in (
        "wraps", "check_call"
    )]
    dundervars = [i for i in globals() if i.startswith("__") and i.endswith("__")]
    classes = ["colors", "Lorem", "StringMethods", "xrange"]

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
        [f"{num:02} {dund}" for num, dund in enumerate(dundervars, func_len + 1)]
        + [""] * (longest - dund_len))

    classes = (
        [f"{num:02} {clss}" for num, clss in enumerate(classes, func_len + dund_len + 1)] 
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
            sep = ""
        )

    try:
        while True:
            
            printf("\n<blue>Type </blue><cyan><i>Exit</i></cyan><blue> or </blue>"
                "<cyan><i>0</i></cyan><blue> to leave interactive help</blue>")
            
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

                        # The program will figure out what you might have meant,
                        # even if you have spelt the name wrong (not 100% accurate)
                        
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
                        errmsg("Please enter a number from " \
                            f"1 to {total} (or 0 to exit)")
                    else:
                        break
            
            if response in ("0", "exit", "quit", "stop", "end", "break"):
                break

            print()

            attr_index = number - 1
            attr = all_attr[attr_index]
        
            name = attr
            value = eval(attr)
            _type = type(value).__name__

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
    
    Example use:
    for_each([1, 2, 3], print, end=" ")
    lst = for_each([4, 5, 6], pow, 3)
    """
    
    returns = []
    
    for i in obj:
        returns.append(func(i, *args, **kwargs))
    
    return tuple(returns)


class xrange:
    
    """
    xrange Class based on the built-in range method, but with added
    abilities and outcomes, which may be useful.
    
    Return object that produces numbers from start (inclusive)
    to stop (exclusive, unless argument inclusive = True), and increases,
    (or decreases) by the given value for step (positive or negative)
    """
    
    def __init__(self, *args, convertint=True, inclusive=False):
        
        """ 
        drange class constructor method 
        
        Positional arguments:
    
            (all can be int or float)
            
            Minimum: 1 argument
            Maximum: 3 arguments
            
            Values depend on position of arguments
            
            1 arg:  drange(stop)
            2 args: drange(start, stop)
            3 args: drange(start, stop, step)
        
        Optional keyword arguments:
            
            convertint (bool): Convert floats with finite integral
                            value to int (default: True)
            inclusive (bool):  Change the final value to the stop value,
                            instead of stop minus step (default: False)
        
        Returns:
            
            drange (iterator): Iterator of the values provided
            
        Example use:
        
            for i in xrange(0, 100, 0.01, inclusive=True):
                print(i, end=", ")
        """
        
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
            raise ValueError(f"drange expected at most 3 positional arguments, got {len(args)}")
        
        else:
            raise ValueError("drange expected 1 positional argument, got 0")
        
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
                raise ValueError("\n\nValues cannot have more than 4 decimal places\n"
                                 "min: 0.0001 or max: -0.0001")
    
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
        return f"xrange({self.first}, {self.end}, {self.step})"

            

if __name__ == "__main__":
    
    helpme()
    
    # TODO: Create menu function
    # TODO: Fix "see line" statements
    # TODO: xrange testing
    # TODO: for_each testing