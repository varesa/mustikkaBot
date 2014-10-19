import re
import logging

from lib.chatter_bot_api import ChatterBotFactory, ChatterBotType

import tools


class Ai:

    log = logging.getLogger("mustikkabot.ai")
    bot = None
    acl = "ai"

    ai = None

    def init(self, bot):
        self.bot = bot
        self.bot.eventmanager.register_message(self)
        self.bot.accessmanager.register_acl(self.acl, default_groups="%all")

        factory = ChatterBotFactory()
        self.ai = factory.create(ChatterBotType.CLEVERBOT).create_session()

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)

    def handle_message(self, data, user, msg):
        """
        Handle an incoming message

        :param data: Raw message
        :type data: str
        :param user: Name of the user sending the message
        :type user: str
        :param msg: Actual user message
        :type msg: str
        :rtype: None
        """

        msg_split = msg.split()
        if msg_split[0].lower().startswith("mustikkabot"):
            out = self.ai.think(' '.join(msg_split[1:]))
            self.bot.send_message(user + ": " + out)