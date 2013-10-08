import re

from log import log
import tools

class raffle:
    bot = None
    acl = "!raffle"

    raffleName = None
    participants = []

    def init(self, bot):
        self.bot = bot
        self.bot.eventlistener.registerMessage(self)
        self.bot.accessmanager.registerAcl(self.acl)
        log("[RAFFLE] Init complete")

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
