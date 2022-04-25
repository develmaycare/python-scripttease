# Imports

from commonkit import parse_jinja_template, read_file
from jinja2 import TemplateNotFound, TemplateError
import logging
import os

log = logging.getLogger(__name__)

# Exports

__all__ = (
    "Command",
    "ItemizedCommand",
    "Sudo",
    "Template",
)

# Classes


class Command(object):

    def __init__(self, statement, cd=None, comment=None, condition=None, name=None, prefix=None, register=None, stop=False, sudo=None, tags=None, **kwargs):
        self.cd = cd
        self.comment = comment
        self.condition = condition
        self.name = name
        self.number = None
        self.prefix = prefix
        self.register = register
        self.statement = statement
        self.stop = stop
        self.tags = tags or list()

        if isinstance(sudo, Sudo):
            self.sudo = sudo
        elif type(sudo) is str:
            self.sudo = Sudo(enabled=True, user=sudo)
        elif sudo is True:
            self.sudo = Sudo(enabled=True)
        else:
            self.sudo = Sudo()

        self.options = kwargs

    def __getattr__(self, item):
        return self.options.get(item)

    def __repr__(self):
        if self.comment:
            return "<%s %s>" % (self.__class__.__name__, self.comment)

        return "<%s>" % self.__class__.__name__

    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Get the full statement.

        :param cd: Include the directory change, if given.
        :type cd: bool

        :param suppress_comment: Don't include the comment.
        :type suppress_comment: bool

        :rtype: str

        """
        a = list()

        if cd and self.cd is not None:
            a.append("( cd %s &&" % self.cd)

        if self.prefix is not None:
            a.append("%s &&" % self.prefix)

        if self.sudo:
            statement = "%s %s" % (self.sudo, self._get_statement())
        else:
            statement = self._get_statement()

        a.append("%s" % statement)

        if cd and self.cd is not None:
            a.append(")")

        b = list()
        if self.comment is not None and include_comment:
            b.append("# %s" % self.comment)

        if self.condition is not None:
            b.append("if [[ %s ]]; then %s; fi;" % (self.condition, " ".join(a)))
        else:
            b.append(" ".join(a))

        if self.register is not None and include_register:
            b.append("%s=$?;" % self.register)

            if self.stop and include_stop:
                b.append("if [[ $%s -gt 0 ]]; exit 1; fi;" % self.register)
        elif self.stop and include_stop:
            b.append("if [[ $? -gt 0 ]]; exit 1; fi;")
        else:
            pass

        return "\n".join(b)

    @property
    def is_itemized(self):
        """Always returns ``False``."""
        return False

    def _get_statement(self):
        """By default, get the statement passed upon command initialization.

        :rtype: str

        """
        return self.statement


class ItemizedCommand(object):
    """An itemized command represents multiple commands of with the same statement but different parameters."""

    def __init__(self, callback, items, *args, **kwargs):
        """Initialize the command.

        :param callback: The function to be used to generate the command.

        :param items: The command arguments.
        :type items: list[str]

        :param name: The name of the command from the mapping. Not used and not required for programmatic use, but
                     automatically assigned during factory instantiation.
        :type name: str

        :param args: The itemized arguments. ``$item`` should be included.

        Keyword arguments are passed to the command class upon instantiation.

        """
        self.args = args
        self.callback = callback
        self.items = items
        self.kwargs = kwargs

        # Set defaults for when ItemizedCommand is referenced directly before individual commands are instantiated. For
        # example, when command filtering occurs.
        self.kwargs.setdefault("tags", list())

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.callback.__name__)

    def get_commands(self):
        """Get the commands to be executed.

        :rtype: list[BaseType(Command)]

        """
        kwargs = self.kwargs.copy()

        a = list()
        for item in self.items:
            args = list()
            for arg in self.args:
                args.append(arg.replace("$item", item))

            command = self.callback(*args, **kwargs)
            a.append(command)

        return a

    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Override to get multiple commands."""
        kwargs = self.kwargs.copy()
        comment = kwargs.pop("comment", "execute multiple commands")

        a = list()

        if include_comment:
            a.append("# %s" % comment)

        commands = self.get_commands()
        for c in commands:
            a.append(c.get_statement(cd=cd, include_comment=False, include_register=include_register, include_stop=include_stop))

        return "\n".join(a)

    @property
    def is_itemized(self):
        """Always returns ``True``."""
        return True


