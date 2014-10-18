#
# Custom exceptions for mustikkabot
#
# Author: Esa Varemo
#


class FatalException(Exception):
    """
    An exception for situations when the bot should not continue (normal behaviour), but halt instead
    """
    pass