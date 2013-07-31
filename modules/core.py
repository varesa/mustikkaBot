import re

from logging import log


def getId():
    return "core"


class core:
    bot = None

    def init(self, bot):
        self.bot = bot
        bot.eventlistener.registerSpecial(self)
        log("[CORE] Init complete")

    def handleSpecial(self, msg):
        result = re.search("PING (.*)", msg)
        if result != None:
            log("[CORE] Ping received")
            self.bot.sendData("PONG " + result.group(1))
