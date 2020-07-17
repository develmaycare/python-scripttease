# Imports

from configparser import RawConfigParser
import os
from superpython.utils import parse_jinja_string
from ..constants import PATH_TO_SCRIPT_TEASE

# Exports

__all__ = (
    "Overlay",
)

# Classes


class Overlay(object):
    """An overlay applies commands specific to a given operating system or platform."""

    def __init__(self, name):
        self.is_loaded = False
        self._name = name
        self._path = os.path.join(PATH_TO_SCRIPT_TEASE, "data", "overlays", "%s.ini" % name)
        self._sections = dict()

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self._name)

    @property
    def exists(self):
        """Indicates whether the overlay file exists.

        :rtype: bool

        """
        return os.path.exists(self._path)

    def get(self, section, key, **kwargs):
        """Get the command statement for the given section and key.

        :param section: The section name.
        :type section: str

        :param key: The key within the section.
        :type key: str

        kwargs are used to parse the value of the key within the section.

        :rtype: str | None

        """
        if not self.has(section, key):
            return None

        template = self._sections[section][key]

        return parse_jinja_string(template, kwargs)

    def has(self, section, key):
        """Determine whether the overlay contains a given section and key.

        :param section: The section name.
        :type section: str

        :param key: The key within the section.
        :type key: str

        :rtype: bool

        """
        if section not in self._sections:
            return False

        if key not in self._sections[section]:
            return False

        return True

    def load(self):
        """Load the overlay.

        :rtype: bool

        """
        if not self.exists:
            return False

        ini = RawConfigParser()
        ini.read(self._path)

        for section in ini.sections():
            self._sections[section] = dict()
            for key, value in ini.items(section):
                self._sections[section][key] = value

        self.is_loaded = True
        return True
