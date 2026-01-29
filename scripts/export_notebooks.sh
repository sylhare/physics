#!/usr/bin/env bash
set -eo pipefail

# Export all notebooks to HTML for GitHub Pages
# GITHUB_REPOSITORY is set automatically in CI

mkdir -p docs

echo "Exporting notebooks to HTML..."

for notebook in notebooks/*.py; do
    name=$(basename "$notebook" .py)
    echo "  Exporting $name..."
    uv run marimo export html "$notebook" -o "docs/${name}.html"
done

echo "Generating index.html..."

# Generate styled index page
cat > docs/index.html << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feynman Physics Visualizations</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e4e4e7;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            color: #a1a1aa;
            margin-bottom: 3rem;
            font-size: 1.1rem;
        }
        .subtitle a {
            color: #60a5fa;
            text-decoration: none;
        }
        .subtitle a:hover {
            text-decoration: underline;
        }
        .notebooks {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .notebook {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
        }
        .notebook:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(96, 165, 250, 0.5);
            transform: translateY(-2px);
        }
        .notebook h2 {
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: #f4f4f5;
        }
        .notebook p {
            color: #a1a1aa;
            font-size: 0.95rem;
        }
        .footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #71717a;
            font-size: 0.875rem;
        }
        .footer a {
            color: #60a5fa;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Feynman Physics Visualizations</h1>
        <p class="subtitle">
            Interactive notebooks exploring physics concepts from the
            <a href="https://www.feynmanlectures.caltech.edu/" target="_blank">Feynman Lectures on Physics</a>
        </p>

        <div class="notebooks">
            <a href="gravitation.html" class="notebook">
                <h2>1. The Theory of Gravitation</h2>
                <p>Kepler's laws, Newton's universal gravitation, orbital mechanics, tidal effects, and Einstein's refinements.</p>
            </a>

            <a href="speed_of_light.html" class="notebook">
                <h2>2. The Speed of Light</h2>
                <p>Historical measurements from Rømer to Michelson, Maxwell's prediction, and electromagnetic wave visualization.</p>
            </a>

            <a href="spacetime.html" class="notebook">
                <h2>3. The Fabric of Spacetime</h2>
                <p>Special relativity: time dilation, length contraction, simultaneity, spacetime diagrams, and E=mc².</p>
            </a>

            <a href="wave_particle.html" class="notebook">
                <h2>4. The Wave-Particle Duality</h2>
                <p>Quantum mechanics: double-slit experiment, photoelectric effect, measurement problem, and Feynman path integrals.</p>
            </a>

            <a href="beyond_light.html" class="notebook">
                <h2>5. Beyond the Speed of Light</h2>
                <p>Spacetime geometry, the cosmic speed limit, tachyons, causality, and why FTL leads to imaginary time.</p>
            </a>

            <a href="exotic_matter.html" class="notebook">
                <h2>6. Exotic Matter</h2>
                <p>Negative energy density, Casimir effect, quantum inequalities, and the path to spacetime engineering.</p>
            </a>

            <a href="magnetism.html" class="notebook">
                <h2>7. Magnetism and Electric Motors</h2>
                <p>From Oersted's discovery to DC motors, AC induction motors, stepper motors, and generators.</p>
            </a>

            <a href="charged_motion.html" class="notebook">
                <h2>8. Motion of Charges in Fields</h2>
                <p>Cyclotrons, mass spectrometers, velocity selectors, magnetic bottles, Hall effect, and aurora.</p>
            </a>

            <a href="black_holes.html" class="notebook">
                <h2>9. Black Holes</h2>
                <p>Event horizons, light cones, time dilation, spacetime curvature, Hawking radiation, and the information paradox.</p>
            </a>
        </div>

        <div class="footer">
            <p>
                Built with <a href="https://marimo.io" target="_blank">marimo</a> •
                <a href="https://github.com/${GITHUB_REPOSITORY}" target="_blank">View source on GitHub</a>
            </p>
        </div>
    </div>
</body>
</html>
EOF

echo "Done! Output in docs/"
