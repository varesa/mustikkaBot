import logging
import datetime
from TwitchAPI.Channel import Channel


def _ts2dt(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


class Follows:

    log = logging.getLogger("mustikkabot.follows")
    bot = None
    """ :type: bot"""

    last_created_at = 0

    def check_followers(self):
        data = Channel("herramustikka").get_followers()

        if self.last_created_at == 0:
            self.last_created_at = _ts2dt(data[0]['created_at'])
            return

        for follow in data[::-1]:

            if _ts2dt(follow['created_at']) > self.last_created_at:
                self.bot.send_message("New follower: " + follow['user']['display_name'])
                self.last_created_at = _ts2dt(follow['created_at'])

    def init(self, bot):
        """
        Initialize the module when added by eventmanager.
        """
        interval = datetime.timedelta(seconds=5)
        bot.timemanager.register_interval(interval=interval, action=self.check_followers)

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)