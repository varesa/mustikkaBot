import re
import logging

class EventManager:

    log = logging.getLogger("mustikkabot.eventmanager")

    messageRegistered = []
    specialRegistered = []

    def register_message(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming messages
        """
        if not module in self.messageRegistered:
            self.messageRegistered.append(module)

    def unregister_message(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming messages
        """
        self.messageRegistered.pop(self.messageRegistered.index(module))

    def register_special(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming "special" (non message) data
        """
        if not module in self.specialRegistered:
            self.specialRegistered.append(module)

    def unregister_special(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming "special" (non message) data
        """
        self.specialRegistered.pop(self.messageRegistered.index(module))

    def handle_message(self, text):
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
            self.log.warning("Received invalid message")
            return  # Invalid message

        for module in self.messageRegistered:
            try:
                module.handle_message(text, user, msg)
            except:
                self.log.exception("Error happened while module '" + str(module) + "' was handling a message")

    def handle_special(self, text):
        """
        :param text: full IRC message to deliver as special data
        :type text: str

        Parse the IRC data and deliver it to registered modules
        """
        for module in self.specialRegistered:
            try:
                module.handle_special(text)
            except:
                self.log.exception("Error happened while module '" + module + "' was handling a special message")
