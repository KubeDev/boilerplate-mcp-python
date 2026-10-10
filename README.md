# boilerplate-mcp-python

Boilerplate de servidor [MCP](https://modelcontextprotocol.io) em Python usando [FastMCP](https://gofastmcp.com). Um único servidor, dois transportes:

- **stdio** — o cliente (Claude Code, Claude Desktop, etc.) inicia o processo localmente.
- **HTTP streamable** — servidor remoto em `/mcp`, pronto para Docker.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker (opcional, para o modo HTTP em container)

## Início rápido

```bash
uv sync
uv run pytest
```

### Modo stdio

```bash
uv run mcp-server
```

Adicionando ao Claude Code:

```bash
claude mcp add meu-servidor -- uv run --directory /caminho/para/o/projeto mcp-server
```

### Modo HTTP

```bash
uv run mcp-server --transport http
# MCP:    http://127.0.0.1:8000/mcp
# Health: http://127.0.0.1:8000/health
```

Adicionando ao Claude Code:

```bash
claude mcp add --transport http meu-servidor http://127.0.0.1:8000/mcp
```

### Docker

```bash
docker compose up --build
```

O compose usa `src/Dockerfile` com o contexto de build na raiz. Para buildar sem o compose:

```bash
docker build -f src/Dockerfile -t mcp-server .
docker run --rm -p 8000:8000 mcp-server
```

## Configuração

Variáveis de ambiente (veja `.env.example`):

| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_TRANSPORT` | `stdio` | `stdio` ou `http` (a flag `--transport` sobrescreve) |
| `MCP_HOST` | `127.0.0.1` | Host do modo HTTP (`0.0.0.0` no container) |
| `MCP_PORT` | `8000` | Porta do modo HTTP |
| `MCP_PATH` | `/mcp` | Caminho do endpoint MCP |
| `MCP_LOG_LEVEL` | `INFO` | Nível de log (sempre no stderr) |

## Estrutura

```
src/
  Dockerfile
  mcp_server/
    __main__.py      # CLI e escolha do transporte
    config.py        # variáveis de ambiente
    server.py        # instância FastMCP + /health
    tools/           # um módulo por domínio, cada um com register(mcp)
tests/
docker-compose.yml
```

## Criando suas tools

A tool `hello_world` é só um exemplo — remova-a ao começar. Para adicionar uma tool:

```python
# src/mcp_server/tools/items.py
from fastmcp import FastMCP
from mcp.types import ToolAnnotations


def register(mcp: FastMCP) -> None:
    @mcp.tool(annotations=ToolAnnotations(title="Search items", read_only_hint=True))
    def search_items(query: str, limit: int = 10) -> list[dict]:
        """Search items by keyword."""
        ...
```

Depois registre o módulo em `src/mcp_server/tools/__init__.py`. Regras e convenções completas estão em [AGENTS.md](AGENTS.md).

## Testando

```bash
uv run pytest                                  # testes com cliente em memória
npx @modelcontextprotocol/inspector            # inspeção interativa (stdio ou HTTP)
```
