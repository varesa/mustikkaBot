import logging
import datetime
import dateutil.parser
import requests

from math import floor

import tools


class Uptime:

    log = logging.getLogger("mustikkabot.uptime")
    bot = None

    restart_threshold = datetime.timedelta(minutes=15)

    STATE_OFFLINE = 0
    STATE_ONLINE  = 1

    # State
    started = None
    state   = STATE_OFFLINE
    state_last_changed = None

    def init(self, bot):
        """
        Initialize the module when called by the modulemanager. Prepares data and initializes ACLs and event listeners
        :param bot: The main bot instance
        :type bot: Bot
        :rtype: None
        """
        self.bot = bot

        bot.accessmanager.register_acl("!uptime", default_groups="%all%")
        bot.eventmanager.register_message(self)
        bot.timemanager.register_interval(self.timer_callback, datetime.timedelta(seconds=30))

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the modulemanager. Unregisters the messagelisteners
        when the module gets disabled.
        :rtype: None
        """
        self.bot.eventmanager.unregister_message(self)
        self.bot.timemanager.unregister(self.timer_callback)
        self.log.info("Disposed")

    def timer_callback(self):
        r = requests.get("https://api.twitch.tv/kraken/streams/" + self.bot.channel[1:])  # Strip leading '#'
        if r.json()['stream'] is None:
            self.offline(r.json())
        else:
            self.online(r.json())

    def offline(self, data):
        if self.state == self.STATE_ONLINE:
            #self.bot.send_message("Stream ended")
            self.state = self.STATE_OFFLINE
            self.state_last_changed = tools.tz_now()
            self.log.info("Detected offline transition")

    def online(self, data):
        if self.state == self.STATE_OFFLINE:
            if self.state_last_changed and tools.tz_now() - self.state_last_changed < self.restart_threshold:
                #self.bot.send_message("Continuing")
                self.log.info("Detected online transition, continuing")
            else:
                #self.bot.send_message("New stream")
                self.started = dateutil.parser.parse(data['stream']['created_at'])
                self.log.info("Detected online transition, starting new")
            self.state = self.STATE_ONLINE
            self.state_last_changed = tools.tz_now()

    def handle_message(self, data, user, msg):
        msg = tools.strip_name(msg)
        args = msg.split()

        if args[0] == "!uptime":
            if self.state == self.STATE_ONLINE:
                uptime = tools.tz_now() - self.started
                msg = "Up for: "
            else:
                uptime = self.state_last_changed - self.started
                msg = "Was up for: "

            total_seconds = uptime.total_seconds()
            total_minutes = floor(total_seconds / 60)
            hours = floor(total_minutes / 60)
            minutes = total_minutes - 60*hours

            self.bot.send_message(msg  + str(hours) + " h, " + str(minutes) + " min")