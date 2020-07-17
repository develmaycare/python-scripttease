from scripttease.library.commands.python import *
from scripttease.library.overlays import Overlay


def test_pip():
    pip = Pip("Pillow")
    assert "pip install -y Pillow" in pip.get_statement()

    overlay = Overlay("ubuntu")
    overlay.load()

    pip = Pip("Pillow", op="remove", overlay=overlay, venv="python")
    assert "source python/bin/activate && pip3 uninstall --quiet Pillow" in pip.get_statement()


def test_virtualenv():
    virt = VirtualEnv()
    assert "virtualenv python" in virt.get_statement()
