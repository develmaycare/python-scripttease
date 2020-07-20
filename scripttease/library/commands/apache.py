# Imports

import logging
from ...constants import LOGGER_NAME
from .base import Command

log = logging.getLogger(LOGGER_NAME)

# Exports

__all__ = (
    "MAPPING",
    "ConfigTest",
    "DisableModule",
    "DisableSite",
    "EnableModule",
    "EnableSite",
    "Reload",
    "Restart",
    "Start",
    "Stop",
)

# Classes


class ConfigTest(Command):
    """Run an apache config test."""

    def __init__(self, overlay=None, **kwargs):
        """There is no argument."""
        if overlay is not None:
            statement = overlay.get("apache", "test")
        else:
            statement = "apachectl configtest"

        kwargs.setdefault('register', "apache_checks_out")

        super().__init__(statement, **kwargs)


class DisableModule(Command):
    """Disable an Apache module."""

    def __init__(self, module_name, overlay=None, **kwargs):
        """Initialize the command.

        :param module_name: The module name.
        :type module_name: str

        """
        if overlay is not None:
            statement = overlay.get("apache", "disable_module", module_name=module_name)

        statement = "a2dismod %s" % module_name

        super().__init__(statement, **kwargs)


class DisableSite(Command):
    """Disable a virtual host."""

    def __init__(self, domain_name, **kwargs):
        """Initialize the command.

        :param domain_name: The domain name.
        :type domain_name: str

        """
        statement = "a2dissite %s.conf" % domain_name

        super().__init__(statement, **kwargs)


class Enable(Command):

    def __init__(self, what, name, **kwargs):
        if what in ("mod", "module"):
            statement = EnableModule(name, **kwargs).statement
        elif what == "site":
            statement = EnableSite(name, **kwargs).statement
        else:
            raise ValueError("Invalid Apache item to be enabled: %s" % what)

        super().__init__(statement, **kwargs)


class EnableModule(Command):
    """Enable an Apache module."""

    def __init__(self, module_name, **kwargs):
        """Initialize the command.

        :param module_name: The module name.
        :type module_name: str

        """
        statement = "a2enmod %s" % module_name

        super().__init__(statement, **kwargs)


class EnableSite(Command):
    """Enable a virtual host."""

    def __init__(self, domain_name, **kwargs):
        """Initialize the command.

        :param domain_name: The domain name.
        :type domain_name: str

        """
        statement = "a2ensite %s.conf" % domain_name

        super().__init__(statement, **kwargs)


MAPPING = {
    # 'apache': Apache,
    'apache.check': ConfigTest,
    'apache.config': ConfigTest,
    'apache.configtest': ConfigTest,
    'apache.disable': Disable,
    'apache.disable_mod': DisableModule,
    'apache.disable_module': DisableModule,
    'apache.disable_site': DisableSite,
    'apache.enable': Enable,
    'apache.enable_mod': EnableModule,
    'apache.enable_module': EnableModule,
    'apache.enable_site': EnableSite,
    'apache.mod': EnableModule,
    'apache.module': EnableModule,
    'apache.test': ConfigTest,
}
