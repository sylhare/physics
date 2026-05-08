"""Visualization utilities for physics notebooks."""

from physics_explorations.visualization.animations import (
    create_animation_figure,
    create_play_pause_buttons,
    create_slider_steps,
)
from physics_explorations.visualization.styles import (
    ANIMATION_SETTINGS,
    COLORS,
    DARK_THEME,
    SCENE_3D,
    SLIDER_STYLE,
    apply_dark_theme,
    get_color_palette,
    get_physics_palette,
    get_plotly_config,
    get_trace_style,
)

__all__ = [
    "ANIMATION_SETTINGS",
    "COLORS",
    "DARK_THEME",
    "SCENE_3D",
    "SLIDER_STYLE",
    "apply_dark_theme",
    "create_animation_figure",
    "create_play_pause_buttons",
    "create_slider_steps",
    "get_color_palette",
    "get_physics_palette",
    "get_plotly_config",
    "get_trace_style",
]
