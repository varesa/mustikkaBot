import re

import logging
import tools


class Raffle:

    def __init__(self):
        self.bot = None

        self.aclManage = "!raffle.manage"
        self.aclJoin = "!raffle.join"

        self.raffleName = None
        self.participants = []

    def init(self, bot):
        self.log = logging.getLogger("mustikkabot.raffle")
        self.bot = bot

        self.bot.eventmanager.registerMessage(self)
        self.bot.accessmanager.registerAcl(self.acl)
        self.log.info("Init complete")

    def dispose(self):
        self.bot.eventmanager.unregister_message(self)

    def handle_message(self, data, user, msg):
        msg = tools.stripPrefix(msg)

        args = msg.split()
        if not args[0] is "!raffle":
            return

        if len(args) is 1:
            if self.raffleName is not None:
                self.bot.sendMessage("No ongoing raffles")
            else:
                self.bot.sendMessage("Ongoing raffle: " + self.raffleName)
            return

        if args[1] is "create":
            pass

        if args[1] is "end":
            pass

        if args[1] is "help":
            pass
