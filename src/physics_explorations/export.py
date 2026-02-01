"""
Notebook export utilities for Physics Explorations.

This module provides functions to:
- Discover notebooks in the notebooks directory
- Extract metadata (title, description, tags) from notebooks
- Export notebooks to HTML
- Generate the index.html page dynamically
"""

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"


@dataclass
class NotebookMetadata:
    """Metadata extracted from a notebook."""

    number: str
    stem: str
    title: str
    description: str
    tags: list[str]
    path: Path
    category: str  # "feynman" or "exploration"


# Notebooks that are part of the Feynman Lectures series
FEYNMAN_NOTEBOOKS = {
    "gravitation", "speed_of_light", "spacetime", "wave_particle",
    "magnetism", "charged_motion", "black_holes"
}


def get_all_notebooks() -> list[Path]:
    """Get all notebook files in the notebooks directory, sorted by name."""
    return sorted(NOTEBOOKS_DIR.glob("*.py"))


def extract_metadata(notebook_path: Path) -> NotebookMetadata:
    """Extract metadata from a notebook file.

    Parses the notebook to find:
    - Number: position in sorted list (1-indexed)
    - Title: from the first markdown heading
    - Description: from content or first paragraph
    - Tags: inferred from content
    """
    content = notebook_path.read_text()
    stem = notebook_path.stem

    # Get number from position in sorted list
    all_notebooks = get_all_notebooks()
    try:
        number = str(all_notebooks.index(notebook_path) + 1)
    except ValueError:
        number = "0"

    # Extract title from first markdown heading (# Title)
    title_match = re.search(r'mo\.md\(\s*r?"""[^"]*?#\s+([^\n]+)', content)
    if title_match:
        title = title_match.group(1).strip()
        # Clean up any trailing asterisks or formatting
        title = re.sub(r"\*+$", "", title).strip()
    else:
        # Fallback: convert filename to title
        title = stem.replace("_", " ").title()

    # Extract description from first substantial paragraph after title
    desc_match = re.search(
        r'mo\.md\(\s*r?"""[^"]*?#[^\n]+\n+([^#\n][^\n]+)',
        content
    )
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        description = f"Interactive exploration of {title.lower()}."

    # Truncate description if too long
    if len(description) > 200:
        description = description[:197] + "..."

    # Infer tags from content
    tags = _infer_tags(content, stem)

    # Determine category based on stem
    category = "feynman" if stem in FEYNMAN_NOTEBOOKS else "exploration"

    return NotebookMetadata(
        number=number,
        stem=stem,
        title=title,
        description=description,
        tags=tags,
        path=notebook_path,
        category=category,
    )


def _infer_tags(content: str, stem: str) -> list[str]:
    """Infer tags from notebook content and filename."""
    tags = []
    content_lower = content.lower()
    stem_lower = stem.lower()

    # Physics tag mappings: keyword -> tag
    tag_keywords = {
        # Mechanics & Gravity
        "gravitation": "Gravity",
        "gravity": "Gravity",
        "kepler": "Orbital Mechanics",
        "orbit": "Orbital Mechanics",
        "newton": "Classical Mechanics",
        # Electromagnetism
        "magnetic": "Electromagnetism",
        "electric": "Electromagnetism",
        "electromagnetic": "Electromagnetism",
        "maxwell": "Electromagnetism",
        "motor": "Motors",
        "induction": "Induction",
        "faraday": "Induction",
        # Relativity
        "relativity": "Relativity",
        "spacetime": "Relativity",
        "lorentz": "Relativity",
        "einstein": "Relativity",
        "time dilation": "Relativity",
        "light speed": "Relativity",
        "speed of light": "Optics",
        # Quantum
        "quantum": "Quantum Mechanics",
        "wave-particle": "Quantum Mechanics",
        "photon": "Quantum Mechanics",
        "double-slit": "Quantum Mechanics",
        "heisenberg": "Quantum Mechanics",
        "de broglie": "Quantum Mechanics",
        # Cosmology & Astrophysics
        "black hole": "Black Holes",
        "schwarzschild": "Black Holes",
        "hawking": "Black Holes",
        "event horizon": "Black Holes",
        # Exotic physics
        "tachyon": "Exotic Physics",
        "wormhole": "Exotic Physics",
        "exotic matter": "Exotic Physics",
        "casimir": "Quantum Field Theory",
        "warp": "Exotic Physics",
        # General
        "animation": "Animations",
        "visualization": "Visualizations",
        "feynman": "Feynman Lectures",
    }

    for keyword, tag in tag_keywords.items():
        if keyword in content_lower or keyword in stem_lower:
            if tag not in tags:
                tags.append(tag)

    # Limit to 4 most relevant tags
    return tags[:4] if tags else ["Physics"]


