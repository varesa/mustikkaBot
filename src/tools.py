import os
import re


def find_basepath():
    """
    Find the basepath of the bot that has all the data, src, etc. subdirs

    :return: Base directory of the bot
    :rtype: str
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def strip_name(text):
    """
    Strip the bots name from commands

    :param text: text to remove the name from
    :type text: str

    :return: passed text without the name
    :rtype: str
    """
    text = re.sub(r'![Mm]ustikka[Bb]ot (.*)', r'!\1', text)
    return text