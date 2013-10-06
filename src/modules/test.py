import logging

class test:
    log = logging.getLogger("mustikkabot.test")

    def init(self, bot):
        bot.eventlistener.registerMessage(self)
        bot.eventlistener.registerSpecial(self)
        self.log.info("Init complete")

    def handleMessage(self, data, user, msg):
        self.log.debug(user + " said: " + msg)

    def handleSpecial(self, data):
        self.log.debug("Received special: " + data)
        
