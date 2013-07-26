#!/usr/bin/env python
#
# Main class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#

import re
import socket
import json
import threading
import sys
import signal
import os
import errno
import imp
from time import sleep

from logging import d, log
from eventlistener import eventlistener

class botti:

    ircsock = None

    user = None
    channel = None
    
    modules = {}
    eventlistener = eventlistener()

    run = True
    
    def parse_config(self):
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
                    passwd = line.split(":")[1]
                if line.find('chnl') != -1:
                    channel = line.split(":")[1]
        except IndexError:
            print("Malformed config file, please fix")
            sys.exit()

        settings_f.close()

        passwd_hidden = ""

        i = 0
        while i < len(passwd):
            passwd_hidden += "*"
            i += 1

        log("PARAMETERS: Host: %s, username: %s, password: %s, channel: %s" % (host, username, passwd_hidden, channel))
        return (host, username, passwd, channel)


    def connect(self, params):
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.ircsock.connect((params[0], 6667))
            
            self.ircsock.setblocking(0)

            self.ircsock.send("Pass %s\n" % (params[2]))
            self.ircsock.send("NICK %s\n" % (params[1]))
            self.ircsock.send("JOIN %s\n" % (params[3]))
        except Exception, e:
            log("Error connecting: %s" % e)
            sys.exit()
            
    def getData(self):
        data = None
        
        try:
            data = self.ircsock.recv(1024)
            data = data.strip('\r\n')
            if not len(data) == 0:
                log("RECV: <>" + data + "<>")
            return data
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return "" # no data
                
    def sendData(self, data):
        if not data == "" or data == None:
            log("SEND: " + data)
            self.ircsock.send(data + "\n")
        
    def sendMessage(self, msg):
        self.sendData("PRIVMSG " + self.channel + " :" + msg)
    
    def loadModule(self, file):
        fpath = os.path.normpath(os.path.join(os.path.dirname(__file__), file))
        dir, fname = os.path.split(fpath)
        mname, ext = os.path.splitext(fname)

        (file, filename, data) = imp.find_module(mname, [dir])
        return imp.load_module(mname, file, filename, data)

    def getModules(self):        
        files = os.listdir("modules/")
        for file in files:
    	    result = re.search(r'\.py$', file)
    	    if result != None:
                module = self.loadModule("modules/" + file)
                id = module.getId()
                self.modules[id] = getattr(module, id)()

    def initModules(self):
        for name, module in self.modules.iteritems():
            module.init(self)

    def sigint(self, signal, frame):
        log("^C received, stopping")
        self.run = False;

    def main(self):
        settings = self.parse_config()

        self.user = settings[1]
        self.channel = settings[3]

        self.getModules()
        self.initModules()

        self.connect(settings)

        signal.signal(signal.SIGINT, self.sigint)
        
        sleep(1)

        while self.run:
            ircmsg = self.getData()

            if not ( ircmag == None or len(ircmsg) == 0):
                for line in ircmsg.split('\n'):
                    #if ircmsg.find('PING ') != -1:
                    #    self.sendData('PING :Pong\n')

                    #result = re.search(':(.*)!.* JOIN #herramustikka', ircmsg)
                    #if not result == None:
                    #    nick = result.group(1)
                    #    print("Found a viewer joining: " + nick + "\n")
                    #    msg = 'PRIVMSG #herramustikka :Tervetuloa ' + nick + "\n"
                    #    print("SENDING: " + msg)
                    #    #self.ircsock.send(msg)
                        
                    if line.find(' PRIVMSG ') != -1:
                        #nick = ircmsg.split('!')[0][1:]
                        #msg = ircmsg.split(' PRIVMSG ')[-1].split(' :')[1]
                        self.eventlistener.handleMessage(line)
                    else:
                        self.eventlistener.handleSpecial(line)
                    
b = botti()         
b.main()
