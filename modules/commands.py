import re
import json
import errno

import tools
from logging import log, d

def getId():
    return "commands"

class commands:
    
    commands = []
    jsonfile = "commands.json"

    def init(self, bot):
	self.readJSON()
        bot.eventlistener.registerMessage(self)

    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)
	args = msg.split()
	if args[0] != "!commands":
	    return
	
	if args[1] == "add":
	    self.addCommand(args[2])
	
	if args[1] == "set":
	    self.setCommand(args[2], ' '.join(args[3:]))

    def readJSON(self):
	jsondata = None
	created = False
	try:
	    file = open(self.jsonfile, "r")
	    jsondata = file.read()
	    file.close()
	except IOError as e:
	    if e.errno == errno.ENOENT:
		log("[COMMANDS] file does not exist, creating")
		self.writeJSON()
	
	try:
	    self.commands = json.loads(jsondata)
	except ValueError:
	    log("[COMMANDS] commands-file malformed")
	    

    def writeJSON(self):
	file = open(self.jsonfile, "w")
	data = json.dumps(self.commands)
	file.write(data)
	file.close()

    def addCommand(self, cmd):
	self.commands.append({"name":cmd})
	self.writeJSON()

    def setCommand(self, cmd, text):
	for command in self.commands:
	    if command['name'] == cmd:
		command['value'] = text
	self.writeJSON()