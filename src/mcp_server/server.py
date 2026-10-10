"""Instância do servidor MCP. Independe do transporte usado para servi-lo."""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp_server import tools


def create_server() -> FastMCP:
    mcp = FastMCP(name="mcp-server", version="0.1.0")

    # Só é servido no modo HTTP; usado pelo healthcheck do Docker/hosts.
    @mcp.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    tools.register_all(mcp)
    return mcp


mcp = create_server()
