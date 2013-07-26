import re

from logging import d, log
import tools

def getId():
    return "reload"

class reload:
    bot = None
    
    def init(self, bot):
        self.bot = bot
        #bot.eventlistener.registerMessage(self)

    def handleMessage(self, msg):
        msg = tools.stripPrefix(msg)
        
        result = re.search("^!reload", msg)
        if result != None:
            log("[RELOAD] !Reload received")
            self.bot.sendData("Reloadin")
            
