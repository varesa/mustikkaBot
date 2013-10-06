import re
import logging

import tools

class Say:

    log = logging.getLogger("mustikkabot.say")
    bot = None
    acl = "!say"

    def init(self, bot):
        self.bot = bot
        self.bot.eventlistener.register_message(self)
        self.bot.accessmanager.register_acl(self.acl)
        self.log.info("Init complete")

    def handle_message(self, data, user, msg):
        msg = tools.strip_prefix(msg)

        result = re.search(r'^!say (.*)', msg)
        if result is not None:
            if self.bot.accessmanager.is_in_acl(user, self.acl):
                self.bot.send_message(' '.join(result.groups(1)))

