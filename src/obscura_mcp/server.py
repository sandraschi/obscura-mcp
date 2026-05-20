import subprocess
import os
import json
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize FastMCP server
# We use the name "Obscura" which will appear in the MCP client
mcp = FastMCP(
    "Obscura",
    instructions="A Rust-native, lightweight, and stealthy headless browser engine for AI agents.",
)

# Configuration: Path to the Obscura binary
# In a real-world scenario, this might be configurable via environment variables
OBSCURA_PATH = os.getenv("OBSCURA_PATH", r"D:\Dev\repos\obscura\obscura.exe")

@mcp.tool()
def fetch_page(
    url: str,
    dump: str = "html",
    selector: Optional[str] = None,
    wait_until: str = "load",
    stealth: bool = True,
    eval_js: Optional[str] = None
) -> str:
    """
    Fetch a single page using the Obscura engine. This is significantly faster than traditional headless browsers.
    
    :param url: The target URL to fetch.
    :param dump: Content format to return. Options: 'html' (full DOM), 'text' (inner text), 'links' (all anchor tags).
    :param selector: Optional CSS selector to wait for before returning.
    :param wait_until: Navigation wait strategy. Options: 'load', 'domcontentloaded', 'networkidle0'.
    :param stealth: Enable built-in anti-detection and tracker blocking (recommended).
    :param eval_js: Optional JavaScript to execute in the page context. The return value will be included in the output.
    """
    if not os.path.exists(OBSCURA_PATH):
        return f"Error: Obscura binary not found at {OBSCURA_PATH}. Please ensure it is installed."

    cmd = [OBSCURA_PATH, "fetch", url, "--dump", dump, "--wait-until", wait_until]
    if stealth:
        cmd.append("--stealth")
    if selector:
        cmd.extend(["--selector", selector])
    if eval_js:
        cmd.extend(["--eval", eval_js])
        
    try:
        # Use subprocess.run for a clean execution
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return f"Error fetching {url}: {error_msg}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
def scrape_batch(
    urls: List[str],
    concurrency: int = 10,
    eval_js: Optional[str] = None,
    format: str = "json"
) -> str:
    """
    Scrape multiple URLs in parallel with extreme speed.
    
    :param urls: A list of URLs to process concurrently.
    :param concurrency: Maximum number of parallel workers (default 10).
    :param eval_js: JavaScript logic to apply to each page for data extraction.
    :param format: Output format for the batch results. Options: 'json', 'text'.
    """
    if not os.path.exists(OBSCURA_PATH):
        return f"Error: Obscura binary not found at {OBSCURA_PATH}."

    if not urls:
        return "Error: No URLs provided for batch scraping."

    cmd = [OBSCURA_PATH, "scrape"]
    cmd.extend(urls)
    cmd.extend(["--concurrency", str(concurrency), "--format", format])
    if eval_js:
        cmd.extend(["--eval", eval_js])
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return f"Error during batch scrape: {error_msg}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
def get_obscura_status() -> str:
    """
    Get the current version and configuration status of the Obscura engine.
    """
    if not os.path.exists(OBSCURA_PATH):
        return f"Obscura is NOT found at {OBSCURA_PATH}"
    
    # Obscura doesn't have a direct --version yet in this version, but we can check help
    try:
        # Just check if we can run it
        subprocess.run([OBSCURA_PATH, "--help"], capture_output=True, check=True)
        return f"Obscura engine is ACTIVE and ready at {OBSCURA_PATH}"
    except Exception as e:
        return f"Obscura engine error: {str(e)}"

def main():
    """Entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
