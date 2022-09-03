from enum import Enum

class JSONConfigErrors(Enum):
    """
    Error values for json config validation.
    """

    NO_DICT = "expected dictionary but found something else"
    NO_LIST = "expected list but found something else"
    NO_STR = "expected string but found something else"
    NO_KEY = "missing key"
    INV_KEY = "invalid key"
    INV_FUN = "function name not found"
