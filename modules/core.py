def getId():
    return "core"

class core:
    def init(self, bot):
        bot.eventlistener.registerSpecial(self)