import tools
import logging

class Modules:
    """
    Modules is a core-module that handles the chat frontend to managing non-core modules.
    """

    log = logging.getLogger("mustikkabot.modules")
    bot = None
    acl = "!modules"

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: Bot

        Initialize the modules-module. Register callback to the message received event.
        Called by the modulemanager when loading the module
        """
        self.bot = bot
        bot.accessmanager.register_acl(self.acl, default_groups=["%operators"])
        bot.eventmanager.register_message(self)
        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the eventmanager. Unregisters the messagelisteners
        when the module gets disabled.
        """
        self.bot.eventmanager.unregister_special(self)


    def handle_message(self, data, user, msg):
        """
        :param data: full IRC command
        :param user: user that sent the message
        :param msg: the chat-message the user sent

        Look for any commands that the command-module should handle and handle any found commands.
        Called by the eventmanager/dispatcher when a message is received
        """
        msg = tools.strip_prefix(msg)
        args = msg.split()


        if len(args) < 1:
            return

        if not args[0].lower() == "!modules":
            return

        if not self.bot.accessmanager.is_in_acl(user, self.acl):
            return

        if len(args) == 1:
            self.bot.send_message("Available commands for !modules are: list, enable, disable, reload")
            return

        if args[1].lower() == "enable":
            if len(args) < 3:
                self.bot.send_message("Name of the module is missing. Correct format: !modules enable <name>")
                return
            if self.bot.modulemanager.is_module_enabled(args[2]):
                self.bot.send_message("Module " + args[2] + " is already enabled")
                return
            if args[2] not in self.bot.modulemanager.get_available_modules():
                self.bot.send_message("Module does not exist")
                return
            self.bot.modulemanager.enable_module(args[2])
            self.bot.send_message("Module " + args[2] + " enabled")

        elif args[1].lower() == "disable":
            if len(args) < 3:
                self.bot.send_message("Name of the module is missing. Correct format: !modules disable <name>")
                return
            if not self.bot.modulemanager.is_module_enabled(args[2]):
                self.bot.send_message("Module " + args[2] + " is not enabled")
                return
            if args[2] not in self.bot.modulemanager.get_available_modules():
                self.bot.send_message("Module does not exist")
                return
            self.bot.modulemanager.disable_module(args[2])
            self.bot.send_message("Module " + args[2] + " disabled")

        elif args[1].lower() == "list":
            enabled = list()
            disabled = list()
            for module in self.bot.modulemanager.get_available_modules():
                if self.bot.modulemanager.is_module_enabled(module):
                    enabled.append(module)
                else:
                    disabled.append(module)
            if len(enabled) == 0:
                enabled.append("None")
            if len(disabled) == 0:
                disabled.append("None")
            self.bot.send_message("Currently enabled modules: " + ", ".join(enabled))
            self.bot.send_message("Currently disabled modules: " + ", ".join(disabled))

        elif args[1].lower() == "reload":
            if len(args) < 3:
                self.bot.send_message("Name of the module is missing. Correct format: !modules reload <name>")
                return
            if not self.bot.modulemanager.is_module_enabled(args[2]):
                self.bot.send_message("Module " + args[2] + " does not exists or is not enabled")
                return
            self.bot.modulemanager.reload_module(args[2])
            self.bot.send_message("Module " + args[2] + " reloaded")