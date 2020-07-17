# Imports

from .base import Command

# Exports

__all__ = (
    "Pip",
    "VirtualEnv",
)

# Classes


class Pip(Command):

    def __init__(self, name, op="install", overlay=None, upgrade=False, venv=None, **kwargs):
        if overlay is not None:
            statement = overlay.get("python", op, package_name=name, upgrade=upgrade)
        else:
            statement = "pip %s -y %s" % (op, name)

        if venv is not None:
            kwargs['prefix'] = "source %s/bin/activate" % venv

        kwargs.setdefault("comment", "%s %s" % (op, name))

        super().__init__(statement, **kwargs)


class VirtualEnv(Command):

    def __init__(self, name="python", overlay=None, **kwargs):
        kwargs.setdefault("comment", "create %s virtual environment" % name)

        statement = "virtualenv %s" % name
        super().__init__(statement, **kwargs)


MAPPING = {
    'pip': Pip,
    'virtualenv': VirtualEnv,
}
