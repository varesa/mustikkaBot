import re

from logging import log
import tools


def getId():
    return "say"


class say:
    bot = None
    acl = "!say"

    def init(self, bot):
        self.bot = bot
        self.bot.eventlistener.registerMessage(self)
        self.bot.accessmanager.registerAcl(self.acl)
        log("[SAY] Init complete")

    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)

        result = re.search(r'^!say (.*)', msg)
        if result is not None:
            if self.bot.accessmanager.isInAcl(user, self.acl):
                self.bot.sendMessage(' '.join(result.groups(1)))

