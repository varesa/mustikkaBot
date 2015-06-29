import imp
import os
import platform
import re
import sys
import logging

if platform.system() == "Windows":
    import ctypes

import exceptions


class ModuleManager:
    """
    A primary module that manages enabling/disabling/loading of pluggable modules
    """

    log = logging.getLogger("mustikkabot.modulemanager")

    modules = {}
    bot = None

    def __init__(self):
        self.modules = dict()

    def init(self, bot):
        """
        :param bot:  Reference to the main bot instance
        :type bot: Bot

        Initialize the module manager
        """
        self.bot = bot

        self.coreModulesPath = os.path.join(self.bot.srcdir, "core_modules")
        self.enabledModulesPath = os.path.join(self.bot.srcdir, "modules_enabled")
        self.availableModulesPath = os.path.join(self.bot.srcdir, "modules")

        self.setup_modules()
        self.init_modules()

        self.log.info("Init complete")

    def dispose(self):
        self.dispose_modules()
        self.log.info("Disposed")

    def import_module(self, file):
        """
        :param file: path to the module to be imported
        :type file: str

        :return: imported module
        :rtype: module

        Load a single module from disk
        """
        fpath = os.path.abspath(file)
        dir, fname = os.path.split(fpath)
        mname, ext = os.path.splitext(fname)

        (file, filename, data) = imp.find_module(mname, [dir])
        return imp.load_module(mname, file, filename, data)

    def load_module(self, name, path=None):
        """
        :param name: Name of the module
        :type name: str
        :param path: optional path to search for the module, defaults to the availableModules variable
        :type path: str

        Load a module given the filename. This does not initialize the module. Do not call directly, but use
        :meth:enableModule
        """
        if path is None:
            path = self.enabledModulesPath

        module = self.import_module(os.path.join(path, name + ".py"))
        self.modules[name] = getattr(module, name.capitalize())()

    def unload_module(self,name):
        """
        :param name: Name of the module
        :type name: str

        Unload a module. This does not tell the module it is being unloaded, and it can stay in the memory. Do not call
        directly, but use :meth:disableModule!
        """
        self.modules.pop(name)

    def setup_modules(self):
        """
        Go through the enabled modules on disk importing them
        """
        if not os.path.isdir(self.enabledModulesPath):
            if not os.path.exists(self.enabledModulesPath):
                self.log.info("Directory for enabled modules does not exist, creating")
                os.mkdir(self.enabledModulesPath)
            else:
                self.log.error("There is something wrong with the enabled modules dir: "
                               + self.enabledModulesPath + ", exiting")
                sys.exit()

        files = os.listdir(self.enabledModulesPath)
        for file in files:
            result = re.search(r'(.*)\.py$', file)
            if result is not None:
                self.load_module(result.group(1))
        corefiles = os.listdir(self.coreModulesPath)
        for file in corefiles:
            result = re.search(r'(.*)\.py$', file)
            if result is not None:
                self.load_module(result.group(1), self.coreModulesPath)

    def create_symlink(self, src, dst):
        """
        Platform independent symlink creation
        :param src: symlink source
        :type src: str
        :param dst: symlink destination
        :type dst: str
        :return: None
        :rtype: None
        """
        if platform.system() != "Windows":
            os.symlink(src, dst)
        else:
            ret = ctypes.windll.kernel32.CreateSymbolicLinkW(dst, src, 0)
            if ret == 0:
                self.log.error("Could not create symlink. NOTE: "
                               "By default only the Administrator has permission to create symlinks")
                raise exceptions.FatalException()

    def enable_module(self, name):
        """
        :param name: name of the module
        :type name: str

        Permanently enable a module
        """
        if self.is_module_enabled(name):
            return

        modules = self.get_available_modules()

        if not name in modules:
            return

        self.create_symlink(os.path.abspath(os.path.join(self.availableModulesPath, name + ".py")),
                            os.path.abspath(os.path.join(self.enabledModulesPath, name + ".py")))

        self.load_module(name)
        self.init_module(name)

    def disable_module(self, name):
        """
        :param name: name of the module
        :type name: str

        Permanently disable a module
        """
        if not self.is_module_enabled(name):
            return

        if self.is_core_module(name):
            raise Exception("Cannot disable a core-module")

        self.dispose_module(name)
        self.unload_module(name)

        os.remove(os.path.join(self.enabledModulesPath, name + ".py"))

    def reload_module(self, name):
        """
        :param name: name of the module
        :type name: str

        Reload a module. Same as :meth:enableModule() && :meth:disableModule()
        """
        self.disable_module(name)
        self.enable_module(name)

    def init_modules(self):
        """
        Go through loaded modules initializing them. To be used for example when initially starting up the bot in order
        to allow the modules to do some preparations (like open files and load data), register callbacks and etc.
        """
        for module in self.modules:
            self.init_module(module)

    def dispose_modules(self):
        """
        Go through loaded modules and dispose them. To be used for example when shutting down the bot in order to allow
        the modules to close any open resources, save data and etc.
        """
        for module in self.modules.keys():
            self.dispose_module(module)

    def init_module(self, name):
        """
        :param name: Name of module
        :type name: str

        Call a module's init(), if it has it. Allows the module to do some preparations like register callbacks
        """
        try:
            self.modules[name].init(self.bot)
        except AttributeError:
            pass # Only call init if it is implemented

    def dispose_module(self, name):
        """
        :param name: Name of module
        :type name: str

        Call a module's dispose(), if it has it. Allows the module to prepare to be shut down like close any open
        resources or save data.
        """
        try:
            self.modules[name].dispose()
        except AttributeError:
            pass # Only call dispose if it is implemented

    def get_module(self, name):
        """
        :param name: name of the module
        :type name: str

        :return: reference to the module
        :rtype: module

        Return a reference to specified module
        """
        return self.modules[name]

    def get_enabled_modules(self):
        """
        :return: A dict of all loaded modules
        :rtype: dict(str:module)

        Return a dictionary of all the loaded modules {"id":module,...}
        """
        return self.modules

    def get_available_modules(self):
        """
        :return: dictionary of available modules and their filenames
        :rtype: dictionary of strings

        Get a list of modules available, whether they are enabled or not
        """
        modules = list()

        files = os.listdir(self.availableModulesPath)
        for file in files:
            result = re.search(r'(.*)\.py$', file)
            if result is not None:
                modules.append(result.group(1))

        return modules

    def is_module_enabled(self, module):
        """
        :param module: name of the module
        :type module: str

        :return: is module enabled
        :rtype: bool

        Checks if a module is enabled
        """
        if module in self.modules.keys():
            return True
        else:
            return False

    def is_core_module(self, name):
        """
        :param name: name of the module
        :type name: str

        :return: is the module "core"?
        :rtype: bool

        Checks if a module belongs to the unloadable core-modules
        """
        if name + ".py" in os.listdir(self.coreModulesPath):
            return True
        else:
            return False