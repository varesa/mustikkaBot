import re

from log import log, d


class eventmanager:
    messageRegistered = []
    specialRegistered = []

    def registerMessage(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming messages
        """
        if not module in self.messageRegistered:
            self.messageRegistered.append(module)

    def unregisterMessage(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming messages
        """
        self.messageRegistered.pop(module, default=None)

    def registerSpecial(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming "special" (non message) data
        """
        if not module in self.specialRegistered:
            self.specialRegistered.append(module)

    def unregisterSpecial(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming "special" (non message) data
        """
        self.specialRegistered.pop(module, default=None)

    def handleMessage(self, text):
        """
        :param text: full IRC message to deliver as a text-message
        :type text: str

        Parse the IRC message and deliver it to registered modules
        """
        result = re.search(":(.*?)!.* PRIVMSG (.*?) :(.*)", text)

        user = None
        msg = None

        if result is not None:
            user = result.group(1)
            msg = result.group(3)
        else:
            log("[EVENTLISTENER] Received invalid message")
            return # Invalid message

        for module in self.messageRegistered:
            module.handleMessage(text, user, msg)

    def handleSpecial(self, text):
        """
        :param text: full IRC message to deliver as special data
        :type text: str

        Parse the IRC data and deliver it to registered modules
        """
        for module in self.specialRegistered:
            module.handleSpecial(text)