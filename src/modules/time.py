import jsonpickle
import os
import exceptions
import logging
import datetime
from math import floor

import tools


class TimerData:
    msg = ""
    target = None


class Time:

    log = logging.getLogger("mustikkabot.time")
    bot = None

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

        self.jsonpath = os.path.join(self.bot.datadir, "time.json")
        self.read_JSON()

        bot.accessmanager.register_acl("!time.print")
        bot.accessmanager.register_acl("!time.set")
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

        if args[0] == "!time":
            if len(args) > 1:
                self.time_set(args)
            else:
                self.time_print()
        else:
            pass

    def time_set(self, args):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if args[1] == "msg":
            if len(args) > 2:
                self.data.msg = ' '.join(args[2:])
                self.write_JSON()
        elif args[1] == "target":
            if len(args) == 5:
                day = int(args[2])
                hour = int(args[3])
                minute = int(args[4])

                self.data.target = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
                self.write_JSON()
                self.bot.send_message("Ajan rakenne muutettu.")
            if len(args) == 4:
                hour = int(args[2])
                minute = int(args[3])

                self.data.target = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
                self.write_JSON()
                self.bot.send_message("Minuutin rakenne muutettu.")
            elif len(args) == 3:
                hour = int(args[2])

                self.data.target = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=0)
                self.write_JSON()
                self.bot.send_message("Tunnin rakenne muutettu.")


    def time_print(self):

            now = datetime.datetime.now()
            target = self.data.target
            delta = target - now
            hours = floor(delta.seconds / 3600)
            minutes = floor( (delta.seconds - 3600*hours) / 60)
            hours = hours+(delta.days*24)


            self.bot.send_message(self.data.msg + " " + str(hours) + " tuntia ja " + str(minutes) + " minuuttia")
