import pytest
from scripttease.parsers.ini import Config


class TestConfig(object):

    def test_get_commands(self):
        c = Config("tests/examples/kitchen_sink.ini")
        assert c.load() is True

        assert len(c.get_commands()) > 0

    def test_get_functions(self):
        c = Config("tests/examples/kitchen_sink.ini")
        assert c.load() is True

        assert len(c.get_functions()) > 0

    def test_load(self):
        c = Config("nonexistent.ini")
        assert c.load() is False

        c = Config("tests/examples/python_examples.ini", overlay="nonexistent")
        assert c.load() is False

        c = Config("tests/examples/bad_examples.ini")
        assert c.load() is False

        c = Config("tests/examples/kitchen_sink.ini")
        assert c.load() is True

        c = Config("tests/examples/kitchen_sink.ini", context={'testing': "yes"})
        assert c.load() is True

        c = Config("tests/examples/bad_command.ini")
        assert c.load() is False

        context = {
            'domain_tld': "example_com",
        }
        c = Config("tests/examples/template_example.ini", context=context)
        assert c.load() is True

        context = {
            'domain_tld': "example_com",
        }
        c = Config("tests/examples/bad_template_example.ini", context=context)
        assert c.load() is False
