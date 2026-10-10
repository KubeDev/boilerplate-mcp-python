# AGENTS.md

Servidor MCP em Python com [FastMCP](https://gofastmcp.com) 4.x. O mesmo servidor é servido por **stdio** (uso local) ou **HTTP streamable** (remoto/Docker), escolhido na inicialização.

> **OBS:** a tool `hello_world` (`src/mcp_server/tools/hello.py`) e o teste `test_hello_world` são apenas exemplo. Remova-os ao começar a implementar as tools reais — e retire `hello` de `src/mcp_server/tools/__init__.py`.

## Comandos

```bash
uv sync                                   # instala dependências
uv run pytest                             # testes (cliente em memória, sem rede)
uv run ruff check . && uv run ruff format .
uv run mcp-server                         # stdio
uv run mcp-server --transport http        # HTTP em http://127.0.0.1:8000/mcp
docker compose up --build                 # HTTP em container (porta 8000)
```

## Estrutura

```
src/mcp_server/
  __main__.py      # CLI: escolhe stdio ou http (flag --transport ou MCP_TRANSPORT)
  config.py        # Settings lidas de variáveis de ambiente (MCP_*)
  server.py        # cria o FastMCP, rota /health, registra as tools
  tools/
    __init__.py    # register_all(mcp): chama register() de cada módulo
    hello.py       # exemplo (remover)
src/Dockerfile     # build com contexto na raiz: docker build -f src/Dockerfile .
docker-compose.yml # sobe o modo HTTP
tests/
```

## Adicionando uma tool

1. Crie `src/mcp_server/tools/<dominio>.py` com uma função `register(mcp: FastMCP)` que declara as tools com `@mcp.tool`.
2. Registre o módulo em `tools/__init__.py` (`register_all`).
3. Adicione testes em `tests/` usando `Client(transport=mcp)`.

As tools não sabem por qual transporte estão sendo chamadas — nunca ramifique lógica por transporte.

## Regras

- **Nunca escreva no stdout.** No modo stdio o stdout é o canal do protocolo; `print()` corrompe a sessão. Use `logging` (já configurado para stderr) ou `ctx.info()`.
- **Toda tool tem anotações** via `ToolAnnotations`: `title` + `read_only_hint=True` (leitura) ou `destructive_hint=True` (escrita/remoção). O teste `test_tools_have_review_annotations` garante isso — é critério de revisão do diretório de conectores do Claude.
- **Separe leitura de escrita.** Nada de tool genérica com parâmetro `method`; prefira `create_x`, `update_x`, `delete_x`.
- **Nomes de tool** em `snake_case`, até 64 caracteres.
- **Docstring = descrição da tool** que vai para o contexto do modelo: curta, diz o que faz e quando usar. Não dê instruções de comportamento ao modelo.
- **Erros acionáveis:** levante `fastmcp.exceptions.ToolError` com mensagem que explique o que corrigir.
- **Respostas enxutas:** retorne só o necessário, pagine listas grandes.
- **Configuração e segredos** só via variáveis de ambiente (adicione em `config.py` e `.env.example`), nunca hardcoded.
- O servidor HTTP roda em modo **stateless** (`stateless_http=True`). Só mude se alguma tool precisar de estado entre chamadas na mesma sessão.
