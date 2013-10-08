import os

from accessmanager import AccessManager


testjsonfile = "/tmp/mustikkabotacl_test.json"
"""
:type : accessmanager
"""

class test_accessmanager():

    am = None

    def setup(self):
        if os.path.exists(testjsonfile):
            os.remove(testjsonfile)

        self.am = AccessManager()
        self.am.jsonfile = testjsonfile

    def destroy(self):
        if os.path.exists(testjsonfile):
            os.remove(testjsonfile)

    def test_accessmanager_init(self):

        self.am.init(None)

        assert self.am.acls == {}
        assert self.am.groups == {'%owner': {'members': ['Herramustikka', 'varesa']},
                                  '%moderators': {'members': []},
                                  '%all%': {'members': []},
                                  '%operators': {'members': []} }

        if os.path.exists(testjsonfile):
            os.remove(testjsonfile)

    def test_accessmanager_json(self):

        self.am.jsonfile = testjsonfile
        self.am.init(None)

        acls = {"a": "b", "c": {"d": [1, 2 ,"3"]}}
        groups = {"A": "B", "C": {"D": [10, 20 ,"30"]}}

        self.am.acls = acls
        self.am.groups = groups

        self.am.write_JSON()

        self.am.acls = None
        self.am.groups = None

        self.am.read_JSON()

        assert self.am.acls == acls
        assert self.am.groups == groups

    def test_accessmanager_addgroup(self):
        self.am.init(None)

        self.am.groups = {}
        self.am.add_group("grp1")
        assert self.am.groups == {'grp1': {'members': []}}
        self.am.add_group("grp2", "member")
        assert self.am.groups == {'grp2': {'members': ['member']}, 'grp1': {'members': []}}
        self.am.add_group("grp3", ["member1","member2"])
        assert self.am.groups == {'grp3': {'members': ['member1', 'member2']},
                                  'grp2': {'members': ['member']}, 'grp1': {'members': []}}

    def test_accessmanager_removegroup(self):
        self.am.init(None)

        self.am.groups = {}
        self.am.remove_group("grp1")
        assert self.am.groups == {}

        self.am.groups = {'grp2': {'members': ['member']}, 'grp1': {'members': []}}
        self.am.remove_group("grp2")
        assert self.am.groups == {'grp1': {'members': []}}

    def test_accessmanager_existsgroup(self):
        self.am.init(None)

        self.am.groups = {}
        self.am.add_group("grp1")

        assert self.am.exists_group("grp1")
        assert not self.am.exists_group("grp2")



