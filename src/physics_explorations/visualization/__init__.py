"""Visualization utilities for physics notebooks."""

from physics_explorations.visualization.styles import (
    COLORS,
    DARK_THEME,
    ANIMATION_SETTINGS,
    SLIDER_STYLE,
    apply_dark_theme,
    get_color_palette,
    get_trace_style,
)
from physics_explorations.visualization.animations import (
    create_animation_figure,
    create_play_pause_buttons,
    create_slider_steps,
)

__all__ = [
    # Styles
    "COLORS",
    "DARK_THEME",
    "ANIMATION_SETTINGS",
    "SLIDER_STYLE",
    "apply_dark_theme",
    "get_color_palette",
    "get_trace_style",
    # Animations
    "create_animation_figure",
    "create_play_pause_buttons",
    "create_slider_steps",
]
