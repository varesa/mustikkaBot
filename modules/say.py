import re

from logging import log
import tools


def getId():
    return "say"


class say:
    bot = None

    def init(self, bot):
        self.bot = bot
        self.bot.eventlistener.registerMessage(self)
        log("[SAY] Init complete")

    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)

        result = re.search(r'^!say (.*)', msg)
        if result is not None:
            self.bot.sendMessage(' '.join(result.groups(1)))

