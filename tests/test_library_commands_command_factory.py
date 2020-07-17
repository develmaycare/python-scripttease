from scripttease.library.commands import command_factory, ItemizedCommand
from scripttease.library.commands.python import Pip
from scripttease.library.overlays import Overlay


def test_command_factory():
    overlay = Overlay("ubuntu")
    overlay.load()

    command = command_factory("nonexistent", "non existent command", overlay)
    assert command is None

    command = command_factory("pip", "install pillow", overlay)
    assert command is None

    command = command_factory("pip", "install pillow", overlay, "Pillow")
    assert isinstance(command, Pip)

    command = command_factory("pip", "install various", overlay, "$item", items=["Pillow", "pyscopg2-binary", "django"])
    assert isinstance(command, ItemizedCommand)
