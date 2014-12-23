#!/usr/bin/env python3
#
# Main class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#

import socket
import select
import sys
import platform
import os
import signal
import errno
from time import sleep
import traceback
import logging
import datetime

import migrations
import logutils
import tools

from eventmanager import EventManager
from modulemanager import ModuleManager
from accessmanager import AccessManager
from timemanager import TimeManager


class Bot:
    """
    Mainclass for the application, everything goes through here
    """

    def __init__(self):
        logutils.setup_logging("mustikkabot")
        self.log = logging.getLogger("mustikkabot")

        self.basepath = tools.find_basepath()
        self.confdir = os.path.join(self.basepath, "config")
        self.datadir = os.path.join(self.basepath, "data")
        self.srcdir = os.path.join(self.basepath, "src")

        migrations.do_migrations(self)

        self.ircsock = None
        self.lastReceived = None

        self.user = None
        self.channel = None

        self.eventmanager = EventManager()
        """ :type: EventManager"""
        self.modulemanager = ModuleManager()
        """ :type: ModuleManager"""
        self.accessmanager = AccessManager()
        """ :type: AccessManager"""
        self.timemanager = TimeManager()
        """ :type: TimeManager"""

        self.run = True

    def parse_config(self):
        """
        :return: list of strings describing parameters
        :rtype: list(string, string, string, string)

        Parse the config file, and read the different defined parameters. Return them as a list
        """
        try:
            settings_f = open(os.path.join(self.confdir, "config.txt"))
        except IOError:
            self.log.error("Config not found, please make a copy of"
                           " \"config/config.txt.template\" as \"config/config.txt\"")
            sys.exit()

        host = None
        username = None
        password = None
        channel = None

        try:
            for line in settings_f:
                line = line.strip("\n\r")
                if line.find('host') != -1:
                    host = line.split(":")[1]
                if line.find('user') != -1:
                    username = line.split(":")[1]
                if line.find('pass') != -1:
                    password = ':'.join(line.split(":")[1:])
                if line.find('chnl') != -1:
                    channel = line.split(":")[1]
        except IndexError:
            self.log.error("Malformed config file, please fix")
            sys.exit()

        settings_f.close()

        passwd_hidden = ""

        for c in password:            # Hide auth token/password from log messages
            passwd_hidden += '*'

        self.log.info("PARAMETERS: Host: %s, username: %s, password: %s, channel: %s" %
                      (host, username, passwd_hidden, channel))

        return host, username, password, channel

    def connect(self, params):
        """
        :param params: A list of the params to be used to connect
        :type params: list(string, string, string, string)

        Try to connect to the IRC server using the provided parameters
        """
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ircsock.settimeout(30)

            self.ircsock.connect((params[0], 6667))

            self.ircsock.setblocking(0)

            self.send_data("PASS %s" % (params[2]), dontLog=True)
            self.send_data("NICK %s" % (params[1]))
            self.send_data("USER %s mustikkaBot 127.0.0.1 :mustikkaBot" % (params[1]))
            self.send_data("JOIN %s" % (params[3]))
        except Exception as e:
            traceback.print_exc()

            self.log.error("\n\nError connecting: %s" % e)
            sys.exit()

    def get_data(self):
        """
        :return: Data received from the socket
        :rtype: str

        Return any data that has been received
        """

        try:
            data = self.ircsock.recv(1024)
            data = data.decode("UTF-8").strip('\r\n')
            if not len(data) == 0:
                self.log.debug("RECV: <>" + data + "<>")
            return data
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return ""  # no data

    def send_data(self, data, dontLog=False):
        """
        :param data: String to be sent
        :type data: str
        :param dontLog: Will the string be logged?
        :type dontLog: bool

        Send data appended with a newline
        """
        if not (data is "" or data is None):
            if not dontLog:
                self.log.debug("SEND: " + data)
            self.ircsock.send(bytes(data + "\n", "UTF-8"))

    def send_message(self, msg):
        """
        :param msg: Message to be sent
        :type msg: str

        Send a message to the channel
        """
        self.send_data("PRIVMSG " + self.channel + " :" + msg)

    def sigint(self, signal, frame):
        """
        :param signal: Signal received
        :param frame: ...

        A signal handler to trap ^C
        """
        self.log.info("^C received, stopping")
        self.run = False

    def main(self):
        """
        The startpoint of the bot
        """
        settings = self.parse_config()

        self.user = settings[1]
        self.channel = settings[3]

        self.accessmanager.init(self)
        self.modulemanager.init(self)

        try:
            self.connect(settings)
            self.lastReceived = datetime.datetime.now()
        except:
            self.log.error("Error connecting to IRC")
            sleep(3)

        signal.signal(signal.SIGINT, self.sigint)

        sleep(1)

        while self.run:
            # Get new data
            ircmsg = self.get_data()

            # Process CLI
            if platform.system() != "Windows":
                cli = select.select([sys.stdin], [], [], 0)[0]
            else:
                cli = False         # No cli on windows because you can't select stdin
            if cli:
                data = sys.stdin.readline().strip()
                if len(data) > 0:
                    self.eventmanager.handle_message(":cli!cli@localhost PRIVMSG " + self.channel + " :" + data)

            # Handle data if received
            if not (ircmsg is None or len(ircmsg) == 0):
                for line in ircmsg.split('\n'):
                    self.lastReceived = datetime.datetime.now()
                    if line.find(' PRIVMSG ') != -1:
                        self.eventmanager.handle_message(line)
                    else:
                        self.eventmanager.handle_special(line)

            # Provied timed events to timemanager
            self.timemanager.handle_events()

            # Check "watchdog"
            if self.lastReceived and datetime.datetime.now() - self.lastReceived > datetime.timedelta(minutes=15):
                self.log.warning("No messages received within 15 minutesr, trying to reconnect")
                try:
                    self.connect(settings)  # Reconnect
                    self.lastReceived = datetime.datetime.now()
                except:
                    self.log.error("Error connecting to IRC")
                    sleep(3)

            sleep(0.01)

        # Shut down
        self.modulemanager.dispose()
        self.accessmanager.dispose()


if __name__ == "__main__":  # Do not start on import
    b = Bot()
    b.main()