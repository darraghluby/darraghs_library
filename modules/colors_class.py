""" colors.py module for main.py"""

# Note: ANSI escape codes may not work on some platforms

class colors:

    """
    colors class - create colored/decorated text

    FOREGROUND COLORS:

        Light colors:
            grey (or gray), red, green, yellow, blue, magenta, cyan, white

        Dark colors:
            darkgrey (or darkgray), darkred, darkgreen, darkyellow,
            darkblue, darkmagenta, darkcyan, darkwhite

    BACKGROUND COLORS:

        To apply background colors, the names are the same as the
        foreground colors, except the prefix for all background colors is "bg"
        e.g. "bgred" or "bgdarkred"

    TEXT DECORATION:
        bold (or b), italic (or i), underlined (or u), reversed (or r)

    RESET ALL:
        none, reset

    Example use:
        green_text = colors.green + "This is green" + colors.none
        italic_text = colors.i + "Italic text" + colors.reset
    """

    # FOREGROUND COLORS
    grey = "\033[90m"
    gray = "\033[90m"
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    magenta = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    darkgrey = "\033[30m"
    darkgray = "\033[30m"
    darkred = "\033[31m"
    darkgreen = "\033[32m"
    darkyellow = "\033[33m"
    darkblue = "\033[34m"
    darkmagenta = "\033[35m"
    darkcyan = "\033[36m"
    darkwhite = "\033[37m"

    # BACKGROUND COLORS
    bggrey = "\033[100m"
    bggray = "\033[100m"
    bgred = "\033[101m"
    bggreen = "\033[102m"
    bgyellow = "\033[103m"
    bgblue = "\033[104m"
    bgmagenta = "\033[105m"
    bgcyan = "\033[106m"
    bgwhite = "\033[107m"
    bgdarkgrey = "\033[40m"
    bgdarkgray = "\033[40m"
    bgdarkred = "\033[41m"
    bgdarkgreen = "\033[42m"
    bgdarkyellow = "\033[43m"
    bgdarkblue = "\033[44m"
    bgdarkmagenta = "\033[45m"
    bgdarkcyan = "\033[46m"
    bgdarkwhite = "\033[47m"

    # TEXT DECORATIONS
    bold = "\033[1m"
    b = "\033[1m"
    italic = "\033[3m"
    i = "\033[3m"
    underlined = "\033[4m"
    u = "\033[4m"
    reverse = "\033[7m"
    r = "\033[7m"

    # RESET ALL
    none = "\033[0;0m"
    reset = "\033[0;0m"

