"""Ponto de entrada: `mcp-server [--transport stdio|http]`."""

import argparse
import logging
import sys

from mcp_server.config import Settings
from mcp_server.server import mcp


def main() -> None:
    settings = Settings.from_env()

    parser = argparse.ArgumentParser(prog="mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default=settings.transport,
        help="Sobrescreve MCP_TRANSPORT (padrão: stdio)",
    )
    args = parser.parse_args()

    # No stdio o stdout é o canal do protocolo: logs sempre no stderr.
    logging.basicConfig(level=settings.log_level, stream=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio", show_banner=False)
    else:
        mcp.run(
            transport="http",
            host=settings.host,
            port=settings.port,
            path=settings.path,
            stateless_http=True,
            show_banner=False,
        )


if __name__ == "__main__":
    main()
