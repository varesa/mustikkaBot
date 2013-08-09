import re

from log import log

class irc:
    """
    Irc is a core-module that responds to things like PING/PONG specified in the IRC specification
    """
    bot = None

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: bot

        Initialize the irc-module and register the specialmsg-callback.
        Called by modulemanager when starting up the module
        """
        self.bot = bot
        bot.eventlistener.registerSpecial(self)
        log("[IRC] Init complete")

    def handleSpecial(self, msg):
        """
        :param msg: the irc command/message
        :type msg: str

        Handle special irc commands and responses to them like PING/PONG
        Called by eventlistener/dispatcher when a special message is received
        """
        result = re.search("PING (.*)", msg)
        if result is not None:
            log("[IRC] Ping received")
            self.bot.sendData("PONG " + result.group(1))
