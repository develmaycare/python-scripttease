import logging
from .commands.base import Command, ItemizedCommand, Template
from .commands.centos import CENTOS_MAPPINGS
from .commands.ubuntu import UBUNTU_MAPPINGS

log = logging.getLogger(__name__)


def command_exists(mappings, name):
    """Indicates whether a given command exists in this overlay.

    :param mappings: A dictionary of command names and command functions.
    :type mappings: dict

    :param name: The name of the command.
    :type name: str

    :rtype: bool

    """
    return name in mappings


def command_factory(loader, profile):
    commands = list()
    number = 1
    for command_name, args, kwargs in loader.commands:
        command = get_command(command_name, profile, *args, **kwargs)
        if command is not None:
            command.number = number
            commands.append(command)

            number += 1

    return commands


def get_command(name, profile, *args, **kwargs):
    """Get a command instance.

    :param name: The name of the command.
    :type name: str

    :param profile: The operating system profile name.
    :type profile: str

    args and kwargs are passed to the command function.

    :rtype: scripttease.lib.commands.base.Command | scripttease.lib.commands.base.ItemizedCommand |
            scripttease.lib.commands.base.Template

    """
    if profile == "centos":
        mappings = CENTOS_MAPPINGS
    elif profile == "ubuntu":
        mappings = UBUNTU_MAPPINGS
    else:
        log.error("Unsupported or unrecognized profile: %s" % profile)
        return None

    _args = list(args)

    if name == "template":
        source = _args.pop(0)
        target = _args.pop(0)
        return Template(source, target, **kwargs)

    if not command_exists(mappings, name):
        log.warning("Command does not exist: %s" % name)
        return None

    callback = mappings[name]

    if "items" in kwargs:
        items = kwargs.pop("items")
        return ItemizedCommand(callback, items, *args, **kwargs)

    return callback(*args, **kwargs)
