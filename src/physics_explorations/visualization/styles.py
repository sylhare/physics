"""Consistent dark theme styling for physics visualizations."""

from typing import Any

import plotly.graph_objects as go
import plotly.io as pio

# Dark theme color palette - physics-specific
COLORS = {
    # Base colors
    "background": "#0a0a1a",
    "paper": "#16213e",
    "text": "#eaeaea",
    "text_secondary": "#a0a0a0",
    "grid": "#2d3a4f",
    # Primary palette
    "primary": "#00d4ff",  # Cyan - main elements
    "secondary": "#ff6b6b",  # Coral - secondary/contrast
    "tertiary": "#4ecdc4",  # Teal - tertiary elements
    "quaternary": "#ffe66d",  # Yellow - highlights
    # Physics-specific colors
    "spacetime": "#a78bfa",  # Purple - spacetime/relativity
    "quantum": "#60a5fa",  # Blue - quantum mechanics
    "gravity": "#f97316",  # Orange - gravity/mass
    "electric": "#facc15",  # Yellow - electric fields
    "magnetic": "#22d3ee",  # Cyan - magnetic fields
    "photon": "#fbbf24",  # Gold - light/photons
    "particle": "#f472b6",  # Pink - particles
    "wave": "#34d399",  # Green - waves
    # Accent colors
    "accent1": "#95e1d3",  # Mint
    "accent2": "#f38181",  # Salmon
    "accent3": "#aa96da",  # Lavender
    "accent4": "#fcbad3",  # Pink
}

# Plotly layout template
DARK_THEME: dict[str, Any] = {
    "paper_bgcolor": COLORS["paper"],
    "plot_bgcolor": COLORS["background"],
    "autosize": True,
    "margin": {"l": 50, "r": 30, "t": 80, "b": 50, "pad": 4},
    "font": {
        "family": "Inter, system-ui, -apple-system, sans-serif",
        "size": 13,
        "color": COLORS["text"],
    },
    "title": {
        "font": {
            "size": 18,
            "color": COLORS["text"],
        },
        "x": 0.5,
        "xanchor": "center",
        "pad": {"t": 10},
    },
    "xaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 1,
        "tickfont": {"color": COLORS["text_secondary"], "size": 11},
        "title_font": {"color": COLORS["text"], "size": 13},
        "showgrid": True,
        "automargin": True,
    },
    "yaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 1,
        "tickfont": {"color": COLORS["text_secondary"], "size": 11},
        "title_font": {"color": COLORS["text"], "size": 13},
        "showgrid": True,
        "automargin": True,
    },
    "legend": {
        "bgcolor": "rgba(22, 33, 62, 0.7)",
        "bordercolor": COLORS["grid"],
        "borderwidth": 1,
        "font": {"color": COLORS["text"], "size": 11},
        "orientation": "h",
        "yanchor": "bottom",
        "y": -0.2,
        "xanchor": "center",
        "x": 0.5,
    },
    "hoverlabel": {
        "bgcolor": COLORS["paper"],
        "bordercolor": COLORS["primary"],
        "font": {"color": COLORS["text"], "family": "Inter, sans-serif"},
    },
    "hovermode": "closest",
}

# 3D Scene settings
SCENE_3D: dict[str, Any] = {
    "xaxis": {
        "gridcolor": COLORS["grid"],
        "zerolinecolor": COLORS["text_secondary"],
        "showbackground": True,
        "backgroundcolor": COLORS["background"],
    },
    "yaxis": {
        "gridcolor": COLORS["grid"],
        "zerolinecolor": COLORS["text_secondary"],
        "showbackground": True,
        "backgroundcolor": COLORS["background"],
    },
    "zaxis": {
        "gridcolor": COLORS["grid"],
        "zerolinecolor": COLORS["text_secondary"],
        "showbackground": True,
        "backgroundcolor": COLORS["background"],
    },
    "camera": {"eye": {"x": 1.5, "y": 1.5, "z": 1.5}},
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


def get_plotly_config() -> dict[str, Any]:
    """Get the recommended Plotly configuration for responsiveness and clean UI."""
    return {
        "responsive": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "select2d",
            "lasso2d",
            "autoScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
        ],
        "displayModeBar": "hover",
        "scrollZoom": False,
    }


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
        "translucent_area": {
            "fillcolor": "rgba(96, 165, 250, 0.2)",  # Transparent blue
            "line": {"width": 0},
        },
        "translucent_field": {
            "line": {"color": "rgba(34, 211, 238, 0.3)", "width": 1},
            "mode": "lines",
        },
    }
    return styles.get(trace_type, styles["primary"])


# Set the default template
pio.templates["physics_dark"] = go.layout.Template(layout=DARK_THEME)
pio.templates.default = "physics_dark"
