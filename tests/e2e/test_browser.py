"""Browser-based smoke tests for the exported notebook site.

These tests verify what static HTML analysis cannot:
1. Pages load without JavaScript console errors
2. Plotly graphs render visible <svg> / <canvas> elements
3. All local inter-page links resolve (no 404s)
4. No failed network requests for local/CDN assets

Requires: uv sync --extra browser && playwright install chromium
"""

import http.server
import threading
from pathlib import Path

import pytest

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")

# Marimo static exports poll a /health endpoint expecting a live server.
# In static mode there is no server, so these 404s are expected.
_BENIGN_404_PATTERNS = ["/health"]

_BENIGN_CONSOLE_ERROR_PATTERNS = [
    "Failed to load resource",  # marimo /health polling
]


@pytest.fixture(scope="module")
def server():
    """Start a local HTTP server for the docs directory."""

    class DocsHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

        def log_message(self, format, *args):
            pass

    httpd = http.server.HTTPServer(("127.0.0.1", 0), DocsHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


@pytest.fixture(scope="module")
def browser_context():
    """Launch a headless Chromium browser."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


def _get_notebook_html_files() -> list[str]:
    """Get all notebook HTML filenames in docs/."""
    return sorted(f.name for f in DOCS_DIR.glob("*.html") if f.name != "index.html")


def _is_benign_error(msg: str) -> bool:
    return any(p in msg for p in _BENIGN_CONSOLE_ERROR_PATTERNS)


def _is_benign_404(url: str) -> bool:
    return any(p in url for p in _BENIGN_404_PATTERNS)


class TestIndexPage:
    """Verify the index page loads correctly in a browser."""

    def test_index_loads_no_console_errors(self, server, browser_context):
        errors = []
        page = browser_context.new_page()
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(f"{server}/index.html", wait_until="networkidle")

        assert page.title() == "Feynman Physics Visualizations"
        assert not errors, f"Console errors on index page: {errors}"
        page.close()

    def test_index_local_links_resolve(self, server, browser_context):
        """Verify all local notebook links on the index page are valid."""
        page = browser_context.new_page()
        page.goto(f"{server}/index.html", wait_until="networkidle")

        links = page.eval_on_selector_all(
            "a[href$='.html']",
            "els => els.map(e => e.getAttribute('href'))  .filter(h => !h.startsWith('http'))",
        )

        failed = []
        for href in links:
            resp = page.request.get(f"{server}/{href}")
            if resp.status != 200:
                failed.append(f"{href}: {resp.status}")

        assert not failed, f"Broken local links on index: {failed}"
        page.close()

    def test_index_notebook_cards_visible(self, server, browser_context):
        page = browser_context.new_page()
        page.goto(f"{server}/index.html", wait_until="networkidle")

        cards = page.query_selector_all(".card")
        expected = len(_get_notebook_html_files())
        assert len(cards) == expected, f"Expected {expected} cards, got {len(cards)}"
        page.close()


class TestNotebookPages:
    """Verify each notebook page loads and renders graphs."""

    @pytest.mark.parametrize("html_file", _get_notebook_html_files())
    def test_no_console_errors(self, server, browser_context, html_file):
        errors = []
        page = browser_context.new_page()
        page.on(
            "console",
            lambda msg: (
                errors.append(msg.text)
                if msg.type == "error" and not _is_benign_error(msg.text)
                else None
            ),
        )

        page.goto(f"{server}/{html_file}", wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(3_000)

        assert not errors, f"Console errors on {html_file}: {errors}"
        page.close()

    @pytest.mark.parametrize("html_file", _get_notebook_html_files())
    def test_plotly_graphs_visible(self, server, browser_context, html_file):
        page = browser_context.new_page()
        page.goto(f"{server}/{html_file}", wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(3_000)

        plotly_containers = page.query_selector_all(".js-plotly-plot")
        assert len(plotly_containers) > 0, f"{html_file}: no rendered Plotly graphs found"

        for i, container in enumerate(plotly_containers):
            svg_or_canvas = container.query_selector("svg.main-svg") or container.query_selector(
                "canvas"
            )
            assert svg_or_canvas, f"{html_file}: Plotly graph #{i + 1} has no rendered SVG/canvas"
        page.close()

    @pytest.mark.parametrize("html_file", _get_notebook_html_files())
    def test_no_failed_network_requests(self, server, browser_context, html_file):
        failed_requests = []
        page = browser_context.new_page()
        page.on(
            "response",
            lambda resp: (
                failed_requests.append(f"{resp.url}: {resp.status}")
                if resp.status >= 400 and not _is_benign_404(resp.url)
                else None
            ),
        )

        page.goto(f"{server}/{html_file}", wait_until="networkidle", timeout=60_000)

        assert not failed_requests, f"Failed network requests on {html_file}: {failed_requests}"
        page.close()
