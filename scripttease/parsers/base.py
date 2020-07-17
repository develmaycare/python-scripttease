# Imports

from superpython.utils import File
from ..library.overlays import Overlay
from ..library.scripts import Script

# Exports

__all__ = (
    "Parser"
)

# Classes


class Parser(File):
    """Base class for implementing a command parser."""

    def __init__(self, path, context=None, locations=None, options=None, overlay=None):
        super().__init__(path)

        self.context = context
        self.is_loaded = False
        self.locations = locations or list()
        self.options = options or dict()
        self.overlay = overlay or Overlay("ubuntu")
        self._commands = list()
        self._functions = list()

        self.overlay.load()

    def as_script(self):
        """Convert loaded commands to a script.

        :rtype: Script

        """
        return Script(
            "%s.sh" % self.name,
            commands=self.get_commands(),
            functions=self.get_functions()
        )

    def get_commands(self):
        """Get the commands that have been loaded from the file.

        :rtype: list[BaseType[scripttease.library.commands.base.Command]]

        """
        a = list()
        for c in self._commands:
            if c.function is not None:
                continue

            a.append(c)

        return a

    def get_functions(self):
        """Get the functions that have been loaded from the file.

        :rtype: list[scripttease.library.scripts.Function]

        """
        a = list()
        for f in self._functions:
            for c in self._commands:
                if c.function is not None and f.name == c.function:
                    f.commands.append(c)

            a.append(f)

        return a

    def load(self):
        raise NotImplementedError()