def export_notebook(
    notebook_path: Path,
    output_dir: Path,
    include_code: bool = False
) -> Path:
    """Export a single notebook to HTML.

    Args:
        notebook_path: Path to the notebook file
        output_dir: Directory to write the HTML file
        include_code: Whether to include source code in output

    Returns:
        Path to the generated HTML file

    Raises:
        subprocess.CalledProcessError: If export fails
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{notebook_path.stem}.html"

    cmd = [
        "uv", "run", "marimo", "export", "html",
        str(notebook_path),
        "-o", str(output_path),
    ]
    if not include_code:
        cmd.append("--no-include-code")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=180,
    )

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )

    return output_path


def generate_index_html(notebooks: list[NotebookMetadata], output_dir: Path) -> Path:
    """Generate the index.html page from notebook metadata.

    Args:
        notebooks: List of notebook metadata
        output_dir: Directory to write the index.html file

    Returns:
        Path to the generated index.html file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split notebooks into categories
    feynman_notebooks = [nb for nb in notebooks if nb.category == "feynman"]
    exploration_notebooks = [nb for nb in notebooks if nb.category == "exploration"]

    # Generate notebook cards for each section
    feynman_cards = "\n".join(_generate_card(nb) for nb in feynman_notebooks)
    exploration_cards = "\n".join(
        _generate_card(nb, show_badge=True) for nb in exploration_notebooks
    )

    # Get GitHub repository URL from environment (set in CI)
    github_repo = os.environ.get("GITHUB_REPOSITORY", "")
    github_url = f"https://github.com/{github_repo}" if github_repo else "#"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feynman Physics Visualizations</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e4e4e7;
            min-height: 100vh;
            padding: 2rem;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 1rem 0;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .subtitle {{
            font-size: 1.1rem;
            color: #a1a1aa;
            margin-bottom: 1rem;
        }}

        .subtitle a {{
            color: #60a5fa;
            text-decoration: none;
        }}

        .subtitle a:hover {{
            text-decoration: underline;
        }}

        .section-header {{
            font-size: 1.5rem;
            color: #60a5fa;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .notebooks {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: all 0.2s ease;
        }}

        .card:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(96, 165, 250, 0.5);
            transform: translateY(-2px);
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }}

        .card-number {{
            font-size: 0.85rem;
            font-weight: 600;
            color: #60a5fa;
            background: rgba(96, 165, 250, 0.1);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
        }}

        .card-title {{
            font-size: 1.25rem;
            color: #f4f4f5;
        }}

        .exploration-badge {{
            background: rgba(167, 139, 250, 0.2);
            color: #a78bfa;
            padding: 0.15rem 0.5rem;
            border-radius: 8px;
            font-size: 0.7rem;
            margin-left: 0.5rem;
        }}

        .card-description {{
            font-size: 0.95rem;
            color: #a1a1aa;
            margin-bottom: 0.75rem;
        }}

        .card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .tag {{
            background: rgba(167, 139, 250, 0.1);
            color: #a78bfa;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
        }}

        footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #71717a;
            font-size: 0.875rem;
        }}

        footer a {{
            color: #60a5fa;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}

            header {{
                padding: 1rem 0;
                margin-bottom: 2rem;
            }}

            h1 {{
                font-size: 1.75rem;
            }}

            .subtitle {{
                font-size: 0.95rem;
            }}

            .section-header {{
                font-size: 1.25rem;
            }}

            .card {{
                padding: 1rem;
            }}

            .card-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }}

            .card-title {{
                font-size: 1.1rem;
            }}

            .card-description {{
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Feynman Physics Visualizations</h1>
            <p class="subtitle">
                Interactive notebooks exploring physics concepts from the
                <a href="https://www.feynmanlectures.caltech.edu/" target="_blank">Feynman Lectures on Physics</a>
            </p>
        </header>

        <main class="notebooks">
            <h2 class="section-header">Feynman Lectures Series</h2>
{feynman_cards}
            <h2 class="section-header">Explorations</h2>
{exploration_cards}
        </main>

        <footer>
            <p>
                Built with <a href="https://marimo.io" target="_blank">marimo</a> &bull;
                <a href="{github_url}" target="_blank">View source on GitHub</a>
            </p>
        </footer>
    </div>
</body>
</html>'''

    output_path = output_dir / "index.html"
    output_path.write_text(html)
    return output_path


def _generate_card(nb: NotebookMetadata, show_badge: bool = False) -> str:
    """Generate HTML for a single notebook card."""
    tags_html = "\n                    ".join(
        f'<span class="tag">{tag}</span>' for tag in nb.tags
    )

    badge_html = '<span class="exploration-badge">Exploration</span>' if show_badge else ''

    return f'''            <a href="{nb.stem}.html" class="card">
                <div class="card-header">
                    <span class="card-number">{nb.number}</span>
                    <h2 class="card-title">{nb.title}{badge_html}</h2>
                </div>
                <p class="card-description">{nb.description}</p>
                <div class="card-tags">
                    {tags_html}
                </div>
            </a>'''


def export_all(output_dir: Path | None = None, include_code: bool = False) -> list[Path]:
    """Export all notebooks and generate index.html.

    Args:
        output_dir: Directory to write files (defaults to PROJECT_ROOT/docs)
        include_code: Whether to include source code in notebook exports

    Returns:
        List of all generated file paths
    """
    if output_dir is None:
        output_dir = DOCS_DIR

    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    # Get all notebooks and extract metadata
    notebooks = get_all_notebooks()
    metadata_list = [extract_metadata(nb) for nb in notebooks]

    # Export each notebook
    print("Exporting physics notebooks...")
    for meta in metadata_list:
        print(f"  {meta.number}. {meta.stem}...")
        output_path = export_notebook(meta.path, output_dir, include_code)
        generated_files.append(output_path)

    # Generate index.html
    print("Generating index.html...")
    index_path = generate_index_html(metadata_list, output_dir)
    generated_files.append(index_path)

    print(f"Done! Output in {output_dir}/")
    return generated_files


if __name__ == "__main__":
    export_all()
