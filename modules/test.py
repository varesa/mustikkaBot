from logging import log, d

def getId():
    return "test"

class test:
    def init(self, bot):
        bot.eventlistener.registerMessage(self)
        bot.eventlistener.registerSpecial(self)
        log("[TEST] Init complete")

    def handleMessage(self, data, user, msg):
        log("[TESTMODULE] " + user + " said: " + msg)

    def handleSpecial(self, data):
        log("[TESTMODULE] Received special: " + data)
        
