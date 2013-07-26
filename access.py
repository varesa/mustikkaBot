import re
import json
import errno

from logging import log, d

class access:
    
    bot = None
    
    groups = {}
    acls = {}
    
    jsonfile = "acls.json"

    def init(self, bot):
	self.bot = bot
	self.readJSON()
        log("[ACCESS] Init complete")

    def readJSON(self):
	jsondata = None
	try:
	    file = open(self.jsonfile, "r")
	    jsondata = file.read()
	    file.close()
	except IOError as e:
	    if e.errno == errno.ENOENT:
		log("[COMMANDS] file does not exist, creating")
		self.writeJSON()
	
	try:
	    data = json.loads(jsondata)
	    self.groups = data['groups']
	    self.acls = data['acls']
	except ValueError:
	    log("[COMMANDS] commands-file malformed")
	    

    def writeJSON(self):
	jsondata = {"groups":self.groups, "acls":self.acls}
	file = open(self.jsonfile, "w")
	data = json.dumps(jsondata)
	file.write(data)
	file.close()