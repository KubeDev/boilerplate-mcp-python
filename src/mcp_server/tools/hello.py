"""Tool de exemplo. Pode ser removida ao começar a implementar o servidor real."""

from fastmcp import FastMCP
from mcp.types import ToolAnnotations


def register(mcp: FastMCP) -> None:
    @mcp.tool(annotations=ToolAnnotations(title="Hello World", read_only_hint=True))
    def hello_world(name: str = "World") -> str:
        """Return a greeting for the given name."""
        return f"Hello, {name}!"
