import imp
import os
import re


class modulemanager:
    modules = {}
    bot = None

    coreModulesPath = "core_modules/"
    enabledModulesPath = "modules_enabled/"
    availableModulesPath = "modules/"

    def init(self, bot):
        """
        :param bot:  Reference to the main bot instance
        :type bot: bot

        Initialize the module manager
        """
        self.bot = bot
        self.setupModules()
        self.initModules()

    def importModule(self, file):
        """
        :param file: path to the module to be imported
        :type file: str

        :return: imported module
        :rtype: module

        Load a single module from disk
        """
        fpath = os.path.normpath(os.path.join(os.path.dirname(__file__), file))
        dir, fname = os.path.split(fpath)
        mname, ext = os.path.splitext(fname)

        (file, filename, data) = imp.find_module(mname, [dir])
        return imp.load_module(mname, file, filename, data)

    def loadModule(self, name, path=None):
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

        module = self.importModule(os.path.join(path, name + ".py"))
        self.modules[name] = getattr(module, name)()

    def unloadModule(self,name):
        """
        :param name: Name of the module
        :type name: str

        Unload a module. This does not tell the module it is being unloaded, and it can stay in the memory. Do not call
        directly, but use :meth:disableModule!
        """
        self.modules.pop(name)

    def setupModules(self):
        """
        Go through the enabled modules on disk importing them
        """
        files = os.listdir(self.enabledModulesPath)
        for file in files:
            result = re.search(r'(.*)\.py$', file)
            if result is not None:
                self.loadModule(result.group(1))
        corefiles = os.listdir(self.coreModulesPath)
        for file in corefiles:
            result = re.search(r'(.*)\.py$', file)
            if result is not None:
                self.loadModule(result.group(1), "core_modules/")

    def enableModule(self, name):
        """
        :param name: name of the module
        :type name: str

        Permanently enable a module
        """
        if self.isModuleEnabled(name):
            return

        modules = self.getAvailableModules()

        if not name in modules:
            return

        os.symlink(os.path.abspath(os.path.join(self.availableModulesPath, name + ".py")),
                   os.path.abspath(os.path.join(self.enabledModulesPath, name + ".py")))
        self.loadModule(name)
        self.initModule(name)

    def disableModule(self, name):
        """
        :param name: name of the module
        :type name: str

        Permanently disable a module
        """
        if not self.isModuleEnabled(name):
            return

        self.disposeModule(name)
        self.unloadModule(name)

        allmodules = self.getAvailableModules()
        file = allmodules[name]

        os.remove(os.path.join(self.enabledModulesPath, file))

    def reloadModule(self, name):
        """
        :param name: name of the module
        :type name: str

        Reload a module. Same as :meth:enableModule() && :meth:disableModule()
        """
        self.disableModule(name)
        self.enableModule(name)

    def initModules(self):
        """
        Go through loaded modules initializing them. To be used for example when initially starting up the bot in order
        to allow the modules to do some preparations (like open files and load data), register callbacks and etc.
        """
        for module in self.modules:
            self.initModule(module)

    def disposeModules(self):
        """
        Go through loaded modules and dispose them. To be used for example when shutting down the bot in order to allow
        the modules to close any open resources, save data and etc.
        """

    def initModule(self, name):
        """
        :param name: Name of module
        :type name: str

        Call a module's init(), if it has it. Allows the module to do some preparations like register callbacks
        """
        self.modules[name].init(self.bot)

    def disposeModule(self, name):
        """
        :param name: Name of module
        :type name: str

        Call a module's dispose(), if it has it. Allows the module to prepare to be shut down like close any open
        resources or save data.
        """
        self.modules[name].dispose()

    def getModule(self, name):
        """
        :param name: name of the module
        :type name: str

        :return: reference to the module
        :rtype: module

        Return a reference to specified module
        """
        return self.modules[name]

    def getEnabledModules(self):
        """
        :return: A dict of all loaded modules
        :rtype: dict(str:module)

        Return a dictionary of all the loaded modules {"id":module,...}
        """
        return self.modules

    def getAvailableModules(self):
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

    def isModuleEnabled(self, module):
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