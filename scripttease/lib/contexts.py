# Imports

from commonkit import smart_cast
from configparser import ParsingError, RawConfigParser
import logging
import os

log = logging.getLogger(__name__)

# Exports

__all__ = (
    "Context",
    "Variable",
)

# Functions


def load_variables(path):
    """Load variables from an INI file.

    :param path: The path to the INI file.
    :type path: str

    :rtype: scripttease.lib.contexts.Context

    """
    if not os.path.exists(path):
        log.warning("Variables file does not exist: %s" % path)
        return Context()

    ini = RawConfigParser()
    try:
        ini.read(path)
    except ParsingError as e:
        log.warning("Failed to parse %s variables file: %s" % (path, str(e)))
        return Context()

    context = Context()
    for variable_name in ini.sections():
        _value = None
        kwargs = dict()
        for key, value in ini.items(variable_name):
            if key == "value":
                _value = smart_cast(value)
                continue

            kwargs[key] = smart_cast(value)

        context.add(variable_name, _value, **kwargs)

    context.is_loaded = True

    return context


# Classes


class Context(object):
    """A collection of context variables."""

    def __init__(self):
        """Initialize the context."""
        self.is_loaded = False
        self.variables = dict()

    def __getattr__(self, item):
        return self.variables.get(item)

    def add(self, name, value, **kwargs):
        """Add a variable to the context.

        :param name: The name of the variable.
        :type name: str

        :param value: The value of the variable.

        :rtype: scripttease.lib.contexts.Variable

        kwargs are passed to instantiate the Variable.

        """
        v = Variable(name, value, **kwargs)
        self.variables[name] = v

        return v

    def mapping(self):
        """Get the context as a dictionary.

        :rtype: dict

        """
        d = dict()
        for name, variable in self.variables.items():
            d[name] = variable.value

        return d


class Variable(object):
    """An individual variable."""

    def __init__(self, name, value, **kwargs):
        """Initialize a variable.

        :param name: The name of the variable.
        :type name: str

        :param value: The value of the variable.

        kwargs are available as dynamic attributes.

        """
        self.attributes = kwargs
        self.name = name
        self.value = value

    def __getattr__(self, item):
        return self.attributes.get(item)

    def __str__(self):
        return str(self.value)
