import re

"""
This function takes a string that represents a function. 
It parses the string to remove any text that occurs above the function header.

Args:
    func_string (str): A string that represents a function.
    end_marker (str): A string that marks the end of the function header.

Returns:
    A string that represents a function, with any text above the function header removed.
"""


def remove_prepended(func_string: str, end_marker="### END FUNCTION ###") -> str:
    func_match = re.search(r"\s*def .+", func_string)
    if func_match:
        func_string = func_string[func_match.start() :]

    end_marker_index = func_string.find(end_marker)
    if end_marker_index != -1:
        func_string = func_string[: end_marker_index + len(end_marker)]

    return func_string


"""
This function takes a string that represents a function. 
It parses the string and returns the function name else raises an error.

Args:
    code (str): A string that represents a function.

Returns:
    A string of the function name.
"""


def extract_func_name(code: str) -> str:
    match = re.search(r"def\s+(\w+)", code)
    if match:
        return match.group(1)
    else:
        raise ValueError("No function definition found in provided code.")


"""
    Convert the provided text into a valid Python function name in snake_case.

    This function performs the following operations:
    1. Strips leading and trailing whitespace.
    2. Converts all characters to lowercase.
    3. Replaces non-alphanumeric characters with underscores.
    4. If the result starts with a digit, prefixes it with an underscore.

    Args:
        text (str): The input string to convert into a valid Python function name.

    Returns:
        str: The input string converted into a valid Python function name in snake_case.
"""


def to_func_name(text: str) -> str:
    # remove leading and trailing whitespace
    text = text.strip()
    # convert to lowercase
    text = text.lower()
    # remove non-alphanumeric characters and replace spaces with underscores
    text = re.sub(r"\W+", " ", text).strip().replace(" ", "_")
    # if it starts with a digit, prefix it with an underscore
    if text[0].isdigit():
        text = "_" + text

    return text
