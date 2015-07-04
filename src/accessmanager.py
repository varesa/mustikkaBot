import json
import errno
import logging
import shutil
import os

import exceptions


class Group:
    accessm = None

    name = None

    def __init__(self, name):
        self.name = name

        global accessmodule
        self.accessm = accessmodule

    def get_members(self):
        return self.accessm.groups[self.name]['members']


class AccessManager:
    bot = None

    log = logging.getLogger("mustikkabot.accessmanager")

    jsonname = "acls.json"
    jsonpath = None

    groups = {}
    acls = {}

    def __init__(self):
        self.acls = dict()
        self.groups = dict()

    def init(self, bot):
        """
        :param bot: Reference to the main bot instance
        :type bot: Bot

        Initialize the access-module
        """
        self.bot = bot

        self.jsonpath = os.path.join(self.bot.datadir, self.jsonname)

        global accessmodule
        accessmodule = self

        self.read_JSON()

        changed = False

        for group in self.groups:
            for member in self.groups[group]['members']:
                if member.lower() != member:
                    self.groups[group]['members'].remove(member)
                    self.groups[group]['members'].append(member.lower())
                    changed = True

        for acl in self.acls:
            for member in self.acls[acl]['members']:
                if member.lower() != member:
                    self.acls[acl]['members'].remove(member)
                    self.acls[acl]['members'].append(member.lower())
                    changed = True

        if changed:
            self.write_JSON()

        self.log.info("Init complete")

        if len(self.groups) is 0:
            self.add_group("%owner")
            self.add_group("%operators")
            self.add_group("%moderators")
            self.add_group("%all%")
            self.write_JSON()

    def dispose(self):
        self.log.info("Disposed")

    # noinspection PyPep8Naming
    def read_JSON(self):
        """
        Read the access-data from a JSON file
        """
        if not os.path.isfile(self.jsonpath):
            if os.path.isfile(os.path.join(self.bot.srcdir, "acls.json")):
                self.log.info("ACL-datafile found at old location, moving")
                os.rename(os.path.join(self.bot.srcdir, "acls.json"),self.jsonpath)
            else:
                self.log.info("ACL-datafile does not exist, creating")
                self.write_JSON()

        jsondata = ""
        try:
            file = open(self.jsonpath, "r")
            jsondata = file.read()
            file.close()
        except:
            raise exceptions.FatalException

        try:
            data = json.loads(jsondata)
            self.groups = data['groups']
            self.acls = data['acls']
        except ValueError:
            self.log.error("acls-file malformed")
            shutil.copyfile(self.jsonpath, self.jsonpath + ".bak")

    # noinspection PyPep8Naming
    def write_JSON(self):
        """
        Write the access-data to a JSON file
        """
        jsondata = {"groups": self.groups, "acls": self.acls}
        file = open(self.jsonpath, "w")
        data = json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))
        file.write(data)
        file.close()

    def add_group(self, group, members=None):
        """
        :param group: Name of the group to be created
        :type group: str
        :param members: Optional list of members to initialize the group with
        :type members: list(str)

        Create a new group and optionally add members to it
        """
        group = group.lower()
        if members is None:
            members = []
        elif isinstance(members, tuple):
            members = list(members)
        elif not isinstance(members, list):
            tmp = members
            members = list()
            members.append(tmp)
        members = [member.lower() for member in members]
        self.groups[group] = {"members": members}
        self.write_JSON()

    def remove_group(self, group):
        """
        :param group: Name of the group to be removed
        :type group: str

        Remove a group if it exists
        """
        group = group.lower()
        self.groups.pop(group, None)
        self.write_JSON()

    def exists_group(self, group):
        """
        :param group: Name of the group to check
        :type group: str

        :return: Does the group exists
        :rtype: bool

        Check if a group exists
        """
        group = group.lower()
        if group in self.groups.keys():
            return True
        else:
            return False

    def get_group(self, group):
        """
        :param name: Name of the group
        :type name: str

        :return: An instance of the group specified
        :rtype: Group

        Return an instance of the :class:group describing the specified group
        """
        group = group.lower()
        if self.exists_group(group):
            return Group(group)
        else:
            return None

    def add_to_group(self, group, name):
        """
        :param group: Name of the group
        :type group: str
        :param name: Name of the person
        :type name: str

        Add a person to a group
        """
        group = group.lower()
        name = name.lower()
        members = self.get_group(group).get_members()
        if name not in members:
            members.append(name)
            self.write_JSON()

    def remove_from_group(self, group, name):
        """
        :param group: Name of the group
        :type group: str
        :param name: Name of the person
        :type name: str

        Remove a person from a group
        """
        group = group.lower()
        name = name.lower()

        self.get_group(group).get_members().remove(name)
        self.write_JSON()

    def create_acl(self, acl):
        """
        :param acl: Name of the acl
        :type acl: str

        Create a new acl
        """
        self.acls[acl] = {"groups": [], "members": []}
        self.write_JSON()

    def remove_acl(self, acl):
        self.acls.pop(acl, None)
        self.log.info("Removed acl: " + acl)

    def exists_acl(self, acl):
        """
        :param acl: Name of the ACL
        :type acl: str

        :return: does the acl exist?
        :rtype: bool

        Check if the ACL exists
        """
        if acl in self.acls.keys():
            return True
        else:
            return False

    def register_acl(self, acl, default_groups=None, default_members=None):
        """
        :param acl: name of the acl
        :type acl: str
        :param default_groups: optional list of groups to add to the acl
        :type default_groups: list(str)
        :param default_members: optional list of members to add to the acl
        :type default_members: list(str)

        Register an acl. Create a new one with the defaults if it does not exist
        """
        if not self.exists_acl(acl):
            self.create_acl(acl)
            if default_groups is None and default_members is None:
                #self.add_group_to_acl(acl, "%owner")
                #self.add_group_to_acl(acl, "%operators")
                self.add_group_to_acl(acl, "%moderators")
            else:
                if default_groups:
                    if type(default_groups) != type(list()) and type(default_groups) != type(tuple()):
                        default_groups = [default_groups]
                    for group in default_groups:
                        self.add_group_to_acl(acl, group)
                if default_members:
                    if type(default_members) != type(list()) and type(default_members) != type(tuple()):
                        default_members = [default_members]
                    for member in default_members:
                        self.add_user_to_acl(acl, member)
            self.write_JSON()

    def add_group_to_acl(self, acl, group):
        """
        :param acl: name of the acl
        :type acl: str
        :param group: name of the group
        :type group: str

        Add a group to the acl
        """
        group = group.lower()

        if not self.exists_group(group):
            self.log.warning("Called group does not exist")
            return
        if not group in self.acls[acl]['groups']:
            self.acls[acl]['groups'].append(group)
        else:
            self.log.warning("Called group is already in acl")
        self.write_JSON()

    def remove_group_from_acl(self, acl, group):
        """
        :param acl: name of the acl
        :type acl: str
        :param group: name of the group
        :type group: str

        Remove a group from an acl if possible
        """
        group = group.lower()
        self.acls[acl]['groups'].remove(group)

    def add_user_to_acl(self, acl, user):
        """
        :param acl: name of the acl
        :type acl: str
        :param user: name of the user
        :type user: str

        Add a user to the acl
        """
        user = user.lower()
        if not user in self.acls[acl]['members']:
            self.acls[acl]['members'].append(user)
            self.write_JSON()

    def remove_user_from_acl(self, acl, user):
        """
        :param acl: name of the acl
        :type acl: str
        :param user: name of the user
        :type user: str

        Remove a user from an acl if possible
        """
        user = user.lower()
        self.acls[acl]['members'].remove(user)

    def expand_groups(self, groups):
        """
        :param groups: list of the groups
        :type groups: list(str)

        :return: expanded list of groups
        :rtype: list(str)

        Expand a list of groups, so that all groups with higher level of privileges get permissions,
        if a lower group has them
        """

        if type(groups) != type(list()) and type(groups) != type(tuple()):
            groups = [groups]

        expanded = []
        expanded += groups

        for group in groups:
            if group == "%operators":
                if "%owner" not in expanded:
                    expanded.append("%owner")
            elif group == "%moderators":
                if "%owner" not in expanded:
                    expanded.append("%owner")
                if "%operators" not in expanded:
                    expanded.append("%operators")
            elif group == "%all":
                if "%owner" not in expanded:
                    expanded.append("%owner")
                if "%operators" not in expanded:
                    expanded.append("%operators")
                if "%moderators" not in expanded:
                    expanded.append("%moderators")

        return expanded

    def is_in_acl(self, user, acl):
        """
        :param user: name of the user
        :type user: str
        :param acl: name of the acl
        :type acl: str

        :return: has the user permissions
        :rtype: bool

        Check if a user is in an acl, either directly or through a group
        """
        if not acl in self.acls.keys():
            raise Exception("ACL does not exist")

        user = user.lower()

        if user == 'cli':
            return True                                             # Give local users all permissions

        if user in self.get_group("%owner").get_members():          # Always allow owner
            return True

        if "%all%" in self.acls[acl]["groups"]:                     # Acl allows everyone
            return True

        if user in self.acls[acl]['members']:                       # User is allowed
            return True

        groups = self.expand_groups(self.acls[acl]['groups'])
        for group in groups:
            if user.lower() in self.groups[group]['members']:       # User is member of allowed group
                return True

        return False
