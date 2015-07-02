import logging
import datetime

class Tj:
    def __init__(self):
        self.bot = None
        self.log = None

        self.acl = "!tj"

        self.release = {
            '115-165': datetime.datetime(2015, 6, 18),
            '115-255': datetime.datetime(2015, 9, 16),
            '115-347': datetime.datetime(2015, 12, 17),

            '215-165': datetime.datetime(2015, 12, 17),
            '215-255': datetime.datetime(2016, 3, 16),
            '215-347': datetime.datetime(2016, 6, 16),

            '116-165': datetime.datetime(2016, 6, 16),
            '116-255': datetime.datetime(2016, 9, 14),
            '116-347': datetime.datetime(2016, 12, 15),

            '216-165': datetime.datetime(2016, 12, 15),
            '216-255': datetime.datetime(2017, 3, 15),
            '216-347': datetime.datetime(2017, 6, 15),
        }

    def init(self, bot):
        self.bot = bot
        self.log = logging.getLogger("mustikkabot.tj")

        self.bot.accessmanager.register_acl(self.acl)
        self.bot.eventmanager.register_message(self)

        self.log.info("Init complete")

    def dispose(self):
        self.bot.eventmanager.unregister_message(self)
        self.log.info("Disposed")

    def handle_message(self, data, user, msg):
        args = msg.split(' ')

        if args[0] != "!tj":
            return

        if len(args) == 1:
            group = "115-347"
        else:
            group = args[1]

        try:
            now = datetime.datetime.now()
            delta = self.release[group] - datetime.datetime(now.year, now.month, now.day)
            if delta.days > 0:
                self.bot.send_message("TJ" + str(delta.days))
            else:
                self.bot.send_message("TJ0!")
        except KeyError:
            self.bot.send_message("Tuntematon saapumiserä")

