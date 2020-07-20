from ..commands import Command


def python_pip(name, op="install", upgrade=False, venv=None, **kwargs):
    if upgrade:
        statement = "pip install --upgrade -y %s" % name
    else:
        statement = "pip %s -y %s" % (op, name)

    if venv is not None:
        kwargs['prefix'] = "source %s/bin/activate" % venv

    kwargs.setdefault("comment", "%s %s" % (op, name))

    return Command(statement, **kwargs)


def python_virtualenv(name="python", **kwargs):
    kwargs.setdefault("comment", "create %s virtual environment" % name)

    return Command("virtualenv %s" % name, **kwargs)
