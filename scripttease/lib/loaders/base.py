# Imports

from commonkit import any_list_item, parse_jinja_string, parse_jinja_template, pick, read_file, smart_cast, split_csv, \
    File
from configparser import ParsingError, RawConfigParser
from jinja2.exceptions import TemplateError, TemplateNotFound
import logging
import os
from ..contexts import Variable
from ..snippets.mappings import MAPPINGS

log = logging.getLogger(__name__)

# Exports


__all__ = (
    "filter_snippets",
    "load_variables",
    "BaseLoader",
    "Snippet",
    "Sudo",
    "Template",
)
# Functions


def filter_snippets(snippets, environments=None, tags=None):
    """Filter snippets based on the given criteria.

    :param snippets: The snippets to be filtered.
    :type snippets: list[scripttease.lib.loaders.base.Snippet]

    :param environments: Environment names to be matched.
    :type environments: list[str]

    :param tags: Tag names to be matched.
    :type tags: list[str]

    """
    filtered = list()
    for snippet in snippets:
        if environments is not None and len(snippet.environments) > 0:
            if not any_list_item(environments, snippet.environments):
                continue

        if tags is not None:
            if not any_list_item(tags, snippet.tags):
                continue

        filtered.append(snippet)

    return filtered


def load_variables(path, env=None):
    """Load variables from an INI file.

    :param path: The path to the INI file.
    :type path: str

    :param env: The environment name of variables to return.
    :type env: str

    :rtype: list[scripttease.lib.contexts.Variable]

    """
    if not os.path.exists(path):
        log.warning("Variables file does not exist: %s" % path)
        return list()

    ini = RawConfigParser()
    try:
        ini.read(path)
    except ParsingError as e:
        log.warning("Failed to parse %s variables file: %s" % (path, str(e)))
        return list()

    variables = list()
    for variable_name in ini.sections():
        if ":" in variable_name:
            variable_name, _environment = variable_name.split(":")
        else:
            _environment = None
            variable_name = variable_name

        kwargs = {
            'environment': _environment,
        }
        _value = None
        for key, value in ini.items(variable_name):
            if key == "value":
                _value = smart_cast(value)
                continue

            kwargs[key] = smart_cast(value)

        variables.append(Variable(variable_name, _value, **kwargs))

    if env is not None:
        filtered_variables = list()
        for var in variables:
            if var.environment and var.environment == env or var.environment is None:
                filtered_variables.append(var)

        return filtered_variables

    return variables


# Classes


class BaseLoader(File):
    """Base class for loading a command file."""

    def __init__(self, path,  context=None, locations=None, mappings=None, profile="ubuntu", **kwargs):
        """Initialize the loader.

        :param path: The path to the command file.
        :type path: str

        :param context: Global context that may be used when to parse the command file, snippets, and templates. This is
                        converted to a ``dict`` when passed to a Snippet or Template.
        :type context: scripttease.lib.contexts.Context

        :param locations: A list of paths where templates and other external files may be found. The ``templates/``
                          directory in which the command file exists is added automatically.
        :type locations: list[str]

        :param mappings: A mapping of canonical command names and their snippets, organized by ``profile``. The profile
                         is typically an operating system such as ``centos`` or ``ubuntu``.
        :type mappings: dict

        :param profile: The profile (operating system or platform) to be used.
        :type profile: str

        kwargs are stored as ``options`` and may include any of the common options for command configuration. These may
        be supplied as defaults for snippet processing.

        """
        self.context = context
        self.is_loaded = False
        self.locations = locations or list()
        self.mappings = mappings or MAPPINGS
        self.options = kwargs
        self.profile = profile
        self.snippets = list()

        super().__init__(path)

        # Always include the path to the current file in locations.
        self.locations.insert(0, os.path.join(self.directory, "templates"))

    def get_context(self):
        """Get the context for parsing command snippets.

        :rtype: dict

        """
        d = self.options.copy()
        if self.context is not None:
            d.update(self.context.mapping().copy())

        return d

    def get_snippets(self):
        """Get the snippets found in a config file.

        :rtype: list[scripttease.lib.loaders.base.Snippet]

        """
        a = list()

        for canonical_name, args, kwargs in self.snippets:
            snippet = self.find_snippet(canonical_name, *args, **kwargs)
            a.append(snippet)

        return a

    def find_snippet(self, name, *args, **kwargs):
        """Find a named snippet that was defined in a config file.

        :param name: The canonical name (or dotted name) of the snippet.
        :type name: str

        :rtype: scripttease.lib.loaders.base.Snippet | scripttease.lib.loaders.base.Template

        ``args`` and ``kwargs`` are passed to instantiate the snippet.

        .. important::
            The snippet may be invalid; always check ``snippet.is_valid``.

        """
        # Templates require special handling.
        if name == "template":
            source = args[0]
            target = args[1]
            kwargs['locations'] = self.locations
            context = kwargs.copy()
            context.update(self.get_context())
            return Template(source, target, context=context, **kwargs)

        # Convert args to a list so we can update it below.
        _args = list(args)

        # The given name is not in the mappings -- which is a typo or invalid name -- but it could also be a dotted path
        # to be followed down through the dictionary structure.
        if name not in self.mappings[self.profile]:
            if "." in name:
                return self.find_snippet_by_dotted_name(name, *args, **kwargs)

            log.error("Command not found in mappings: %s" % name)
            return Snippet(name, args=_args, kwargs=kwargs)

        # Get the global context for use in snippet instantiation below.
        context = self.get_context()

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
                return Snippet(_name, args=_args, content=snippet, context=context, kwargs=kwargs, parser=parser)

            # Django allows pre-defined as well as adhoc commands. The name of the command is provided as the first
            # argument in the config file. The following statements are only invoked if the possible_sub_command is not
            # in the django dictionary. The "command" entry in the django dictionary is for handling ad hoc commands.
            if name == "django":
                sub = _args.pop(0)
                kwargs['_name'] = sub
                snippet = self.mappings[self.profile]['django']['command']
                parser = self.mappings[self.profile]['django']['_parser']
                return Snippet("django.%s" % sub, args=_args, content=snippet, context=context, kwargs=kwargs,
                               parser=parser)

            log.warning("Sub-command could not be determined for: %s" % name)
            return Snippet(name, args=list(args), context=context, kwargs=kwargs)

        # The found snippet should just be a string.
        return Snippet(name, args=list(args), content=self.mappings[self.profile][name], context=context, kwargs=kwargs)

    def find_snippet_by_dotted_name(self, name, *args, **kwargs):
        """Find a snippet using it's dotted name.

        :param name: The dotted name of the snippet.

        :param args:
        :param kwargs:

        ``args`` and ``kwargs`` are passed to instantiate the snippet.

        .. important::
            The snippet may be invalid; always check ``snippet.is_valid``.

        """
        # This may not exist. If so, None is the value of the Snippet.content attribute.
        snippet = pick(name, self.mappings[self.profile])

        # The name of the builder callback is always the root of the given name plus _parser.
        builder_name = "%s._parser" % name.split(".")[0]
        parser = pick(builder_name, self.mappings[self.profile])

        # Return the snippet instance.
        return Snippet(name, args=list(args), parser=parser, content=snippet, context=self.get_context(), kwargs=kwargs)

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
                return parse_jinja_template(self.path, self.context.mapping())
            except Exception as e:
                log.error("Failed to process %s file as template: %s" % (self.path, e))
                return None

        return read_file(self.path)

    # noinspection PyMethodMayBeStatic
    def _get_key_value(self, key, value):
        """Process a key/value pair.

        :param key: The key to be processed.
        :type key: str

        :param value: The value to be processed.

        :rtype: tuple
        :returns: The key and value, both of which may be modified from the originals.

        This handles special names in the following manner:

        - ``environments``, ``environs``, ``envs``, and ``env`` are treated as a CSV list of environment names
          if provided as a string. These are normalized to the keyword ``environments``.
        - ``func`` and ``function`` are normalized to the keyword ``function``. The value is the name of the function to
          be defined.
        - ``groups`` is assumed to be a CSV list of groups if provided as a string.
        - ``items`` is assumed to be a CSV list if provided as a string. These are used to create an "itemized" command.
        - ``tags`` is assumed to be a CSV list oif provided as a string.

        All other keys are used as is. Values provided as a CSV list are smart cast to a Python value.

        """
        if key in ("environments", "environs", "envs", "env"):
            _key = "environments"
            if type(value) in (list, tuple):
                _value = value
            else:
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
            if type(value) in (list, tuple):
                _value = value
            else:
                _value = split_csv(value)
        else:
            _key = key
            _value = smart_cast(value)

        return _key, _value


