import logging

class Test:
    log = logging.getLogger("mustikkabot.test")

    def init(self, bot):
        bot.eventlistener.register_message(self)
        bot.eventlistener.register_special(self)
        self.log.info("Init complete")

    def handle_message(self, data, user, msg):
        self.log.debug(user + " said: " + msg)

    def handle_special(self, data):
        self.log.debug("Received special: " + data)
        
