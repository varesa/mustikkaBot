import re

from log import log

class core:
    bot = None

    def init(self, bot):
        self.bot = bot
        bot.eventlistener.registerSpecial(self)
        log("[CORE] Init complete")

    def handleSpecial(self, msg):
        result = re.search("PING (.*)", msg)
        if result is not None:
            log("[CORE] Ping received")
            self.bot.sendData("PONG " + result.group(1))
