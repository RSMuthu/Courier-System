"""
This module provides few simple decorative utils for the CLI
"""


def red(txt: str) -> str:
    """
    Changes input string to red color

    The function appends the ascii code (of needed color)
    to the input

    Args:
        txt (str): input string whose color need to be cyan

    Returns:
        type: str
    """
    return "\033[91m{}\033[0m".format(txt)


def yellow(txt: str) -> str:
    """
    Changes input string to yellow color

    The function appends the ascii code (of needed color)
    to the input

    Args:
        txt (str): input string whose color need to be cyan

    Returns:
        type: str
    """
    return "\033[93m{}\033[0m".format(txt)


def green(txt: str) -> str:
    """
    Changes input string to green color

    The function appends the ascii code (of needed color)
    to the input

    Args:
        txt (str): input string whose color need to be cyan

    Returns:
        type: str
    """
    return "\033[92m{}\033[0m".format(txt)


def cyan(txt: str) -> str:
    """
    Changes input string to cyan color

    The function appends the ascii code (of needed color)
    to the input

    Args:
        txt (str): input string whose color need to be cyan

    Returns:
        type: str
    """
    return "\033[96m{}\033[0m".format(txt)


# TBD: Add additional styling if needed
