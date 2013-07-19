#!/usr/bin/env python
#
# Main class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#

import re, socket, json, threading, sys

from logging import d, log

# Globals
ircsock = None

def parse_config():
    try:
	settings_f = open("config.txt")
    except IOError:
        print("Config not found, please make a copy of \"config.txt.template\" as \"config.txt\"")
        sys.exit()

    host = None
    username = None
    passwd = None
    channel = None


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

    settings_f.close()

    passwd_hidden = ""

    i = 0
    while i < len(passwd):
	passwd_hidden += "*"
	i += 1

    log("PARAMETERS: Host: %s, username: %s, password: %s, channel: %s" % (host, username, passwd_hidden, channel))
    return (host, username, passwd, channel)


def connect(params):
	global ircsock
	
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ircsock.setblocking(0)

	ircsock.connect((params[0], 6667))
	ircsock.send("Pass %s\n" % (params[2]))
	ircsock.send("NICK %s\n" % (params[1]))
	ircsock.send("JOIN %s\n" % (params[3]))


def main():

	settings = parse_config()

	try:
		connect(settings)
	except Exception as e:
		print e

	while True:
		ircmsg = ircsock.recv(1024)
		ircmsg = ircmsg.strip('\r\n')

		print ircmsg

		if ircmsg.find('PING ') != -1:
			ircsock.send('PING :Pong\n')

		#if ircmsg.find(' JOIN ') != -1:
		#	print("join found")
		#	msg = "PRIVMSG #herramustikka test?\n"
		#	print("Sending: " + msg)
		#	ircsock.send(msg)
		
		result = re.search(':(.*)!.* JOIN #herramustikka', ircmsg)
		if not result == None:
			nick = result.group(1)
			print("Found a viewer joining: " + nick + "\n")
			#print("\n\n" + result.group(1) + "\n\n")
			msg = 'PRIVMSG #herramustikka :Tervetuloa ' + nick + "\n"
			print("SENDING: " + msg)
			#ircsock.send(msg)
		

		if ircmsg.find(' PRIVMSG ') != -1:
			nick = ircmsg.split('!')[0][1:]
			msg = ircmsg.split(' PRIVMSG ')[-1].split(' :')[1]

main()

