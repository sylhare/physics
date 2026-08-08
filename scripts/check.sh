#!/usr/bin/env bash
#
# Local verification gate — run this before/after changing notebooks or the
# visualization library to make sure the notebooks and the exported website
# still build and render. Mirrors .github/workflows/ci.yml.
#
# Usage:
#   scripts/check.sh              # lint + unit + notebook/website render + build
#   RUN_BROWSER=1 scripts/check.sh  # also run the real-browser tests
#                                   # (needs: uv sync --extra browser
#                                   #         && uv run playwright install chromium)
#
set -euo pipefail

cd "$(dirname "$0")/.."

step() { printf '\n\033[1;34m==> %s\033[0m\n' "$1"; }

step "Lint (ruff check)"
uv run ruff check .

step "Lint (ruff format --check)"
uv run ruff format --check .

step "Unit tests"
uv run pytest tests/unit -q

step "Notebook + website render tests"
# Executes every notebook, exports it to HTML and asserts each Plotly figure
# renders, math/KaTeX loads, and the index links to all notebooks.
uv run pytest tests/e2e/test_notebooks.py -q --tb=short

step "Build static site (docs/)"
uv run python -m physics_explorations.export

if [ "${RUN_BROWSER:-0}" = "1" ]; then
    step "Browser render tests"
    uv run pytest tests/e2e/test_browser.py -q --tb=short
else
    printf '\n(skipping browser tests — set RUN_BROWSER=1 to include them)\n'
fi

printf '\n\033[1;32m✓ All checks passed.\033[0m\n'
