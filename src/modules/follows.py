import logging
import datetime

from TwitchAPI.Channel import Channel
from urllib.error import HTTPError


def _ts2dt(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


class Follows:

    log = logging.getLogger("mustikkabot.follows")
    bot = None
    """ :type: Bot"""

    followed = []
    """ :type: list"""

    last_created_at = 0

    def check_followers(self):
        try:
            data = Channel("herramustikka").get_followers()
        except HTTPError:
            self.log.warning("Connectivity problem with twitch API")
            return

        if self.last_created_at == 0:
            self.last_created_at = _ts2dt(data[0]['created_at'])
            return

        for follow in data[::-1]:

            if _ts2dt(follow['created_at']) > self.last_created_at:
                if follow['user']['display_name'] not in self.followed:
                    self.bot.send_message("Kiitos followista / Thank you for the follow: " + follow['user']['display_name'])
                    self.followed.append(follow['user']['display_name'])
                    self.log.info("New follower: " + follow['user']['display_name'])
                else:
                    self.log.info("Follow spam: " + follow['user']['display_name'])
                self.last_created_at = _ts2dt(follow['created_at'])

    def init(self, bot):
        """
        Initialize the module when added by eventmanager.
        """
        self.bot = bot

        interval = datetime.timedelta(seconds=5)
        self.bot.timemanager.register_interval(interval=interval, action=self.check_followers)

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.timemanager.unregister(self.check_followers)
        self.log.info("Disposed")