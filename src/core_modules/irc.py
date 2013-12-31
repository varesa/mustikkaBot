import re
import logging

class Irc:
    """
    Irc is a core-module that responds to things like PING/PONG specified in the IRC specification
    """

    log = logging.getLogger("mustikkabot.irc")
    bot = None

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: Bot

        Initialize the irc-module and register the specialmsg-callback.
        Called by modulemanager when starting up the module
        """
        self.bot = bot
        bot.eventmanager.register_special(self)
        self.log.info("Init complete")

    def handle_special(self, msg):
        """
        :param msg: the irc command/message
        :type msg: str

        Handle special irc commands and responses to them like PING/PONG
        Called by eventlistener/dispatcher when a special message is received
        """
        result = re.search("PING (.*)", msg)
        if result is not None:
            self.log.info("Ping received")
            self.bot.send_data("PONG " + result.group(1))

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)
