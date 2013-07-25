import re

from logging import d, log

def getId():
    return "reload"

class reload:
    bot = None
    
    def init(self, bot):
        self.bot = bot
        #bot.eventlistener.registerMessage(self)

    def handleMessage(self, msg):
        msg = re.sub(r'!(mustikkabot)? (.*)',r'!\2',msg)
        
        result = re.search("^!reload", msg)
        if result != None:
            log("[RELOAD] !Reload received")
            self.bot.sendData("Reloadin")
            
