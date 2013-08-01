import re
import json
import errno

from logging import log, d


class group:
    accessm = None

    name = None

    def __init__(self, accessm, name):
        self.name = name
        self.accessm = accessm

    def getMembers(self):
        return self.accessm.groups[self.name]['members']


class access:
    bot = None

    groups = {}
    acls = {}

    jsonfile = "acls.json"

    def init(self, bot):
        self.bot = bot
        self.readJSON()
        log("[ACCESS] Init complete")

        if len(self.groups) is 0:
            self.addGroup("%owner")
            self.addGroup("%operators")
            self.addGroup("%moderators")
            self.writeJSON()

        self.addToGroup("%owner", "Herramustikka")
        self.addToGroup("%owner", "varesa")

    def readJSON(self):
        jsondata = ""
        try:
            file = open(self.jsonfile, "r")
            jsondata = file.read()
            file.close()
        except IOError as e:
            if e.errno == errno.ENOENT:
                log("[COMMANDS] file does not exist, creating")
                self.writeJSON()

        try:
            data = json.loads(jsondata)
            self.groups = data['groups']
            self.acls = data['acls']
        except ValueError:
            log("[COMMANDS] commands-file malformed")

    def writeJSON(self):
        jsondata = {"groups": self.groups, "acls": self.acls}
        file = open(self.jsonfile, "w")
        data = json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))
        file.write(data)
        file.close()

    def addGroup(self, name, members=None):
        if members is None:
            members = []
        self.groups[name] = {"members": members}
        self.writeJSON()

    def removeGroup(self, name):
        self.groups.pop(name, None)
        self.writeJSON()

    def existsGroup(self, name):
        if name in self.groups.keys():
            return True
        else:
            return False

    def getGroup(self, name):
        if self.existsGroup(name):
            return group(name)
        else:
            return None

    def addToGroup(self, group, name):
        members = self.getGroup(group).getMembers()
        if name not in members:
            members.append(name)
            self.writeJSON()

    def removeFromGroup(self, group, name):
        self.getGroup(group).getMembers().pop(name, None)
        self.writeJSON()

    def createAcl(self, acl):
        self.acls[acl] = {"groups":[], "members":[]}
        self.writeJSON()

    def registerAcl(self, acl, defaultGroups=None,defaultMembers=None):
        self.createAcl(acl)
        if defaultGroups is None and defaultMembers is None:
            self.addGroupToAcl(acl, "%owner")
            self.addGroupToAcl(acl, "%operators")
        else:
            if defaultGroups:
                for group in defaultGroups:
                    self.addGroupToAcl(self,acl, group)
            if defaultMembers:
                for member in defaultMembers:
                    self.addUserToAcl(acl, member)
        self.writeJSON()

    def addGroupToAcl(self, acl, group):
        if not self.existsGroup(group):
            log("[ACCESS] group does not exist")
            return
        self.acls[acl]['groups'].append(group)
        self.writeJSON()

    def addUserToAcl(self, acl, user):
        self.acls[acl]['members'].append(user)
        self.writeJSON()

    def expandGroups(self, groups):
        expanded = []
        expanded += groups

        for group in groups:
            if group is "%operators":
                if "%owner" not in expanded:
                    expanded.append("%owner")
            elif group is "%moderators":
                if "%owner" not in expanded:
                    expanded.append("%owner")
                if "%operators" not in expanded:
                    expanded.append("%operators")
            elif group is not "%owner":
                if "%owner" not in expanded:
                    expanded.append("%owner")
                if "%operators" not in expanded:
                    expanded.append("%operators")
                if "%moderators" not in expanded:
                    expanded.append("%moderators")

        return expanded

    def isInAcl(self, user, acl):
        if user in self.acls[acl]['members']:
            return True

        groups = self.expandGroups(self.acls[acl]['groups'])
        for group in groups:
            if user in self.groups[group]['members']:
                return True

        return False
