from scripttease.library.overlays import Overlay


class TestOverlay(object):

    def test_get(self):
        overlay = Overlay("ubuntu")
        overlay.load()
        assert overlay.get("nonexistent", "nonexistent") is None

    def test_has(self):
        overlay = Overlay("ubuntu")
        overlay.load()
        assert overlay.has("nonexistent", "nonexistent") is False
        assert overlay.has("python", "nonexistent") is False

    def test_load(self):
        overlay = Overlay("nonexistent")
        assert overlay.load() is False
