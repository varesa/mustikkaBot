import jsonpickle
import exceptions
import os
import logging
import datetime
from math import floor

import tools


class TimerData:
    msg = ""
    target = None


class Uptime:

    log = logging.getLogger("mustikkabot.uptime")
    bot = None
    juoksee = 0

    jsonpath = None

    data = None
    """:type: TimerData"""

    def init(self, bot):
        """
        Initialize the module when called by the modulemanager. Prepares data and initializes ACLs and event listeners
        :param bot: The main bot instance
        :type bot: Bot
        :rtype: None
        """
        self.bot = bot

        self.jsonpath = os.path.join(self.bot.datadir, "uptime.json")
        self.read_JSON()

        bot.accessmanager.register_acl("!uptime.print")
        bot.accessmanager.register_acl("!uptime.set")
        bot.eventmanager.register_message(self)

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the modulemanager. Unregisters the messagelisteners
        when the module gets disabled.
        :rtype: None
        """
        self.bot.eventmanager.unregister_message(self)
        self.log.info("Disposed")

    # noinspection PyPep8Naming
    def read_JSON(self):
        """
        Read the JSON datafile from disk that contains the last time
        :rtype: None
        """

        if not os.path.isfile(self.jsonpath):
            self.log.info("Time-datafile does not exist, creating")
            self.data = TimerData()
            self.data.msg = "Aikaa puoleenyöhön"
            self.data.target = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0)
            self.write_JSON()

        try:
            with open(self.jsonpath, "r") as file:
                jsondata = file.read()
        except:
            self.log.error("Could not open " + self.jsonpath)
            raise exceptions.FatalException("Could not open " + self.jsonpath)

        self.data = jsonpickle.decode(jsondata)

    # noinspection PyPep8Naming
    def write_JSON(self):
        """
        Write the loaded commands to disk in JSON format
        :rtype: None
        """

        with open(self.jsonpath, "w") as file:
            data = jsonpickle.encode(self.data)
            file.write(data)

    def handle_message(self, data, user, msg):
        msg = tools.strip_name(msg)
        args = msg.split()

        if args[0] == "!uptime":
            if len(args) > 1:
                if args[1] == "reset":
                    self.uptime_reset(args)
                else:
                    pass
            else:
                self.uptime_print()
        else:
            pass

    def uptime_reset(self, args):

        now = datetime.datetime.now()

        self.data.target = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
        self.write_JSON()
        self.bot.send_message("Timeri resetattu.")


    def uptime_print(self):

            uptime_now = datetime.datetime.now()
            uptime_target = self.data.target
            uptime_delta = uptime_now - uptime_target
            delta_hours = floor(uptime_delta.seconds / 3600)
            delta_minutes = floor( (uptime_delta.seconds - 3600*delta_hours) / 60)
            delta_seconds = floor(uptime_delta.seconds - (60*delta_minutes + 3600*delta_hours))

            self.bot.send_message("Striimiä on kulunut " + str(delta_hours) + " Tuntia,  " + str(delta_minutes) + " Minuuttia ja " + str(delta_seconds) + " Sekunttia. musCasual")
