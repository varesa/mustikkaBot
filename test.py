#!/usr/bin/env python
import re, socket, json, threading

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(server, port):
	ircsock.connect((server, port))
	ircsock.send("Pass %s\n" % ("legolego"))
	ircsock.send("NICK %s\n" % ("mustikkaBot"))
	ircsock.send("JOIN %s\n" % ("#herramustikka"))



#host = "herramustikka.jtvirc.com"
host = "199.9.253.199"


def main():

	try:
		connect(host, 6667)
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
			ircsock.send(msg)
		

		if ircmsg.find(' PRIVMSG ') != -1:
			nick = ircmsg.split('!')[0][1:]
			msg = ircmsg.split(' PRIVMSG ')[-1].split(' :')[1]

main()

