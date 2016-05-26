import re
import logging


class EventManager:

    log = logging.getLogger("mustikkabot.eventmanager")

    message_registered = []
    special_registered = []

    def __init__(self):
        self.message_registered = list()
        self.special_registered = list()

    def register_message(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming messages
        """
        self.log.info("Module " + str(module) + " registering for messages")
        if module not in self.message_registered:
            self.message_registered.append(module)

    def unregister_message(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming messages
        """
        self.log.info("Module " + str(module) + " unregistering messages")
        remove = None
        for registered in self.message_registered:
            if type(registered) == type(module):
                remove = registered
        if remove is not None:
            self.message_registered.pop(self.message_registered.index(remove))

    def register_special(self, module):
        """
        :param module: instance of the module that will handle the event

        Registers a module to receive events on incoming "special" (non message) data
        """
        self.log.info("Module " + str(module) + " registering for special messages")
        if module not in self.special_registered:
            self.special_registered.append(module)

    def unregister_special(self, module):
        """
        :param module: instance of the module

        Unregister a module to stop it from receiving events on incoming "special" (non message) data
        """
        self.log.info("Module " + str(module) + " unregistering special messages")
        remove = None
        for registered in self.special_registered:
            if type(registered) == type(module):
                remove = registered
        if remove is not None:
            self.special_registered.pop(self.special_registered.index(remove))

    def handle_message(self, text):
        """
        :param text: full IRC message to deliver as a text-message
        :type text: str

        Parse the IRC message and deliver it to registered modules
        """
        result = re.search(":(.*?)!(.*) PRIVMSG (.*?) :(.*)", text)

        user = None
        msg = None

        if result is not None:
            user = result.group(1)
            msg = result.group(4)
        else:
            self.log.warning("Received invalid message")
            return  # Invalid message

        for module in self.message_registered:
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
        for module in self.special_registered:
            try:
                module.handle_special(text)
            except:
                self.log.exception("Error happened while module '" + module + "' was handling a special message")
