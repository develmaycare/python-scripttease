# Imports

from commonkit import indent, parse_jinja_template, read_file, split_csv
from jinja2 import TemplateNotFound, TemplateError
import logging
import os
from ...variables import LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)

# Exports

__all__ = (
    "Command",
    "Content",
    "ItemizedCommand",
    "Prompt",
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


class Content(object):

    def __init__(self, content_type, caption=None, css=None, heading=None, height=None, image=None, message=None,
                 width=None, **kwargs):
        self.caption = caption
        self.css = css
        self.heading = heading
        self.height = height
        self.image = image
        self.message = message
        self.width = width
        self.name = "content"
        self.type = content_type

        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.content_type)

    @property
    def is_itemized(self):
        """Always returns ``False``. Content cannot be itemized."""
        return False

    def get_output(self, output_format):
        if self.content_type == "explain":
            return self._get_message_output(output_format)
        elif self.content_type == "screenshot":
            return self._get_image_output(output_format)
        else:
            log.warning("Invalid content type: %s" % self.content_type)
            return None

    # noinspection PyUnusedLocal
    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Override to return only bash output format."""
        return self.get_output("bash")

    def _get_image_output(self, output_format):
        """Get the output of the content when the content type is an image."""
        a = list()

        if output_format == "bash":
            if self.caption:
                a.append("# %s" % self.caption)

            a.append("# %s" % self.image)
        elif output_format == "html":
            b = list()
            b.append('<img src="%s"' % self.image)
            b.append('alt="%s"' % self.caption or self.comment)

            if self.css is not None:
                b.append('class="%s"' % self.css)

            if self.height is not None:
                b.append('height="%s"' % self.height)

            if self.width is not None:
                b.append('width="%s"' % self.width)

            a.append(" ".join(b) + ">")
        elif output_format == "md":
            a.append("![%s](%s)" % (self.caption or self.comment, self.image))
            a.append("")
        elif output_format == "rst":
            a.append(".. figure:: %s" % self.image)

            if self.caption is not None:
                a.append(indent(":alt: %s" % self.caption, 8))

            if self.height is not None:
                a.append(indent(":height: %s" % self.height, 8))

            if self.height is not None:
                a.append(indent(":height: %s" % self.height, 8))
        else:
            if self.caption:
                a.append("%s: %s" % (self.caption, self.image))
            else:
                a.append(self.image)

        return "\n".join(a)

    def _get_message_output(self, output_format):
        """Get the output of the content when the content type is a message."""
        a = list()

        if output_format == "bash":
            if self.heading:
                a.append("# %s: %s" % (self.heading, self.message))
            else:
                a.append("# %s" % self.message)

            a.append("")
        elif output_format == "html":
            if self.heading:
                a.append("<h2>%s</h2>" % self.heading)

            a.append("<p>%s</p>" % self.message)
        elif output_format == "md":
            if self.heading:
                a.append("## %s" % self.heading)
                a.append("")

            a.append(self.message)
            a.append("")
        elif output_format == "rst":
            if self.heading:
                a.append(self.heading)
                a.append("=" * len(self.heading))
                a.append("")

            a.append(self.message)
            a.append("")
        else:
            if self.heading:
                a.append("***** %s *****" % self.heading)
                a.append("")

            a.append(self.message)
            a.append("")

        return "\n".join(a)


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


class Prompt(Command):
    """Prompt the user for input."""

    def __init__(self, name, back_title="Input", choices=None, default=None, dialog=False, help_text=None, label=None,
                 **kwargs):
        """Initialize a prompt for user input.

        :param name: The variable name.
        :type name: str

        :param back_title: The back title of the input. Used only when ``dialog`` is enabled.
        :type back_title: str

        :param choices: Valid choices for the variable. May be given as a list of strings or a comma separated string.
        :type choices: list[str] | str

        :param default: The default value of the variable.

        :param dialog: Indicates the dialog command should be used.
        :type dialog: bool

        :param help_text: Additional text to display. Only use when ``fancy`` is ``True``.
        :type help_text: str

        :param label: The label of the prompt.

        """
        self.back_title = back_title
        self.default = default
        self.dialog_enabled = dialog
        self.help_text = help_text
        self.label = label or name.replace("_", " ").title()
        self.variable_name = name

        if type(choices) in (list, tuple):
            self.choices = choices
        elif type(choices) is str:
            self.choices = split_csv(choices, smart=False)
        else:
            self.choices = None

        kwargs.setdefault("comment", "prompt user for %s input" % name)

        super().__init__(name, **kwargs)

    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Get the statement using dialog or read."""
        if self.dialog_enabled:
            return self._get_dialog_statement()

        return self._get_read_statement()

    def _get_dialog_statement(self):
        """Get the dialog statement."""
        a = list()

        a.append('dialog --clear --backtitle "%s" --title "%s"' % (self.back_title, self.label))

        if self.choices is not None:
            a.append('--menu "%s" 15 40 %s' % (self.help_text or "Select", len(self.choices)))
            count = 1
            for choice in self.choices:
                a.append('"%s" %s' % (choice, count))
                count += 1

            a.append('2>/tmp/input.txt')
        else:
            if self.help_text is not None:
                a.append('--inputbox "%s"' % self.help_text)
            else:
                a.append('--inputbox ""')

            a.append('8 60 2>/tmp/input.txt')

        b = list()

        b.append('touch /tmp/input.txt')
        b.append(" ".join(a))

        b.append('%s=$(</tmp/input.txt)' % self.variable_name)
        b.append('clear')
        b.append('rm /tmp/input.txt')

        if self.default is not None:
            b.append('if [[ -z "$%s" ]]; then %s="%s"; fi;' % (self.variable_name, self.variable_name, self.default))

        # b.append('echo "$%s"' % self.name)

        return "\n".join(b)

    def _get_read_statement(self):
        """Get the standard read statement."""
        a = list()

        if self.choices is not None:
            a.append('echo "%s "' % self.label)

            options = list()
            for choice in self.choices:
                options.append('"%s"' % choice)

            a.append('options=(%s)' % " ".join(options))
            a.append('select opt in "${options[@]}"')
            a.append('do')
            a.append('    case $opt in')

            for choice in self.choices:
                a.append('        "%s") %s=$opt; break;;' % (choice, self.variable_name))

            # a.append('        %s) %s=$opt;;' % ("|".join(self.choices), self.name))
            a.append('        *) echo "invalid choice";;')
            a.append('    esac')
            a.append('done')

            # a.append("read %s" % self.name)
        else:
            a.append('echo -n "%s "' % self.label)
            a.append("read %s" % self.variable_name)

        if self.default is not None:
            a.append('if [[ -z "$%s" ]]; then %s="%s"; fi;' % (self.variable_name, self.variable_name, self.default))

        # a.append('echo "$%s"' % self.name)

        return "\n".join(a)


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
        if content is None:
            lines.append("# NOT CONTENT AVAILABLE")
            return "\n".join(lines)

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
