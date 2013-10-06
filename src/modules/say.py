import re
import logging

import tools

class Say:

    log = logging.getLogger("mustikkabot.say")
    bot = None
    acl = "!say"

    def init(self, bot):
        self.bot = bot
        self.bot.eventlistener.registerMessage(self)
        self.bot.accessmanager.registerAcl(self.acl)
        self.log.info("Init complete")

    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)

        result = re.search(r'^!say (.*)', msg)
        if result is not None:
            if self.bot.accessmanager.isInAcl(user, self.acl):
                self.bot.sendMessage(' '.join(result.groups(1)))

