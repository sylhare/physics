import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from physics_explorations.visualization import (
        COLORS,
        create_play_pause_buttons,
    )

    return COLORS, create_play_pause_buttons, go, make_subplots, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # The Geometry of Spacetime: Dimensions of Space and Time

        *An exploration of what it means to have different numbers of spatial and temporal dimensions*

        ---

        ## Why 3+1 Dimensions?

        We live in a universe with **three spatial dimensions** (length, width, height) and
        **one temporal dimension** (time). Physicists write this as "3+1 dimensions" or sometimes
        "3+1D spacetime."

        But why these numbers? What would the universe look like with different combinations?
        And why does time behave so differently from space?

        $$\text{Our universe: } (x, y, z, t) \rightarrow \text{3 space + 1 time}$$

        This notebook explores these deep questions:

        - **What makes time different from space?** (The arrow of time)
        - **What would 1+1 dimensions look like?** (Flatland meets physics)
        - **What about 2+2 dimensions?** (Two time dimensions!)
        - **Could we move "sideways" in time?**
        - **Does the speed of light depend on dimensionality?**
        - **What happens at quantum scales?**

        > *"Time is nature's way of keeping everything from happening at once."*
        > — John Wheeler
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Fundamental Asymmetry: Space vs Time

        In our everyday experience, space and time seem utterly different:

        | Property | Space | Time |
        |----------|-------|------|
        | Dimensions | 3 | 1 |
        | Movement | Any direction | Forward only |
        | Reversal | Easy (turn around) | Impossible? |
        | Perception | All at once | Sequential |

        **But special relativity reveals a deep connection:**

        The spacetime interval between two events is:

        $$s^2 = c^2 \Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$$

        Notice the **minus signs** in front of the spatial terms! This is the signature of
        spacetime: $(+, -, -, -)$ or equivalently $(-, +, +, +)$.

        **The minus sign is everything.** It's what makes time different from space.
        If time had the same sign as space, you could rotate freely between them—
        turning around in time like you turn around in space.

        **Why can't we go backward in time?**

        It's not just the equations—it's thermodynamics. The **Second Law** says entropy
        always increases. This creates the "arrow of time" we experience. But is this
        fundamental, or emergent?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 1+1 Dimensions: A Line Through Time

        Let's start with the simplest spacetime: **one spatial dimension + one time dimension**.

        Imagine beings that can only move along a single line—call them "Linelanders."
        They can go forward or backward along their line, but that's it.

        **Their spacetime diagram:**

        - Horizontal axis: their single spatial dimension $x$
        - Vertical axis: time $t$
        - Their worldline traces their history

        **Key insight:** Even though they can move backward in *space* (reverse direction
        on the line), they still move forward in *time*. The "forward" motion in time
        is built into the structure of spacetime itself.

        $$ds^2 = c^2 dt^2 - dx^2 \quad \text{(1+1D spacetime)}$$

        *The animation below shows a Linelander's journey through spacetime.*
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_1d_spacetime_animation():
        """Animate motion in 1+1 dimensional spacetime."""
        n_frames = 100

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 10  # Time from 0 to 10

            # Particle oscillates in x while always moving forward in t
            x_particle = 2 * np.sin(t * 0.8)

            # Worldline history
            t_history = np.linspace(0, t, max(2, i + 1))
            x_history = 2 * np.sin(t_history * 0.8)

            # Light cones from origin
            t_cone = np.linspace(0, 10, 50)
            x_cone_right = t_cone  # c = 1 units
            x_cone_left = -t_cone

            # Future light cone from current position
            t_future = np.linspace(t, 10, 30)
            x_future_right = x_particle + (t_future - t)
            x_future_left = x_particle - (t_future - t)

            frame_data = [
                # Light cone from origin
                go.Scatter(
                    x=x_cone_right, y=t_cone,
                    mode="lines",
                    line=dict(color=COLORS["photon"], width=1, dash="dash"),
                    name="Light cone",
                    showlegend=(i == 0),
                ),
                go.Scatter(
                    x=x_cone_left, y=t_cone,
                    mode="lines",
                    line=dict(color=COLORS["photon"], width=1, dash="dash"),
                    showlegend=False,
                ),
                # Future light cone from particle
                go.Scatter(
                    x=x_future_right, y=t_future,
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=1, dash="dot"),
                    name="Future light cone",
                    showlegend=(i == 0),
                ),
                go.Scatter(
                    x=x_future_left, y=t_future,
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=1, dash="dot"),
                    showlegend=False,
                ),
                # Worldline
                go.Scatter(
                    x=x_history, y=t_history,
                    mode="lines",
                    line=dict(color=COLORS["primary"], width=3),
                    name="Worldline",
                    showlegend=(i == 0),
                ),
                # Current position
                go.Scatter(
                    x=[x_particle], y=[t],
                    mode="markers",
                    marker=dict(size=15, color=COLORS["secondary"]),
                    name="Linelander",
                    showlegend=(i == 0),
                ),
                # Time arrow
                go.Scatter(
                    x=[-4.5, -4.5], y=[0, 9],
                    mode="lines+text",
                    line=dict(color=COLORS["text"], width=2),
                    text=["", "TIME →"],
                    textposition="top center",
                    textfont=dict(color=COLORS["text"], size=12),
                    showlegend=False,
                ),
                # Annotation
                go.Scatter(
                    x=[x_particle + 0.3], y=[t + 0.5],
                    mode="text",
                    text=[f"t = {t:.1f}"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>1+1 Spacetime:</b> A Linelander's Journey<br><sub>Can move left/right in space, but always forward in time</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(
                    title="Space (x)",
                    range=[-5, 5],
                    gridcolor=COLORS["grid"],
                    zerolinecolor=COLORS["text_secondary"],
                ),
                yaxis=dict(
                    title="Time (t)",
                    range=[-0.5, 11],
                    gridcolor=COLORS["grid"],
                    zerolinecolor=COLORS["text_secondary"],
                ),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    bgcolor="rgba(22, 33, 62, 0.8)",
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    spacetime_1d_fig = create_1d_spacetime_animation()
    spacetime_1d_fig
    return (create_1d_spacetime_animation, spacetime_1d_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## What If Time Were 2-Dimensional?

        This is where things get strange. What would it mean to have **two time dimensions**?

        In 2+1 spacetime (2 space, 1 time), the interval is:
        $$ds^2 = c^2 dt^2 - dx^2 - dy^2$$

        But in 1+2 spacetime (1 space, **2 time**), it would be:
        $$ds^2 = c^2 dt_1^2 + c^2 dt_2^2 - dx^2$$

        **Wait—two time coordinates?** What does that even mean?

        **Imagine having two independent "clocks":**
        - $t_1$ ticks forward at one rate
        - $t_2$ ticks forward at another rate
        - Your "time position" is $(t_1, t_2)$—a point on a **time plane**!

        **"Moving sideways in time"** would mean:
        - Keeping $t_1$ constant while $t_2$ changes
        - Or moving diagonally through the time plane

        **The problem:** With 2D time, causality becomes extremely complicated.
        Multiple "futures" could exist simultaneously, and the arrow of time
        would point in a 2D direction, not a single line.

        *The visualization below explores what 2D time might look like.*
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_2d_time_animation():
        """Visualize 1 space + 2 time dimensions."""
        n_frames = 80

        frames = []
        for i in range(n_frames):
            progress = i / n_frames

            # In 2D time, we can move in a circle through the time plane
            t1 = 3 + 2 * np.cos(progress * 2 * np.pi)
            t2 = 3 + 2 * np.sin(progress * 2 * np.pi)

            # Spatial position oscillates
            x = 2 * np.sin(progress * 4 * np.pi)

            # History in the time plane
            angles = np.linspace(0, progress * 2 * np.pi, max(2, int(i * 2)))
            t1_history = 3 + 2 * np.cos(angles)
            t2_history = 3 + 2 * np.sin(angles)

            # Time plane grid
            t_grid = np.linspace(0, 6, 7)

            frame_data = [
                # Time plane grid (horizontal lines)
                *[go.Scatter(
                    x=[0, 6], y=[t, t],
                    mode="lines",
                    line=dict(color=COLORS["grid"], width=1),
                    showlegend=False,
                ) for t in t_grid],
                # Time plane grid (vertical lines)
                *[go.Scatter(
                    x=[t, t], y=[0, 6],
                    mode="lines",
                    line=dict(color=COLORS["grid"], width=1),
                    showlegend=False,
                ) for t in t_grid],
                # Path through time plane
                go.Scatter(
                    x=t1_history, y=t2_history,
                    mode="lines",
                    line=dict(color=COLORS["spacetime"], width=3),
                    name="Path through 2D time",
                    showlegend=(i == 0),
                ),
                # Current position
                go.Scatter(
                    x=[t1], y=[t2],
                    mode="markers+text",
                    marker=dict(size=15, color=COLORS["secondary"]),
                    text=[f"x={x:.1f}"],
                    textposition="top right",
                    textfont=dict(color=COLORS["text"]),
                    name="Observer",
                    showlegend=(i == 0),
                ),
                # Arrow showing "forward" in 2D time
                go.Scatter(
                    x=[t1, t1 + 0.3 * np.cos(progress * 2 * np.pi + np.pi/2)],
                    y=[t2, t2 + 0.3 * np.sin(progress * 2 * np.pi + np.pi/2)],
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=3),
                    name="Time direction",
                    showlegend=(i == 0),
                ),
                # Origin marker
                go.Scatter(
                    x=[3], y=[3],
                    mode="markers",
                    marker=dict(size=8, color=COLORS["text_secondary"], symbol="x"),
                    name="Origin",
                    showlegend=(i == 0),
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>2D Time:</b> Moving Through a Time Plane<br><sub>The observer traces a circle in the (t₁, t₂) plane</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(
                    title="Time dimension t₁",
                    range=[-0.5, 6.5],
                    gridcolor=COLORS["grid"],
                    scaleanchor="y",
                ),
                yaxis=dict(
                    title="Time dimension t₂",
                    range=[-0.5, 6.5],
                    gridcolor=COLORS["grid"],
                ),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(bgcolor="rgba(22, 33, 62, 0.8)"),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    time_2d_fig = create_2d_time_animation()
    time_2d_fig
    return (create_2d_time_animation, time_2d_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Problem with 2D Time: Closed Timelike Curves

        With two time dimensions, you could potentially **return to your starting point
        in time** by going "around" in the time plane—just like walking in a circle
        brings you back to your starting point in space.

        This creates **closed timelike curves (CTCs)**—paths through spacetime that loop
        back to their own past. CTCs lead to:

        - **Grandfather paradoxes**: Could you prevent your own existence?
        - **Causal loops**: Events that cause themselves
        - **Violation of free will**: Your future already constrains your past

        Most physicists believe 2D time is forbidden precisely because it makes
        causality incoherent. The universe seems to "choose" 1D time to preserve
        cause and effect.

        > *"The distinction between past, present and future is only a stubbornly
        > persistent illusion."* — Einstein

        But even Einstein's illusion had a direction!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Exotic Matter and Dimensional Engineering

        Could we ever *create* paths through extra dimensions or manipulate the
        structure of time? This is where **exotic matter** enters the picture.

        **Exotic matter** has negative energy density—it gravitationally *repels*
        instead of attracts. In general relativity, exotic matter can:

        - **Hold wormholes open**: Connecting distant points in space (or time!)
        - **Enable the Alcubierre warp drive**: Contracting space ahead, expanding behind
        - **Potentially stabilize CTCs**: Making closed timelike curves traversable

        **The connection to dimensions:**

        In higher-dimensional theories (string theory, M-theory), our 3+1D spacetime
        is embedded in a larger space with 10 or 11 dimensions. Exotic matter might:

        1. **Allow access to extra dimensions** by warping the "brane" we live on
        2. **Create shortcuts** through higher-dimensional space
        3. **Modify the effective dimensionality** locally

        **The Casimir effect** proves exotic matter exists—vacuum fluctuations between
        conducting plates create regions of negative energy density. But the amounts
        are tiny: $\sim 1$ J/m³ at 100 nm separation.

        For spacetime engineering, we'd need $\sim 10^{27}$ J/m³—a gap of **27 orders
        of magnitude**. Whether this can ever be bridged remains one of physics'
        greatest open questions.

        $$\rho_{\text{Casimir}} \approx -\frac{\pi^2 \hbar c}{720 a^4}$$

        *See the [Exotic Matter notebook](exotic_matter.html) for a deep dive into
        negative energy and quantum inequalities.*

        *The visualizations below show spacetime in different dimensions, wormholes,
        and how exotic matter behaves.*
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_spacetime_dimensions_animation():
        """Show 2D, 3D, and 4D spacetime representations."""
        n_frames = 80

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 2 * np.pi

            # === 1+1D (2D spacetime): x and t ===
            # A worldline in 1+1D
            t_vals = np.linspace(0, 4, 50)
            x_1d = np.sin(t_vals * 2) * 0.5
            # Light cone
            lc_t = np.linspace(0, 4, 20)

            # === 2+1D (3D spacetime): x, y, and t ===
            # Show as 3D with time as vertical axis
            theta_2d = np.linspace(0, 2 * np.pi, 30)
            # Particle spiraling upward in time
            spiral_t = np.linspace(0, 3, 50)
            spiral_x = 0.4 * np.cos(spiral_t * 3 + t)
            spiral_y = 0.4 * np.sin(spiral_t * 3 + t)

            # === 3+1D (4D spacetime): projected ===
            # Show a tesseract-like projection (hypercube)
            # Outer cube
            cube_scale = 0.6
            inner_scale = 0.3

            # Current position marker
            marker_x = 0.3 * np.cos(t)
            marker_y = 0.3 * np.sin(t)

            frame_data = [
                # ========== 1+1D SPACETIME (left) ==========
                # Label
                go.Scatter(
                    x=[-3.5], y=[4.5],
                    mode="text",
                    text=["<b>1+1D Spacetime</b><br>(1 space + 1 time)"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
                # Axes
                go.Scatter(
                    x=[-5, -2], y=[0, 0],
                    mode="lines+text",
                    line=dict(color=COLORS["text_secondary"], width=2),
                    text=["", "x"],
                    textposition="middle right",
                    textfont=dict(color=COLORS["text"]),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[-5, -5], y=[0, 4],
                    mode="lines+text",
                    line=dict(color=COLORS["text_secondary"], width=2),
                    text=["", "t"],
                    textposition="top center",
                    textfont=dict(color=COLORS["text"]),
                    showlegend=False,
                ),
                # Light cone
                go.Scatter(
                    x=[-5 + lc_t * 0.5, -5 - lc_t * 0.5 + 3][::-1],
                    y=[lc_t.tolist() + lc_t.tolist()[::-1]][0][:len(lc_t)],
                    mode="lines",
                    line=dict(color=COLORS["photon"], width=1, dash="dash"),
                    name="Light cone" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                go.Scatter(
                    x=-5 - lc_t * 0.5 + 3, y=lc_t,
                    mode="lines",
                    line=dict(color=COLORS["photon"], width=1, dash="dash"),
                    showlegend=False,
                ),
                # Worldline
                go.Scatter(
                    x=x_1d - 3.5, y=t_vals,
                    mode="lines",
                    line=dict(color=COLORS["primary"], width=3),
                    name="Worldline" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                # Moving point
                go.Scatter(
                    x=[np.sin(t * 2) * 0.5 - 3.5],
                    y=[t / (2 * np.pi) * 4],
                    mode="markers",
                    marker=dict(size=10, color=COLORS["secondary"]),
                    showlegend=False,
                ),

                # ========== 2+1D SPACETIME (center) ==========
                # Label
                go.Scatter(
                    x=[0], y=[4.5],
                    mode="text",
                    text=["<b>2+1D Spacetime</b><br>(2 space + 1 time)"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
                # Spatial plane at t=0
                go.Scatter(
                    x=[-1, 1, 1, -1, -1], y=[-0.5, -0.5, 0.5, 0.5, -0.5],
                    mode="lines",
                    line=dict(color=COLORS["grid"], width=1),
                    fill="toself",
                    fillcolor="rgba(45, 58, 79, 0.3)",
                    name="Space (t=0)" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                # Time axis (vertical)
                go.Scatter(
                    x=[0, 0], y=[0, 4],
                    mode="lines+text",
                    line=dict(color=COLORS["quaternary"], width=2),
                    text=["", "t ↑"],
                    textposition="top center",
                    textfont=dict(color=COLORS["quaternary"]),
                    showlegend=False,
                ),
                # Spiral worldline (projected)
                go.Scatter(
                    x=spiral_x, y=spiral_t,
                    mode="lines",
                    line=dict(color=COLORS["spacetime"], width=2),
                    name="Spiral worldline" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                # Current point
                go.Scatter(
                    x=[marker_x], y=[t / (2 * np.pi) * 3],
                    mode="markers",
                    marker=dict(size=10, color=COLORS["particle"]),
                    showlegend=False,
                ),

                # ========== 3+1D SPACETIME (right) ==========
                # Label
                go.Scatter(
                    x=[3.5], y=[4.5],
                    mode="text",
                    text=["<b>3+1D Spacetime</b><br>(3 space + 1 time)"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
                # Hypercube projection (tesseract) - outer cube
                go.Scatter(
                    x=[3.5 - cube_scale, 3.5 + cube_scale, 3.5 + cube_scale, 3.5 - cube_scale, 3.5 - cube_scale],
                    y=[1 - cube_scale, 1 - cube_scale, 1 + cube_scale, 1 + cube_scale, 1 - cube_scale],
                    mode="lines",
                    line=dict(color=COLORS["primary"], width=2),
                    name="3D space (now)" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                # Inner cube (future)
                go.Scatter(
                    x=[3.5 - inner_scale, 3.5 + inner_scale, 3.5 + inner_scale, 3.5 - inner_scale, 3.5 - inner_scale],
                    y=[2.5 - inner_scale, 2.5 - inner_scale, 2.5 + inner_scale, 2.5 + inner_scale, 2.5 - inner_scale],
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    name="3D space (future)" if i == 0 else None,
                    showlegend=(i == 0),
                ),
                # Connecting lines (time evolution)
                *[go.Scatter(
                    x=[3.5 + dx * cube_scale, 3.5 + dx * inner_scale],
                    y=[1 + dy * cube_scale, 2.5 + dy * inner_scale],
                    mode="lines",
                    line=dict(color=COLORS["text_secondary"], width=1, dash="dot"),
                    showlegend=False,
                ) for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]],
                # Rotating point showing 4D motion
                go.Scatter(
                    x=[3.5 + 0.3 * np.cos(t * 2)],
                    y=[1.75 + 0.3 * np.sin(t)],
                    mode="markers",
                    marker=dict(size=12, color=COLORS["secondary"]),
                    name="4D observer" if i == 0 else None,
                    showlegend=(i == 0),
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Visualizing Spacetime Dimensions</b><br><sub>How we represent 2D, 3D, and 4D spacetime</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(range=[-6, 6], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1, 5.5], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    bgcolor="rgba(22, 33, 62, 0.8)",
                    font=dict(size=10),
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    spacetime_dim_fig = create_spacetime_dimensions_animation()
    spacetime_dim_fig
    return (create_spacetime_dimensions_animation, spacetime_dim_fig)


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_wormhole_animation():
        """Visualize a wormhole connecting two regions of 2D space."""
        n_frames = 80

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 2 * np.pi

            # Wormhole as two "mouths" connected through higher dimension
            # Represented as an embedding diagram

            # Create the curved space surface
            x_surface = np.linspace(-3, 3, 60)

            # Upper sheet (our universe)
            y_upper = 2 + 0.3 * np.exp(-x_surface**2 / 2)

            # Lower sheet (other region / other universe)
            y_lower = -2 - 0.3 * np.exp(-x_surface**2 / 2)

            # Wormhole throat connecting them
            throat_y = np.linspace(y_lower[30], y_upper[30], 20)
            throat_x = 0.3 * np.sin(np.linspace(0, np.pi, 20)) * np.cos(t * 2)

            # Particle traveling through wormhole
            progress = (i / n_frames) % 1
            if progress < 0.3:
                # On upper surface, moving toward throat
                p = progress / 0.3
                particle_x = 2.5 - p * 2.5
                particle_y = 2 + 0.3 * np.exp(-particle_x**2 / 2)
            elif progress < 0.7:
                # In throat
                p = (progress - 0.3) / 0.4
                particle_x = 0.2 * np.sin(p * np.pi) * np.cos(t)
                particle_y = y_upper[30] - p * (y_upper[30] - y_lower[30])
            else:
                # On lower surface, moving away
                p = (progress - 0.7) / 0.3
                particle_x = p * 2.5
                particle_y = -2 - 0.3 * np.exp(-particle_x**2 / 2)

            # Light rays showing connection
            ray_progress = (t / (2 * np.pi)) % 1

            frame_data = [
                # Upper surface (our universe)
                go.Scatter(
                    x=x_surface, y=y_upper,
                    mode="lines",
                    line=dict(color=COLORS["primary"], width=3),
                    fill="tozeroy",
                    fillcolor="rgba(0, 212, 255, 0.1)",
                    name="Our universe",
                    showlegend=(i == 0),
                ),
                # Lower surface
                go.Scatter(
                    x=x_surface, y=y_lower,
                    mode="lines",
                    line=dict(color=COLORS["spacetime"], width=3),
                    fill="tozeroy",
                    fillcolor="rgba(167, 139, 250, 0.1)",
                    name="Other region",
                    showlegend=(i == 0),
                ),
                # Wormhole throat
                go.Scatter(
                    x=throat_x, y=throat_y,
                    mode="lines",
                    line=dict(color=COLORS["secondary"], width=4),
                    name="Wormhole throat",
                    showlegend=(i == 0),
                ),
                # Exotic matter at throat (negative energy)
                go.Scatter(
                    x=[0], y=[0],
                    mode="markers",
                    marker=dict(
                        size=25,
                        color="rgba(255, 100, 100, 0.5)",
                        line=dict(color=COLORS["secondary"], width=2),
                        symbol="diamond",
                    ),
                    name="Exotic matter",
                    showlegend=(i == 0),
                ),
                # Particle
                go.Scatter(
                    x=[particle_x], y=[particle_y],
                    mode="markers",
                    marker=dict(size=12, color=COLORS["quaternary"]),
                    name="Traveler",
                    showlegend=(i == 0),
                ),
                # Labels
                go.Scatter(
                    x=[2.5], y=[2.8],
                    mode="text",
                    text=["Region A"],
                    textfont=dict(color=COLORS["primary"], size=12),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[2.5], y=[-2.8],
                    mode="text",
                    text=["Region B"],
                    textfont=dict(color=COLORS["spacetime"], size=12),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[0.8], y=[0],
                    mode="text",
                    text=["ρ < 0"],
                    textfont=dict(color=COLORS["secondary"], size=11),
                    showlegend=False,
                ),
                # Distance annotations
                go.Scatter(
                    x=[-2.5, 2.5], y=[3.2, 3.2],
                    mode="lines+text",
                    line=dict(color=COLORS["text_secondary"], width=1, dash="dot"),
                    text=["", "Normal path: far"],
                    textposition="top center",
                    textfont=dict(color=COLORS["text_secondary"], size=10),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[0], y=[0.8],
                    mode="text",
                    text=["Shortcut!"],
                    textfont=dict(color=COLORS["quaternary"], size=10),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Wormhole:</b> A Shortcut Through Spacetime<br><sub>Exotic matter (ρ < 0) holds the throat open</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(range=[-4, 4], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-4, 4], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(bgcolor="rgba(22, 33, 62, 0.8)"),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    wormhole_fig = create_wormhole_animation()
    wormhole_fig
    return (create_wormhole_animation, wormhole_fig)


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_exotic_matter_spacetime_animation():
        """Show exotic matter behavior in 2D space + 1D time."""
        n_frames = 100

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 8  # Time evolution

            # Grid representing 2D space at current time slice
            x_grid = np.linspace(-3, 3, 15)
            y_grid = np.linspace(-3, 3, 15)

            # Normal matter: attracts, curves space inward
            # Position of normal matter
            nm_x, nm_y = -1.5, 0

            # Exotic matter: repels, curves space outward
            # Position of exotic matter
            em_x, em_y = 1.5, 0

            # Test particles
            n_test = 8
            test_angles = np.linspace(0, 2 * np.pi, n_test, endpoint=False)

            # Particles around normal matter (fall inward)
            nm_r = max(0.3, 1.5 - t * 0.15)
            nm_test_x = nm_x + nm_r * np.cos(test_angles + t * 0.5)
            nm_test_y = nm_y + nm_r * np.sin(test_angles + t * 0.5)

            # Particles around exotic matter (pushed outward)
            em_r = min(2.5, 0.5 + t * 0.2)
            em_test_x = em_x + em_r * np.cos(test_angles - t * 0.3)
            em_test_y = em_y + em_r * np.sin(test_angles - t * 0.3)

            # Spacetime curvature visualization (deformed grid)
            grid_traces = []
            for gx in x_grid:
                line_y = y_grid.copy()
                line_x = np.full_like(line_y, gx)
                # Deform based on matter locations
                for j in range(len(line_y)):
                    # Normal matter pulls grid inward
                    d_nm = np.sqrt((gx - nm_x)**2 + (line_y[j] - nm_y)**2)
                    if d_nm > 0.3:
                        pull = 0.3 / d_nm**1.5
                        line_x[j] += pull * (nm_x - gx) / d_nm
                        line_y[j] += pull * (nm_y - line_y[j]) / d_nm

                    # Exotic matter pushes grid outward
                    d_em = np.sqrt((gx - em_x)**2 + (line_y[j] - em_y)**2)
                    if d_em > 0.3:
                        push = 0.3 / d_em**1.5
                        line_x[j] -= push * (em_x - gx) / d_em  # Opposite direction!
                        line_y[j] -= push * (em_y - line_y[j]) / d_em

                grid_traces.append(go.Scatter(
                    x=line_x, y=line_y,
                    mode="lines",
                    line=dict(color=COLORS["grid"], width=1),
                    showlegend=False,
                ))

            # Horizontal grid lines
            for gy in y_grid:
                line_x = x_grid.copy()
                line_y = np.full_like(line_x, gy)
                for j in range(len(line_x)):
                    d_nm = np.sqrt((line_x[j] - nm_x)**2 + (gy - nm_y)**2)
                    if d_nm > 0.3:
                        pull = 0.3 / d_nm**1.5
                        line_x[j] += pull * (nm_x - line_x[j]) / d_nm
                        line_y[j] += pull * (nm_y - gy) / d_nm

                    d_em = np.sqrt((line_x[j] - em_x)**2 + (gy - em_y)**2)
                    if d_em > 0.3:
                        push = 0.3 / d_em**1.5
                        line_x[j] -= push * (em_x - line_x[j]) / d_em
                        line_y[j] -= push * (em_y - gy) / d_em

                grid_traces.append(go.Scatter(
                    x=line_x, y=line_y,
                    mode="lines",
                    line=dict(color=COLORS["grid"], width=1),
                    showlegend=False,
                ))

            frame_data = [
                # Deformed spacetime grid
                *grid_traces,
                # Normal matter (positive energy)
                go.Scatter(
                    x=[nm_x], y=[nm_y],
                    mode="markers+text",
                    marker=dict(size=30, color=COLORS["gravity"],
                               line=dict(color="white", width=2)),
                    text=["ρ > 0"],
                    textposition="bottom center",
                    textfont=dict(color=COLORS["gravity"], size=11),
                    name="Normal matter (ρ > 0)",
                    showlegend=(i == 0),
                ),
                # Exotic matter (negative energy)
                go.Scatter(
                    x=[em_x], y=[em_y],
                    mode="markers+text",
                    marker=dict(size=30, color=COLORS["secondary"],
                               line=dict(color="white", width=2),
                               symbol="diamond"),
                    text=["ρ < 0"],
                    textposition="bottom center",
                    textfont=dict(color=COLORS["secondary"], size=11),
                    name="Exotic matter (ρ < 0)",
                    showlegend=(i == 0),
                ),
                # Test particles around normal matter
                go.Scatter(
                    x=nm_test_x, y=nm_test_y,
                    mode="markers",
                    marker=dict(size=8, color=COLORS["quaternary"]),
                    name="Attracted particles",
                    showlegend=(i == 0),
                ),
                # Test particles around exotic matter
                go.Scatter(
                    x=em_test_x, y=em_test_y,
                    mode="markers",
                    marker=dict(size=8, color=COLORS["wave"]),
                    name="Repelled particles",
                    showlegend=(i == 0),
                ),
                # Arrows showing attraction
                go.Scatter(
                    x=[nm_x - 0.8, nm_x - 0.4], y=[0.8, 0.4],
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=2),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[nm_x + 0.8, nm_x + 0.4], y=[-0.8, -0.4],
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=2),
                    showlegend=False,
                ),
                # Arrows showing repulsion
                go.Scatter(
                    x=[em_x + 0.4, em_x + 0.8], y=[0.4, 0.8],
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[em_x - 0.4, em_x - 0.8], y=[-0.4, -0.8],
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    showlegend=False,
                ),
                # Labels
                go.Scatter(
                    x=[-1.5], y=[2.5],
                    mode="text",
                    text=["<b>ATTRACTS</b><br>Curves space inward"],
                    textfont=dict(color=COLORS["gravity"], size=10),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[1.5], y=[2.5],
                    mode="text",
                    text=["<b>REPELS</b><br>Curves space outward"],
                    textfont=dict(color=COLORS["secondary"], size=10),
                    showlegend=False,
                ),
                # Time indicator
                go.Scatter(
                    x=[3.2], y=[-2.8],
                    mode="text",
                    text=[f"t = {t:.1f}"],
                    textfont=dict(color=COLORS["text_secondary"], size=11),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Exotic Matter in 2D Space:</b> Gravitational Repulsion<br><sub>Normal matter attracts; exotic matter repels</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    bgcolor="rgba(22, 33, 62, 0.8)",
                    font=dict(size=10),
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    exotic_spacetime_fig = create_exotic_matter_spacetime_animation()
    exotic_spacetime_fig
    return (create_exotic_matter_spacetime_animation, exotic_spacetime_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## What Does "Sideways in Time" Mean?

        If time were 2D, "sideways in time" would mean moving perpendicular to your
        current time direction—like turning 90° in the time plane.

        **In our 1D time universe:**
        - Forward in time: the future
        - Backward in time: the past (forbidden by thermodynamics)
        - Sideways in time: **undefined** (there's no perpendicular direction!)

        **In a hypothetical 2D time universe:**
        - Forward in $t_1$: one "future"
        - Forward in $t_2$: a different "future"
        - Diagonal: combination of both
        - Sideways: moving in one time while the other stays constant

        **The strange implication:** In 2D time, there might be events that are
        neither in your past nor your future—they're "beside" you in time.
        You can't reach them by waiting, and they can't affect you... yet they exist.

        *The animation below shows the difference between 1D and 2D time trajectories.*
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_time_directions_animation():
        """Compare 1D vs 2D time directions."""
        n_frames = 60

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 6

            # 1D time: can only go forward/backward
            x_1d = np.sin(t)
            t_1d = t

            # 2D time: can also go "sideways"
            angle = t * 0.5
            t1_2d = 1.5 + t * 0.4 * np.cos(angle)
            t2_2d = 1.5 + t * 0.4 * np.sin(angle)

            # Histories
            t_vals = np.linspace(0, t, max(2, i + 1))
            x_1d_hist = np.sin(t_vals)
            t1_2d_hist = 1.5 + t_vals * 0.4 * np.cos(t_vals * 0.5)
            t2_2d_hist = 1.5 + t_vals * 0.4 * np.sin(t_vals * 0.5)

            frame_data = [
                # ===== LEFT PLOT: 1D Time =====
                # Worldline
                go.Scatter(
                    x=x_1d_hist - 5, y=t_vals,
                    mode="lines",
                    line=dict(color=COLORS["primary"], width=3),
                    name="1D time worldline",
                    showlegend=(i == 0),
                ),
                # Current position
                go.Scatter(
                    x=[x_1d - 5], y=[t_1d],
                    mode="markers",
                    marker=dict(size=12, color=COLORS["secondary"]),
                    name="Observer (1D time)",
                    showlegend=(i == 0),
                ),
                # Forward arrow
                go.Scatter(
                    x=[x_1d - 5, x_1d - 5], y=[t_1d, t_1d + 0.5],
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=3),
                    showlegend=False,
                ),
                # Label
                go.Scatter(
                    x=[-5], y=[7],
                    mode="text",
                    text=["<b>1D Time</b><br>Only forward/backward"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),

                # ===== RIGHT PLOT: 2D Time =====
                # Path
                go.Scatter(
                    x=t1_2d_hist + 2, y=t2_2d_hist,
                    mode="lines",
                    line=dict(color=COLORS["spacetime"], width=3),
                    name="2D time path",
                    showlegend=(i == 0),
                ),
                # Current position
                go.Scatter(
                    x=[t1_2d + 2], y=[t2_2d],
                    mode="markers",
                    marker=dict(size=12, color=COLORS["particle"]),
                    name="Observer (2D time)",
                    showlegend=(i == 0),
                ),
                # Direction arrows (showing 2D freedom)
                go.Scatter(
                    x=[t1_2d + 2, t1_2d + 2.4], y=[t2_2d, t2_2d],
                    mode="lines",
                    line=dict(color=COLORS["quaternary"], width=2),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[t1_2d + 2, t1_2d + 2], y=[t2_2d, t2_2d + 0.4],
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    showlegend=False,
                ),
                # Label
                go.Scatter(
                    x=[5], y=[7],
                    mode="text",
                    text=["<b>2D Time</b><br>Can move in t₁ or t₂"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),

                # Dividing line
                go.Scatter(
                    x=[0, 0], y=[-0.5, 8],
                    mode="lines",
                    line=dict(color=COLORS["text_secondary"], width=1, dash="dash"),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Comparing Time Dimensions:</b> 1D vs 2D Time<br><sub>Left: Our universe | Right: Hypothetical 2D time</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(
                    range=[-7, 8],
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
                yaxis=dict(
                    range=[-0.5, 8],
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    bgcolor="rgba(22, 33, 62, 0.8)",
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.12,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=70),
            ),
            frames=frames,
        )

        return fig

    directions_fig = create_time_directions_animation()
    directions_fig
    return (create_time_directions_animation, directions_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Speed of Light and Dimensionality

        Does the speed of light depend on the number of dimensions? This is a profound question.

        **In our 3+1 universe:**
        $$c = \frac{1}{\sqrt{\epsilon_0 \mu_0}} \approx 3 \times 10^8 \text{ m/s}$$

        The speed of light emerges from the electric permittivity ($\epsilon_0$) and magnetic
        permeability ($\mu_0$) of free space. These constants describe how electromagnetic
        fields propagate.

        **How might $c$ change with dimensions?**

        1. **Fewer spatial dimensions → different field behavior**
           - In 2D space, fields spread over circles instead of spheres
           - Force laws change: inverse-square becomes inverse-linear
           - This affects how electromagnetic waves propagate

        2. **Multiple time dimensions → multiple "speeds"**
           - In 2D time, there might be different speeds for different time directions
           - The "light cone" becomes a "light surface"

        3. **At the Planck scale:**
           - Quantum gravity effects might modify the effective dimensionality
           - Some theories propose extra dimensions that are "curled up" too small to detect
           - The speed of light could depend on energy at extreme scales

        **String theory prediction:** There are 10 or 11 spacetime dimensions, but 6 or 7 are
        compactified at the Planck scale (~$10^{-35}$ m). Physics looks 3+1D at our scales.
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_dimensional_light_animation():
        """Show how light propagation differs by dimension."""
        n_frames = 60

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 4

            # Light expanding in different dimensions
            theta = np.linspace(0, 2 * np.pi, 100)

            # 1D: just two points
            x_1d = [-t, t]

            # 2D: circle
            x_2d = t * np.cos(theta)
            y_2d = t * np.sin(theta)

            # 3D: sphere (show cross-section)
            # Multiple circles at different z levels
            phi_vals = np.linspace(0, np.pi, 5)

            frame_data = [
                # ===== 1D LIGHT =====
                go.Scatter(
                    x=np.array(x_1d) - 6, y=[0, 0],
                    mode="markers+lines",
                    marker=dict(size=10, color=COLORS["photon"]),
                    line=dict(color=COLORS["photon"], width=2),
                    name="1D light (2 points)",
                    showlegend=(i == 0),
                ),
                go.Scatter(
                    x=[-6], y=[1.5],
                    mode="text",
                    text=["<b>1D Space</b><br>Light = 2 points"],
                    textfont=dict(color=COLORS["text"], size=10),
                    showlegend=False,
                ),

                # ===== 2D LIGHT =====
                go.Scatter(
                    x=x_2d, y=y_2d - 4,
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    name="2D light (circle)",
                    showlegend=(i == 0),
                ),
                go.Scatter(
                    x=[0], y=[-2.5],
                    mode="text",
                    text=["<b>2D Space</b><br>Light = circle"],
                    textfont=dict(color=COLORS["text"], size=10),
                    showlegend=False,
                ),

                # ===== 3D LIGHT =====
                # Multiple circles representing sphere cross-sections
                *[go.Scatter(
                    x=t * np.sin(phi) * np.cos(theta) + 6,
                    y=t * np.sin(phi) * np.sin(theta),
                    mode="lines",
                    line=dict(color=COLORS["quantum"], width=1),
                    name="3D light (sphere)" if j == 0 and i == 0 else None,
                    showlegend=(j == 0 and i == 0),
                ) for j, phi in enumerate(phi_vals)],
                go.Scatter(
                    x=[6], y=[1.5],
                    mode="text",
                    text=["<b>3D Space</b><br>Light = sphere"],
                    textfont=dict(color=COLORS["text"], size=10),
                    showlegend=False,
                ),

                # Time indicator
                go.Scatter(
                    x=[-8], y=[-5],
                    mode="text",
                    text=[f"t = {t:.2f}"],
                    textfont=dict(color=COLORS["quaternary"], size=14),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Light Propagation by Dimension</b><br><sub>How a flash of light expands in 1D, 2D, and 3D space</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(
                    range=[-9, 9],
                    scaleanchor="y",
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
                yaxis=dict(
                    range=[-6, 3],
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    bgcolor="rgba(22, 33, 62, 0.8)",
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.12,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=70),
            ),
            frames=frames,
        )

        return fig

    light_dim_fig = create_dimensional_light_animation()
    light_dim_fig
    return (create_dimensional_light_animation, light_dim_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Quantum Question: Does Time Behave Differently at Small Scales?

        At the quantum level, some strange things happen that blur our classical
        understanding of time:

        **1. Quantum Superposition**

        A particle can be in multiple states *simultaneously*—until measured.
        Is it in multiple places in time too? Some interpretations suggest
        quantum states "spread" through time, not just space.

        **2. Wheeler-DeWitt Equation**

        In quantum gravity, the fundamental equation has **no time parameter**:

        $$\hat{H}\Psi = 0$$

        Time seems to emerge from the quantum state, not be fundamental!
        This is the "problem of time" in quantum gravity.

        **3. Quantum Entanglement**

        Entangled particles show correlations that seem to transcend time—
        measuring one particle instantly affects its partner, regardless of
        distance. Does this hint at a different structure of time?

        **4. Time Crystals**

        Recently discovered states of matter that repeat in time like crystals
        repeat in space. They break **time translation symmetry**—they're not
        the same at every moment.

        **5. CPT Symmetry**

        The laws of physics are symmetric under the combined operation of
        Charge conjugation (C), Parity inversion (P), and Time reversal (T).
        This suggests time reversal *is* meaningful at the fundamental level,
        even if we can't achieve it macroscopically.

        $$\text{CPT}|\psi\rangle = |\psi\rangle$$
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_quantum_time_animation():
        """Visualize quantum superposition spreading in space and time."""
        n_frames = 80

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 6

            # Quantum wavepacket spreading
            x = np.linspace(-5, 5, 200)
            sigma = 0.5 + t * 0.3  # Spreading width
            psi = np.exp(-x**2 / (2 * sigma**2)) * np.cos(3 * x - t * 2)
            prob = psi**2

            # Probability at different "times" (superposition)
            psi_past = np.exp(-(x + 1)**2 / (2 * 0.5**2)) * 0.3
            psi_future = np.exp(-(x - 1)**2 / (2 * 0.8**2)) * 0.3

            # Classical particle position
            x_classical = 2 * np.sin(t * 0.5)

            frame_data = [
                # Probability density
                go.Scatter(
                    x=x, y=prob + 2,
                    mode="lines",
                    fill="tozeroy",
                    fillcolor="rgba(0, 212, 255, 0.3)",
                    line=dict(color=COLORS["quantum"], width=2),
                    name="|ψ|² (probability)",
                    showlegend=(i == 0),
                ),
                # Wave function (real part)
                go.Scatter(
                    x=x, y=psi,
                    mode="lines",
                    line=dict(color=COLORS["wave"], width=2),
                    name="ψ (wave function)",
                    showlegend=(i == 0),
                ),
                # "Ghost" of past state
                go.Scatter(
                    x=x, y=psi_past - 1.5,
                    mode="lines",
                    line=dict(color=COLORS["text_secondary"], width=1, dash="dot"),
                    name="Past state (fading)",
                    showlegend=(i == 0),
                ),
                # Classical particle for comparison
                go.Scatter(
                    x=[x_classical], y=[-2.5],
                    mode="markers",
                    marker=dict(size=15, color=COLORS["secondary"]),
                    name="Classical particle",
                    showlegend=(i == 0),
                ),
                # Labels
                go.Scatter(
                    x=[-4.5], y=[2.5],
                    mode="text",
                    text=["<b>Quantum</b>: Spread in space AND time?"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[-4.5], y=[-2.5],
                    mode="text",
                    text=["<b>Classical</b>: Definite position"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
                # Time indicator
                go.Scatter(
                    x=[4], y=[3.5],
                    mode="text",
                    text=[f"t = {t:.2f}"],
                    textfont=dict(color=COLORS["quaternary"], size=12),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Quantum Time:</b> Does the Wavefunction Extend in Time?<br><sub>Quantum mechanics challenges our classical notion of 'now'</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(
                    title="Position",
                    range=[-5.5, 5.5],
                    gridcolor=COLORS["grid"],
                ),
                yaxis=dict(
                    title="Amplitude / Probability",
                    range=[-3.5, 4],
                    gridcolor=COLORS["grid"],
                ),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    bgcolor="rgba(22, 33, 62, 0.8)",
                ),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    quantum_fig = create_quantum_time_animation()
    quantum_fig
    return (create_quantum_time_animation, quantum_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Different Dimensional Signatures: What's Possible?

        Physicists use the notation $(s, t)$ for $s$ spatial and $t$ temporal dimensions.
        Here's what different signatures would mean:

        | Signature | Metric | Properties |
        |-----------|--------|------------|
        | **(3,1)** — Our universe | $ds^2 = c^2dt^2 - dx^2 - dy^2 - dz^2$ | Stable atoms, causality, life possible |
        | **(2,1)** — Flatland | $ds^2 = c^2dt^2 - dx^2 - dy^2$ | No stable orbits, no complex life |
        | **(4,1)** — Extra space | $ds^2 = c^2dt^2 - dx^2 - dy^2 - dz^2 - dw^2$ | Unstable orbits, inverse-cube gravity |
        | **(3,0)** — Timeless | $ds^2 = -dx^2 - dy^2 - dz^2$ | No dynamics, frozen universe |
        | **(2,2)** — Two times | $ds^2 = c^2dt_1^2 + c^2dt_2^2 - dx^2 - dy^2$ | Causal chaos, paradoxes |
        | **(1,1)** — Minimal | $ds^2 = c^2dt^2 - dx^2$ | Line universe, simple but restrictive |

        **Why (3,1)?**

        Physicist Max Tegmark argued that (3,1) is the *only* signature that allows:
        - Stable atoms (electron orbits)
        - Stable planetary orbits
        - Information processing (for brains/computers)
        - Predictable causality

        Any other combination either has no time for dynamics, or too much time for causality,
        or unstable structures.

        > *"We exist in (3,1) spacetime because it's the only place where 'existing'
        > is meaningful."*
        """
    )
    return


@app.cell
def _(COLORS, go, np):
    def create_signature_comparison():
        """Create a static comparison of different spacetime signatures."""

        # Create subplots-like layout with scatter traces
        fig = go.Figure()

        # (3,1) - Our universe: stable orbit
        theta = np.linspace(0, 2 * np.pi, 100)
        x_31 = np.cos(theta) * 0.8 - 3
        y_31 = np.sin(theta) * 0.8 + 2

        # (2,1) - Flatland: spiral inward (unstable)
        t = np.linspace(0, 4 * np.pi, 100)
        r = 0.8 * np.exp(-t / 10)
        x_21 = r * np.cos(t)
        y_21 = r * np.sin(t) + 2

        # (4,1) - 4D space: spiral outward (unstable)
        r_41 = 0.3 * np.exp(t / 15)
        x_41 = r_41 * np.cos(t) + 3
        y_41 = r_41 * np.sin(t) + 2

        # (3,0) - No time: just a point
        x_30 = -3
        y_30 = -2

        # (2,2) - 2 times: chaotic path
        x_22 = np.sin(t) * 0.5 + np.sin(t * 2.3) * 0.3
        y_22 = np.cos(t * 1.7) * 0.5 + np.cos(t * 0.7) * 0.3 - 2

        # (1,1) - Minimal: just oscillation on a line
        x_11 = np.sin(t) * 0.7 + 3
        y_11 = np.zeros_like(t) - 2

        # Add traces
        fig.add_trace(go.Scatter(
            x=x_31, y=y_31, mode="lines",
            line=dict(color=COLORS["wave"], width=3),
            name="(3,1) Stable orbit"
        ))
        fig.add_trace(go.Scatter(
            x=[-3], y=[2], mode="markers",
            marker=dict(size=15, color=COLORS["gravity"]),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=x_21, y=y_21, mode="lines",
            line=dict(color=COLORS["secondary"], width=2),
            name="(2,1) Spiral in"
        ))
        fig.add_trace(go.Scatter(
            x=[0], y=[2], mode="markers",
            marker=dict(size=12, color=COLORS["gravity"]),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=x_41, y=y_41, mode="lines",
            line=dict(color=COLORS["spacetime"], width=2),
            name="(4,1) Spiral out"
        ))
        fig.add_trace(go.Scatter(
            x=[3], y=[2], mode="markers",
            marker=dict(size=12, color=COLORS["gravity"]),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[x_30], y=[y_30], mode="markers",
            marker=dict(size=20, color=COLORS["text_secondary"]),
            name="(3,0) Frozen"
        ))

        fig.add_trace(go.Scatter(
            x=x_22, y=y_22, mode="lines",
            line=dict(color=COLORS["particle"], width=2),
            name="(2,2) Chaotic"
        ))

        fig.add_trace(go.Scatter(
            x=x_11, y=y_11, mode="lines",
            line=dict(color=COLORS["primary"], width=3),
            name="(1,1) Linear"
        ))

        # Labels
        labels = [
            (-3, 3.5, "<b>(3,1)</b><br>Our Universe"),
            (0, 3.5, "<b>(2,1)</b><br>Unstable"),
            (3, 3.5, "<b>(4,1)</b><br>Unstable"),
            (-3, -3.5, "<b>(3,0)</b><br>No dynamics"),
            (0, -3.5, "<b>(2,2)</b><br>Causal chaos"),
            (3, -3.5, "<b>(1,1)</b><br>Minimal"),
        ]

        for x, y, text in labels:
            fig.add_trace(go.Scatter(
                x=[x], y=[y], mode="text",
                text=[text],
                textfont=dict(color=COLORS["text"], size=11),
                showlegend=False
            ))

        fig.update_layout(
            title=dict(
                text="<b>Spacetime Signatures:</b> Why (3,1) is Special<br><sub>Only our signature allows stable structures and causality</sub>",
                font=dict(size=16, color=COLORS["text"]),
            ),
            xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-4.5, 4.5], showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor=COLORS["background"],
            paper_bgcolor=COLORS["paper"],
            font=dict(color=COLORS["text"]),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                bgcolor="rgba(22, 33, 62, 0.8)",
            ),
            height=500,
        )

        return fig

    signature_fig = create_signature_comparison()
    signature_fig
    return (create_signature_comparison, signature_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Why We Can Only Move Forward in Time

        The arrow of time—our inability to move backward—emerges from multiple sources:

        **1. Thermodynamic Arrow**

        The Second Law of Thermodynamics: entropy always increases.
        $$\Delta S \geq 0$$

        Broken eggs don't unbreak. This gives time a direction.

        **2. Cosmological Arrow**

        The universe is expanding, not contracting. The Big Bang was a low-entropy
        state; we're evolving toward higher entropy.

        **3. Psychological Arrow**

        We remember the past, not the future. Our brains create memories
        by increasing entropy (writing information requires energy dissipation).

        **4. Quantum Arrow**

        Wavefunction collapse is irreversible—once measured, a quantum state
        "chooses" an outcome. (Though this is debated!)

        **5. Causal Arrow**

        Causes precede effects. If we could go backward in time, causality would break.

        **The deep question:** Are these arrows independent, or do they all stem from
        one fundamental asymmetry in the laws of physics—or in the initial conditions
        of the universe?

        *The animation below shows entropy increasing with time.*
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    def create_entropy_arrow_animation():
        """Visualize the thermodynamic arrow of time."""
        n_frames = 100
        n_particles = 50

        # Initial state: particles clustered
        np.random.seed(42)
        x_init = np.random.normal(0, 0.3, n_particles)
        y_init = np.random.normal(0, 0.3, n_particles)

        # Velocities (random)
        vx = np.random.normal(0, 0.05, n_particles)
        vy = np.random.normal(0, 0.05, n_particles)

        frames = []
        for i in range(n_frames):
            t = i / n_frames * 20

            # Particles spread out over time
            x = x_init + vx * t
            y = y_init + vy * t

            # Bounce off walls
            x = np.where(np.abs(x) > 2, np.sign(x) * (4 - np.abs(x)), x)
            y = np.where(np.abs(y) > 2, np.sign(y) * (4 - np.abs(y)), y)

            # Calculate "entropy" (spread)
            spread = np.std(x) * np.std(y)
            entropy = np.log(spread + 0.1) + 3

            frame_data = [
                # Box
                go.Scatter(
                    x=[-2, 2, 2, -2, -2], y=[-2, -2, 2, 2, -2],
                    mode="lines",
                    line=dict(color=COLORS["text_secondary"], width=2),
                    showlegend=False,
                ),
                # Particles
                go.Scatter(
                    x=x, y=y,
                    mode="markers",
                    marker=dict(
                        size=8,
                        color=COLORS["quantum"],
                        opacity=0.7,
                    ),
                    name="Gas particles",
                    showlegend=(i == 0),
                ),
                # Entropy indicator
                go.Scatter(
                    x=[3.5], y=[entropy - 2],
                    mode="markers",
                    marker=dict(size=12, color=COLORS["secondary"]),
                    name="Entropy",
                    showlegend=(i == 0),
                ),
                # Entropy axis
                go.Scatter(
                    x=[3.5, 3.5], y=[-2, 2],
                    mode="lines",
                    line=dict(color=COLORS["text_secondary"], width=2),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[3.5], y=[2.3],
                    mode="text",
                    text=["S (entropy)"],
                    textfont=dict(color=COLORS["text"], size=10),
                    showlegend=False,
                ),
                # Time arrow
                go.Scatter(
                    x=[-2.5, -2.5], y=[-2, 2],
                    mode="lines+text",
                    line=dict(color=COLORS["quaternary"], width=2),
                    text=["", "TIME ↑"],
                    textposition="top center",
                    textfont=dict(color=COLORS["quaternary"], size=10),
                    showlegend=False,
                ),
                # Status
                go.Scatter(
                    x=[0], y=[-2.8],
                    mode="text",
                    text=[f"t = {t:.1f}  |  Low entropy → High entropy"],
                    textfont=dict(color=COLORS["text"], size=11),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Arrow of Time:</b> Entropy Always Increases<br><sub>Ordered state → Disordered state (never spontaneously reverses)</sub>",
                    font=dict(size=16, color=COLORS["text"]),
                ),
                xaxis=dict(range=[-3, 4.5], scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3.5, 3], showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(bgcolor="rgba(22, 33, 62, 0.8)"),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.12,
                        x=0.5,
                        xanchor="center",
                        buttons=create_play_pause_buttons(),
                        bgcolor=COLORS["paper"],
                        font=dict(color=COLORS["text"]),
                    )
                ],
                margin=dict(b=70),
            ),
            frames=frames,
        )

        return fig

    entropy_fig = create_entropy_arrow_animation()
    entropy_fig
    return (create_entropy_arrow_animation, entropy_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Deep Structure of Time

        **What we know:**

        1. **Time is 1-dimensional** in our universe—a single line from past to future
        2. **The metric signature matters**: the minus sign between time and space prevents rotation between them
        3. **Multiple time dimensions** would break causality and create paradoxes
        4. **(3,1) spacetime** appears to be the only signature allowing stable, complex structures

        **What remains mysterious:**

        1. **Why is time 1D?** Is this a fundamental constraint or emergent?
        2. **Why the arrow?** Is time's direction fundamental or from initial conditions?
        3. **Quantum gravity:** Does time even exist at the Planck scale?
        4. **The present:** Why do we experience a "now" that moves forward?

        **The deepest question:**

        Is time fundamental—woven into the fabric of reality—or is it emergent,
        arising from something more basic like quantum entanglement or information?

        Some physicists suspect that time, like temperature, is not fundamental but
        emerges from the statistics of more basic entities. In this view, "the flow
        of time" is an illusion created by our macroscopic perspective on a timeless
        quantum reality.

        > *"Time is what keeps everything from happening at once...
        > but at the quantum level, maybe everything IS happening at once."*
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References and Further Reading

        ### Foundational Physics

        - **Tegmark, M.** (1997). "On the dimensionality of spacetime."
          Classical and Quantum Gravity, 14, L69-L75.
          - Analysis of why (3,1) dimensions are special

        - **Feynman, R.** Lectures on Physics, Volume I, Chapters 15-17.
          - Special relativity and spacetime structure

        - **Minkowski, H.** (1908). "Space and Time."
          - The original formulation of 4D spacetime

        ### Time and Thermodynamics

        - **Eddington, A.** (1928). "The Nature of the Physical World."
          - Introduction of the "arrow of time" concept

        - **Penrose, R.** (1989). "The Emperor's New Mind."
          - Discussion of time, entropy, and consciousness

        - **Carroll, S.** (2010). "From Eternity to Here."
          - Accessible explanation of time's arrow

        ### Quantum Aspects

        - **Wheeler, J.A. & DeWitt, B.** (1967). "Quantum Theory of Gravity."
          - The Wheeler-DeWitt equation (timeless quantum gravity)

        - **Rovelli, C.** (2018). "The Order of Time."
          - Modern perspective on time in physics

        ### Multiple Time Dimensions

        - **Bars, I.** (2001). "Survey of two-time physics."
          Physics Reports, 354, 1-100.
          - Theoretical exploration of 2T physics

        - **Tegmark, M.** (1998). "Is 'the Theory of Everything' merely the ultimate
          ensemble theory?" Annals of Physics, 270, 1-51.
          - Why other signatures may not support observers

        ### Exotic Matter and Spacetime Engineering

        - **Morris, M. & Thorne, K.** (1988). "Wormholes in spacetime."
          American Journal of Physics, 56, 395-412.
          - Exotic matter requirements for traversable wormholes

        - **Visser, M.** (1995). "Lorentzian Wormholes: From Einstein to Hawking."
          - Comprehensive treatment of exotic matter in general relativity

        - **Ford, L.H. & Roman, T.A.** (1996). "Quantum field theory constrains
          traversable wormhole geometries." Physical Review D, 53, 5496.
          - Quantum inequalities limiting negative energy

        - **Casimir, H.B.G.** (1948). "On the attraction between two perfectly
          conducting plates." Proceedings of the Royal Netherlands Academy.
          - Original prediction of the Casimir effect
        """
    )
    return


if __name__ == "__main__":
    app.run()
