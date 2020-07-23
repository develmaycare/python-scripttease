from scripttease.library.commands.base import Command, ItemizedCommand, Sudo
from scripttease.library.commands.templates import Template


class TestTemplate(object):

    def test_get_content(self):
        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/simple.txt",
            "tests/tmp/simple.txt",
            backup=False,
            context=context,
            parser=Template.PARSER_SIMPLE
        )
        content = t.get_content()
        assert "I am testing? yes" in content
        assert "How many times? 123" in content

        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/simple.sh.txt",
            "tests/tmp/simple.sh",
            backup=False,
            context=context,
            parser=Template.PARSER_SIMPLE
        )
        content = t.get_content()
        assert "I am testing? yes" in content
        assert "How many times? 123" in content

        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/good.j2.txt",
            "tests/tmp/good.txt",
            backup=False,
            context=context
        )
        content = t.get_content()
        assert "I am testing? yes" in content
        assert "How many times? 123" in content

        t = Template("tests/examples/templates/nonexistent.j2.txt", "test/tmp/nonexistent.txt")
        assert t.get_content() is None

        t = Template("tests/examples/templates/bad.j2.txt", "test/tmp/nonexistent.txt")
        assert t.get_content() is None

    def test_get_statement(self):
        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/simple.txt",
            "tests/tmp/simple.txt",
            context=context,
            parser=Template.PARSER_SIMPLE
        )
        s = t.get_statement()
        assert "I am testing? yes" in s
        assert "How many times? 123" in s

        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/simple.sh.txt",
            "tests/tmp/simple.txt",
            context=context,
            parser=Template.PARSER_SIMPLE
        )
        s = t.get_statement()
        assert "I am testing? yes" in s
        assert "How many times? 123" in s

        context = {
            'testing': "yes",
            'times': 123,
        }
        t = Template(
            "tests/examples/templates/good.j2.txt",
            "tests/tmp/good.txt",
            context=context
        )
        s = t.get_statement()
        assert "I am testing? yes" in s
        assert "How many times? 123" in s

        t = Template(
            "tests/examples/templates/simple.txt",
            "tests/tmp/simple.txt",
            parser="nonexistent"
        )
        assert t.get_statement() is None

    def test_get_template(self):
        t = Template(
            "simple.txt",
            "tests/tmp/simple.txt",
            locations=["tests/examples/templates"]
        )
        assert t.get_template() == "tests/examples/templates/simple.txt"
