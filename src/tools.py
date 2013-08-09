import re


def stripPrefix(text):
    """
    :param text: text to remove the prefix from
    :type text: str

    :return: passed text without the prefix
    :rtype: str

    Strip a prefix (the bots name) from commands
    """
    text = re.sub(r'![Mm]ustikka[Bb]ot (.*)', r'!\1', text)
    return text