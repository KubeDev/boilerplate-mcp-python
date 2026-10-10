"""Registro das tools. Cada módulo expõe `register(mcp)`."""

from fastmcp import FastMCP

from mcp_server.tools import hello


def register_all(mcp: FastMCP) -> None:
    hello.register(mcp)
