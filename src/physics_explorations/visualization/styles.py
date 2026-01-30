"""Consistent dark theme styling for physics visualizations."""

from typing import Any

# Dark theme color palette - physics-specific
COLORS = {
    # Base colors
    "background": "#0a0a1a",
    "paper": "#16213e",
    "text": "#eaeaea",
    "text_secondary": "#a0a0a0",
    "grid": "#2d3a4f",
    # Primary palette
    "primary": "#00d4ff",       # Cyan - main elements
    "secondary": "#ff6b6b",     # Coral - secondary/contrast
    "tertiary": "#4ecdc4",      # Teal - tertiary elements
    "quaternary": "#ffe66d",    # Yellow - highlights
    # Physics-specific colors
    "spacetime": "#a78bfa",     # Purple - spacetime/relativity
    "quantum": "#60a5fa",       # Blue - quantum mechanics
    "gravity": "#f97316",       # Orange - gravity/mass
    "electric": "#facc15",      # Yellow - electric fields
    "magnetic": "#22d3ee",      # Cyan - magnetic fields
    "photon": "#fbbf24",        # Gold - light/photons
    "particle": "#f472b6",      # Pink - particles
    "wave": "#34d399",          # Green - waves
    # Accent colors
    "accent1": "#95e1d3",       # Mint
    "accent2": "#f38181",       # Salmon
    "accent3": "#aa96da",       # Lavender
    "accent4": "#fcbad3",       # Pink
}

# Plotly layout template
DARK_THEME: dict[str, Any] = {
    "paper_bgcolor": COLORS["paper"],
    "plot_bgcolor": COLORS["background"],
    "font": {
        "family": "JetBrains Mono, Fira Code, monospace",
        "size": 14,
        "color": COLORS["text"],
    },
    "title": {
        "font": {
            "size": 18,
            "color": COLORS["text"],
        },
        "x": 0.5,
        "xanchor": "center",
    },
    "xaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 2,
        "tickfont": {"color": COLORS["text_secondary"]},
        "titlefont": {"color": COLORS["text"]},
        "showgrid": True,
    },
    "yaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 2,
        "tickfont": {"color": COLORS["text_secondary"]},
        "titlefont": {"color": COLORS["text"]},
        "showgrid": True,
    },
    "legend": {
        "bgcolor": "rgba(22, 33, 62, 0.8)",
        "bordercolor": COLORS["grid"],
        "borderwidth": 1,
        "font": {"color": COLORS["text"]},
    },
    "hoverlabel": {
        "bgcolor": COLORS["paper"],
        "bordercolor": COLORS["primary"],
        "font": {"color": COLORS["text"], "family": "JetBrains Mono, monospace"},
    },
}

# Animation settings
ANIMATION_SETTINGS: dict[str, Any] = {
    "frame_duration": 50,
    "transition_duration": 0,
    "redraw": True,
    "mode": "immediate",
}

# Slider styling
SLIDER_STYLE: dict[str, Any] = {
    "bgcolor": COLORS["paper"],
    "bordercolor": COLORS["grid"],
    "borderwidth": 1,
    "tickcolor": COLORS["text_secondary"],
    "font": {"color": COLORS["text"]},
    "activebgcolor": COLORS["primary"],
}


def apply_dark_theme(fig: Any) -> Any:
    """Apply the dark theme to a Plotly figure.

    Args:
        fig: A Plotly figure object

    Returns:
        The figure with dark theme applied
    """
    fig.update_layout(**DARK_THEME)
    return fig


def get_color_palette() -> list[str]:
    """Return a list of colors for multi-series plots."""
    return [
        COLORS["primary"],
        COLORS["secondary"],
        COLORS["tertiary"],
        COLORS["quaternary"],
        COLORS["accent1"],
        COLORS["accent2"],
        COLORS["accent3"],
        COLORS["accent4"],
    ]


def get_physics_palette() -> dict[str, str]:
    """Return physics-specific color mappings."""
    return {
        "spacetime": COLORS["spacetime"],
        "quantum": COLORS["quantum"],
        "gravity": COLORS["gravity"],
        "electric": COLORS["electric"],
        "magnetic": COLORS["magnetic"],
        "photon": COLORS["photon"],
        "particle": COLORS["particle"],
        "wave": COLORS["wave"],
    }


def get_trace_style(trace_type: str = "primary") -> dict[str, Any]:
    """Get consistent trace styling based on type.

    Args:
        trace_type: One of 'primary', 'secondary', 'tertiary', 'dashed',
                   'dotted', 'point', 'area', or any physics color name

    Returns:
        Dictionary of trace styling options
    """
    styles = {
        "primary": {
            "line": {"color": COLORS["primary"], "width": 3},
            "mode": "lines",
        },
        "secondary": {
            "line": {"color": COLORS["secondary"], "width": 3},
            "mode": "lines",
        },
        "tertiary": {
            "line": {"color": COLORS["tertiary"], "width": 2},
            "mode": "lines",
        },
        "dashed": {
            "line": {"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
            "mode": "lines",
        },
        "dotted": {
            "line": {"color": COLORS["quaternary"], "width": 2, "dash": "dot"},
            "mode": "lines",
        },
        "point": {
            "marker": {"color": COLORS["quaternary"], "size": 12, "symbol": "circle"},
            "mode": "markers",
        },
        "area": {
            "fillcolor": "rgba(0, 212, 255, 0.3)",
            "line": {"color": COLORS["primary"], "width": 1},
        },
        # Physics-specific styles
        "photon": {
            "line": {"color": COLORS["photon"], "width": 2},
            "mode": "lines",
        },
        "particle": {
            "marker": {"color": COLORS["particle"], "size": 10},
            "mode": "markers",
        },
        "field": {
            "line": {"color": COLORS["electric"], "width": 1},
            "mode": "lines",
        },
    }
    return styles.get(trace_type, styles["primary"])
