import logging

class Test:
    log = logging.getLogger("mustikkabot.test")

    def init(self, bot):
        bot.eventmanager.register_message(self)
        bot.eventmanager.register_special(self)
        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)

    def handle_message(self, data, user, msg):
        self.log.debug(user + " said: " + msg)

    def handle_special(self, data):
        self.log.debug("Received special: " + data)
        
