import tools

def test_stripPrefix_cases():
    test1 = "!mustikkabot a"
    test2 = "!MustikkaBot a"
    test3 = "!Mustikkabot a"
    test4 = "!mustikkaBot a"

    assert tools.strip_prefix(test1) == "!a"
    assert tools.strip_prefix(test2) == "!a"
    assert tools.strip_prefix(test3) == "!a"
    assert tools.strip_prefix(test4) == "!a"

def test_stripPrefix_nomatch():
    test1 = "!mustikkaot a"
    test2 = "MustikkaBot a"

    assert tools.strip_prefix(test1) == test1
    assert tools.strip_prefix(test2) == test2
