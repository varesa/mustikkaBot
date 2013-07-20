def getId():
    return "commands"

class commands:
    def init(self, bot):
        bot.eventlistener.registerMessage(self)

    def handleMessage(self, data, user, msg):
        pass
