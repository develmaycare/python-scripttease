from .base import Command
from ...exceptions import InvalidInput


def dialog(message, height=15, title="Message", width=100, **kwargs):
    statement = list()
    statement.append("dialog --clear")
    statement.append('--backtitle "%s"' % title)
    statement.append('--msgbox "%s" %s %s;' % (message, height, width))
    statement.append("clear;")

    return Command(" ".join(statement), **kwargs)


def echo(message, **kwargs):
    return Command('echo "%s"' % message, **kwargs)


def explain(message, heading=None, **kwargs):
    kwargs['heading'] = heading
    return Command(message, **kwargs)


def screenshot(image, caption=None, **kwargs):
    kwargs['caption'] = caption

    return Command(image, **kwargs)


def slack(message, url=None, **kwargs):
    if url is None:
        raise InvalidInput("Slack command requires a url parameter.")

    statement = list()
    statement.append("curl -X POST -H 'Content-type: application/json' --data")
    statement.append('{"text": "%s"}' % message)
    statement.append(url)

    return Command(statement, **kwargs)


def twist(message, title="Notice", url=None, **kwargs):
    if url is None:
        raise InvalidInput("Twist command requires a url parameter.")

    statement = list()
    statement.append("curl -X POST -H 'Content-type: application/json' --data")
    statement.append('{"content": "%s", "title": "%s"' % (message, title))
    statement.append(url)

    return Command(" ".join(statement), **kwargs)
