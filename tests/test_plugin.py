from vedro.core import Plugin

from vedro_jj import RemoteMockPlugin, RemoteMock


def test_interactive_plugin():
    plugin = RemoteMockPlugin(RemoteMock)
    assert isinstance(plugin, Plugin)
