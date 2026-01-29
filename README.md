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
uv run marimo run notebooks/gravitation.py   # View mode
uv run marimo edit notebooks/gravitation.py  # Edit mode
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
uv run marimo run notebooks/speed_of_light.py   # View mode
uv run marimo edit notebooks/speed_of_light.py  # Edit mode
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
uv run marimo run notebooks/spacetime.py   # View mode
uv run marimo edit notebooks/spacetime.py  # Edit mode
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

### 4. The Wave-Particle Duality

Based on [Feynman Lectures, Volume III, Chapter 1](https://www.feynmanlectures.caltech.edu/III_01.html) on Quantum Behavior

```bash
uv run marimo run notebooks/wave_particle.py   # View mode
uv run marimo edit notebooks/wave_particle.py  # Edit mode
```

**Contents:**
- Wave interference patterns (animated)
- Photoelectric effect with photon visualization (animated)
- Double-slit experiment with single particles (animated)
- The measurement problem - watching destroys interference
- de Broglie wavelength and matter waves (animated)
- Heisenberg's uncertainty principle
- Feynman's path integral visualization (animated)

### 5. Beyond the Speed of Light

A thought experiment exploring the structure of spacetime and the cosmic speed limit

```bash
uv run marimo run notebooks/beyond_light.py   # View mode
uv run marimo edit notebooks/beyond_light.py  # Edit mode
```

**Contents:**
- Spacetime velocity: everything moves at c through spacetime (animated)
- The energy barrier at light speed (animated)
- Tachyons and imaginary mass
- What if c were larger or smaller?
- Light cones and causality (animated)
- Why time becomes imaginary, not negative, above c
- Length contraction beyond c (animated)
- **Deep dive: The Newtonian universe** - what if c were 1000x larger? (animated)
- **Deep dive: The geometric barrier** - Minkowski hyperbolic geometry (animated)
- **Deep dive: Wormholes** - Einstein-Rosen bridges visualized (animated 3D)
- **Deep dive: Exotic matter** - negative energy and the Casimir effect
- **Deep dive: Causality paradoxes** - how FTL creates time machines (animated)
- Alcubierre warp drive visualization (animated)
- Why physicists believe FTL is impossible

### 6. Exotic Matter: The Key to Spacetime Engineering

A researcher's guide to negative energy density and its possibilities

```bash
uv run marimo run notebooks/exotic_matter.py   # View mode
uv run marimo edit notebooks/exotic_matter.py  # Edit mode
```

**Contents:**
- Historical timeline from Einstein-Rosen (1935) to quantum inequalities (1996)
- Energy conditions (WEC, NEC, SEC, DEC) with detailed explanations of the mathematics
- **The Casimir effect** - real negative energy, math derivation, experimental verification (animated)
- **Quantum inequalities** - Ford-Roman constraints, the "borrow and repay" principle (animated)
- **Squeezed vacuum states** - engineering negative energy in quantum optics (animated)
- Research directions: scaling Casimir, topological effects, quantum gravity loopholes
- The 40 orders of magnitude gap between what we have and what we need
- **Experimental validation** - precision Casimir, analog gravity systems (animated)
- Research roadmap: phases from foundations to spacetime engineering
- **Making the mathematics work** - 5 theoretical approaches:
  - Exploiting quantum inequality loopholes in curved spacetime
  - Interacting field enhancement (nonlinear QED)
  - Topological negative energy (kink solutions)
  - Extra dimensions from string theory
  - Modified gravity (f(R) theories)
- Self-consistency challenge visualization (animated)
- Mathematical deep dives: deriving quantum inequalities, Casimir calculation

### 7. Magnetism and Electric Motors

Based on [Feynman Lectures, Volume II](https://www.feynmanlectures.caltech.edu/II_toc.html) on Electromagnetism

```bash
uv run marimo run notebooks/magnetism.py   # View mode
uv run marimo edit notebooks/magnetism.py  # Edit mode
```

**Contents:**
- Oersted's 1820 discovery - electricity creates magnetism
- Magnetic field around a wire (animated 3D)
- Solenoids and electromagnets (animated)
- Force on current-carrying wires - the motor principle (animated)
- Electromagnetic induction - Faraday's law (animated)
- DC motor with commutator (animated)
- AC induction motor - Tesla's invention (animated)
- Stepper motor - discrete positioning (animated)
- AC generator - motors in reverse (animated)

### 8. Motion of Charges in Fields

Based on [Feynman Lectures, Volume II, Chapter 29](https://www.feynmanlectures.caltech.edu/II_29.html)

```bash
uv run marimo run notebooks/charged_motion.py   # View mode
uv run marimo edit notebooks/charged_motion.py  # Edit mode
```

**Contents:**
- Motion in uniform electric field - CRT displays (animated)
- Circular motion in magnetic field - cyclotron radius (animated)
- Mass spectrometer - separating isotopes (animated)
- The cyclotron particle accelerator (animated)
- Velocity selector - crossed E and B fields (animated)
- Magnetic bottles and plasma confinement (animated)
- The Hall effect - measuring fields with voltage (animated)
- Aurora borealis - Earth's magnetic bottle (animated)

### 9. Black Holes

Based on [Feynman Lectures, Volume II, Chapter 42: Curved Space](https://www.feynmanlectures.caltech.edu/II_42.html) and general relativity

```bash
uv run marimo run notebooks/black_holes.py   # View mode
uv run marimo edit notebooks/black_holes.py  # Edit mode
```

**Contents:**
- Schwarzschild radius and gravitational collapse (animated)
- Light cones near black holes - causality visualized (animated)
- Gravitational time dilation - clocks near the horizon (animated)
- Gravitational redshift - light losing energy (animated)
- Spacetime curvature - Flamm's paraboloid embedding (3D)
- Inside the black hole - Kruskal diagram (animated)
- Kerr rotating black holes with ergosphere (3D)
- Hawking radiation and black hole evaporation (animated)
- The information paradox

## Features

All notebooks include:
- Animated Plotly visualizations with Play/Pause controls
- Interactive sliders and controls
- Expandable mathematical derivations
- LaTeX-rendered equations
- Feynman-style explanations with historical context

## Development

Install with dev dependencies:

```bash
uv sync --extra dev
```

Run tests:

```bash
uv run pytest tests/ -v
```

## Export to HTML

Generate static HTML versions locally:

```bash
uv run python -m physics_explorations.export
```

Preview locally:

```bash
cd docs && python -m http.server 8000
# Open http://localhost:8000
```

## Project Structure

```
physics/
├── notebooks/           # Marimo notebook files
├── src/
│   └── physics_explorations/
│       ├── export.py           # Export and index generation
│       └── visualization/      # Shared styles and animation helpers
├── tests/
│   └── e2e/                    # End-to-end notebook tests
└── docs/                       # Generated HTML (by CI)
```

## GitHub Pages

The notebooks are automatically deployed to GitHub Pages on every push to `main`.

To enable for your fork:
1. Go to **Settings** > **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push to `main` to trigger deployment
