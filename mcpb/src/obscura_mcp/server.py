import os
import shutil
import subprocess

from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(
    "Obscura",
    instructions="A Rust-native, lightweight, and stealthy headless browser engine for AI agents.",
)

# Candidates for the Obscura binary location
CANDIDATE_PATHS = [
    os.getenv("OBSCURA_PATH"),
    os.getenv("OBSCURA_BIN"),
    r"D:\Dev\repos\external\obscura\target\release\obscura.exe",
    r"D:\Dev\repos\external\obscura\target\debug\obscura.exe",
    r"D:\Dev\repos\obscura\obscura.exe",
    shutil.which("obscura"),
]


def find_obscura_binary() -> str:
    """Resolve the absolute path to the Obscura binary."""
    for candidate in CANDIDATE_PATHS:
        if candidate and os.path.exists(candidate):
            return candidate
    return r"D:\Dev\repos\external\obscura\target\release\obscura.exe"


OBSCURA_PATH = find_obscura_binary()


def fetch_with_obscura(
    url: str,
    dump: str = "html",
    selector: str | None = None,
    wait_until: str = "load",
    stealth: bool = True,
    eval_js: str | None = None,
    timeout: int = 30,
) -> str:
    """
    Python helper to fetch a URL using the Obscura Rust engine.
    Used internally and by other fleet scrapers as a stealth rendering fallback.
    """
    bin_path = find_obscura_binary()
    if not os.path.exists(bin_path):
        raise FileNotFoundError(f"Obscura binary not found at {bin_path}")

    cmd = [bin_path, "fetch", url, "--dump", dump, "--wait-until", wait_until]
    if stealth:
        cmd.append("--stealth")
    if selector:
        cmd.extend(["--selector", selector])
    if eval_js:
        cmd.extend(["--eval", eval_js])

    result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout)
    return result.stdout


@mcp.tool()
def fetch_page(
    url: str,
    dump: str = "html",
    selector: str | None = None,
    wait_until: str = "load",
    stealth: bool = True,
    eval_js: str | None = None,
) -> str:
    """
    Fetch a single page using the Obscura engine. This is significantly faster than traditional headless browsers.

    :param url: The target URL to fetch.
    :param dump: Content format to return. Options: 'html' (full DOM), 'text' (inner text), 'markdown' (LLM formatted), 'links' (all anchor tags).
    :param selector: Optional CSS selector to wait for before returning.
    :param wait_until: Navigation wait strategy. Options: 'load', 'domcontentloaded', 'networkidle0'.
    :param stealth: Enable built-in anti-detection and tracker blocking (recommended).
    :param eval_js: Optional JavaScript to execute in the page context. The return value will be included in the output.
    """
    try:
        return fetch_with_obscura(
            url=url,
            dump=dump,
            selector=selector,
            wait_until=wait_until,
            stealth=stealth,
            eval_js=eval_js,
        )
    except FileNotFoundError as e:
        return f"Error: {e}. Please build obscura (cargo build --release) in d:\\Dev\\repos\\external\\obscura."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return f"Error fetching {url}: {error_msg}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@mcp.tool()
def scrape_batch(
    urls: list[str], concurrency: int = 10, eval_js: str | None = None, format: str = "json"
) -> str:
    """
    Scrape multiple URLs in parallel with extreme speed.

    :param urls: A list of URLs to process concurrently.
    :param concurrency: Maximum number of parallel workers (default 10).
    :param eval_js: JavaScript logic to apply to each page for data extraction.
    :param format: Output format for the batch results. Options: 'json', 'text'.
    """
    bin_path = find_obscura_binary()
    if not os.path.exists(bin_path):
        return f"Error: Obscura binary not found at {bin_path}."

    if not urls:
        return "Error: No URLs provided for batch scraping."

    cmd = [bin_path, "scrape"]
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
    bin_path = find_obscura_binary()
    if not os.path.exists(bin_path):
        return f"Obscura is NOT found at {bin_path}. Run 'cargo build --release' in d:\\Dev\\repos\\external\\obscura."

    try:
        subprocess.run([bin_path, "--help"], capture_output=True, check=True)
        return f"Obscura engine is ACTIVE and ready at {bin_path}"
    except Exception as e:
        return f"Obscura engine error: {str(e)}"


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
