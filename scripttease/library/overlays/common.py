# Imports

from ..commands import Command

# Exports

__all__ = (
    "COMMON_MAPPINGS",
    "python_pip",
    "python_virtualenv",
    "run",
)

# Functions


def python_pip(name, op="install", upgrade=False, venv=None, **kwargs):
    """Use pip to install or uninstall a Python package.

    - name (str): The name of the package.
    - op (str): The operation to perform; install, uninstall
    - upgrade (bool): Upgrade an installed package.
    - venv (str): The name of the virtual environment to load.

    """
    if upgrade:
        statement = "pip install --upgrade %s" % name
    else:
        statement = "pip %s %s" % (op, name)

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


def run(statement, **kwargs):
    """Run any statement.

    - statement (str): The statement to be executed.

    """
    kwargs.setdefault("comment", "run statement")
    return Command(statement, **kwargs)


# Mappings

COMMON_MAPPINGS = {
    'pip': python_pip,
    'run': run,
    'virtualenv': python_virtualenv,
}
