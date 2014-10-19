import json
import logging
import os
import datetime
import jsonpickle

import tools
import exceptions


class Command():
    """
    Class to represent a command and its properties
    """
    def __init__(self, name="", value="", repeat=False, repeat_lines=0, repeat_minutes=0):
        self.name = name
        ":type: str"
        self.value = value
        ":type: str"

        self.repeat = repeat
        ":type: bool"
        self.repeat_lines = repeat_lines
        ":type: int"
        self.repeat_minutes = repeat_minutes
        ":type: int"

        self.lastshown_line = None
        ":type: int"
        self.lastshown_time = None
        ":type: datetime.timedelta"


class Commands:
    """
    Module to manage custom commands
    """

    def __init__(self):
        # Logger instance for this module
        self.log = logging.getLogger("mustikkabot.commands")
        ":type: RootLogger"

        # Handle to the root instance
        self.bot = None
        ":type: Bot"

        # Path to the JSON file
        self.jsonpath = None
        ":type: str"

        # Array of the commands loaded
        self.commands = []
        ":type: list of Command"

        # Message line counter for "execute every x lines"
        self.lines_received = 0
        ":type: int"

        # Message to show when called without arguments
        self.helpMessage = "Usage: !commands list | add <cmd> | remove <cmd> | set <cmd> <text> | " \
                           "regulars <cmd> <value> | setrepeat <cmd> <time> [<lines>]"
        ":type: str"
        # Hidden commands: '!commands save' and '!commands load' for managing the JSON

    def init(self, bot):
        """
        Initialize the module when it it loaded. Called by the modulemanager. Registers listeners.

        :param bot: Reference to the main bot instance
        :type bot: Bot
        :rtype: None
        """
        self.bot = bot

        self.jsonpath = os.path.join(self.bot.datadir, "commands.json")

        self.read_JSON()

        for command in self.commands:
            bot.accessmanager.register_acl("commands.!" + command.name)

        bot.eventmanager.register_message(self)
        bot.timemanager.register_interval(self.check_repeats,
                                          datetime.timedelta(seconds=20), datetime.timedelta(seconds=10))

        self.log.info("Init complete")

    def dispose(self):
        """
        Uninitialize the module when called by the modulemanager. Unregisters the messagelisteners
        when the module gets disabled.

        :rtype: None
        """
        self.bot.eventmanager.unregister_message(self)

    def does_command_exist(self, name):
        """
        Check if a command exists

        :param name: Name of command to check
        :type name: str
        :return: does command exist true/false
        :rtype: bool
        """
        for command in self.commands:
            if command.name == name:
                return True
        return False

    def get_command_by_name(self, name):
        """
        Get a command from the array by name. Returns None if command doesn't exist

        :param name: Name of the command to get
        :type name: str
        :return: Command with the name
        :rtype: Command
        """
        for command in self.commands:
            if command.name == name:
                return command
        return None

    def check_repeats(self):
        """
        Timer callback that handles the repeating of commands. Checks line/time conditions

        :rtype: None
        """
        for command in self.commands:
            if command.repeat:
                if command.lastshown_time is None:  # Message has not been shown, do so now
                    self.bot.send_message(command.value)
                    self.log.info("Showed message for command " + command.name + " on repeat")
                    command.lastshown_time = datetime.datetime.now()
                    command.lastshown_line = self.lines_received
                    return                          # Send only one command/cycle to prevent spam

                if command.repeat_minutes > 0:
                    if (datetime.datetime.now() - command.lastshown_time) > \
                            datetime.timedelta(minutes=command.repeat_minutes):
                        timecondition = True
                    else:
                        timecondition = False
                else:
                    timecondition = True

                if command.repeat_lines > 0:
                    if (self.lines_received - command.lastshown_line) >= command.repeat_lines:
                        linecondition = True
                    else:
                        linecondition = False
                else:
                    linecondition = True

                if timecondition and linecondition:
                    self.bot.send_message(command.value)
                    self.log.info("Showed message for command " + command.name + " on repeat")
                    command.lastshown_time = datetime.datetime.now()
                    command.lastshown_line = self.lines_received
                    return  # Send only one command/cycle to prevent spam

    # noinspection PyUnusedLocal
    def handle_message(self, data, user, msg):
        """
        Callback that handles all incoming chat messages for this modules

        :param data: Raw message (unused)
        :type data: str
        :param user: User sending the message
        :type user: str
        :param msg: Actual message content
        :type msg: str
        :rtype: None
        """
        msg = tools.strip_prefix(msg)
        args = msg.split()

        if args[0] == "!commands" or args[0] == "!comm":
            self.setup_commands(user, args)
        else:
            self.run_commands(user, args)

        self.lines_received += 1

    # noinspection PyUnusedLocal
    def setup_commands(self, user, args):
        """
        Hub for different management commands. Command creation/editing/removal
        :param user: Name of the user
        :type user: str
        :param args: Message split into words
        :type args: list of str
        :rtype: None
        """
        if len(args) > 1:
            if args[1] == "list":
                self.list_commands()

            if args[1] == "add":
                self.add_command(args)

            if args[1] == "set":
                self.set_command(args)

            if args[1] == "setrepeat":
                self.set_repeat(args)

            if args[1] == "regulars":
                self.set_regulars(args)

            if args[1] == "remove":
                self.remove_command(args)

            if args[1] == "load":
                self.read_JSON()

            if args[1] == "save":
                self.write_JSON()
        else:
            self.bot.send_message(self.helpMessage)

    def run_commands(self, user, args):
        if self.does_command_exist(args[0][1:]):
            command = self.get_command_by_name(args[0])
            if self.bot.accessmanager.is_in_acl(user, "commands.!" + command.name):
                self.bot.send_message(command.value)
                self.log.info("Running command " + command.value + ": " + command.value)

    # noinspection PyPep8Naming
    def read_JSON(self):
        """
        Read the JSON datafile from disk that contains all saved commands
        :rtype: None
        """

        if not os.path.isfile(self.jsonpath):
            if os.path.isfile(os.path.join(self.bot.basepath, "src", "commands.json")):
                self.log.info("Commands-datafile found at old location, moving")
                if not os.path.isdir(self.bot.datadir):
                    os.mkdir(self.bot.datadir)
                os.rename(os.path.join(self.bot.basepath, "src", "commands.json"), self.jsonpath)
            else:
                self.log.info("Commands-datafile does not exist, creating")
                self.write_JSON()

        try:
            with open(self.jsonpath, "r") as file:
                jsondata = file.read()
        except:
            self.log.error("Could not open " + self.jsonpath)
            raise exceptions.FatalException("Could not open " + self.jsonpath)

        if not 'py/object' in jsondata:
            self.log.info("Commands JSON found in old format, migrating")
            self.migrate_JSON(jsondata)
        else:
            self.commands = jsonpickle.decode(jsondata)
            for command in self.commands:
                command.lastshown_line = None
                command.lastshown_time = None

    # noinspection PyPep8Naming
    def migrate_JSON(self, jsondata):
        try:
            tmp = json.loads(jsondata)
            for command in tmp:
                c = Command(name=command['name'], value=command['value'])
                if 'repeat' in command.keys():
                    c.repeat = command['repeat']
                if 'repeatlines' in command.keys():
                    c.repeat_lines = command['repeatlines']
                if 'repeattime' in command.keys():
                    c.repeat_minutes = command['repeattime']
                self.commands.append(c)
            self.write_JSON()
        except ValueError:
            self.log.error("commands-file malformed")

    # noinspection PyPep8Naming
    def write_JSON(self):
        """
        Write the loaded commands to disk in JSON format
        :rtype: None
        """

        with open(self.jsonpath, "w") as file:
            data = jsonpickle.encode(self.commands)
            file.write(data)

    """
    " User commands
    """

    def add_command(self, args):
        """
        Try adding a new command.
        :param args: Chat message split into array at spaces.
        :type args: list of str

        :rtype: None
        """
        cmd = args[2]

        if not self.does_command_exist(cmd):
            if len(args) > 3:
                text = ' '.join(args[3:])
            else:
                text = ""

            command = Command(name=cmd, value=text)
            self.commands.append(command)

            self.bot.accessmanager.register_acl("commands.!" + cmd)
            self.write_JSON()
            self.bot.send_message("Added command " + cmd)
            self.log.info("Added new command:" + cmd)
        else:
            self.bot.send_message("Command " + cmd + " already exists")
            self.log.warning("Tried to create a command " + cmd + " that already exists")

    def set_command(self, args, quiet=False):
        """
        Try to set the message of a command.

        :param args: Chat message split into array at spaces.
        :type args: list of str
        :param quiet: Whether to output a message to chat
        :type quiet: bool
        :rtype: None
        """
        cmd = args[2]
        text = ' '.join(args[3:])

        if not self.does_command_exist(cmd):
            if not quiet:
                self.bot.send_message("Command " + cmd + " not found")
            self.log.warning("Tried to change the text of a nonexisting command: " + cmd)
        else:
            self.get_command_by_name(cmd).value = text
            self.write_JSON()
            if not quiet:
                self.bot.send_message("New message for command " + cmd + ": " + text)
            self.log.info("Modified the value of command " + cmd + " to: " + text)

    def remove_command(self, args):
        cmd = args[2]

        if self.does_command_exist(cmd):
            self.commands.remove(self.get_command_by_name(cmd))

            self.bot.accessmanager.remove_acl("commands.!" + cmd)
            self.write_JSON()
            self.bot.send_message("Deleted command " + cmd)
            self.log.info("Deleted command:" + cmd)
        else:
            self.bot.send_message("Command " + cmd + " does not exist")
            self.log.warning("Tried to delete a command " + cmd + " that does not exist")

    def list_commands(self):
        cmds = ""
        for command in self.commands:
            if cmds is "":
                cmds += command.name
            else:
                cmds += ", " + command.name

        self.bot.send_message("Available commands: " + cmds)

    def set_regulars(self, args):
        if len(args) < 4:
            self.bot.send_message("Not enough arguments")
            self.log.warning("Not enough arguments given to \"regulars\" command")
            return

        cmd = args[2]
        if not self.does_command_exist(cmd):
            self.bot.send_message("No such command as: " + cmd)
            self.log.warning("tried to change the \"regulars\"-value on an invalid command")
            return

        value = args[3].lower()
        if not (value == "on" or value == "off"):
            self.bot.send_message("Invalid value for regulars: " + value)
            self.log.warning("Invalid value passed to set-regulars")
            return
        if value == "on":
            self.bot.accessmanager.add_group_to_acl("commands.!" + cmd, "%all%")
            self.bot.send_message("Allowed access for regular viewers to command " + cmd)
        if value == "off":
            self.bot.accessmanager.remove_group_from_acl("commands.!" + cmd, "%all%")
            self.bot.send_message("Removed access for regular viewers to command " + cmd)
        self.write_JSON()

    def set_repeat(self, args):
        #args: !commands setrepeat cmd time lines
        if len(args) < 4:
            self.bot.send_message("Not enough arguments. Please use '!commands setrepeat <cmd> <time> [<lines>]'. Zero "
                                  "<time> or <lines> means that the condition is ignored. Zeroing both removes repeat.")
            return

        try:
            cmd = args[2]
            time = int(args[3])
            if len(args) < 5:
                lines = 0
            else:
                lines = int(args[4])

            if time < 0 or lines < 0:
                raise ValueError
        except ValueError:
            self.bot.send_message("Invalid arguments, <time> and <lines> must be numbers 0 or bigger")
            self.log.warning("Invalid non-integer arguments given to setrepeat")
            return

        if not self.does_command_exist(cmd):
            self.bot.send_message("Invalid command name " + cmd)
            self.log.warning("Tried to modify repeat setting for invalid command " + cmd)
            return

        if time == 0 and lines == 0:
            self.get_command_by_name(cmd).repeat = False
            self.bot.send_message("Repetition disabled for command " + cmd)
        else:
            command = self.get_command_by_name(cmd)
            command.repeat = True
            command.repeat_minutes = time
            command.repeat_lines = lines
            self.write_JSON()

            msg = "Repetition enabled for command " + cmd + " every "
            if time:
                msg += str(time) + " minutes"
            if time and lines:
                msg += " and "
            if lines:
                msg += str(lines) + " lines"

            self.bot.send_message(msg)
            self.log.info(msg)
