from logging import log, d

def getId():
    return "test"

class test:
    def init(self, bot):
        bot.eventlistener.registerMessage(self)
        bot.eventlistener.registerSpecial(self)

    def handleMessage(self, data, user, msg):
        log("[TESTMODULE] Received message: " + data)

    def handleSpecial(self, data):
        log("[TESTMODULE] Received special: " + data)
        
