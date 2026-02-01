"""End-to-end tests for physics marimo notebooks.

These tests verify that:
1. All notebooks execute without errors
2. HTML export works correctly
3. Math content renders properly (LaTeX/KaTeX)
4. Plotly visualizations are generated
5. No Python errors appear in output
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from physics_explorations.export import (
    get_all_notebooks,
    extract_metadata,
    export_notebook,
    export_all,
)


class TestNotebookExecution:
    """Test that notebooks execute without errors."""

    def test_notebooks_exist(self):
        """Verify that notebook files exist."""
        notebooks = get_all_notebooks()
        assert len(notebooks) > 0, "No notebooks found in notebooks directory"
        for notebook in notebooks:
            assert notebook.exists(), f"Notebook {notebook} does not exist"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_syntax(self, notebook: Path):
        """Verify notebook has valid Python syntax."""
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(notebook)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in {notebook.name}: {result.stderr}"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_exports_without_errors(self, notebook: Path):
        """Verify notebook exports to HTML without cell execution errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            try:
                output_path = export_notebook(notebook, output_dir)
            except subprocess.CalledProcessError as e:
                pytest.fail(
                    f"Export failed for {notebook.name}:\n"
                    f"stdout: {e.stdout}\n"
                    f"stderr: {e.stderr}"
                )

            # Verify output file was created
            assert output_path.exists(), f"Output HTML not created for {notebook.name}"
            assert output_path.stat().st_size > 0, f"Output HTML is empty for {notebook.name}"


class TestNotebookContent:
    """Test that exported notebooks have proper content."""

    # Size limits for exported HTML (in bytes)
    MIN_HTML_SIZE = 100 * 1024        # 100 KB minimum
    MAX_HTML_SIZE = 50 * 1024 * 1024  # 50 MB maximum (physics notebooks have large animations)

    @pytest.fixture(scope="class")
    def exported_html(self) -> dict[str, tuple[str, int]]:
        """Export all notebooks and return their HTML content and size."""
        html_content = {}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            for notebook in get_all_notebooks():
                try:
                    output_path = export_notebook(notebook, output_dir)
                    if output_path.exists():
                        content = output_path.read_text()
                        size = output_path.stat().st_size
                        html_content[notebook.stem] = (content, size)
                except subprocess.CalledProcessError:
                    pass  # Skip failed exports for this fixture
        return html_content

    def test_output_size_reasonable(self, exported_html: dict[str, tuple[str, int]]):
        """Verify exported HTML is neither too small nor too large."""
        for name, (content, size) in exported_html.items():
            assert size >= self.MIN_HTML_SIZE, (
                f"{name}: Output too small ({size / 1024:.1f} KB). "
                f"Expected at least {self.MIN_HTML_SIZE / 1024:.0f} KB."
            )
            assert size <= self.MAX_HTML_SIZE, (
                f"{name}: Output too large ({size / (1024*1024):.1f} MB). "
                f"Expected at most {self.MAX_HTML_SIZE / (1024*1024):.0f} MB."
            )

    def test_html_is_valid(self, exported_html: dict[str, tuple[str, int]]):
        """Verify exported HTML has basic structure."""
        for name, (html, _size) in exported_html.items():
            assert "<!DOCTYPE html>" in html or "<html" in html, (
                f"{name}: Missing HTML doctype/root element"
            )
            assert "</html>" in html, f"{name}: HTML not properly closed"

    def test_katex_is_loaded(self, exported_html: dict[str, tuple[str, int]]):
        """Verify KaTeX is loaded for math rendering."""
        for name, (html, _size) in exported_html.items():
            assert "katex" in html.lower(), f"{name}: KaTeX not loaded"

    def test_plotly_visualizations_present(self, exported_html: dict[str, tuple[str, int]]):
        """Verify Plotly visualizations are embedded in the output."""
        for name, (html, _size) in exported_html.items():
            has_plotly = any([
                "plotly" in html.lower(),
                "Plotly.newPlot" in html,
                '"data":' in html and '"layout":' in html,
            ])
            assert has_plotly, f"{name}: Expected Plotly visualizations but found none"

    def test_no_error_messages(self, exported_html: dict[str, tuple[str, int]]):
        """Verify no Python error messages appear in output."""
        error_patterns = [
            r"Traceback \(most recent call last\)",
            r"ModuleNotFoundError",
            r"ImportError",
            r"NameError:",
            r"TypeError:",
            r"ValueError:",
            r"AttributeError:",
        ]

        for name, (html, _size) in exported_html.items():
            for pattern in error_patterns:
                matches = re.findall(pattern, html)
                if matches:
                    # Check context - might be educational content
                    if not any(
                        ctx in html.lower()
                        for ctx in ["example of error", "error handling"]
                    ):
                        assert False, f"{name}: Found error pattern '{pattern}' in output"

    def test_no_output_too_large(self, exported_html: dict[str, tuple[str, int]]):
        """Verify no 'output too large' warnings from marimo."""
        for name, (html, _size) in exported_html.items():
            if "Your output is too large" in html:
                assert False, (
                    f"{name}: Found 'output too large' warning. "
                    f"Some visualizations have too many frames or data points."
                )

    def test_no_katex_errors(self, exported_html: dict[str, tuple[str, int]]):
        """Verify no KaTeX parsing errors in output."""
        error_indicators = [
            "katex-error",
            "ParseError",
            "KaTeX parse error",
        ]

        for name, (html, _size) in exported_html.items():
            for error in error_indicators:
                if error.lower() in html.lower():
                    # Find context around error
                    idx = html.lower().find(error.lower())
                    context = html[max(0, idx-50):idx+100]
                    assert False, f"{name}: KaTeX error found: {context}"

    def test_aligned_equations_render(self, exported_html: dict[str, tuple[str, int]]):
        """Verify LaTeX aligned environments are rendered (not shown as raw text)."""
        # If aligned environments aren't rendered, they show up as raw text
        raw_latex_patterns = [
            r"\\begin\{aligned\}",  # Raw \begin{aligned}
            r"\\end\{aligned\}",    # Raw \end{aligned}
            r"&amp;=",              # HTML-escaped &= (alignment marker not processed)
        ]

        for name, (html, _size) in exported_html.items():
            for pattern in raw_latex_patterns:
                matches = re.findall(pattern, html)
                # Some raw LaTeX might appear in code examples or source views
                # but shouldn't appear many times if rendering works
                if len(matches) > 20:  # Allow some for code display
                    assert False, (
                        f"{name}: Found many instances of raw LaTeX '{pattern}' ({len(matches)}x). "
                        f"LaTeX aligned environments may not be rendering correctly."
                    )


