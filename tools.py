import re

def stripPrefix(text):
    text = re.sub(r'![Mm]ustikka[Bb]ot (.*)', r'!\1', text)
    return text