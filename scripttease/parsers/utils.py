# Imports

from commonkit import any_list_item, smart_cast, split_csv
from configparser import RawConfigParser
import logging
import os
from ..constants import LOGGER_NAME
from .ini import Config

log = logging.getLogger(LOGGER_NAME)

# Exports

__all__ = (
    "filter_commands",
    "load_commands",
    "load_config",
    "load_variables",
    "Context",
    "Variable",
)

# Functions


def filter_commands(commands, environments=None, tags=None):
    """Filter commands based on the given criteria. 
    
    :param commands: The commands to be filtered.
    :type commands: list
    
    :param environments: Environment names to be matched.
    :type environments: list[str]
     
    :param tags: Tag names to be matched.
    :type tags: list[str]

    """
    filtered = list()
    for command in commands:
        if environments is not None and len(command.environments) > 0:
            if not any_list_item(environments, command.environments):
                continue
        
        if tags is not None:
            if not any_list_item(tags, command.tags):
                continue
        
        filtered.append(command)
        
    return filtered


def load_commands(path, filters=None, overlay="ubuntu", **kwargs):
    """Load commands from a configuration file.

    :param path: The path to the configuration file.
    :type path: str

    :param filters: Used to filter commands.
    :type filters: dict

    :param overlay: The name of the command overlay to apply to generated commands.
    :type overlay: str

    :rtype: list[scriptetease.library.commands.base.Command] | scriptetease.library.commands.base.ItemizedCommand] |
            None

    :returns: A list of command instances or ``None`` if the configuration could not be loaded.

    kwargs are passed to the configuration class for instantiation.

    """
    _config = load_config(path, overlay, **kwargs)
    if _config is None:
        return None

    commands = _config.get_commands()

    if filters is not None:
        criteria = dict()
        for attribute, values in filters.items():
            criteria[attribute] = values

        commands = filter_commands(commands, **criteria)

    return commands


def load_config(path, overlay="ubuntu", **kwargs):
    """Load a command configuration.

    :param path: The path to the configuration file.
    :type path: str

    :param overlay: The name of the command overlay to apply to generated commands.
    :type overlay: str

    :rtype: Config | None

    kwargs are passed to the configuration class for instantiation.

    """
    if path.endswith(".ini"):
        _config = Config(path, overlay=overlay, **kwargs)
    # elif path.endswith(".yml"):
    #     _config = YAML(path, **kwargs)
    else:
        log.warning("Input file format is not currently supported: %s" % path)
        return None

    if not _config.load():
        log.error("Failed to load config file: %s" % path)
        return None

    return _config


def load_variables(path, environment=None):
    """Load variables from a file.

    :param path: The path to the file.
    :type path: str

    :param environment: Filter variables by the given environment name.
    :type environment: str

    :rtype: list[scripttease.parsers.utils.Variable]

    """
    if not os.path.exists(path):
        log.warning("Path to variables file does not exist: %s" % path)
        return list()

    if path.endswith(".ini"):
        return _load_variables_ini(path, environment=environment)
    else:
        log.warning("Variable file format is not currently supports: %s" % path)
        return list()


def _load_variables_ini(path, environment=None):
    """Load variables from an INI file. See ``load_variables()``."""

    ini = RawConfigParser()
    ini.read(path)

    a = list()
    for section in ini.sections():
        if ":" in section:
            variable_name, _environment = section.split(":")
        else:
            _environment = None
            variable_name = section

        _kwargs = {
            'environment': _environment,
        }
        for key, value in ini.items(section):
            if key == "tags":
                value = split_csv(value)
            else:
                value = smart_cast(value)

            _kwargs[key] = value

        a.append(Variable(variable_name, **_kwargs))

    if environment is not None:
        b = list()
        for var in a:
            if var.environment and var.environment == environment or var.environment is None:
                b.append(var)

        return b

    return a

# Classes


class Context(object):
    """A collection of variables."""

    def __init__(self, **kwargs):
        """Initialize the context.

        kwargs are added as variable instances.

        """
        self.variables = dict()

        for key, value in kwargs.items():
            self.add(key, value)

    def __getattr__(self, item):
        if item in self.variables:
            return self.variables[item].value

        return None

    def __repr__(self):
        return "<%s (%s)>" % (self.__class__.__name__, len(self.variables))

    def add(self, name, value, environment=None, tags=None):
        """Add a variable to the context.

        :param name: The name of the variable.
        :type name: str

        :param value: The value of the variable in this context.

        :param environment: The environment name to which the variable applies. ``None`` applies to all environments.
        :type environment: str

        :param tags: A list of tags that describe the variable.
        :type tags: list[str]

        :rtype: scripttease.parsers.utils.Variable

        :raise: RuntimeError
        :raises: ``RuntimeError`` if the variable already exists.

        """
        if name in self.variables:
            raise RuntimeError("Variable already exists: %s" % name)

        v = Variable(name, value, environment=environment, tags=tags)
        self.variables[name] = v

        return v

    def get(self, name, default=None):
        """Get a the value of the variable from the context.

        :param name: The name of the variable.
        :type name: str

        :param default: The default value to return.

        """
        if not self.has(name):
            return default

        return self.variables[name].value

    def has(self, name):
        """Indicates whether the named variable exists in this context, and whether the value is not ``None``.

        :rtype: bool

        """
        if name not in self.variables:
            return False

        return self.variables[name].value is not None

    def join(self, variables):
        """Join a list of variables to the context.

        :param variables: the list of variables to be added.
        :type variables: list[scripttease.parsers.utils.Variable]

        .. note::
            This *replaces* a variable if it already exists.

        """
        for v in variables:
            self.variables[v.name] = v

    def mapping(self):
        """Export the context as a dictionary.

        :rtype: dict

        """
        values = dict()
        for key, var in self.variables.items():
            values[key] = var.value or var.default

        return values

    def merge(self, context):
        """Merge another context with this one.

        :param context: The context to be merged.
        :type context: scripttease.parser.utils.Context

        .. note::
            Variables that exist in the current context are *not* replaced with variables from the provided context.

        """
        for name, var in context.variables.items():
            if not self.has(name):
                self.variables[name] = var


class Variable(object):
    """Represents a variable to be used in the context of pre-processing a config file."""

    def __init__(self, name, value, **kwargs):
        """Initialize a variable.

        :param name: The variable name.
        :type name: str

        :param value: The value of the variable.

        kwargs are added as attributes of the instance.

        """
        self.name = name
        self.value = value

        kwargs.setdefault("tags", list())
        self._attributes = kwargs

    def __eq__(self, other):
        return self.value == other

    def __getattr__(self, item):
        return self._attributes.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)
