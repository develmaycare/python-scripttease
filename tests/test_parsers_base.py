import pytest
from scripttease.library.overlays.posix import touch, Function
from scripttease.library.scripts import Script
# from scripttease.parsers import filter_commands, load_commands
from scripttease.parsers.base import Parser


class TestParser(object):

    def test_as_script(self):
        p = Parser("/path/to/nonexistent.txt")
        assert isinstance(p.as_script(), Script)

    # def test_get_commands(self):
    #     pass
    #
    def test_get_functions(self):
        parser = Parser("/it/does/not/matter.ini")

        command = touch("/path/to/file.txt", function="testing")
        function = Function("testing")
        parser._commands.append(command)
        parser._functions.append(function)

        assert len(parser.get_functions()) == 1

    def test_load(self):
        p = Parser("/path/to/nonexistent.txt")
        with pytest.raises(NotImplementedError):
            p.load()
