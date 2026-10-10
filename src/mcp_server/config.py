"""Configuração lida de variáveis de ambiente."""

import os
from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "http"]


@dataclass(frozen=True)
class Settings:
    transport: Transport
    host: str
    port: int
    path: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport not in ("stdio", "http"):
            raise ValueError(f"MCP_TRANSPORT inválido: {transport!r} (use 'stdio' ou 'http')")
        return cls(
            transport=transport,  # type: ignore[arg-type]
            host=os.getenv("MCP_HOST", "127.0.0.1"),
            port=int(os.getenv("MCP_PORT", "8000")),
            path=os.getenv("MCP_PATH", "/mcp"),
            log_level=os.getenv("MCP_LOG_LEVEL", "INFO").upper(),
        )
