from logging import d, log

def getId():
    return "echo"

class echo:
    bot = None

    def init(self,bot):
        self.bot = bot
        bot.eventlistener.registerMessage(self)

    def handleMessage(self, data, user, msg):
        args = msg.split()
        if not args[0] == "!echo":
            return

        if len(args) > 1:
            msg = ""
            for arg in args[1:]:
                msg += " " + arg
            self.bot.sendMessage("Echo:" + msg)
                
        else:
            self.bot.sendMessage("Echo!")
