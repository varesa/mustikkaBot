import json
import errno
import logging

import tools

class commands:

    log = logging.getLogger("mustikkabot.commands")
    bot = None

    commands = []
    jsonfile = "commands.json"

    helpMessage = "Usage: !commands list | add <cmd> | remove <cmd> | set <cmd> <text> | regulars <cmd> <value>"

    def init(self, bot):
        self.bot = bot
        self.readJSON()
        bot.eventlistener.registerMessage(self)
        self.log.info("Init complete")

    def handleMessage(self, data, user, msg):
        msg = tools.stripPrefix(msg)
        args = msg.split()

        if args[0] == "!commands":
            self.setupCommands(user, args)
        else:
            self.runCommands(user, args)

    def setupCommands(self, user, args):
        if len(args) > 1:
            if args[1] == "list":
                self.listCommands()

            if args[1] == "add":
                self.addCommand(args)

            if args[1] == "set":
                self.setCommand(args)

            if args[1] == "regulars":
                self.setRegulars(args)

            if args[1] == "remove":
                self.removeCommand(args)
        else:
            self.bot.sendMessage(self.helpMessage)

    def runCommands(self, user, args):
        for command in self.commands:
            if "!" + command['name'] == args[0]:
                self.runCommand(command, args, user)

    def runCommand(self, command, args, user):
        if self.bot.accessmanager.isInAcl(user, "commands.!" + command['name']):
            self.bot.sendMessage(command['value'])
            self.log.info("Running command " + command['name'] + ": " + command['value'])

    def readJSON(self):
        jsondata = ""
        try:
            file = open(self.jsonfile, "r")
            jsondata = file.read()
            file.close()
        except IOError as e:
            if e.errno == errno.ENOENT:
                self.log.info("file does not exist, creating")
                self.writeJSON()

        try:
            self.commands = json.loads(jsondata)
        except ValueError:
            self.log.error("commands-file malformed")

    def writeJSON(self):
        file = open(self.jsonfile, "w")
        data = json.dumps(self.commands, sort_keys=True, indent=4, separators=(',', ': '))
        file.write(data)
        file.close()

    def existsCommand(self, cmd):
        """
        :param cmd: Name of a command
        :type cmd: str
        :return: does command exist
        :rtype: bool

        Check if a command exists
        """
        for command in self.commands:
            if command == cmd:
                return True
        return False

    def addCommand(self, args):
        cmd = args[2]

        if not self.existsCommand(cmd):
            self.commands.append({"name": cmd})
            self.bot.accessmanager.registerAcl("commands.!" + cmd)
            self.writeJSON()
            self.bot.sendMessage("Added command " + cmd)
            self.log.info("Added new command:" + cmd)
        else:
            self.bot.sendMessage("Command " + cmd + " already exists")
            self.log.warning("Tried to create a command " + cmd + " that already exists")

    def setCommand(self, args):
        cmd = args[2]
        text = ' '.join(args[3:])

        for command in self.commands:
            if command['name'] == cmd:
                command['value'] = text
                self.writeJSON()
                self.bot.sendMessage("New message for command " + cmd + ": " + text)
                self.log.info("Modified the value of command " + cmd + " to: " + text)
                return
        self.bot.sendMessage("Command " + cmd + " not found")
        self.log.warning("Tried to change the text of a nonexisting command: " + cmd)

    def listCommands(self):
        cmds = ""
        for command in self.commands:
            if cmds is "":
                cmds += command["name"]
            else:
                cmds += ", " + command["name"]

        self.bot.sendMessage("Available commands: " + cmds)

    def setRegulars(self, args):
        if len(args) < 4:
            self.bot.sendMessage("Not enough arguments")
            self.log.warning("Not enough arguments given to \"regulars\" command")
            return

        cmd = args[2]
        if not self.existsCommand(cmd):
            self.bot.sendMessage("No such command as: " + cmd)
            self.log.warning("tried to change the \"regulars\"-value on an invalid command")
            return

        value = args[3].lower()
        if not (value == "on" or value == "off"):
            self.bot.sendMessage("Invalid value for regulars: " + value)
            self.log.warning("Invalid value passed to set-regulars")
            return
        if value == "on":
            self.bot.accessmanager.addGroupToAcl("commands.!" + cmd, "%all%")
        if value == "off":
            self.bot.accessmanager.removeGroupFromAcl("commands.!" + cmd, "%all%")