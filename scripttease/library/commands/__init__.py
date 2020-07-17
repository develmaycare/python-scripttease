# Imports

import logging
# from ..scripts import Function
from ...constants import LOGGER_NAME
from .base import ItemizedCommand
from .mappings import MAPPING

log = logging.getLogger(LOGGER_NAME)

# Functions


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
