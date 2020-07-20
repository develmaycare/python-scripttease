# Imports

from importlib import import_module
import logging
# from ..scripts import Function
from ...constants import LOGGER_NAME
# from .base import ItemizedCommand
# from .mappings import MAPPING

log = logging.getLogger(LOGGER_NAME)

# Functions


def command_factory(name, comment, overlay, *args, **kwargs):
    # try:
    #     _overlay = import_module("scripttease.library.overlays.%s" % overlay)
    # except ImportError as e:
    #     log.error("The %s overlay could not be imported: %s" % (overlay, str(e)))
    #     return None

    if not overlay.command_exists(name):
        log.warning("Command does not exist in %s overlay: %s" % (overlay.name, name))
        return None

    kwargs['comment'] = comment

    callback = overlay.MAPPINGS[name]
    return callback(*args, **kwargs)

'''
def command_exists(name):
    """Indicates whether the named command exists.

    :param name: The name of the command to be checked.
    :type name: str

    :rtype: bool

    """
    return name in MAPPING


def command_factory(name, comment, overlay, *args, **kwargs):
    # if name in ("func", "function"):
    #     kwargs['comment'] = comment
    #     return Function(*args, **kwargs)

    if not command_exists(name):
        log.warning("No mapping for command: %s" % name)
        return None

    _args = list(args)
    kwargs['comment'] = comment
    kwargs['overlay'] = overlay

    log.debug("%s: %s" % (comment, kwargs))

    command_class = MAPPING[name]
    try:
        items = kwargs.pop("items", None)
        if items is not None:
            return ItemizedCommand(command_class, items, *_args, **kwargs)

        return command_class(*_args, **kwargs)
    except (KeyError, TypeError, ValueError) as e:
        log.critical("Failed to load %s command: %s" % (name, e))
        return None
'''

#
#
#
# MAPPINGS = {
#     'apache.disable_module': apache_disable_module,
#     'apache.disable_site': apache_disable_site,
#     'apache.enable_module': apache_enable_module,
#     'apache.enable_site': apache_enable_site,
#     'apache.reload': apache_reload,
#     'apache.restart': apache_restart,
#     'apache.start': apache_start,
#     'apache.stop': apache_stop,
#     'apache.test': apache_test,
#     'copy': file_copy,
#     'pip': python_pip,
#     'virtualenv': python_virtualenv,
#     # 'python': ("pip", "virtualenv"),
#     # 'apache': ("disable_module", "disable_site", "enable_module", "enable_site", "test"),
# }


def nother_command_exists(name):
    return name in MAPPINGS


def other_command_exists(name, section=None):
    if section is not None:
        if section not in MAPPINGS:
            return False

        return name in MAPPINGS[section]

    for _section, commands in MAPPINGS.items():
        if name in commands:
            return True

    return False



def other_command_factory(name, comment, overlay, *args, **kwargs):
    if not overlay.command_exists(name):
        log.warning("The %s overlay does not have a mapping for command: %s" % (overlay, name))
        return None

    items = kwargs.pop("items", None)
    if items is not None:
        return ItemizedCommand

