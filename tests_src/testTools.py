import tools

def test_stripPrefix_cases():
    test1 = "!mustikkabot a"
    test2 = "!MustikkaBot a"
    test3 = "!Mustikkabot a"
    test4 = "!mustikkaBot a"

    assert tools.stripPrefix(test1) == "!a"
    assert tools.stripPrefix(test2) == "!a"
    assert tools.stripPrefix(test3) == "!a"
    assert tools.stripPrefix(test4) == "!a"

def test_stripPrefix_nomatch():
    test1 = "!mustikkaot a"
    test2 = "MustikkaBot a"

    assert tools.stripPrefix(test1) == test1
    assert tools.stripPrefix(test2) == test2
