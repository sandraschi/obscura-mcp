# obscura-mcp (MCPB Bundle)

Add your description here

## Usage

Add to \claude_desktop_config.json\:
\\\json
{
  "mcpServers": {
    "obscura-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "\D:\Dev\repos", "python", "-m", "obscura_mcp"],
      "env": { "PYTHONPATH": "\D:\Dev\repos/src" }
    }
  }
}
\\\

## Tools

- **obscura-mcp**: Add your description here

## Requirements

- Python 3.12+
- uv
