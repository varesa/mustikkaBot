import imp
import os
import re


class modulemanager:
    modules = {}
    bot = None

    enabledModulesPath = "modules_enabled/"
    availableModulesPath = "modules"

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

    def setupModules(self):
        """
        Go through the modules on disk importing them
        """
        files = os.listdir(self.enabledModulesPath)
        for file in files:
            result = re.search(r'\.py$', file)
            if result is not None:
                module = self.importModule(os.path.join(self.enabledModulesPath, file))
                id = module.getId()
                self.modules[id] = getattr(module, id)()

    def addModule(self, name):
        """
        :param name: Name of the module
        :type name: str

        Load a module by name
        """
        file = self.enabledModulesPath + name + ".py"
        if os.path.exists(file):
            module = self.importModule(file)
            id = module.getId()
            self.modules[id] = getattr(module, id)()

    def removeModule(self, id):
        """
        :param id: Id of the module
        :type id: str

        Unload a module by name
        """
        self.modules.pop(id, None)

    def initModules(self):
        """
        Go through loaded modules initializing them
        """
        for name, module in self.modules.items():
            module.init(self.bot)

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
        :return: list of available modules
        :rtype: list of strings

        Get a list of modules available, whether they are enabled or not
        """
        modules = list()

        files = os.listdir(self.availableModulesPath)
        for file in files:
            result = re.search(r'\.py$', file)
            if result is not None:
                modules.append(file)
        return modules