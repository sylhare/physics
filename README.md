# Feynman Physics Visualizations

Interactive marimo notebooks exploring physics concepts based on the [Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/).

## Setup

```bash
uv sync
```

## Notebooks

### 1. The Theory of Gravitation

Based on [Feynman Lectures, Chapter 7](https://www.feynmanlectures.caltech.edu/I_07.html)

```bash
uv run marimo run notebooks/feynman_gravitation.py   # View mode
uv run marimo edit notebooks/feynman_gravitation.py  # Edit mode
```

**Contents:**
- Kepler's Three Laws with animated visualizations
- Newton's Law of Universal Gravitation
- Newton's Cannon thought experiment (animated)
- Interactive eccentricity explorer
- Tidal effects with rotating Earth animation
- Einstein's General Relativity refinements

### 2. The Speed of Light

Based on Feynman Lectures discussions of light and electromagnetism

```bash
uv run marimo run notebooks/feynman_speed_of_light.py   # View mode
uv run marimo edit notebooks/feynman_speed_of_light.py  # Edit mode
```

**Contents:**
- Rømer's measurement using Jupiter's moons (animated)
- Fizeau's rotating wheel experiment (animated)
- Foucault's rotating mirror method
- Maxwell's theoretical prediction (c from ε₀ and μ₀)
- Electromagnetic wave visualization (3D animated)
- Michelson's precision measurements
- Historical progression of measurements

### 3. The Fabric of Spacetime

Based on [Feynman Lectures, Chapters 15-17](https://www.feynmanlectures.caltech.edu/I_15.html) on Special Relativity

```bash
uv run marimo run notebooks/feynman_spacetime.py   # View mode
uv run marimo edit notebooks/feynman_spacetime.py  # Edit mode
```

**Contents:**
- Einstein's two postulates
- Time dilation with light clock animation
- Interactive gamma factor explorer
- Length contraction visualization (animated)
- Relativity of simultaneity - Einstein's train (animated)
- Spacetime diagrams and light cones
- The invariant spacetime interval
- E = mc² and mass-energy equivalence

## Features

All notebooks include:
- Animated Plotly visualizations with Play/Pause controls
- Interactive sliders and controls
- Expandable mathematical derivations
- LaTeX-rendered equations
- Feynman-style explanations with historical context

## Export to HTML

Generate static HTML versions locally:

```bash
./scripts/export_notebooks.sh
```

Preview locally:

```bash
cd docs && python -m http.server 8000
# Open http://localhost:8000
```

## GitHub Pages

The notebooks are automatically deployed to GitHub Pages on every push to `main`.

To enable for your fork:
1. Go to **Settings** > **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push to `main` to trigger deployment
