import re
import json
import errno

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
        pass

    """def createFile(self):
	file = open(self.jsonfile, "w")
	file.write("")
	file.close()"""

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
		"""self.createFile()"""
	
	try:
	    self.commands = json.loads(jsondata)
	except ValueError:
	    log("[COMMANDS] commands-file malformed")
	    

    def writeJSON(self):
	file = open(self.jsonfile, "w")
	data = json.dumps(self.commands)
	file.write(data)
	file.close()

    def addCmd(self, cmd):
	pass

    def setCmd(self, cmd, text):
	pass