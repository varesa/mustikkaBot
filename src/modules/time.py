import json
import errno
import logging
import datetime
from math import floor

import tools

class Time:

    log = logging.getLogger("mustikkabot.time")
    bot = None

    def init(self, bot):
        self.bot = bot

        bot.accessmanager.register_acl("!time")
        bot.eventmanager.register_message(self)
        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_message(self)
        
    def handle_message(self, data, user, msg):
        msg = tools.strip_prefix(msg)
        args = msg.split()

        if args[0] == "!time":
                now = datetime.datetime.now()
                target = datetime.datetime(2014, 8, 31, 12, 00)
                
                delta = target - now
                hours = floor(delta.seconds / 3600)
                minutes = floor( (delta.seconds - 3600*hours) / 60)
                
                self.bot.send_message("24 tunnista on jäljellä " + str(hours) + "tuntia ja " + str(minutes) + " minuuttia") 