import logging
import requests
import time

from math import floor

import tools


class Ruokaa:

    log = logging.getLogger("mustikkabot.ruokaa")
    bot = None

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

        bot.accessmanager.register_acl("!ruokaa", default_groups="%all%")
        bot.eventmanager.register_message(self)
        #bot.timemanager.register_interval(self.timer_callback, datetime.timedelta(seconds=30))

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the modulemanager. Unregisters the messagelisteners
        when the module gets disabled.
        :rtype: None
        """
        self.bot.eventmanager.unregister_message(self)
        #self.bot.timemanager.unregister(self.timer_callback)
        self.log.info("Disposed")


    def handle_message(self, data, user, msg):
        msg = tools.strip_name(msg)
        args = msg.split()

        if args[0] == "!ruokaa":
            r = requests.get("https://api.ruoka.xyz/2016-09-19").json()
            for restaurant in r['restaurants']:
                self.bot.send_message(restaurant['name'] + ": ")
                for menu in restaurant['menus']:
                    for meal in menu['meals']:
                        if meal['prices'][0] != "2,60":
                            continue
                        if restaurant['name'] == 'Reaktori' and meal['name'] != 'Linjasto':
                            continue
                        contents = []
                        for content in meal['contents']:
                            contents.append(content['name'])
                        self.bot.send_message("- " + ", ".join(contents))
                        time.sleep(0.8)
                time.sleep(2)
