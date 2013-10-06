import logging
import tools

class about:
    """
    About is a core-module that tells about the bot and it's author
    """

    bot = None
    log = logging.getLogger("mustikkabot.about")

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: bot

        Initialize the about-module. Called by the modulemanager when the module gets enabled
        """
        self.bot = bot
        bot.eventlistener.registerMessage(self)
        self.log.info("Init complete")

    def handleMessage(self, data, user, msg):
        """
        :param data: Full IRC command
        :type data: str
        :param user: name of the user that sent the message
        :type user: str
        :param msg: the message itself
        :type msg: str

        Handle incoming chat-messages. Check if it contains either !about or !bot commmands
        """
        msg = tools.stripPrefix(msg)
        args = msg.split()

        if args[0] == "!about" or args[0] == "!bot":
            self.log.info("Printing \"about\"")
            self.bot.sendMessage("MustikkaBot is a IRC/Twitch chatbot created in python " +
                            "for the awesome youtuber/streamer Mustikka. Author: Esa Varemo")