import os
import re


def find_basepath():
    if os.path.isfile("main.py"):
        return os.path.join(os.path.curdir, "..")
    if os.path.isfile(os.path.join(os.path.curdir, "src", "main.py")):
        return os.path.curdir
    raise Exception("Can't determine main program location")


def strip_prefix(text):
    """
    :param text: text to remove the prefix from
    :type text: str

    :return: passed text without the prefix
    :rtype: str

    Strip a prefix (the bots name) from commands
    """
    text = re.sub(r'![Mm]ustikka[Bb]ot (.*)', r'!\1', text)
    return text