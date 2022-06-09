import pytest
from aiohttp import ClientSession
from vedro.core import Dispatcher, Report
from vedro.events import CleanupEvent, StartupEvent

import vedro_jj
from vedro_jj import RemoteMockPlugin


@pytest.fixture()
def dispatcher() -> Dispatcher:
    return Dispatcher()


@pytest.fixture()
async def plugin(dispatcher: Dispatcher) -> RemoteMockPlugin:
    class RemoteMock(vedro_jj.RemoteMock):
        threaded = False

    plugin = RemoteMockPlugin(RemoteMock)
    plugin.subscribe(dispatcher)

    await dispatcher.fire(StartupEvent([]))
    yield plugin
    await dispatcher.fire(CleanupEvent(Report()))


@pytest.fixture()
async def plugin_threaded(dispatcher: Dispatcher) -> RemoteMockPlugin:
    class RemoteMockThreaded(vedro_jj.RemoteMock):
        threaded = True

    plugin = RemoteMockPlugin(RemoteMockThreaded)
    plugin.subscribe(dispatcher)

    await dispatcher.fire(StartupEvent([]))
    yield plugin
    await dispatcher.fire(CleanupEvent(Report()))


@pytest.mark.asyncio
async def test_mock(plugin: RemoteMockPlugin, dispatcher):
    async with ClientSession() as session:
        response = await session.get("http://localhost:8080")
    assert response.status == 404


@pytest.mark.asyncio
async def test_mock_threaded(plugin: RemoteMockPlugin, dispatcher):
    async with ClientSession() as session:
        response = await session.get("http://localhost:8080")
    assert response.status == 404
