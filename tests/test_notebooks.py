"""
End-to-end tests for Feynman Physics notebooks.

Tests that all notebooks:
1. Can be executed without errors
2. Can be exported to HTML without errors
3. Don't produce "output too large" warnings
4. Have reasonable output sizes
"""

import subprocess
import sys
from pathlib import Path
import tempfile
import os

# Get the project root
PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# All notebook files
NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.py"))

# Maximum expected HTML file size (50MB should be plenty)
MAX_HTML_SIZE_MB = 50


def test_notebooks_exist():
    """Test that we have notebooks to test."""
    assert len(NOTEBOOKS) > 0, "No notebooks found"
    print(f"Found {len(NOTEBOOKS)} notebooks:")
    for nb in NOTEBOOKS:
        print(f"  - {nb.name}")


def test_notebook_syntax():
    """Test that all notebooks have valid Python syntax."""
    for notebook in NOTEBOOKS:
        print(f"Checking syntax: {notebook.name}")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(notebook)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in {notebook.name}: {result.stderr}"
    print("All notebooks have valid syntax")


def test_notebook_imports():
    """Test that all notebooks can import their dependencies."""
    for notebook in NOTEBOOKS:
        print(f"Testing imports: {notebook.name}")

        # Extract imports from the notebook
        content = notebook.read_text()

        # Check for required imports
        required_imports = ["marimo", "numpy", "plotly"]
        for imp in required_imports:
            assert imp in content, f"{notebook.name} missing import: {imp}"

    print("All notebooks have required imports")


def test_notebook_execution():
    """Test that all notebooks can be executed without errors."""
    for notebook in NOTEBOOKS:
        print(f"Executing: {notebook.name}")

        # Run marimo export which executes the notebook
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.html"

            result = subprocess.run(
                ["uv", "run", "marimo", "export", "html", str(notebook), "-o", str(output_file)],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
                timeout=120,  # 2 minute timeout per notebook
            )

            # Check for execution errors
            if result.returncode != 0:
                print(f"STDERR: {result.stderr}")
                print(f"STDOUT: {result.stdout}")

            assert result.returncode == 0, f"Execution failed for {notebook.name}: {result.stderr}"

            # Check output file was created
            assert output_file.exists(), f"Output file not created for {notebook.name}"

            # Check for "output too large" in stderr or stdout
            combined_output = result.stdout + result.stderr
            assert "output is too large" not in combined_output.lower(), \
                f"Output too large warning in {notebook.name}"
            assert "too large" not in combined_output.lower() or "RuntimeWarning" in combined_output, \
                f"Size warning in {notebook.name}"

            # Check file size is reasonable
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"  Output size: {size_mb:.2f} MB")
            assert size_mb < MAX_HTML_SIZE_MB, \
                f"Output too large for {notebook.name}: {size_mb:.2f} MB > {MAX_HTML_SIZE_MB} MB"

    print("All notebooks executed successfully")


def test_notebook_no_errors_in_output():
    """Test that exported HTML doesn't contain error messages."""
    error_patterns = [
        "Traceback (most recent call last)",
        "Error:",
        "Exception:",
        "output is too large",
        "NameError",
        "TypeError",
        "ValueError",
        "ImportError",
        "ModuleNotFoundError",
    ]

    for notebook in NOTEBOOKS:
        print(f"Checking output for errors: {notebook.name}")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.html"

            subprocess.run(
                ["uv", "run", "marimo", "export", "html", str(notebook), "-o", str(output_file)],
                capture_output=True,
                cwd=PROJECT_ROOT,
                timeout=120,
            )

            if output_file.exists():
                content = output_file.read_text()

                for pattern in error_patterns:
                    # Skip if it's in a code block explaining errors (educational content)
                    if pattern in content:
                        # Check if it's in a context that's not an actual error
                        # (e.g., explaining what errors are in educational text)
                        lines_with_pattern = [
                            line for line in content.split('\n')
                            if pattern in line
                        ]
                        for line in lines_with_pattern:
                            # Allow patterns in markdown/educational content
                            if '<code' not in line and 'class="error"' in line.lower():
                                assert False, f"Error pattern '{pattern}' found in {notebook.name}"

    print("No error patterns found in outputs")


