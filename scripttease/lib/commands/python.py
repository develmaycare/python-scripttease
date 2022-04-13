from .base import Command


def python_pip(name, op="install", upgrade=False, venv=None, version=3, **kwargs):
    """Use pip to install or uninstall a Python package.

    - name (str): The name of the package.
    - op (str): The operation to perform; install, uninstall
    - upgrade (bool): Upgrade an installed package.
    - venv (str): The name of the virtual environment to load.
    - version (int): The Python version to use, e.g. ``2`` or ``3``.

    """
    manager = "pip"
    if version == 3:
        manager = "pip3"

    if upgrade:
        statement = "%s install --upgrade %s" % (manager, name)
    else:
        statement = "%s %s %s" % (manager, op, name)

    if venv is not None:
        kwargs['prefix'] = "source %s/bin/activate" % venv

    kwargs.setdefault("comment", "%s %s" % (op, name))

    return Command(statement, **kwargs)


def python_virtualenv(name, **kwargs):
    """Create a Python virtual environment.

    - name (str): The name of the environment to create.

    """
    kwargs.setdefault("comment", "create %s virtual environment" % name)

    return Command("virtualenv %s" % name, **kwargs)