class TestNotebookStructure:
    """Test notebook structural requirements."""

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_has_marimo_app(self, notebook: Path):
        """Verify notebook defines a marimo app."""
        content = notebook.read_text()
        assert "marimo.App" in content, f"{notebook.name}: Missing marimo.App definition"
        assert "@app.cell" in content, f"{notebook.name}: Missing @app.cell decorators"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_has_main_guard(self, notebook: Path):
        """Verify notebook has proper main guard for execution."""
        content = notebook.read_text()
        assert 'if __name__ == "__main__"' in content, (
            f"{notebook.name}: Missing __main__ guard"
        )

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_imports(self, notebook: Path):
        """Verify notebook has required imports."""
        content = notebook.read_text()
        required_imports = ["marimo", "numpy", "plotly"]

        for imp in required_imports:
            has_import = f"import {imp}" in content or f"from {imp}" in content
            assert has_import, f"{notebook.name}: Missing import for {imp}"


class TestNoRuntimeWarnings:
    """Test that notebooks don't produce runtime warnings."""

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_runtime_warnings_during_export(self, notebook: Path):
        """Verify notebook export doesn't produce RuntimeWarnings (e.g., invalid sqrt)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / f"{notebook.stem}.html"

            result = subprocess.run(
                [
                    sys.executable, "-m", "marimo", "export", "html",
                    str(notebook), "-o", str(output_path), "--no-include-code"
                ],
                capture_output=True,
                text=True,
                env={**subprocess.os.environ, "PYTHONWARNINGS": "error::RuntimeWarning"},
            )

            # Check stderr for RuntimeWarnings (may appear even with non-zero exit)
            warning_patterns = [
                "RuntimeWarning",
                "invalid value encountered",
                "divide by zero",
                "overflow encountered",
            ]

            for pattern in warning_patterns:
                if pattern in result.stderr:
                    pytest.fail(
                        f"{notebook.name}: RuntimeWarning during export:\n{result.stderr}"
                    )


class TestMetadataExtraction:
    """Test that notebook metadata extraction works correctly."""

    def test_all_notebooks_have_metadata(self):
        """Verify metadata can be extracted from all notebooks."""
        for notebook in get_all_notebooks():
            meta = extract_metadata(notebook)
            assert meta.number, f"{notebook.name}: Missing number"
            assert meta.title, f"{notebook.name}: Missing title"
            assert meta.description, f"{notebook.name}: Missing description"
            assert len(meta.tags) > 0, f"{notebook.name}: No tags inferred"

    def test_notebook_titles_are_unique(self):
        """Verify all notebooks have unique titles."""
        notebooks = get_all_notebooks()
        titles = [extract_metadata(nb).title for nb in notebooks]
        assert len(titles) == len(set(titles)), "Duplicate notebook titles found"


class TestExportAll:
    """Test the full export workflow."""

    def test_export_all_creates_files(self):
        """Verify export_all creates all expected files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            generated = export_all(output_dir)

            # Should have one HTML per notebook plus index.html
            notebooks = get_all_notebooks()
            expected_count = len(notebooks) + 1

            assert len(generated) == expected_count, (
                f"Expected {expected_count} files, got {len(generated)}"
            )

            # Verify index.html exists and has content
            index_path = output_dir / "index.html"
            assert index_path.exists(), "index.html not created"
            index_content = index_path.read_text()
            assert "Feynman Physics" in index_content
            assert "card" in index_content  # Should have notebook cards

    def test_index_links_all_notebooks(self):
        """Verify index.html links to all notebooks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            export_all(output_dir)

            index_content = (output_dir / "index.html").read_text()
            for notebook in get_all_notebooks():
                html_name = f"{notebook.stem}.html"
                assert html_name in index_content, (
                    f"index.html missing link to {html_name}"
                )
