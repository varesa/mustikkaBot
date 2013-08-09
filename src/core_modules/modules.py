import tools
from log import log

class modules:

    bot = None

    def init(self, bot):
        self.bot = bot
        bot.eventlistener.registerMessage(self)
        log("[MODULES] Init complete")


    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)
        args = msg.split()

        if len(args) < 1:
            return

        if not args[0].lower() == "!modules":
            return

        if len(args) == 1:
            self.bot.sendMessage("Available commands for !modules are: list, enable, disable, reload")
            return

        if args[1].lower() == "enable":
            if len(args) < 3:
                self.bot.sendMessage("Name of the module is missing. Correct format: !modules enable <name>")
                return
            if self.bot.modulemanager.isModuleEnabled(args[2]):
                self.bot.sendMessage("Module " + args[2] + " is already enabled")
                return
            if args[2] not in self.bot.modulemanager.getAvailableModules():
                self.bot.sendMessage("Module does not exist")
                return
            self.bot.modulemanager.enableModule(args[2])

        elif args[1].lower() == "disable":
            if len(args) < 3:
                self.bot.sendMessage("Name of the module is missing. Correct format: !modules disable <name>")
                return
            if not self.bot.modulemanager.isModuleEnabled(args[2]):
                self.bot.sendMessage("Module " + args[2] + " is not enabled")
                return
            if args[2] not in self.bot.modulemanager.getAvailableModules():
                self.bot.sendMessage("Module does not exist")
                return
            self.bot.modulemanager.disableModule(args[2])

        elif args[1].lower() == "list":
            enabled = list()
            disabled = list()
            for module in self.bot.modulemanager.getAvailableModules():
                if self.bot.modulemanager.isModuleEnabled(module):
                    enabled.append(module)
                else:
                    disabled.append(module)
            self.bot.sendMessage("Currently enabled modules: " + " ".join(enabled))
            self.bot.sendMessage("Currently disabled modules: " + " ".join(disabled))

        elif args[1].lower() == "reload":
            if len(args) < 3:
                self.bot.sendMessage("Name of the module is missing. Correct format: !modules reload <name>")
                return
            if not self.bot.modulemanager.isModuleEnabled(args[2]):
                self.bot.sendMessage("Module " + args[2] + " does not exists or is not enabled")
                return
            self.bot.modulemanager.reloadModule(args[2])