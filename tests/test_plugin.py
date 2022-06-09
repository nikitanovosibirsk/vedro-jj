import pytest
from aiohttp import ClientSession
from vedro.core import Dispatcher, Report
from vedro.events import CleanupEvent, StartupEvent

import jj
import vedro_jj
from jj.mock import Mocked, mocked
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


@pytest.fixture()
async def mock() -> Mocked:
    async with mocked(jj.match("*"), jj.Response()) as mock:
        yield mock


@pytest.mark.asyncio
async def test_mock(plugin: RemoteMockPlugin, mock: Mocked):
    async with mock:
        async with ClientSession() as session:
            response = await session.get("http://localhost:8080")
        assert response.status == 200


@pytest.mark.asyncio
async def test_mock_threaded(plugin_threaded: RemoteMockPlugin, mock: Mocked):
    async with ClientSession() as session:
        response = await session.get("http://localhost:8080")
    assert response.status == 200
