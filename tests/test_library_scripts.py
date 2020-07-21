from scripttease.library.commands import Command, ItemizedCommand
from scripttease.library.overlays.posix import Function
from scripttease.library.scripts import Script


class TestScript(object):

    def test_append(self):
        s = Script("testing")
        s.append(Command("ls -ls", comment="list some stuff"))
        s.append(Command("touch /path/to/file.txt", comment="touch a file"))
        s.append(Command("ln -s /path/to/file.txt", comment="link to a file"))

        assert len(s.commands) == 3

    def test_to_string(self):
        s = Script("testing")
        s.append(Command("ls -ls", comment="list some stuff"))
        s.append(Command("touch /path/to/file.txt", comment="touch a file"))
        s.append(Command("ln -s /path/to/file.txt", comment="link to a file"))

        s.functions = list()
        s.functions.append(Function("testing"))

        output = s.to_string()
        assert output == str(s)

        assert "ls -ls" in output
        assert "touch /path/to/file.txt" in output
        assert "ln -s /path/to/file.txt" in output
        assert "function testing()" in output
