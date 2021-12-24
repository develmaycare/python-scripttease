# Imports

from commonkit import parse_jinja_string, parse_jinja_template, pick, read_file, smart_cast, split_csv, File
from jinja2.exceptions import TemplateError, TemplateNotFound
import logging
import os
from ..library.snippets.mappings import MAPPINGS

log = logging.getLogger(__name__)

# Exports

__all__ = (
    "BaseLoader",
)

# Classes


class BaseLoader(File):

    def __init__(self, path,  context=None, locations=None, mappings=None, profile="ubuntu", **kwargs):
        self.context = context or dict()
        self.is_loaded = False
        self.locations = locations or list()
        self.mappings = mappings or MAPPINGS
        self.options = kwargs
        self.profile = profile
        self.snippets = list()

        # Always include the path to the current file in locations.
        self.locations.insert(0, self.directory)

        super().__init__(path)

    def get_snippets(self):
        a = list()

        for canonical_name, args, kwargs in self.snippets:
            snippet = self.find_snippet(canonical_name, *args, **kwargs)
            a.append(snippet)

        return a

    def find_snippet(self, name, *args, **kwargs):
        # Templates require special handling.
        if name == "template":
            source = args[0]
            target = args[1]
            kwargs['locations'] = self.locations
            return Template(source, target, **kwargs)

        # Convert args to a list so we can update it below.
        _args = list(args)

        # The given name is not in the mappings -- which is a typo or invalid name -- but it could also be a dotted path
        # to be followed down through the dictionary structure.
        if name not in self.mappings[self.profile]:
            if "." in name:
                return self.find_snippet_by_dotted_name(name, *args, **kwargs)

            log.error("Command not found in mappings: %s" % name)
            return Snippet(name, args=_args, kwargs=kwargs)

        # Formal or informal sub-commands exist in a dictionary.
        if type(self.mappings[self.profile][name]) is dict:
            try:
                possible_sub_command = _args[0]
            except IndexError:
                log.warning("No sub-command argument for: %s" % name)
                return Snippet(name)

            if possible_sub_command in self.mappings[self.profile][name]:
                sub = _args.pop(0)
                snippet = self.mappings[self.profile][name][sub]

                parser = self.mappings[self.profile][name].get('_parser', None)

                _name = "%s.%s" % (name, sub)
                return Snippet(_name, args=_args, content=snippet, context=self.context, kwargs=kwargs, parser=parser)

            # Django allows pre-defined as well as adhoc commands. The name of the command is provided as the first
            # argument in the config file. The following statements are only invoked if the possible_sub_command is not
            # in the django dictionary.
            if name == "django":
                sub = _args.pop(0)
                kwargs['_name'] = sub
                print(kwargs)
                snippet = self.mappings[self.profile]['django']['command']
                parser = self.mappings[self.profile]['django']['_parser']
                return Snippet("django.%s" % sub, args=_args, content=snippet, context=self.context, kwargs=kwargs,
                               parser=parser)

            log.warning("Sub-command could not be determined for: %s" % name)
            return Snippet(name, args=list(args), context=self.context, kwargs=kwargs)

        # The found snippet should just be a string.
        return Snippet(name, args=list(args), content=self.mappings[self.profile][name], kwargs=kwargs)

    def find_snippet_by_dotted_name(self, name, *args, **kwargs):
        # This may not exist. If so, None is the value of the Snippet.content attribute.
        snippet = pick(name, self.mappings[self.profile])

        # The name of the builder callback is always the root of the given name plus _parser.
        builder_name = "%s._parser" % name.split(".")[0]
        parser = pick(builder_name, self.mappings[self.profile])

        # Return the snippet instance.
        return Snippet(name, args=list(args), parser=parser, content=snippet, kwargs=kwargs)

    def load(self):
        """Load the command file.

        :rtype: bool

        """
        raise NotImplementedError()

    def read_file(self):
        """Get the content of the command file.

        :rtype: str | None

        """
        if self.context is not None:
            try:
                return parse_jinja_template(self.path, self.context)
            except Exception as e:
                log.error("Failed to process %s file as template: %s" % (self.path, e))
                return None

        return read_file(self.path)

    # def _get_command(self, name, *args, **kwargs):
    #     args = list(args)
    #
    #     if name not in self.mappings:
    #         return None
    #
    #     if type(self.mappings[name]) is dict:
    #         sub = args.pop(0)
    #         subs = self.mappings[name]
    #         if sub not in subs:
    #             return None
    #
    #         _command = subs[sub]
    #     else:
    #         _command = self.mappings[name]
    #
    #     context = self.context.copy()
    #     context['args'] = args
    #     context.update(kwargs)
    #
    #     if type(_command) in (list, tuple):
    #         # print(" ".join(_command))
    #         a = list()
    #         for i in _command:
    #             i = parse_jinja_string(i, context)
    #             a.append(i)
    #
    #         return " ".join(a)
    #
    #     return parse_jinja_string(_command, context)

    # noinspection PyMethodMayBeStatic
    def _get_key_value(self, key, value):
        """Process a key/value pair from an INI section.

        :param key: The key to be processed.
        :type key: str

        :param value: The value to be processed.

        :rtype: tuple
        :returns: The key and value, both of which may be modified from the originals.

        """
        if key in ("environments", "environs", "envs", "env"):
            _key = "environments"
            _value = split_csv(value)
        elif key in ("func", "function"):
            _key = "function"
            _value = value
        elif key == "groups":
            _key = "groups"
            if type(value) in (list, tuple):
                _value = value
            else:
                _value = split_csv(value)
        elif key == "items":
            _key = "items"
            if type(value) in (list, tuple):
                _value = value
            else:
                _value = split_csv(value)
        elif key == "tags":
            _key = "tags"
            _value = split_csv(value)
        else:
            _key = key
            _value = smart_cast(value)

        return _key, _value