class Snippet(object):
    """A snippet is a pseudo-command which collects the content of the snippet as well as the parameters that may be
    used to create an executable statement.

    The purpose of a snippet is *not* to provide command execution, but to capture the parameters of a command defined
    in a configuration file.

    """

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

        self.environments = kwargs.pop("environments", list())
        self.tags = kwargs.pop("tags", list())

        sudo = self.kwargs.pop("sudo", None)
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
        """Get the command statement represented by the snippet.

        :param cd: Indicates whether the change directory option should be included in the output. The ``cd`` option
                   must also be provided for the command in the configuration file.
        :type cd: bool

        :param include_comment: Indicates whether the command comment should be included in the output.
        :type include_comment: bool

        :param include_register: Indicates whether an additional statement to capture the result of the command should
                                 be included in the output. The register option must also be defined for the command in
                                 the configuration file.
        :type include_register: bool

        :param include_stop: Indicates whether an additional statement to exit on failure of the command should be
                             included in the output. The stop option must also be defined for the command in the
                             configuration file.
        :type include_stop: bool

        :rtype: str

        .. note::
            The boolean options allow implementers to exercise control over the output of the statement, so that the
            snippet may be used in ways appropriate to the implementation.

        """
        lines = list()
        if self.comment and include_comment:
            lines.append("# %s" % self.comment)

        # Handle snippet itemization. Note that register and stop options are ignored.
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

        # Handle normal (not itemized) snippets.
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
        """Indicates whether the snippet includes multiple occurrences of the same command.

        :rtype: bool

        """
        s = " ".join(self.args)
        return "$item" in s

    @property
    def is_valid(self):
        """Indicates whether the snippet is valid.

        :rtype: bool

        .. note::
            This is done by determining if snippet content is not ``None``. The content is found during the loading
            process when the Snippet instance is created.

        """
        return self.content is not None

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
            lines.append('if [[ -f "%s" ]]; then %s fi;' % (self.target, command.lstrip()))

        # Get the content; e.g. parse the template.
        content = self.get_content()

        # Templates that are bash scripts will fail to write because of the shebang.
        if content.startswith("#!"):
            _content = content.split("\n")
            first_line = _content.pop(0)
            command = '%s echo "%s" > %s' % (self.sudo, first_line, self.target)
            lines.append(command.lstrip())
            command = "%s cat >> %s << EOF" % (self.sudo, self.target)
            lines.append(command.lstrip())
            lines.append("\n".join(_content))
            lines.append("EOF")
        else:
            command = "%s cat >> %s << EOF" % (self.sudo, self.target)
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

    @property
    def is_valid(self):
        return True
