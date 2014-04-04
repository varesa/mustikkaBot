import os

from accessmanager import AccessManager


testjsonfile = "mustikkabotacl_test.json"
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
        #self.am.log = None
        self.am.init(None)

    def teardown(self):
        if os.path.exists(testjsonfile):
            os.remove(testjsonfile)

    def test_accessmanager_init(self):
        """assert self.am.acls == {}
        assert self.am.groups == {'%owner': {'members': ['Herramustikka', 'varesa']},
                                  '%moderators': {'members': []},
                                  '%all%': {'members': []},
                                  '%operators': {'members': []} }

        if os.path.exists(testjsonfile):
            os.remove(testjsonfile)"""
        #TODO: test something here?

    def test_accessmanager_json(self):
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
        self.am.groups = {}
        self.am.add_group("grp1")
        assert self.am.groups == {'grp1': {'members': []}}
        self.am.add_group("grp2", "member")
        assert self.am.groups == {'grp2': {'members': ['member']}, 'grp1': {'members': []}}
        self.am.add_group("grp3", ["member1", "member2"])
        assert self.am.groups == {'grp3': {'members': ['member1', 'member2']},
                                  'grp2': {'members': ['member']}, 'grp1': {'members': []}}

    def test_accessmanager_removegroup(self):
        self.am.groups = {}
        self.am.remove_group("grp1")
        assert self.am.groups == {}

        self.am.groups = {'grp2': {'members': ['member']}, 'grp1': {'members': []}}
        self.am.remove_group("grp2")
        assert self.am.groups == {'grp1': {'members': []}}

    def test_accessmanager_existsgroup(self):
        self.am.groups = {}
        self.am.add_group("grp1")

        assert self.am.exists_group("grp1")
        assert not self.am.exists_group("grp2")

    def test_accessmanager_getgroup(self):
        self.am.add_group("getgroup")

        grp = self.am.get_group("getgroup")
        assert grp.name == "getgroup"

    def test_accessmanager_addtogroup(self):
        self.am.add_group("test")
        self.am.add_to_group("test", "user")

        assert self.am.get_group("test").get_members() == ["user"]

    def test_accessmanager_removefromgroup(self):
        self.am.add_group("g1", ["a", "b"])
        self.am.add_group("g2", ["a", "b"])

        self.am.remove_from_group("g1", "a")
        self.am.remove_from_group("g2", "b")

        assert self.am.get_group("g1").get_members() == ["b"]
        assert self.am.get_group("g2").get_members() == ["a"]

    def test_accessmanager_createacl(self):
        self.am.create_acl("a.b.c.*")

        assert self.am.acls["a.b.c.*"] == {"groups": [], "members": []}
        assert not "a.b.c.d" in self.am.acls.keys()

    def test_accessmanager_removeacl(self):
        self.am.create_acl("a")
        self.am.create_acl("b")

        self.am.remove_acl("a")
        self.am.remove_acl("c")

        assert self.am.acls.keys() == ["b"]

    def test_accessmanager_existsacl(self):
        self.am.create_acl("a")

        assert "a" in self.am.acls.keys()
        assert "b" not in self.am.acls.keys()

    def test_accessmanager_registeracl(self):
        self.am.register_acl("acl1")
        self.am.register_acl("acl1")
        self.am.register_acl("acl1")

        assert len(self.am.acls) == 1
        assert "%moderators" in self.am.acls["acl1"]["groups"]
        assert len(self.am.acls["acl1"]["members"]) == 0

        self.am.register_acl("acl2", "a", "b")
        self.am.register_acl("acl3", ["c"], ["d"])

        assert self.am.acls["acl2"]["groups"] == ["a"]
        assert self.am.acls["acl2"]["members"] == ["b"]

        assert self.am.acls["acl3"]["groups"] == ["c"]
        assert self.am.acls["acl3"]["members"] == ["d"]

    def test_accessmanager_addgrouptoacl(self):
        self.am.register_acl("acl", ["a"], [])
        self.am.add_group_to_acl("acl", "b")

        assert self.am.acls["acl"]["groups"] == ["a", "b"]

    def test_accessmanager_removegroupfromacl(self):
        self.am.register_acl("acl", ["a", "b"], [])
        self.am.remove_group_from_acl("acl", "a")

        assert self.am.acls["acl"]["groups"] == ["b"]

    def test_accessmanager_addusertoacl(self):
        self.am.register_acl("acl", [], ["a"])
        self.am.add_user_to_acl("acl", "b")

        assert self.am.acls["acl"]["members"] == ["a", "b"]


