import logging


class Test:
    log = logging.getLogger("mustikkabot.test")
    bot = None

    def init(self, bot):
        """
        Initializer method that will be called when the module is loaded

        :param bot: The main instance of the bot
        :type bot: Bot
        :rtype: None
        """
        self.bot = bot

        self.bot.eventmanager.register_message(self)
        self.bot.eventmanager.register_special(self)
        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_message(self)
        self.bot.eventmanager.unregister_special(self)
        self.log.info("Disposed")

    def handle_message(self, data, user, msg):
        self.log.debug(user + " said: " + msg)

    def handle_special(self, data):
        self.log.debug("Received special: " + data)
