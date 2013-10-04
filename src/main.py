#!/usr/bin/env python
#
# Main class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#

import socket
import sys
import signal
import errno
from time import sleep
import traceback

from log import log

from eventmanager import eventmanager
from modulemanager import modulemanager
from accessmanager import accessmanager


class bot:
    ircsock = None

    user = None
    channel = None

    eventlistener = eventmanager()
    """ :type: eventlistener"""
    modulemanager = modulemanager()
    """ :type: modulemanager"""
    accessmanager = accessmanager()
    """ :type: access"""

    run = True

    def parse_config(self):
        """
        :return: list of strings describing parameters
        :rtype: list(string, string, string, string)

        Parse the config file, and read the different defined parameters. Return them as a list
        """
        try:
            settings_f = open("config.txt")
        except IOError:
            print("Config not found, please make a copy of \"config.txt.template\" as \"config.txt\"")
            sys.exit()

        host = None
        username = None
        passwd = None
        channel = None

        try:
            for line in settings_f:
                line = line.strip("\n\r")
                if line.find('host') != -1:
                    host = line.split(":")[1]
                if line.find('user') != -1:
                    username = line.split(":")[1]
                if line.find('pass') != -1:
                    passwd = ':'.join(line.split(":")[1:])
                if line.find('chnl') != -1:
                    channel = line.split(":")[1]
        except IndexError:
            print("Malformed config file, please fix")
            sys.exit()

        settings_f.close()

        passwd_hidden = ""

        print(passwd)

        i = 0
        while i < len(passwd):
            passwd_hidden += "*"
            i += 1

        log("PARAMETERS: Host: %s, username: %s, password: %s, channel: %s" % (host, username, passwd_hidden, channel))
        return (host, username, passwd, channel)


    def connect(self, params):
        """
        :param params: A list of the params to be used to connect
        :type params: list(string, string, string, string)

        Try to connect to the IRC server using the provided parameters
        """
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.ircsock.connect((params[0], 6667))

            self.ircsock.setblocking(0)

            self.sendData("PASS %s" % (params[2]), dontLog=True)
            self.sendData("NICK %s" % (params[1]))
            self.sendData("USER %s mustikkaBot 127.0.0.1 :mustikkaBot" % (params[1]))
            self.sendData("JOIN %s" % (params[3]))
        except Exception as e:
            traceback.print_exc()

            log("\n\nError connecting: %s" % e)
            sys.exit()

    def getData(self):
        """
        :return: Data received from the socket
        :rtype: str

        Return any data that has been received
        """
        data = None

        try:
            data = self.ircsock.recv(1024)
            data = data.decode("UTF-8").strip('\r\n')
            if not len(data) == 0:
                log("RECV: <>" + data + "<>")
            return data
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return ""  # no data

    def sendData(self, data, dontLog=False):
        """
        :param data: String to be sent
        :type data: str
        :param dontLog: Will the string be logged?
        :type dontLog: bool

        Send data appended with a newline
        """
        if not (data is "" or data is None):
            if not dontLog:
                log("SEND: " + data)
            self.ircsock.send(bytes(data + "\n", "UTF-8"))

    def sendMessage(self, msg):
        """
        :param msg: Message to be sent
        :type msg: str

        Send a message to the channel
        """
        self.sendData("PRIVMSG " + self.channel + " :" + msg)

    def sigint(self, signal, frame):
        """
        :param signal: Signal received
        :param frame: ...

        A signal handler to trap ^C
        """
        log("^C received, stopping")
        self.run = False;

    def main(self):
        """
        The startpoint of the bot
        """
        settings = self.parse_config()

        self.user = settings[1]
        self.channel = settings[3]

        self.accessmanager.init(self)
        self.modulemanager.init(self)

        self.connect(settings)

        signal.signal(signal.SIGINT, self.sigint)

        sleep(1)

        while self.run:
            ircmsg = self.getData()

            if not ( ircmsg is None or len(ircmsg) == 0):
                for line in ircmsg.split('\n'):

                    if line.find(' PRIVMSG ') != -1:
                        self.eventlistener.handleMessage(line)
                    else:
                        self.eventlistener.handleSpecial(line)

if __name__ == "__main__": # Do not start on import
    b = bot()
    b.main()
