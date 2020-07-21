import pytest
from scripttease.library.commands import Command, ItemizedCommand
from scripttease.parsers import filter_commands, load_commands


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