class Snippet(object):

    def __init__(self, name, args=None, content=None, context=None, kwargs=None, parser=None):
        """Initialize a snippet.

        :param name: The canonical name of the snippet.
        :type name: str

        :param args: A list of arguments found in the config file.
        :type args: list[str]

        :param content: The content of the snippet.
        :type content: str | list[str]

        :param context: Additional context variables used to render the command.
        :type context: dict

        :param kwargs: The keyword arguments found in the config file. These may be specific to the command or one of
                       the common options. They are accessible as dynamic attributes of the Snippet instance.
        :type kwargs: dict

        :param parser: A callback that may be used to assemble the command.
        :type parser: callable

        """
        self.args = args or list()
        self.parser = parser
        self.content = content
        self.context = context or dict()
        self.kwargs = kwargs or dict()
        self.name = name

        sudo = self.kwargs.get("sudo", None)
        if isinstance(sudo, Sudo):
            self.sudo = sudo
        elif type(sudo) is str:
            self.sudo = Sudo(enabled=True, user=sudo)
        elif sudo is True:
            self.sudo = Sudo(enabled=True)
        else:
            self.sudo = Sudo()

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def __str__(self):
        return str(self.name)

    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        lines = list()
        if self.comment and include_comment:
            lines.append("# %s" % self.comment)

        # Handle command itemization. Note that register and stop options are ignored.
        if self.is_itemized:
            for item in self.items:
                args = list()
                for arg in self.args:
                    args.append(arg.replace("$item", item))

                if self.parser:
                    statement = self.parser(self, args=args)
                else:
                    statement = self._parse(args=args)

                a = list()
                if cd and self.cd is not None:
                    a.append("( cd %s &&" % self.cd)

                if self.prefix is not None:
                    a.append("%s &&" % self.prefix)

                if self.sudo:
                    statement = "%s %s" % (self.sudo, statement)

                a.append(statement)

                if cd and self.cd is not None:
                    a.append(")")

                lines.append(" ".join(a))

            return "\n".join(lines)

        # Handle normal (not itemized) comands.
        a = list()
        if cd and self.cd is not None:
            a.append("( cd %s &&" % self.cd)

        if self.prefix is not None:
            a.append("%s &&" % self.prefix)

        if self.parser:
            statement = self.parser(self)
        else:
            statement = self._parse()

        if self.sudo:
            statement = "%s %s" % (self.sudo, statement)

        a.append(statement)

        if cd and self.cd is not None:
            a.append(")")

        if self.condition is not None:
            lines.append("if [[ %s ]]; then %s; fi;" % (self.condition, " ".join(a)))
        else:
            lines.append(" ".join(a))

        if include_register and self.register is not None:
            lines.append("%s=$?;" % self.register)

            if include_stop and self.stop:
                lines.append("if [[ $%s -gt 0 ]]; exit 1; fi;" % self.register)
        elif include_stop and self.stop:
            lines.append("if [[ $? -gt 0 ]]; exit 1; fi;")
        else:
            pass

        return "\n".join(lines)

    @property
    def is_itemized(self):
        s = " ".join(self.args)
        return "$item" in s

    @property
    def is_valid(self):
        return self.content is not None

    # def _get_statement(self):
    #     if self.is_itemized:
    #         a = list()
    #         for item in self.items:
    #             args = list()
    #             for arg in self.args:
    #                 args.append(arg.replace("$item", item))
    #
    #             context = self.context.copy()
    #             context['args'] = args
    #             context.update(self.kwargs)
    #
    #             if type(self.content) is list:
    #                 b = list()
    #                 for i in self.content:
    #                     i = parse_jinja_string(i, context)
    #                     b.append(i)
    #
    #                 a.append(" ".join(b))
    #             else:
    #                 a.append(parse_jinja_string(self.content, context))
    #
    #         return "\n".join(a)
    #
    #     context = self.context.copy()
    #     context['args'] = self.args
    #     context.update(self.kwargs)
    #
    #     a = list()
    #     if type(self.content) is list:
    #         b = list()
    #         for i in self.content:
    #             i = parse_jinja_string(i, context)
    #             b.append(i)
    #
    #         a.append(" ".join(b))
    #     else:
    #         a.append(parse_jinja_string(self.content, context))
    #
    #     return " ".join(a)

    def _parse(self, args=None, kwargs=None):
        """Build the command statement from snippet content.

        :param args: A list of arguments which override those provided by the command configuration.
        :type args: list[str]

        :param kwargs: A dictionary which overrides the options provided by the command configuration.
        :type kwargs: dict

        :rtype: str

        """
        context = self.context.copy()
        context['args'] = args or self.args
        context.update(kwargs or self.kwargs)

        if type(self.content) is list:
            a = list()
            for string in self.content:
                output = parse_jinja_string(string, context)
                if len(output) == 0:
                    continue

                a.append(output)

            return " ".join(a)

        return parse_jinja_string(self.content, context)


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
    PARSER_SIMPLE = "simple"

    def __init__(self, source, target, backup=True, parser=None, **kwargs):
        self.backup_enabled = backup
        self.context = kwargs.pop("context", dict())
        self.parser = parser or self.PARSER_JINJA
        self.locations = kwargs.pop("locations", list())
        self.source = os.path.expanduser(source)
        self.target = target

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

        try:
            return parse_jinja_template(template, self.context)
        except TemplateNotFound:
            log.error("Template not found: %s" % template)
            return None
        except TemplateError as e:
            log.error("Could not parse %s template: %s" % (template, e))
            return None

    def get_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        if self.parser == self.PARSER_SIMPLE:
            return self._get_simple_statement(cd=cd, include_comment=include_comment, include_register=include_register,
                                              include_stop=include_stop)
        else:
            return self._get_jinja2_statement(cd=cd, include_comment=include_comment, include_register=include_register,
                                              include_stop=include_stop)

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
        return "$item" in self.target

    @property
    def is_valid(self):
        return True

    def _get_command(self, content):
        """Get the cat command."""
        output = list()

        # TODO: Template backup is not system safe, but is specific to bash.
        if self.backup_enabled:
            output.append('if [[ -f "%s" ]]; then mv %s %s.b; fi;' % (self.target, self.target, self.target))

        if content.startswith("#!"):
            _content = content.split("\n")
            first_line = _content.pop(0)
            output.append('echo "%s" > %s' % (first_line, self.target))
            output.append("cat >> %s << EOF" % self.target)
            output.append("\n".join(_content))
            output.append("EOF")
        else:
            output.append("cat > %s << EOF" % self.target)
            output.append(content)
            output.append("EOF")

        statement = "\n".join(output)

    # noinspection PyUnusedLocal
    def _get_jinja2_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Parse a Jinja2 template."""
        content = self.get_content()
        return self._get_command(content)

    # noinspection PyUnusedLocal
    def _get_simple_statement(self, cd=True, include_comment=True, include_register=True, include_stop=True):
        """Parse a "simple" template."""
        content = self.get_content()

        return self._get_command(content)

