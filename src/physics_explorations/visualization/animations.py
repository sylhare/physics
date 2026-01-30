"""Animation utilities for physics visualizations."""

from typing import Any, Callable
import plotly.graph_objects as go

from physics_explorations.visualization.styles import (
    COLORS,
    DARK_THEME,
    ANIMATION_SETTINGS,
    SLIDER_STYLE,
)


def create_play_pause_buttons(
    play_label: str = "Play",
    pause_label: str = "Pause",
) -> list[dict[str, Any]]:
    """Create standard Play/Pause animation buttons.

    Args:
        play_label: Label for play button (default: "Play")
        pause_label: Label for pause button (default: "Pause")

    Returns:
        List of button definitions for updatemenus
    """
    return [
        {
            "label": f"▶ {play_label}",
            "method": "animate",
            "args": [
                None,
                {
                    "frame": {"duration": ANIMATION_SETTINGS["frame_duration"], "redraw": True},
                    "fromcurrent": True,
                    "transition": {"duration": ANIMATION_SETTINGS["transition_duration"]},
                    "mode": "immediate",
                },
            ],
        },
        {
            "label": f"⏸ {pause_label}",
            "method": "animate",
            "args": [
                [None],
                {
                    "frame": {"duration": 0, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 0},
                },
            ],
        },
    ]


def create_slider_steps(
    n_frames: int,
    labels: list[str] | None = None,
    prefix: str = "",
    suffix: str = "",
) -> list[dict[str, Any]]:
    """Create slider steps for animation control.

    Args:
        n_frames: Number of animation frames
        labels: Optional list of labels for each step
        prefix: Prefix for auto-generated labels
        suffix: Suffix for auto-generated labels

    Returns:
        List of slider step definitions
    """
    steps = []
    for i in range(n_frames):
        if labels and i < len(labels):
            label = labels[i]
        else:
            label = f"{prefix}{i}{suffix}"

        steps.append({
            "args": [
                [str(i)],
                {
                    "frame": {"duration": ANIMATION_SETTINGS["frame_duration"], "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": ANIMATION_SETTINGS["transition_duration"]},
                },
            ],
            "label": label,
            "method": "animate",
        })

    return steps


def create_animation_figure(
    initial_data: list,
    frames: list[go.Frame],
    title: str = "",
    xaxis_title: str = "",
    yaxis_title: str = "",
    xaxis_range: list | None = None,
    yaxis_range: list | None = None,
    show_slider: bool = True,
    slider_prefix: str = "",
    height: int = 600,
    showlegend: bool = True,
    aspect_equal: bool = False,
) -> go.Figure:
    """Create a complete animated Plotly figure with standard controls.

    Args:
        initial_data: List of traces for the initial frame
        frames: List of go.Frame objects for animation
        title: Figure title
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        xaxis_range: Optional [min, max] for x-axis
        yaxis_range: Optional [min, max] for y-axis
        show_slider: Whether to show the animation slider
        slider_prefix: Prefix for slider labels
        height: Figure height in pixels
        showlegend: Whether to show the legend
        aspect_equal: Whether to use equal aspect ratio

    Returns:
        Configured go.Figure with animation controls
    """
    # Build layout
    layout = go.Layout(
        title=dict(text=title, font=dict(size=18, color=COLORS["text"])),
        xaxis=dict(
            title=xaxis_title,
            range=xaxis_range,
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["text_secondary"],
            tickfont=dict(color=COLORS["text_secondary"]),
        ),
        yaxis=dict(
            title=yaxis_title,
            range=yaxis_range,
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["text_secondary"],
            tickfont=dict(color=COLORS["text_secondary"]),
        ),
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["paper"],
        font=dict(color=COLORS["text"]),
        showlegend=showlegend,
        legend=dict(
            bgcolor="rgba(22, 33, 62, 0.8)",
            bordercolor=COLORS["grid"],
        ),
        height=height,
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=1.15,
                x=0.5,
                xanchor="center",
                buttons=create_play_pause_buttons(),
                font=dict(color=COLORS["text"]),
                bgcolor=COLORS["paper"],
                bordercolor=COLORS["grid"],
            )
        ],
    )

    # Add slider if requested
    if show_slider and frames:
        layout["sliders"] = [
            dict(
                active=0,
                yanchor="top",
                xanchor="left",
                currentvalue=dict(
                    prefix=slider_prefix,
                    visible=True,
                    xanchor="center",
                    font=dict(color=COLORS["text"]),
                ),
                transition=dict(duration=ANIMATION_SETTINGS["transition_duration"]),
                pad=dict(b=10, t=50),
                len=0.9,
                x=0.05,
                y=0,
                steps=create_slider_steps(len(frames)),
                bgcolor=COLORS["paper"],
                bordercolor=COLORS["grid"],
                tickcolor=COLORS["text_secondary"],
                font=dict(color=COLORS["text_secondary"]),
            )
        ]

    # Handle equal aspect ratio
    if aspect_equal:
        layout["yaxis"]["scaleanchor"] = "x"
        layout["yaxis"]["scaleratio"] = 1

    # Create figure
    fig = go.Figure(data=initial_data, layout=layout, frames=frames)

    return fig


def build_frames(
    n_frames: int,
    frame_builder: Callable[[int], list],
) -> list[go.Frame]:
    """Build animation frames using a builder function.

    Args:
        n_frames: Number of frames to generate
        frame_builder: Function that takes frame index and returns list of traces

    Returns:
        List of go.Frame objects
    """
    frames = []
    for i in range(n_frames):
        frame_data = frame_builder(i)
        frames.append(go.Frame(data=frame_data, name=str(i)))
    return frames
