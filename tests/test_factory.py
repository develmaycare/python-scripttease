import pytest
from scripttease.library.commands import Command, ItemizedCommand
from scripttease.factory import Factory


class TestFactory(object):

    def test_get_command(self):
        f = Factory("ubuntu")
        with pytest.raises(RuntimeError):
            f.get_command("testing")

        f = Factory("ubuntu")
        f.load()

        # Non-existent command.
        c = f.get_command("nonexistent")
        assert c is None

        # A good command with itemized parameters.
        c = f.get_command(
            "pip",
            "$item",
            items=["Pillow", "psycopg2-binary", "django"]
        )
        assert isinstance(c, ItemizedCommand)

        # A good, normal command.
        c = f.get_command("pip", "django")
        assert isinstance(c, Command)

        # Command exists, but given bad arguments.
        c = f.get_command("pip")
        assert c is None

    def test_load(self):
        f = Factory("nonexistent")
        assert f.load() is False

        f = Factory("ubuntu")
        assert f.load() is True

    def test_repr(self):
        f = Factory("centos")
        assert repr(f) == "<Factory centos>"
