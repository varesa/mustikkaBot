import re

from logging import d, log

def getId():
    return "say"

class say:
    
    bot = None
    
    def init(self, bot):
	self.bot = bot
	self.bot.eventlistener.registerMessage(self)
	
    def handleMessage(self, data, user, msg):
        msg = re.sub(r'!(mustikkabot)? (.*)',r'!\2',msg)
        
        result = re.search(r'^!say (.*)', msg) 
        if result != None:
	    self.bot.sendMessage(' '.join(result.groups(1)))

