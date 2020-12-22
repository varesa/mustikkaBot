import logging
import tools

class About:
    """
    About is a core-module that tells about the bot and it's author
    """

    bot = None
    log = logging.getLogger("mustikkabot.about")

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: Bot

        Initialize the about-module. Called by the modulemanager when the module gets enabled
        """
        self.bot = bot
        bot.eventmanager.register_message(self)
        self.log.info("Init complete")

    def handle_message(self, data, user, msg):
        """
        :param data: Full IRC command
        :type data: str
        :param user: name of the user that sent the message
        :type user: str
        :param msg: the message itself
        :type msg: str

        Handle incoming chat-messages. Check if it contains either !about or !bot commmands
        """
        msg = tools.strip_name(msg)
        args = msg.split()

        if args[0] == "!about" or args[0] == "!bot":
            self.log.info("Printing \"about\"")
            self.bot.send_message("MustikkaBot (2013-2020) is a Twitch bot written in python " +
                                  "for the great streamer HerraMustikka. Author: varesa")

    def dispose(self):
        """
        Uninitialize the module. Unregisters messagelisteners when the module gets disabled.
        """
        self.bot.eventmanager.unregister_message(self)
        self.log.info("Disposed")
