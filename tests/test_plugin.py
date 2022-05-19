from vedro.core import Plugin

from vedro_jj import RemoteMock, RemoteMockPlugin


def test_interactive_plugin():
    plugin = RemoteMockPlugin(RemoteMock)
    assert isinstance(plugin, Plugin)
