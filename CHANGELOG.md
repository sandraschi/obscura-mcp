# Changelog

All notable changes to obscura-mcp are documented here.

## [Unreleased] — 2026-08-24

### Changed
- **Binary Path Resolution**: Updated default binary path resolution to search `d:\Dev\repos\external\obscura\target\release\obscura.exe`, `OBSCURA_BIN`, `OBSCURA_PATH`, and system `PATH`.

### Added
- **Markdown Dump Support**: Added support for `--dump markdown` format in `fetch_page` MCP tool.
- **Python Integration Helper**: Exported `fetch_with_obscura()` helper for direct Python import by fleet scrapers (`tvtropes-mcp`, `aiwatcher-mcp`, `scraper-mcp`).
