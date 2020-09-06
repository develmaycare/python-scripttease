# Imports

from ..commands import Command

# Exports

__all__ = (
    "COMMON_MAPPINGS",
    "python_pip",
    "python_virtualenv",
    "run",
    "slack",
)

# Functions


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


def run(statement, **kwargs):
    """Run any statement.

    - statement (str): The statement to be executed.

    """
    kwargs.setdefault("comment", "run statement")
    return Command(statement, **kwargs)


def slack(message, url=None, **kwargs):
    """Send a message to Slack.

    - message (str): The message to be sent.
    - url (str): The webhook URL. This is required. See documentation.

    """
    kwargs.setdefault("comment", "send a message to slack")

    a = list()

    a.append("curl -X POST -H 'Content-type: application/json' --data")
    a.append("'" + '{"text": "%s"}' % message + "'")
    a.append(url)

    return Command(" ".join(a), **kwargs)


# Mappings

COMMON_MAPPINGS = {
    'pip': python_pip,
    'run': run,
    'slack': slack,
    'virtualenv': python_virtualenv,
}
