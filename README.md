# obscura-mcp

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

FastMCP wrapper server for **Obscura** ([`d:\Dev\repos\external\obscura`](file:///d:/Dev/repos/external/obscura)), a Rust-native, lightweight, ultra-fast, and stealthy headless browser engine.

## Overview

Obscura is a drop-in headless browser replacement for Puppeteer/Playwright that runs **~12x faster** and consumes **~6x less RAM** than Chromium. It combines a real V8 engine (`deno_core`) with custom Rust DOM parsing and TLS fingerprinting (matching Chrome 145) to bypass Cloudflare anti-bot challenges and render client-side JavaScript applications.

This MCP server exposes Obscura's capabilities to AI agents and provides a reusable Python helper (`fetch_with_obscura`) for other scrapers across the fleet.

## Available MCP Tools

- `fetch_page`: Fetch a single webpage with options for `html`, `text`, `markdown`, or `links` output format, `--stealth` mode, and custom JS evaluation.
- `scrape_batch`: Perform parallel high-speed scraping across multiple URLs concurrently.
- `get_obscura_status`: Inspect the installation, version, and binary path status of the Obscura engine.

## Python Integration Helper

Other Python packages across the workspace fleet can import `fetch_with_obscura`:

```python
from obscura_mcp.server import fetch_with_obscura

# Stealth fetch DOM with JS execution
html = fetch_with_obscura("https://example.com", dump="html", stealth=True)

# Dump clean LLM-formatted Markdown
markdown = fetch_with_obscura("https://example.com", dump="markdown", stealth=True)
```

## Binary Path Resolution

The server automatically checks for the Obscura binary in the following priority:
1. `OBSCURA_PATH` environment variable
2. `OBSCURA_BIN` environment variable
3. `d:\Dev\repos\external\obscura\target\release\obscura.exe`
4. `d:\Dev\repos\external\obscura\target\debug\obscura.exe`
5. System `PATH` (`obscura`)
