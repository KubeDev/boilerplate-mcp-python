import pytest
from fastmcp.client import Client

from mcp_server.server import mcp


@pytest.fixture
async def client():
    async with Client(transport=mcp) as c:
        yield c


async def test_tools_have_review_annotations(client: Client):
    for tool in await client.list_tools():
        assert len(tool.name) <= 64
        assert tool.annotations is not None and tool.annotations.title
        assert tool.annotations.read_only_hint or tool.annotations.destructive_hint


async def test_hello_world(client: Client):
    result = await client.call_tool("hello_world", {"name": "MCP"})
    assert result.data == "Hello, MCP!"
