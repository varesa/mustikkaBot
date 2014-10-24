import tools
import os

def test_strip_prefix_cases():
    test1 = "!mustikkabot a"
    test2 = "!MustikkaBot a"
    test3 = "!Mustikkabot a"
    test4 = "!mustikkaBot a"

    assert tools.strip_name(test1) == "!a"
    assert tools.strip_name(test2) == "!a"
    assert tools.strip_name(test3) == "!a"
    assert tools.strip_name(test4) == "!a"


def test_strip_prefix_nomatch():
    test1 = "!mustikkaot a"
    test2 = "MustikkaBot a"

    assert tools.strip_name(test1) == test1
    assert tools.strip_name(test2) == test2


def test_find_basepath():
    testfile = __file__
    real_base = os.path.join(os.path.dirname(testfile), "..")

    os.chdir(real_base)
    assert os.path.abspath(tools.find_basepath()) == os.path.abspath(real_base)
    os.chdir(os.path.join(real_base, "src"))
    assert os.path.abspath(tools.find_basepath()) == os.path.abspath(real_base)

    os.chdir(os.path.dirname(__file__))