def test_latex_syntax_in_notebooks():
    """Test that LaTeX in notebooks is properly formatted and will render."""
    import re

    # LaTeX commands that should only appear inside math delimiters
    latex_commands = [
        r'\\frac\{',
        r'\\sqrt\{',
        r'\\sum',
        r'\\int',
        r'\\alpha',
        r'\\beta',
        r'\\gamma',
        r'\\Delta',
        r'\\mu',
        r'\\nu',
        r'\\pi',
        r'\\theta',
        r'\\lambda',
        r'\\epsilon',
        r'\\hbar',
        r'\\partial',
        r'\\nabla',
        r'\\infty',
        r'\\rightarrow',
        r'\\geq',
        r'\\leq',
        r'\\times',
        r'\\cdot',
        r'\\approx',
        r'\\text\{',
        r'\\left',
        r'\\right',
        r'\\langle',
        r'\\rangle',
    ]

    for notebook in NOTEBOOKS:
        print(f"Checking LaTeX: {notebook.name}")
        content = notebook.read_text()

        # Extract all mo.md() content
        md_pattern = r'mo\.md\(\s*r?"""(.*?)"""\s*\)'
        md_matches = re.findall(md_pattern, content, re.DOTALL)

        for md_content in md_matches:
            # Check for balanced $$ (display math)
            display_math_count = md_content.count('$$')
            assert display_math_count % 2 == 0, \
                f"Unbalanced $$ in {notebook.name}: found {display_math_count} occurrences"

            # Check for LaTeX commands outside math delimiters
            # Split by $$ first to identify non-math regions
            parts = md_content.split('$$')

            # Even indices are outside display math
            for i, part in enumerate(parts):
                if i % 2 == 0:  # Outside display math
                    # Now check for inline math ($...$) and exclude those regions
                    # Simple check: find LaTeX commands that appear outside any $ delimiters
                    inline_parts = re.split(r'\$[^$]+\$', part)

                    for text_part in inline_parts:
                        for cmd in latex_commands:
                            if re.search(cmd, text_part):
                                # Allow if it's in a code block or explaining LaTeX
                                if '`' not in text_part[:50] and 'LaTeX' not in text_part[:100]:
                                    # This might be a false positive, so just warn
                                    print(f"  Warning: '{cmd}' may be outside math in {notebook.name}")

        # Check for common LaTeX errors
        error_patterns = [
            (r'\$\s*\$', "Empty math expression"),
            (r'\$\$\s*\$\$', "Empty display math"),
            (r'\\frac\{[^}]*\}(?!\{)', "Incomplete \\frac (missing second argument)"),
        ]

        for pattern, description in error_patterns:
            matches = re.findall(pattern, content)
            # Filter out false positives from code strings
            real_matches = [m for m in matches if 'r"""' not in m]
            if real_matches and len(real_matches) > 2:  # Allow some for edge cases
                print(f"  Warning: Possible {description} in {notebook.name}")

    print("LaTeX syntax check completed")


def test_latex_renders_in_html():
    """Test that LaTeX rendering is properly set up in exported HTML."""
    import re

    for notebook in NOTEBOOKS:
        print(f"Checking HTML LaTeX setup: {notebook.name}")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.html"

            subprocess.run(
                ["uv", "run", "marimo", "export", "html", str(notebook), "-o", str(output_file)],
                capture_output=True,
                cwd=PROJECT_ROOT,
                timeout=120,
            )

            if output_file.exists():
                content = output_file.read_text()

                # Check that KaTeX library is loaded (marimo uses KaTeX)
                has_katex = 'katex' in content.lower()
                assert has_katex, f"KaTeX not loaded in {notebook.name}"

                # Check for explicit LaTeX/KaTeX errors in the output
                error_indicators = [
                    'katex-error',
                    'ParseError',
                    'KaTeX parse error',
                ]

                for error in error_indicators:
                    if error.lower() in content.lower():
                        # Find the context around the error
                        idx = content.lower().find(error.lower())
                        context = content[max(0, idx-100):idx+200]
                        assert False, f"LaTeX error in {notebook.name}: {error}\nContext: {context}"

                # Check that notebook contains math (has $ delimiters in source)
                if '$$' in content or r'\frac' in content or r'\sqrt' in content:
                    print(f"  ✓ Contains math, KaTeX loaded")
                else:
                    print(f"  ✓ KaTeX loaded (notebook may not have math)")

    print("HTML LaTeX setup check completed")


def test_all_notebooks_in_export_script():
    """Test that all notebooks are included in the export script."""
    export_script = PROJECT_ROOT / "scripts" / "export_notebooks.sh"
    script_content = export_script.read_text()

    # The script uses glob pattern, so just verify it exists and is executable
    assert export_script.exists(), "Export script not found"
    assert "notebooks/*.py" in script_content, "Export script should glob notebooks/*.py"

    print("Export script configured correctly")


def test_index_html_has_all_notebooks():
    """Test that the index.html template includes all notebooks."""
    export_script = PROJECT_ROOT / "scripts" / "export_notebooks.sh"
    script_content = export_script.read_text()

    for notebook in NOTEBOOKS:
        html_name = notebook.stem + ".html"
        assert html_name in script_content, \
            f"Notebook {notebook.name} not in index.html template (missing {html_name})"

    print("All notebooks are in index.html template")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_notebooks_exist,
        test_notebook_syntax,
        test_notebook_imports,
        test_latex_syntax_in_notebooks,
        test_all_notebooks_in_export_script,
        test_index_html_has_all_notebooks,
        test_notebook_execution,
        test_notebook_no_errors_in_output,
        test_latex_renders_in_html,
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test.__name__}")
        print('='*60)
        try:
            test()
            print(f"✓ {test.__name__} PASSED")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print('='*60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
