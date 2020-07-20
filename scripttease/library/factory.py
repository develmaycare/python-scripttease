# Imports

from importlib import import_module

# Exports

__all__ = (
    "Factory",
)

# Classes


class Factory(object):
    """A command factory."""

    def __init__(self, overlay):
        """Initialize the factory.

        :param overlay: The name of the overlay to use for generating commands.
        :type overlay: str

        """
        self.is_loaded = False
        self.overlay = None
        self._overlay = overlay

    def get_command(self, name, *args, **kwargs):
        """Get a command.

        :param name: The name of the command.
        :type name: str

        args and kwargs are passed to the initialize the command.

        :rtype: scripttease.library.commands.Command | scripttease.library.commands.ItemizedCommand

        """
        if not self.overlay.command_exists(name):
            # log.warning("Command does not exist in %s overlay: %s" % (overlay.name, name))
            return None

        callback = self.overlay.MAPPINGS[name]

        try:
            # items = kwargs.pop("items", None)
            # if items is not None:
            #     return ItemizedCommand(callback, items, *args, **kwargs)

            return callback(*args, **kwargs)
        except (KeyError, TypeError, ValueError) as e:
            # log.critical("Failed to load %s command: %s" % (name, e))
            return None

    def load(self):
        """Load the factory.

        :rtype: bool

        """
        try:
            self.overlay = import_module("scripttease.library.overlays.%s" % self._overlay)
            self.is_loaded = True
        except ImportError as e:
            # log.error("The %s overlay could not be imported: %s" % (overlay, str(e)))
            pass

        return self.is_loaded