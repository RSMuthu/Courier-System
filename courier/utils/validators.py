"""
This Module provides few validator functions for the Models and user inputs
"""

from pydantic.fields import ModelField
from re import match


def unsigned_int_str(_, string: str) -> bool:
    """
    Check input string is unsigned integer

    Regex match is used to validate if the string is unsigned int.
    This is used with `inquire` for validating user cli input

    Args:
        variable (type): description
        string (str): input string to validate

    Returns:
        bool: True if the input is unsigned integer
    """
    return match("^(\d+)$", string)


def unsigned_float_str(_, string: str) -> bool:
    """
    Check input string is unsigned float

    Regex match is used to validate if the string is unsigned float.
    This is used with `inquire` for validating user cli input

    Args:
        variable (type): description
        string (str): input string to validate

    Returns:
        bool: True if the input is unsigned float
    """
    return match("^(\d+(\.\d+)?)$", string)


def unsigned_model_validate(value: float | int, field: ModelField) -> float | int:
    """
    Check input is valid unsigned int/float

    Args:
        value (float | int): actual input value to be validated
        field (ModelField): This holds the information about the Model field which is validated
    Returns:
        int | float: After validation, same input value is returned

    Raises:
        ValueError: invalid error if the value is not unsigned int/float
    """
    if (isinstance(value, int) or isinstance(value, float)) and value < 0:
        raise ValueError(f"{field.name} Should be an unsigned value")
    return value
