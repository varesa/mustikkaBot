import re

from logging import d


class eventlistener:
    messageRegistered = []
    specialRegistered = []

    def registerMessage(self, module):
        self.messageRegistered.append(module)

    def registerSpecial(self, module):
        self.specialRegistered.append(module)

    def handleMessage(self, text):
        result = re.search(":(.*?)!.* PRIVMSG (.*?) :(.*)", text)

        user = None
        msg = None

        if result is not None:
            user = result.group(1)
            msg = result.group(3)
        else:
            d("Invalid message: " + text)
            return  # Invalid message

        for module in self.messageRegistered:
            module.handleMessage(text, user, msg)

    def handleSpecial(self, text):
        for module in self.specialRegistered:
            module.handleSpecial(text)
