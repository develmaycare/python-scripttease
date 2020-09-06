from scripttease.library.overlays.common import *


def test_python_pip():
    c = python_pip("Pillow")
    assert "pip3 install Pillow" in c.get_statement()

    c = python_pip("Pillow", upgrade=True)
    assert "--upgrade" in c.get_statement()

    c = python_pip("Pillow", venv="python")
    assert "source python/bin/activate" in c.get_statement()


def test_python_virtual_env():
    c = python_virtualenv("python")
    assert "virtualenv python" in c.get_statement()


def test_run():
    c = run("ls -ls")
    assert "ls -ls" in c.get_statement()


def test_slack():
    c = slack("This is a test.", url="https://example.slack.com/asdf/1234")
    s = c.get_statement(suppress_comment=True)
    assert "curl -X POST -H 'Content-type: application/json' --data" in s
    assert "This is a test." in s
    assert "https://example.slack.com/asdf/1234" in s
