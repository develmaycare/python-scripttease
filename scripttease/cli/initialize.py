# Imports

from configparser import ConfigParser
import logging
import os
from superpython.utils import smart_cast
from ..constants import LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)

# Functions


def context_from_cli(variables):
    context = dict()
    for i in variables:
        key, value = i.split(":")
        context[key] = smart_cast(value)

    return context


def filters_from_cli(filters):
    _filters = dict()
    for i in filters:
        key, value = i.split(":")
        if key not in filters:
            _filters[key] = list()

        _filters[key].append(value)

    return _filters


def options_from_cli(options):
    _options = dict()
    for i in options:
        key, value = i.split(":")
        _options[key] = smart_cast(value)

    return _options


def variable_from_file(path):
    if not os.path.exists(path):
        log.warning("Variables file does not exist: %s" % path)
        return None

    ini = ConfigParser()
    ini.read(path)

    variables = dict()
    for section in ini.sections():
        for key, value in ini.items(section):
            key = "%s_%s" % (section, key)
            variables[key] = smart_cast(vaue)

    return variables
