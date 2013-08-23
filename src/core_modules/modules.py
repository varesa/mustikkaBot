import tools
from log import log

class modules:
    """
    Modules is a core-module that handles the chat frontend to managing non-core modules.
    """

    bot = None
    acl = "!modules"

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: bot

        Initialize the modules-module. Register callback to the message received event.
        Called by the modulemanager when loading the module
        """
        self.bot = bot
        bot.accessmanager.registerAcl(self.acl, defaultGroups="%operators")
        bot.eventlistener.registerMessage(self)
        log("[MODULES] Init complete")


    def handleMessage(self, data, user, msg):
        """
        :param data: full IRC command
        :param user: user that sent the message
        :param msg: the chat-message the user sent

        Look for any commands that the command-module should handle and handle any found commands.
        Called by the eventmanager/dispatcher when a message is received
        """
        msg = tools.stripPrefix(msg)
        args = msg.split()


        if len(args) < 1:
            return

        if not args[0].lower() == "!modules":
            return

        if not self.bot.accessmanager.isInAcl(user, self.acl):
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
            self.bot.sendMessage("Module " + args[2] + " enabled")

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
            self.bot.sendMessage("Module " + args[2] + " disabled")

        elif args[1].lower() == "list":
            enabled = list()
            disabled = list()
            for module in self.bot.modulemanager.getAvailableModules():
                if self.bot.modulemanager.isModuleEnabled(module):
                    enabled.append(module)
                else:
                    disabled.append(module)
            if len(enabled) == 0:
                enabled.append("None")
            if len(disabled) == 0:
                disabled.append("None")
            self.bot.sendMessage("Currently enabled modules: " + ", ".join(enabled))
            self.bot.sendMessage("Currently disabled modules: " + ", ".join(disabled))

        elif args[1].lower() == "reload":
            if len(args) < 3:
                self.bot.sendMessage("Name of the module is missing. Correct format: !modules reload <name>")
                return
            if not self.bot.modulemanager.isModuleEnabled(args[2]):
                self.bot.sendMessage("Module " + args[2] + " does not exists or is not enabled")
                return
            self.bot.modulemanager.reloadModule(args[2])
            self.bot.sendMessage("Module " + args[2] + " reloaded")