class Sudo(object):
    """Helper class for defining sudo options."""

    def __init__(self, enabled=False, user="root"):
        """Initialize the helper.

        :param enabled: Indicates sudo is enabled.
        :type enabled: bool

        :param user: The user to be invoked.
        :type user: str

        """
        self.enabled = enabled
        self.user = user

    def __bool__(self):
        return self.enabled

    def __str__(self):
        if self.enabled:
            return "sudo -u %s" % self.user

        return ""


class Template(object):

    PARSER_JINJA = "jinja2"
    PARSER_PYTHON = "python"
    PARSER_SIMPLE = "simple"

    def __init__(self, source, target, backup=True, parser=PARSER_JINJA, **kwargs):
        self.backup_enabled = backup
        self.context = kwargs.pop("context", dict())
        self.name = "template"
        self.parser = parser
        self.language = kwargs.pop("lang", None)
        self.locations = kwargs.pop("locations", list())
        self.source = os.path.expanduser(source)
        self.target = target

        sudo = kwargs.pop("sudo", None)
        if isinstance(sudo, Sudo):
            self.sudo = sudo
        elif type(sudo) is str:
            self.sudo = Sudo(enabled=True, user=sudo)
        elif sudo is True:
            self.sudo = Sudo(enabled=True)
        else:
            self.sudo = Sudo()

        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def __str__(self):
        return "template"

    def get_content(self):
        """Parse the template.

        :rtype: str | None

        """
        template = self.get_template()

        if self.parser == self.PARSER_SIMPLE:
            content = read_file(template)
            for key, value in self.context.items():
                replace = "$%s$" % key
                content = content.replace(replace, str(value))

            return content

        if self.parser == self.PARSER_PYTHON:
            content = read_file(template)
            return content % self.context

        try:
            return parse_jinja_template(template, self.context)
        except TemplateNotFound:
            log.error("Template not found: %s" % template)
            return None
        except TemplateError as e:
            log.error("Could not parse %s template: %s" % (template, e))
            return None

    # noinspection PyUnusedLocal
    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        lines = list()
        if include_comment and self.comment is not None:
            lines.append("# %s" % self.comment)

        # TODO: Backing up a template's target is currently specific to bash.
        if self.backup_enabled:
            command = "%s mv %s %s.b" % (self.sudo, self.target, self.target)
            lines.append('if [[ -f "%s" ]]; then %s; fi;' % (self.target, command.lstrip()))

        # Get the content; e.g. parse the template.
        content = self.get_content()

        # Templates that are bash scripts will fail to write because of the shebang.
        if content.startswith("#!"):
            _content = content.split("\n")
            first_line = _content.pop(0)
            command = '%s echo "%s" > %s' % (self.sudo, first_line, self.target)
            lines.append(command.lstrip())
            command = "%s cat > %s << EOF" % (self.sudo, self.target)
            lines.append(command.lstrip())
            lines.append("\n".join(_content))
            lines.append("EOF")
        else:
            command = "%s cat > %s << EOF" % (self.sudo, self.target)
            lines.append(command.lstrip())
            lines.append(content)
            lines.append("EOF")

        if include_register and self.register is not None:
            lines.append("%s=$?;" % self.register)

            if include_stop and self.stop:
                lines.append("if [[ $%s -gt 0 ]]; exit 1; fi;" % self.register)
        elif include_stop and self.stop:
            lines.append("if [[ $? -gt 0 ]]; exit 1; fi;")
        else:
            pass

        return "\n".join(lines)

    def get_target_language(self):
        if self.language is not None:
            return self.language

        if self.target.endswith(".conf"):
            return "conf"
        elif self.target.endswith(".ini"):
            return "ini"
        elif self.target.endswith(".php"):
            return "php"
        elif self.target.endswith(".py"):
            return "python"
        elif self.target.endswith(".sh"):
            return "bash"
        elif self.target.endswith(".yml"):
            return "yaml"
        else:
            return "text"

    def get_template(self):
        """Get the template path.

        :rtype: str

        """
        source = self.source
        for location in self.locations:
            _source = os.path.join(location, self.source)
            if os.path.exists(_source):
                return _source

        return source

    @property
    def is_itemized(self):
        # return "$item" in self.target
        return False
