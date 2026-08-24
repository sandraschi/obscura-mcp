# AGENTS.md — obscura-mcp

FastMCP 3.2 server exposing the Obscura Rust headless browser engine to AI agents.

## Architecture

- **`src/obscura_mcp/server.py`**: Main FastMCP entry point. Defines `fetch_page`, `scrape_batch`, `get_obscura_status` tools, and `fetch_with_obscura` Python helper.
- **Engine Binary**: Located at `d:\Dev\repos\external\obscura\target\release\obscura.exe`.

## Conventions

- Python 3.11+ managed with `uv`.
- Uses `FastMCP` framework.
- Standard linting via `ruff`.
