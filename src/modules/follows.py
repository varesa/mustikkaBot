import logging
import datetime

def test():
    print("abc")

class Follows:

    log = logging.getLogger("mustikkabot.follows")
    bot = None
    """ :type: bot"""

    def check_followers(self):
        self.log.debug("Interval!")

    def init(self, bot):
        """
        Initialize the module when added by eventmanager.
        """
        interval = datetime.timedelta(seconds=5)
        bot.timemanager.register_interval(interval=interval, action=test)

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)