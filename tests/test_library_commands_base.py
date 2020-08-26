from scripttease.library.commands.base import Command, ItemizedCommand, Sudo
from scripttease.library.overlays.common import python_pip


class TestCommand(object):

    def test_getattr(self):
        c = Command("ls -ls", extra=True)
        assert c.extra is True

    def test_get_statement(self):
        c = Command(
            "ls -ls",
            comment="kitchen sink",
            condition="$last_command -eq 0",
            cd="/path/to/project",
            prefix="source python/bin/active",
            register="list_success",
            stop=True,
            sudo="deploy"
        )
        statement = c.get_statement(cd=True)
        assert "( cd" in statement
        assert "sudo" in statement
        assert ")" in statement
        assert "# kitchen sink" in statement
        assert "if [[ $last_command" in statement
        assert "list_success=$?" in statement
        assert "if [[ $list_success" in statement

        c = Command(
            "ls -ls",
            stop=True
        )
        statement = c.get_statement()
        assert "if [[ $?" in statement

    def test_has_attribute(self):
        c = Command("ls -ls")
        assert c.has_attribute("testing") is False

    def test_init(self):
        c = Command("ls -ls", sudo=Sudo(user="deploy"))
        assert isinstance(c.sudo, Sudo)
        assert c.sudo.user == "deploy"

        c = Command("ls -ls", sudo="deploy")
        assert isinstance(c.sudo, Sudo)
        assert c.sudo.user == "deploy"

        c = Command("ls -ls", sudo=True)
        assert isinstance(c.sudo, Sudo)
        assert c.sudo.user == "root"

        c = Command("ls -ls")
        assert isinstance(c.sudo, Sudo)
        assert c.sudo.user == "root"
        assert c.sudo.enabled is False

    def test_repr(self):
        c = Command("ls -ls", comment="listing")
        assert repr(c) == "<Command listing>"

        c = Command("ls -ls")
        assert repr(c) == "<Command>"

    def test_set_attribute(self):
        c = Command("ls -ls")
        assert c.testing is None
        c.set_attribute("testing", True)
        assert c.testing is True


class TestItemizedCommand(object):

    def test_getattr(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item", extra=True)
        assert c.extra is True

    def test_get_commands(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item")
        commands = c.get_commands()
        for i in commands:
            assert isinstance(i, Command)

    def test_get_statement(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item")
        statement = c.get_statement()
        assert "Pillow" in statement
        assert "psycopg2-binary" in statement
        assert "django" in statement

    def test_has_attribute(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item")
        assert c.has_attribute("testing") is False

    def test_repr(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item")
        assert repr(c) == "<ItemizedCommand python_pip>"

    def test_set_attribute(self):
        c = ItemizedCommand(python_pip, ["Pillow", "psycopg2-binary", "django"], "$item")
        assert c.testing is None
        c.set_attribute("testing", True)
        assert c.testing is True
