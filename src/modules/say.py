import re
import logging

import tools


class Say:

    log = logging.getLogger("mustikkabot.say")
    bot = None
    acl = "!say"

    def init(self, bot):
        """
        Initializer method for the module that will be called when the module is enabled.
        Registers the message listeners and registers the ACL

        :param bot: Main instance of the bot
        :type bot: Bot
        :rtype: None
        """
        self.bot = bot
        self.bot.eventmanager.register_message(self)
        self.bot.accessmanager.register_acl(self.acl)
        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitializer method for the module that will be called when the module is disabled.
        Unregisters the messagelisteners
        """
        self.bot.eventmanager.unregister_message(self)

    # noinspection PyUnusedLocal
    def handle_message(self, data, user, msg):
        msg = tools.strip_name(msg)

        result = re.search(r'^!say (.*)', msg)
        if result is not None:
            if self.bot.accessmanager.is_in_acl(user, self.acl):
                self.bot.send_message(' '.join(result.groups(1)))
