import os
import pytest
from scripttease.library.commands import Command, ItemizedCommand
from scripttease.parsers.utils import *


def test_filter_commands():
    commands = [
        Command("apt-get install apache2 -y", environments=["base"], tags=["web"]),
        Command("apt-get install apache-top -y", environments=["live"], tags=["web"]),
        Command("pip install django-debug-toolbar", environments=["development"], tags=["django"]),
        Command("pip install django", environments=["base"], tags=["django"]),
    ]
    f1 = filter_commands(commands, environments=["base", "live"])
    assert len(f1) == 3

    f2 = filter_commands(commands, tags=["django"])
    assert len(f2) == 2

    f3 = filter_commands(commands, environments=["base", "development"])
    assert len(f3) == 3

    f4 = filter_commands(commands, environments=["base"], tags=["web"])
    assert len(f4) == 1


def test_load_commands():
    commands = load_commands("nonexistent.xml")
    assert commands is None

    commands = load_commands("nonexistent.ini")
    assert commands is None

    commands = load_commands("tests/examples/bad_examples.ini")
    assert commands is None

    commands = load_commands(
        "tests/examples/python_examples.ini",
        filters={
            'tags': ["python-support"],
        }
    )
    assert len(commands) == 2


def test_load_variables():
    assert len(load_variables("nonexistent.ini")) == 0

    assert len(load_variables(os.path.join("tests", "examples", "templates", "simple.txt"))) == 0

    variables = load_variables(os.path.join("tests", "examples", "variables.ini"))
    assert len(variables) == 5

    variables = load_variables(os.path.join("tests", "examples", "variables.ini"), environment="testing")
    assert len(variables) == 4


class TestContext(object):

    def test_add(self):
        c = Context()
        c.add("testing", True)
        assert len(c.variables) == 1

        c.add("also_testing", False)
        assert len(c.variables) == 2

        assert isinstance(c.add("still_testing", True), Variable)

        with pytest.raises(RuntimeError):
            c.add("testing", True)

    def test_get(self):
        c = Context(testing=True)
        assert c.get("testing") is True
        assert c.get("nonexistent") is None
        assert c.get("nonexistent", default=True) is True

    def test_getattr(self):
        c = Context(testing=True)
        assert c.testing is True
        assert c.nonexistent is None

    def test_has(self):
        c = Context(testing=True)
        assert c.has("testing") is True
        assert c.has("nonexistent") is False

    def test_init(self):
        c = Context(testing=True, also_testing=123)
        assert len(c.variables) == 2

    def test_join(self):
        c = Context(testing=True)

        variables = [
            Variable("testing", True),
            Variable("also_testing", True),
        ]
        c.join(variables)
        assert len(c.variables) == 2

    def test_mapping(self):
        c = Context(testing=True, also_testing=False, still_testing=True)
        assert type(c.mapping()) is dict
        assert len(c.mapping()) == 3

    def test_merge(self):
        c1 = Context(testing=True, also_testing=False)
        c2 = Context(still_testing=True)
        c1.merge(c2)
        assert len(c1.variables) == 3

    def test_repr(self):
        c = Context(testing=True, also_testing=False, still_testing=True)
        assert repr(c) == "<Context (3)>"


class TestVariable(object):

    def test_eq(self):
        var = Variable("testing", True)
        assert var == True

    def test_getattr(self):
        var = Variable("testing", True, one="a", two="b")
        assert var.one == "a"
        assert var.two == "b"
        assert var.three is None

    def test_repr(self):
        var = Variable("testing", True)
        assert repr(var) == "<Variable testing>"
