import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


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
        # Beyond the Speed of Light?

        *A thought experiment exploring the deep structure of spacetime*

        ---

        ## The Cosmic Speed Limit

        Why can't anything travel faster than light? The usual answer—"Einstein said so"—
        isn't satisfying. Let's dig deeper into *why* this limit exists, and explore what
        would happen if we could somehow exceed it.

        The speed of light isn't just about light. It's the **speed of causality**—the
        maximum rate at which any influence can propagate through the universe. It emerges
        from the very geometry of spacetime itself.

        > *"The speed of light is the conversion factor between space and time.
        > It tells us how much space equals how much time."*

        $$c = 299,792,458 \text{ m/s} = 1 \text{ light-second per second}$$

        In natural units, physicists often set $c = 1$, treating space and time as
        fundamentally the same thing measured in different units—like measuring height
        in feet and width in meters.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Spacetime Velocity: Everything Moves at c

        Here's a profound insight: **everything always moves through spacetime at exactly c**.

        When you're sitting still in space, you're moving through time at the maximum rate.
        When you move through space, some of your "spacetime velocity" shifts from time to space.

        Think of it as a velocity vector in spacetime with fixed magnitude $c$:

        $$|\vec{v}_{spacetime}|^2 = v_{space}^2 + v_{time}^2 = c^2$$

        Wait—that's not quite right. Due to the hyperbolic geometry of spacetime, it's actually:

        $$v_{time}^2 - v_{space}^2 = c^2$$

        This is the **spacetime interval**—and it's always preserved.

        - At rest: $v_{space} = 0$, so $v_{time} = c$ (maximum aging)
        - Moving at $0.6c$: $v_{time} = \sqrt{c^2 - (0.6c)^2} = 0.8c$ (time dilation!)
        - Moving at $c$: $v_{time} = 0$ (time stops—photons don't age)

        *The animation shows how your "velocity through time" decreases as you move through space.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_spacetime_velocity_animation():
        """Animate the tradeoff between space and time velocity."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            # Velocity through space (0 to 0.99c)
            v_space = 0.99 * i / n_frames

            # Velocity through time (using Minkowski geometry)
            # v_time^2 - v_space^2 = c^2, so v_time = sqrt(c^2 + v_space^2)
            # But for proper time: gamma = 1/sqrt(1 - v^2/c^2)
            # Rate of proper time: dtau/dt = 1/gamma = sqrt(1 - v^2/c^2)
            gamma = 1 / np.sqrt(1 - v_space**2) if v_space < 1 else float('inf')
            v_time = np.sqrt(1 - v_space**2) if v_space < 1 else 0  # As fraction of c

            # For the circle visualization (Euclidean analogy)
            theta = np.linspace(0, 2 * np.pi, 100)
            circle_x = np.cos(theta)
            circle_y = np.sin(theta)

            # Current velocity vector
            angle = np.arcsin(v_space) if v_space <= 1 else np.pi/2

            frame_data = [
                # Unit circle (represents c)
                go.Scatter(
                    x=circle_x, y=circle_y,
                    mode="lines",
                    line=dict(color="rgba(255,255,255,0.3)", width=2, dash="dot"),
                    name="|v| = c",
                ),
                # Axes
                go.Scatter(
                    x=[-1.3, 1.3], y=[0, 0],
                    mode="lines",
                    line=dict(color="rgba(255,255,255,0.5)", width=1),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[0, 0], y=[-0.3, 1.3],
                    mode="lines",
                    line=dict(color="rgba(255,255,255,0.5)", width=1),
                    showlegend=False,
                ),
                # Velocity vector
                go.Scatter(
                    x=[0, v_space], y=[0, v_time],
                    mode="lines+markers",
                    line=dict(color="cyan", width=4),
                    marker=dict(size=[0, 12], color="cyan"),
                    name=f"v<sub>space</sub> = {v_space:.2f}c",
                ),
                # Components
                go.Scatter(
                    x=[0, v_space], y=[0, 0],
                    mode="lines",
                    line=dict(color="orange", width=3),
                    name=f"Space velocity: {v_space:.2f}c",
                ),
                go.Scatter(
                    x=[0, 0], y=[0, v_time],
                    mode="lines",
                    line=dict(color="yellow", width=3),
                    name=f"Time velocity: {v_time:.2f}c",
                ),
                # Info text
                go.Scatter(
                    x=[0.7], y=[-0.2],
                    mode="text",
                    text=[f"γ = {gamma:.2f}" if gamma < 100 else "γ → ∞"],
                    textfont=dict(size=14, color="white"),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Spacetime Velocity:</b> Trading Time for Space<br><sub>As you move faster through space, you move slower through time</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Velocity through SPACE (v/c)", range=[-0.3, 1.4],
                          showgrid=False, zeroline=False),
                yaxis=dict(title="Velocity through TIME (fraction of c)", range=[-0.3, 1.4],
                          showgrid=False, zeroline=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    spacetime_velocity_fig = create_spacetime_velocity_animation()
    spacetime_velocity_fig
    return create_spacetime_velocity_animation, spacetime_velocity_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Energy Barrier

        One reason we can't reach $c$ is the **energy requirement**. As an object speeds up,
        its relativistic mass-energy increases:

        $$\begin{aligned}
        E &= \gamma m c^2 \\
        &= \frac{mc^2}{\sqrt{1 - v^2/c^2}}
        \end{aligned}$$

        | Speed | γ (gamma) | Energy (× rest mass) |
        |-------|-----------|---------------------|
        | 0 | 1.00 | 1.00 |
        | 0.5c | 1.15 | 1.15 |
        | 0.9c | 2.29 | 2.29 |
        | 0.99c | 7.09 | 7.09 |
        | 0.999c | 22.4 | 22.4 |
        | 0.9999c | 70.7 | 70.7 |

        As $v \to c$, $\gamma \to \infty$, meaning **infinite energy** is needed to reach $c$.

        But what if we could somehow *start* above $c$? What if particles were *born* faster
        than light? This leads us to the hypothetical world of **tachyons**.

        *The animation shows energy diverging as velocity approaches c.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_energy_barrier_animation():
        """Animate the energy barrier at c."""
        n_frames = 50

        frames = []

        for i in range(n_frames):
            # Current velocity being explored
            v_current = 0.999 * i / n_frames

            v = np.linspace(0, 0.999, 500)
            gamma = 1 / np.sqrt(1 - v**2)
            energy = gamma  # In units of rest mass energy

            # Marker position
            if v_current > 0:
                gamma_current = 1 / np.sqrt(1 - v_current**2)
            else:
                gamma_current = 1

            frame_data = [
                # Energy curve
                go.Scatter(
                    x=v, y=energy,
                    mode="lines",
                    line=dict(color="cyan", width=3),
                    name="E = γmc²",
                    fill="tozeroy",
                    fillcolor="rgba(0, 255, 255, 0.2)",
                ),
                # Speed of light barrier
                go.Scatter(
                    x=[1, 1], y=[0, 50],
                    mode="lines",
                    line=dict(color="red", width=3, dash="dash"),
                    name="c (light barrier)",
                ),
                # Current position marker
                go.Scatter(
                    x=[v_current], y=[gamma_current],
                    mode="markers",
                    marker=dict(size=15, color="yellow", symbol="star"),
                    name=f"v = {v_current:.3f}c, E = {gamma_current:.1f}mc²",
                ),
                # Asymptote region shading
                go.Scatter(
                    x=[0.95, 1, 1, 0.95],
                    y=[0, 0, 50, 50],
                    fill="toself",
                    fillcolor="rgba(255, 0, 0, 0.1)",
                    line=dict(width=0),
                    name="Forbidden region",
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Energy Barrier:</b> E → ∞ as v → c<br><sub>No finite energy can accelerate mass to light speed</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Velocity (v/c)", range=[0, 1.1], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(title="Energy (units of mc²)", range=[0, 25], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 60, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    energy_barrier_fig = create_energy_barrier_animation()
    energy_barrier_fig
    return create_energy_barrier_animation, energy_barrier_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Tachyons: Faster Than Light?

        Let's explore what happens mathematically if $v > c$. The Lorentz factor becomes:

        $$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$

        When $v > c$, the term under the square root is **negative**, giving an **imaginary** result:

        $$\begin{aligned}
        \gamma &= \frac{1}{\sqrt{1 - v^2/c^2}} \\
        &= \frac{i}{\sqrt{v^2/c^2 - 1}} \quad \text{(imaginary!)}
        \end{aligned}$$

        For the energy to be real, tachyons would need **imaginary mass**:

        $$\begin{aligned}
        E &= \gamma m c^2 \\
        &= \frac{i \cdot (im_0) \cdot c^2}{\sqrt{v^2/c^2 - 1}} \\
        &= \frac{m_0 c^2}{\sqrt{v^2/c^2 - 1}}
        \end{aligned}$$

        With $m = im_0$ (imaginary rest mass), the energy becomes real again!

        **Strange properties of tachyons:**

        - They can never slow down *to* c (just as we can't speed up to c)
        - Adding energy makes them go **slower** (toward c)
        - Removing energy makes them go **faster** (toward infinity)
        - Their minimum energy state is infinite speed!

        *The animation shows the bizarre energy-velocity relationship for tachyons.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_tachyon_energy():
        """Show energy curves for normal matter and tachyons."""
        # Normal matter (v < c)
        v_normal = np.linspace(0, 0.99, 200)
        gamma_normal = 1 / np.sqrt(1 - v_normal**2)
        E_normal = gamma_normal

        # Tachyons (v > c)
        v_tachyon = np.linspace(1.01, 5, 200)
        E_tachyon = 1 / np.sqrt(v_tachyon**2 - 1)

        # Photons (v = c, E depends on frequency, not mass)
        v_photon = [1]
        E_photon = [0]  # Zero rest mass, but finite energy

        fig = go.Figure()

        # Normal matter
        fig.add_trace(go.Scatter(
            x=v_normal, y=E_normal,
            mode="lines",
            line=dict(color="cyan", width=3),
            name="Normal matter (v < c)",
            fill="tozeroy",
            fillcolor="rgba(0, 255, 255, 0.2)",
        ))

        # Tachyons
        fig.add_trace(go.Scatter(
            x=v_tachyon, y=E_tachyon,
            mode="lines",
            line=dict(color="magenta", width=3),
            name="Tachyons (v > c)",
            fill="tozeroy",
            fillcolor="rgba(255, 0, 255, 0.2)",
        ))

        # Light barrier
        fig.add_vline(x=1, line_dash="dash", line_color="yellow",
                     annotation_text="c (barrier)", annotation_position="top")

        # Annotations
        fig.add_annotation(x=0.5, y=3, text="Accelerating →<br>needs MORE energy",
                          showarrow=False, font=dict(color="cyan", size=12))
        fig.add_annotation(x=2.5, y=1.5, text="← Accelerating<br>needs LESS energy!",
                          showarrow=False, font=dict(color="magenta", size=12))

        fig.update_layout(
            title=dict(
                text="<b>Energy vs Velocity:</b> Two Separate Worlds<br><sub>Normal matter and tachyons can't cross the light barrier</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Velocity (v/c)", range=[0, 4], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Energy (units of |m|c²)", range=[0, 10], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    tachyon_energy_fig = create_tachyon_energy()
    return create_tachyon_energy, tachyon_energy_fig


@app.cell
def _(mo, tachyon_energy_fig):
    mo.vstack(
        [
            tachyon_energy_fig,
            mo.md(
                "**What this shows:** The energy-velocity relationship reveals two separate 'worlds'—normal matter (cyan) that can never reach light speed, and hypothetical tachyons (magenta) that can never slow down to it. The light barrier at v = c acts as an impenetrable wall: accelerating normal matter requires infinite energy as you approach c, while tachyons paradoxically lose energy as they speed up."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## What if c Were Larger?

        Now let's ask: what if the speed of light were different? Say, $c' = 2c$?

        This changes the **scale** of the universe in profound ways:

        **1. Time dilation weakens:**

        $$\begin{aligned}
        \gamma' &= \frac{1}{\sqrt{1 - v^2/{c'}^2}} \\
        &= \frac{1}{\sqrt{1 - v^2/4c^2}}
        \end{aligned}$$

        At $v = 0.5c$, with our $c$: $\gamma = 1.15$ (15% time dilation)

        At $v = 0.5c$, with $c' = 2c$: $\gamma' = 1.03$ (only 3% time dilation)

        **2. The universe becomes more "Newtonian":**

        Relativistic effects only become noticeable at speeds close to $c$. A larger $c$
        means you can go faster before spacetime geometry becomes important.

        **3. E = mc² changes scale:**

        $$\begin{aligned}
        E &= m{c'}^2 \\
        &= m(2c)^2 \\
        &= 4mc^2
        \end{aligned}$$

        Each kilogram contains 4× more energy! Nuclear reactions would be more powerful,
        stars would burn differently, and the balance of forces in the universe would shift.

        *The animation compares time dilation for different values of c.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_different_c_comparison():
        """Compare time dilation for different values of c."""
        v = np.linspace(0, 0.95, 200)  # Velocity in units of our c

        # Our universe (c = 1)
        gamma_1 = 1 / np.sqrt(1 - v**2)

        # c' = 2c (so v/c' = v/2)
        gamma_2 = 1 / np.sqrt(1 - (v/2)**2)

        # c' = 0.5c (so v/c' = 2v, only valid for v < 0.5)
        v_small = np.linspace(0, 0.49, 100)
        gamma_half = 1 / np.sqrt(1 - (2*v_small)**2)

        fig = go.Figure()

        # Our universe
        fig.add_trace(go.Scatter(
            x=v, y=gamma_1,
            mode="lines",
            line=dict(color="cyan", width=3),
            name="Our universe (c)",
        ))

        # Larger c
        fig.add_trace(go.Scatter(
            x=v, y=gamma_2,
            mode="lines",
            line=dict(color="green", width=3),
            name="Larger c (c' = 2c)",
        ))

        # Smaller c
        fig.add_trace(go.Scatter(
            x=v_small, y=gamma_half,
            mode="lines",
            line=dict(color="red", width=3),
            name="Smaller c (c' = 0.5c)",
        ))

        # Reference line
        fig.add_hline(y=1, line_dash="dot", line_color="white", opacity=0.5)

        # Annotations
        fig.add_annotation(x=0.7, y=8, text="Smaller c:<br>Relativistic effects<br>kick in sooner",
                          showarrow=True, arrowhead=2, ax=0, ay=-40,
                          font=dict(color="red", size=11))
        fig.add_annotation(x=0.8, y=1.5, text="Larger c:<br>More Newtonian<br>behavior",
                          showarrow=True, arrowhead=2, ax=0, ay=40,
                          font=dict(color="green", size=11))

        fig.update_layout(
            title=dict(
                text="<b>What if c Were Different?</b><br><sub>Time dilation (γ) vs velocity for different light speeds</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Velocity (in units of our c)", range=[0, 1], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Lorentz factor γ (time dilation)", range=[0.8, 12], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    different_c_fig = create_different_c_comparison()
    return create_different_c_comparison, different_c_fig


@app.cell
def _(mo, different_c_fig):
    mo.vstack(
        [
            different_c_fig,
            mo.md(
                "**What this shows:** How the Lorentz factor γ (time dilation) depends on the speed of light. With a smaller c (red), relativistic effects kick in at lower velocities—clocks slow dramatically even at modest speeds. With a larger c (green), the universe behaves more like Newton imagined: you could travel at half our light speed with barely any time dilation. Our universe (cyan) sits between these extremes."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Causal Structure: Why FTL Breaks Physics

        Here's the deepest problem with faster-than-light travel: it breaks **causality**.

        In special relativity, whether event A happens "before" or "after" event B depends
        on your reference frame—*unless* A and B are connected by a light signal or slower.

        **The light cone defines causality:**

        - Events inside your **future light cone** can be affected by you
        - Events inside your **past light cone** could have affected you
        - Events **outside** your light cone are "elsewhere"—causally disconnected

        **The problem with FTL:**

        If you could send a signal faster than light, some observers would see it arrive
        *before* it was sent. You could send a message to yourself in the past!

        This creates paradoxes: What if you send a message saying "don't send this message"?

        *The animation shows how the light cone defines the boundary of causality.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_light_cone_animation():
        """Animate the light cone and causal structure."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            t = 2 * np.pi * i / n_frames

            # Light cone edges
            x_cone = np.linspace(-3, 3, 100)
            t_future = np.abs(x_cone)  # Future light cone
            t_past = -np.abs(x_cone)   # Past light cone

            # A "signal" trying different speeds
            signal_speed = 0.3 + 1.7 * (i / n_frames)  # 0.3c to 2c
            signal_x = np.linspace(0, 2 * min(signal_speed, 2), 50)
            signal_t = signal_x / signal_speed if signal_speed > 0 else signal_x * 0

            # Color based on whether signal is inside light cone
            if signal_speed <= 1:
                signal_color = "cyan"
                signal_name = f"Causal signal (v={signal_speed:.1f}c)"
                region = "Inside light cone ✓"
            else:
                signal_color = "red"
                signal_name = f"FTL signal (v={signal_speed:.1f}c)"
                region = "Outside light cone ✗"

            frame_data = [
                # Future light cone
                go.Scatter(
                    x=x_cone, y=t_future,
                    mode="lines",
                    line=dict(color="yellow", width=2),
                    name="Light (c)",
                    fill="tozeroy",
                    fillcolor="rgba(255, 255, 0, 0.1)",
                ),
                # Past light cone
                go.Scatter(
                    x=x_cone, y=t_past,
                    mode="lines",
                    line=dict(color="yellow", width=2),
                    showlegend=False,
                    fill="tozeroy",
                    fillcolor="rgba(255, 255, 0, 0.1)",
                ),
                # Origin event
                go.Scatter(
                    x=[0], y=[0],
                    mode="markers",
                    marker=dict(size=12, color="white"),
                    name="Event (here, now)",
                ),
                # Signal
                go.Scatter(
                    x=signal_x, y=signal_t,
                    mode="lines",
                    line=dict(color=signal_color, width=4),
                    name=signal_name,
                ),
                # Region label
                go.Scatter(
                    x=[2.5], y=[2.5],
                    mode="text",
                    text=[region],
                    textfont=dict(size=14, color=signal_color),
                    showlegend=False,
                ),
                # "Elsewhere" labels
                go.Scatter(
                    x=[-2.5, 2.5], y=[0, 0],
                    mode="text",
                    text=["ELSEWHERE<br>(spacelike)", "ELSEWHERE<br>(spacelike)"],
                    textfont=dict(size=10, color="rgba(255,255,255,0.5)"),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[0], y=[2.5],
                    mode="text",
                    text=["FUTURE<br>(timelike)"],
                    textfont=dict(size=10, color="rgba(255,255,0,0.7)"),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Light Cone:</b> Boundary of Causality<br><sub>FTL signals exit the light cone and can violate causality</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Space (x)", range=[-4, 4], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)", zeroline=True),
                yaxis=dict(title="Time (t)", range=[-3, 4], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)", zeroline=True, scaleanchor="x"),
                showlegend=True,
                legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    light_cone_fig = create_light_cone_animation()
    light_cone_fig
    return create_light_cone_animation, light_cone_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The "Time Goes Negative" Question

        You asked: if we go faster than c, does time become negative?

        Let's work through the math carefully.

        **Proper time** (time experienced by the traveler):

        $$d\tau^2 = dt^2 - \frac{dx^2}{c^2}$$

        For a moving object: $dx = v \cdot dt$, so:

        $$d\tau^2 = dt^2\left(1 - \frac{v^2}{c^2}\right)$$

        - When $v < c$: $(1 - v^2/c^2) > 0$, so $d\tau$ is real. Time passes normally (just slower).
        - When $v = c$: $d\tau = 0$. Time stops completely (photons don't age).
        - When $v > c$: $(1 - v^2/c^2) < 0$, so $d\tau$ is **imaginary**.

        Imaginary proper time means the interval becomes **spacelike**. The "traveler"
        isn't moving through time at all—they're moving through something more like space.

        **This is why tachyons can't exist as normal matter:** they don't experience time
        in any meaningful sense. They'd be more like "spatial objects" than "temporal beings."
        """
    )
    return


@app.cell
def _(go, np):
    def create_proper_time_visualization():
        """Visualize proper time becoming imaginary above c."""
        v = np.linspace(0, 2, 400)

        # Proper time factor: sqrt(1 - v²/c²)
        # Real part (v < 1)
        v_subluminal = v[v < 1]
        tau_real = np.sqrt(1 - v_subluminal**2)

        # At v = 1, it's zero
        # Imaginary part (v > 1)
        v_superluminal = v[v > 1]
        tau_imag = np.sqrt(v_superluminal**2 - 1)

        fig = go.Figure()

        # Real proper time (v < c)
        fig.add_trace(go.Scatter(
            x=v_subluminal, y=tau_real,
            mode="lines",
            line=dict(color="cyan", width=3),
            name="Real proper time (dτ/dt)",
            fill="tozeroy",
            fillcolor="rgba(0, 255, 255, 0.2)",
        ))

        # Zero at c
        fig.add_trace(go.Scatter(
            x=[1], y=[0],
            mode="markers",
            marker=dict(size=12, color="yellow", symbol="diamond"),
            name="At c: time stops (dτ = 0)",
        ))

        # Imaginary proper time (v > c)
        fig.add_trace(go.Scatter(
            x=v_superluminal, y=tau_imag,
            mode="lines",
            line=dict(color="magenta", width=3, dash="dash"),
            name="Imaginary time (i × shown)",
            fill="tozeroy",
            fillcolor="rgba(255, 0, 255, 0.2)",
        ))

        # Zero line
        fig.add_hline(y=0, line_color="white", line_width=1)

        # Barrier at c
        fig.add_vline(x=1, line_dash="dash", line_color="yellow")

        # Annotations
        fig.add_annotation(x=0.5, y=0.6, text="Time flows<br>(slower at high v)",
                          font=dict(color="cyan", size=12), showarrow=False)
        fig.add_annotation(x=1.5, y=0.8, text="Time is<br>IMAGINARY",
                          font=dict(color="magenta", size=12), showarrow=False)
        fig.add_annotation(x=1, y=-0.15, text="c",
                          font=dict(color="yellow", size=14), showarrow=False)

        fig.update_layout(
            title=dict(
                text="<b>Proper Time vs Velocity:</b> Real → Zero → Imaginary<br><sub>Above c, proper time becomes imaginary (not negative!)</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Velocity (v/c)", range=[0, 2], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Proper time factor |dτ/dt|", range=[-0.3, 1.5], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    proper_time_fig = create_proper_time_visualization()
    return create_proper_time_visualization, proper_time_fig


@app.cell
def _(mo, proper_time_fig):
    mo.vstack(
        [
            proper_time_fig,
            mo.md(
                "**What this shows:** Proper time (the time experienced by a traveler) as a function of velocity. Below c (cyan), time flows normally but slows down as you approach light speed. At exactly c, time stops completely—photons don't age. Above c (magenta dashed), proper time becomes imaginary, not negative. This means FTL travelers wouldn't experience 'backwards time' but rather something that isn't time at all."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Length Contraction: What Happens Above c?

        For a moving object, length contracts:

        $$\begin{aligned}
        L &= L_0 \sqrt{1 - v^2/c^2} \\
        &= \frac{L_0}{\gamma}
        \end{aligned}$$

        - At $v = 0$: $L = L_0$ (no contraction)
        - At $v = 0.866c$: $L = 0.5 L_0$ (half length)
        - At $v = c$: $L = 0$ (infinite contraction)
        - At $v > c$: $L$ becomes **imaginary**

        What does imaginary length mean? One interpretation:

        The object has "rotated" in spacetime so that what was a space dimension is now
        more like a time dimension. The object doesn't have a meaningful spatial extent
        in our reference frame—it's spread out in *time* instead.

        **This connects to the interval:**

        $$\Delta s^2 = \Delta x^2 - c^2 \Delta t^2$$

        - Timelike interval ($\Delta s^2 < 0$): More time separation than space
        - Spacelike interval ($\Delta s^2 > 0$): More space separation than time
        - Lightlike interval ($\Delta s^2 = 0$): On the light cone

        FTL travel converts timelike intervals into spacelike ones—you're not traveling
        through time anymore, you're taking a shortcut through "elsewhere."
        """
    )
    return


@app.cell
def _(go, np):
    def create_length_contraction_animation():
        """Animate length contraction approaching and beyond c."""
        n_frames = 50

        frames = []

        for i in range(n_frames):
            v = 1.8 * i / n_frames  # 0 to 1.8c

            if v < 1:
                # Normal contraction
                L = np.sqrt(1 - v**2)
                L_display = L
                bar_color = "cyan"
                status = f"L = {L:.2f}L₀"
            elif v == 1:
                L_display = 0
                bar_color = "yellow"
                status = "L = 0 (fully contracted)"
            else:
                # "Imaginary" length - display as negative for visualization
                L_imag = np.sqrt(v**2 - 1)
                L_display = -L_imag * 0.5  # Show below axis
                bar_color = "magenta"
                status = f"L = i × {L_imag:.2f}L₀"

            # Spaceship representation
            ship_width = max(abs(L_display), 0.05)

            frame_data = [
                # Reference (rest length)
                go.Scatter(
                    x=[-0.5, 0.5, 0.5, -0.5, -0.5],
                    y=[1.2, 1.2, 1.5, 1.5, 1.2],
                    fill="toself",
                    fillcolor="rgba(255, 255, 255, 0.3)",
                    line=dict(color="white", width=2),
                    name="Rest length L₀",
                ),
                # Moving object
                go.Scatter(
                    x=[-ship_width/2, ship_width/2, ship_width/2, -ship_width/2, -ship_width/2],
                    y=[0 if v <= 1 else L_display - 0.15,
                       0 if v <= 1 else L_display - 0.15,
                       0.3 if v <= 1 else L_display + 0.15,
                       0.3 if v <= 1 else L_display + 0.15,
                       0 if v <= 1 else L_display - 0.15],
                    fill="toself",
                    fillcolor=bar_color,
                    line=dict(color=bar_color, width=2),
                    name=f"Moving at v = {v:.2f}c",
                ),
                # Velocity indicator
                go.Scatter(
                    x=[v], y=[-0.8],
                    mode="markers",
                    marker=dict(size=15, color=bar_color, symbol="triangle-up"),
                    name=status,
                ),
                # Velocity axis
                go.Scatter(
                    x=[0, 2], y=[-0.8, -0.8],
                    mode="lines",
                    line=dict(color="white", width=1),
                    showlegend=False,
                ),
                # c marker
                go.Scatter(
                    x=[1], y=[-0.8],
                    mode="markers+text",
                    marker=dict(size=8, color="yellow"),
                    text=["c"],
                    textposition="bottom center",
                    textfont=dict(size=12, color="yellow"),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Length Contraction:</b> Real → Zero → Imaginary<br><sub>Watch the object contract to zero at c, then become 'imaginary'</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-1.5, 2.5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1.5, 2], showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    length_contraction_fig = create_length_contraction_animation()
    length_contraction_fig
    return create_length_contraction_animation, length_contraction_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Loophole: Warp Drives and Wormholes

        General relativity might offer loopholes. The speed limit applies to objects
        moving *through* spacetime, but spacetime itself can do whatever it wants.

        **Alcubierre Warp Drive (1994):**

        What if you don't move through space, but instead *move space itself*?

        Contract space in front of you, expand it behind you. You sit in a "warp bubble"
        locally at rest, while the bubble itself moves faster than light.

        $$ds^2 = -dt^2 + (dx - v_s(t) f(r_s) dt)^2 + dy^2 + dz^2$$

        The math works! But it requires **negative energy density**—exotic matter that
        may not exist. And it still has causality problems.

        **Wormholes:**

        A shortcut connecting distant points in spacetime. You enter here, exit there,
        having traveled less distance than light would through normal space.

        Again, requires exotic matter to keep the throat open. And again, causality issues.

        > *"The laws of physics don't forbid FTL; they just make it really, really hard
        > and probably paradoxical."*
        """
    )
    return


@app.cell
def _(go, np):
    def create_warp_bubble_animation():
        """Visualize the Alcubierre warp drive concept."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            progress = i / n_frames

            # Bubble position
            bubble_x = -3 + 6 * progress

            # Grid distortion
            x = np.linspace(-4, 4, 30)
            y = np.linspace(-2, 2, 15)
            X, Y = np.meshgrid(x, y)

            # Distort grid around bubble
            r = np.sqrt((X - bubble_x)**2 + Y**2)
            warp_strength = 1.5 * np.exp(-r**2 / 0.5)

            # Contracted in front, expanded behind
            X_warped = X.copy()
            front_mask = X > bubble_x
            back_mask = X < bubble_x
            X_warped[front_mask] -= warp_strength[front_mask] * 0.3
            X_warped[back_mask] += warp_strength[back_mask] * 0.3

            frame_data = []

            # Draw warped grid lines (horizontal)
            for j in range(len(y)):
                frame_data.append(go.Scatter(
                    x=X_warped[j, :], y=Y[j, :],
                    mode="lines",
                    line=dict(color="rgba(100, 100, 255, 0.4)", width=1),
                    showlegend=False,
                ))

            # Draw warped grid lines (vertical)
            for k in range(len(x)):
                frame_data.append(go.Scatter(
                    x=X_warped[:, k], y=Y[:, k],
                    mode="lines",
                    line=dict(color="rgba(100, 100, 255, 0.4)", width=1),
                    showlegend=False,
                ))

            # Warp bubble
            theta = np.linspace(0, 2 * np.pi, 50)
            bubble_x_pts = bubble_x + 0.4 * np.cos(theta)
            bubble_y_pts = 0.3 * np.sin(theta)

            frame_data.append(go.Scatter(
                x=bubble_x_pts, y=bubble_y_pts,
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 255, 255, 0.3)",
                line=dict(color="cyan", width=2),
                name="Warp bubble",
            ))

            # Ship in bubble
            frame_data.append(go.Scatter(
                x=[bubble_x], y=[0],
                mode="markers",
                marker=dict(size=10, color="white", symbol="diamond"),
                name="Ship (locally at rest)",
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[bubble_x + 1], y=[0.8],
                mode="text",
                text=["Space contracted →"],
                textfont=dict(size=10, color="orange"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[bubble_x - 1], y=[0.8],
                mode="text",
                text=["← Space expanded"],
                textfont=dict(size=10, color="green"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Alcubierre Warp Drive:</b> Moving Space, Not Ship<br><sub>Contract space ahead, expand behind—the ship stays locally at rest</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Space", range=[-5, 5], showgrid=False, zeroline=False),
                yaxis=dict(title="", range=[-2.5, 2.5], showgrid=False, zeroline=False,
                          showticklabels=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    warp_bubble_fig = create_warp_bubble_animation()
    warp_bubble_fig
    return create_warp_bubble_animation, warp_bubble_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Deep Dive: The Newtonian Universe

        What would a universe with a much larger $c$ actually look like? Let's explore
        the consequences systematically.

        **If $c$ were 1000× larger** (about $3 \times 10^{11}$ m/s):

        **1. Everyday life would be purely Newtonian**

        At highway speeds (30 m/s), time dilation in our universe is about 1 part in
        $10^{15}$—utterly negligible. But relativistic effects become noticeable at
        ~10% of c. With $c' = 1000c$, you'd need to travel at 10% of $c'$—that's
        $3 \times 10^{10}$ m/s, or 100× the speed of light in our universe!

        Rockets, planes, even interplanetary travel would obey Newton's laws perfectly.
        GPS satellites wouldn't need relativistic corrections.

        **2. Nuclear energy would be vastly more powerful**

        $$\begin{aligned}
        E &= mc'^2 \\
        &= m(1000c)^2 \\
        &= 10^6 \times mc^2
        \end{aligned}$$

        One kilogram of matter would contain a million times more energy! Nuclear reactors
        would be proportionally more powerful, but so would nuclear weapons. The sun would
        burn a million times faster (or be a million times smaller for the same output).

        **3. Atomic structure would change**

        The fine-structure constant $\alpha \approx 1/137$ includes $c$ in its denominator.
        With larger $c$, electromagnetic interactions would be relatively weaker compared
        to other effects. Atoms might be larger, chemistry different.

        **4. Gravity would work differently**

        Gravitational waves travel at $c$. Black hole horizons form where escape velocity
        equals $c$. With larger $c$, black holes would need to be much denser, and
        gravitational effects would propagate faster.

        *The animation below shows how physics changes in a "more Newtonian" universe.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_newtonian_universe_comparison():
        """Compare relativistic effects across different c values."""
        # Velocities in m/s (log scale)
        v_log = np.linspace(0, 11, 500)  # 1 to 10^11 m/s
        v = 10**v_log

        c_our = 3e8  # Our c

        # Gamma for our universe (use maximum to avoid sqrt of negative)
        v_ratio_our = v / c_our
        gamma_our = np.where(v_ratio_our < 0.9999,
                            1 / np.sqrt(np.maximum(1e-10, 1 - v_ratio_our**2)),
                            np.nan)

        # Gamma for c' = 10c
        c_10 = 10 * c_our
        v_ratio_10 = v / c_10
        gamma_10 = np.where(v_ratio_10 < 0.9999,
                           1 / np.sqrt(np.maximum(1e-10, 1 - v_ratio_10**2)),
                           np.nan)

        # Gamma for c' = 1000c
        c_1000 = 1000 * c_our
        v_ratio_1000 = v / c_1000
        gamma_1000 = np.where(v_ratio_1000 < 0.9999,
                             1 / np.sqrt(np.maximum(1e-10, 1 - v_ratio_1000**2)),
                             np.nan)

        fig = go.Figure()

        # Reference speeds
        reference_speeds = {
            "Airplane (300 m/s)": 300,
            "Earth orbit (8 km/s)": 8000,
            "Solar escape (42 km/s)": 42000,
            "1% of our c": 0.01 * c_our,
            "Our c": c_our,
        }

        # Our universe
        fig.add_trace(go.Scatter(
            x=v, y=gamma_our,
            mode="lines",
            line=dict(color="cyan", width=3),
            name="Our universe (c)",
        ))

        # 10x c
        fig.add_trace(go.Scatter(
            x=v, y=gamma_10,
            mode="lines",
            line=dict(color="yellow", width=3),
            name="c' = 10c",
        ))

        # 1000x c
        fig.add_trace(go.Scatter(
            x=v, y=gamma_1000,
            mode="lines",
            line=dict(color="green", width=3),
            name="c' = 1000c (Newtonian)",
        ))

        # Newtonian baseline
        fig.add_hline(y=1, line_dash="dot", line_color="white", opacity=0.5,
                     annotation_text="Newtonian (γ=1)")

        # Noticeable threshold
        fig.add_hline(y=1.1, line_dash="dash", line_color="orange", opacity=0.5,
                     annotation_text="10% time dilation")

        # Reference speed markers
        for name, speed in reference_speeds.items():
            if speed <= 1e11:
                fig.add_vline(x=speed, line_dash="dot", line_color="rgba(255,255,255,0.3)")
                fig.add_annotation(x=np.log10(speed), y=0.1, text=name,
                                  textangle=-90, font=dict(size=9, color="white"),
                                  showarrow=False, xref="x", yref="paper")

        fig.update_layout(
            title=dict(
                text="<b>The Newtonian Universe:</b> When Does Relativity Matter?<br><sub>With larger c, you can go much faster before spacetime curves</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Velocity (m/s)", type="log", range=[0, 11.5],
                      showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Lorentz factor γ", range=[0.95, 5], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    newtonian_fig = create_newtonian_universe_comparison()
    return create_newtonian_universe_comparison, newtonian_fig


@app.cell
def _(mo, newtonian_fig):
    mo.vstack(
        [
            newtonian_fig,
            mo.md(
                "**What this shows:** In our universe (cyan), relativistic effects become significant near c = 3×10⁸ m/s. With c' = 10c (yellow) or c' = 1000c (green), you could reach speeds far beyond our light limit before spacetime curvature matters. At c' = 1000c, even escaping the solar system would feel perfectly Newtonian—Newton's physics would be an excellent approximation for almost everything we'd ever want to do."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Deep Dive: The Geometric Barrier

        Why is $c$ a barrier at all? The answer lies in the **geometry of spacetime**.

        In ordinary Euclidean geometry, the distance between two points is:

        $$d^2 = \Delta x^2 + \Delta y^2 + \Delta z^2$$

        All positive terms, all adding up. A circle has the same distance from center
        to edge in all directions.

        But spacetime has a different geometry—**Minkowski geometry**:

        $$s^2 = c^2\Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$$

        That minus sign changes everything! Time and space don't add—they **subtract**.

        **What does this mean geometrically?**

        Instead of circles, we get **hyperbolas**. The "unit circle" in spacetime
        is actually two hyperbolic curves that asymptotically approach the light cone
        but never cross it.

        **The light cone ($s^2 = 0$) is geometrically special:**

        It's the boundary where the interval changes from timelike to spacelike.
        Crossing it isn't like crossing a line—it's like trying to rotate a vector
        from pointing "up" to pointing "sideways" by going through "null" (zero length).

        In Euclidean space, you can smoothly rotate any direction to any other.
        In Minkowski space, you **cannot smoothly transform** a timelike vector into
        a spacelike one. They're geometrically incompatible.

        *This is why the speed limit is geometric, not technological.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_minkowski_geometry_animation():
        """Visualize the hyperbolic geometry of spacetime."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            # Boost parameter (rapidity)
            rapidity = 2.0 * i / n_frames

            # Light cone
            x_cone = np.linspace(-3, 3, 100)
            t_cone_up = np.abs(x_cone)
            t_cone_down = -np.abs(x_cone)

            # Hyperbola of constant proper time (timelike, s² < 0)
            # -t² + x² = -1 → t² - x² = 1 → t = sqrt(1 + x²)
            x_hyp = np.linspace(-2.5, 2.5, 100)
            t_hyp_future = np.sqrt(1 + x_hyp**2)
            t_hyp_past = -np.sqrt(1 + x_hyp**2)

            # Hyperbola of constant proper distance (spacelike, s² > 0)
            # -t² + x² = 1 → x² - t² = 1 → x = sqrt(1 + t²)
            t_hyp_space = np.linspace(-2, 2, 100)
            x_hyp_right = np.sqrt(1 + t_hyp_space**2)
            x_hyp_left = -np.sqrt(1 + t_hyp_space**2)

            # A boosted observer's worldline (straight line at angle)
            # For rapidity φ: t = cosh(φ)τ, x = sinh(φ)τ
            tau = np.linspace(0, 2, 50)
            x_boosted = np.sinh(rapidity) * tau
            t_boosted = np.cosh(rapidity) * tau

            # The point on the hyperbola corresponding to proper time τ=1
            x_event = np.sinh(rapidity)
            t_event = np.cosh(rapidity)

            frame_data = [
                # Light cone
                go.Scatter(
                    x=x_cone, y=t_cone_up,
                    mode="lines",
                    line=dict(color="yellow", width=2),
                    name="Light cone (v=c)",
                ),
                go.Scatter(
                    x=x_cone, y=t_cone_down,
                    mode="lines",
                    line=dict(color="yellow", width=2),
                    showlegend=False,
                ),
                # Timelike hyperbola
                go.Scatter(
                    x=x_hyp, y=t_hyp_future,
                    mode="lines",
                    line=dict(color="cyan", width=2, dash="dash"),
                    name="Constant proper time (τ=1)",
                ),
                go.Scatter(
                    x=x_hyp, y=t_hyp_past,
                    mode="lines",
                    line=dict(color="cyan", width=2, dash="dash"),
                    showlegend=False,
                ),
                # Spacelike hyperbola
                go.Scatter(
                    x=x_hyp_right, y=t_hyp_space,
                    mode="lines",
                    line=dict(color="magenta", width=2, dash="dot"),
                    name="Constant proper distance (s=1)",
                ),
                go.Scatter(
                    x=x_hyp_left, y=t_hyp_space,
                    mode="lines",
                    line=dict(color="magenta", width=2, dash="dot"),
                    showlegend=False,
                ),
                # Boosted worldline
                go.Scatter(
                    x=x_boosted, y=t_boosted,
                    mode="lines",
                    line=dict(color="white", width=3),
                    name=f"Observer (v={np.tanh(rapidity):.2f}c)",
                ),
                # Event marker
                go.Scatter(
                    x=[x_event], y=[t_event],
                    mode="markers",
                    marker=dict(size=12, color="cyan"),
                    name="τ=1 event",
                ),
                # Origin
                go.Scatter(
                    x=[0], y=[0],
                    mode="markers",
                    marker=dict(size=8, color="white"),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Minkowski Geometry:</b> Hyperbolas, Not Circles<br><sub>The point moves along the hyperbola but never reaches the light cone</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Space (x)", range=[-4, 4], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)", zeroline=True),
                yaxis=dict(title="Time (t)", range=[-3, 4], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)", zeroline=True, scaleanchor="x"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, font=dict(size=10)),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    minkowski_fig = create_minkowski_geometry_animation()
    minkowski_fig
    return create_minkowski_geometry_animation, minkowski_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Deep Dive: Wormholes (Einstein-Rosen Bridges)

        In 1935, Einstein and Rosen discovered that the mathematics of general relativity
        allowed for "bridges" connecting distant regions of spacetime.

        **How a wormhole works:**

        Imagine spacetime as a rubber sheet. Normally, to get from point A to point B,
        you travel along the surface. But what if you could poke a hole at A, another at B,
        and connect them with a tube through the "bulk"?

        The distance through the wormhole could be much shorter than the distance along
        the surface—even if A and B are light-years apart in normal space.

        **The metric for a simple wormhole:**

        $$ds^2 = -dt^2 + dl^2 + (b^2 + l^2)(d\theta^2 + \sin^2\theta \, d\phi^2)$$

        where $b$ is the throat radius and $l$ is the proper distance through the wormhole.

        **The problem: wormholes collapse instantly**

        A Schwarzschild wormhole (connecting two black holes) pinches off faster than
        light can travel through it. You'd be crushed before reaching the other side.

        **The solution: exotic matter**

        To hold a wormhole open, you need matter with **negative energy density**—stuff
        that gravitationally repels rather than attracts. This would push the walls apart
        and keep the throat from collapsing.

        *The animation below shows how a wormhole could connect distant regions.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_wormhole_animation():
        """Visualize a wormhole connecting distant regions of spacetime."""
        n_frames = 50

        frames = []

        for i in range(n_frames):
            progress = i / n_frames

            # Create embedding diagram (2D slice of curved spacetime)
            # Two "sheets" connected by a throat

            # Radial coordinate
            r = np.linspace(0.5, 4, 40)
            theta = np.linspace(0, 2 * np.pi, 30)
            R, Theta = np.meshgrid(r, theta)

            # Embedding function: z = sqrt(r² - b²) for r > b (throat radius b)
            b = 0.5  # Throat radius
            Z_upper = np.sqrt(R**2 - b**2 + 0.01)
            Z_lower = -np.sqrt(R**2 - b**2 + 0.01)

            # Convert to Cartesian for 3D plot
            X = R * np.cos(Theta)
            Y = R * np.sin(Theta)

            # Traveler position
            if progress < 0.4:
                # Approaching from upper sheet
                traveler_r = 3 - 2.5 * (progress / 0.4)
                traveler_z = np.sqrt(max(traveler_r**2 - b**2, 0.01))
            elif progress < 0.6:
                # Through throat
                throat_progress = (progress - 0.4) / 0.2
                traveler_r = b
                traveler_z = 0.5 * (1 - 2 * throat_progress)
            else:
                # Exiting to lower sheet
                exit_progress = (progress - 0.6) / 0.4
                traveler_r = b + 2.5 * exit_progress
                traveler_z = -np.sqrt(max(traveler_r**2 - b**2, 0.01))

            traveler_angle = np.pi / 4
            traveler_x = traveler_r * np.cos(traveler_angle)
            traveler_y = traveler_r * np.sin(traveler_angle)

            frame_data = [
                # Upper sheet
                go.Surface(
                    x=X, y=Y, z=Z_upper,
                    colorscale=[[0, 'rgba(0,100,200,0.7)'], [1, 'rgba(0,200,255,0.7)']],
                    showscale=False,
                    name="Upper region",
                ),
                # Lower sheet
                go.Surface(
                    x=X, y=Y, z=Z_lower,
                    colorscale=[[0, 'rgba(200,100,0,0.7)'], [1, 'rgba(255,200,0,0.7)']],
                    showscale=False,
                    name="Lower region",
                ),
                # Traveler
                go.Scatter3d(
                    x=[traveler_x], y=[traveler_y], z=[traveler_z],
                    mode="markers",
                    marker=dict(size=8, color="white"),
                    name="Traveler",
                ),
                # Traveler trail
                go.Scatter3d(
                    x=[traveler_x * 0.9, traveler_x],
                    y=[traveler_y * 0.9, traveler_y],
                    z=[traveler_z * 1.1 if traveler_z > 0 else traveler_z * 0.9, traveler_z],
                    mode="lines",
                    line=dict(color="white", width=3),
                    showlegend=False,
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Wormhole:</b> A Shortcut Through Spacetime<br><sub>Two distant regions connected by a throat</sub>",
                    font=dict(size=16),
                ),
                scene=dict(
                    xaxis=dict(showgrid=False, showticklabels=False, title=""),
                    yaxis=dict(showgrid=False, showticklabels=False, title=""),
                    zaxis=dict(showgrid=False, showticklabels=False, title=""),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
                ),
                showlegend=False,
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 60, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
            ),
            frames=frames,
        )

        return fig

    wormhole_fig = create_wormhole_animation()
    return create_wormhole_animation, wormhole_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Deep Dive: Exotic Matter and Negative Energy

        Both warp drives and wormholes require **exotic matter**—material with negative
        energy density. This sounds like science fiction, but quantum mechanics actually
        allows for it in limited circumstances.

        **The Casimir Effect (1948):**

        Place two uncharged metal plates very close together in a vacuum. Quantum
        fluctuations create virtual particle-antiparticle pairs everywhere, but
        between the plates, only certain wavelengths "fit." This creates a pressure
        difference—the plates are pushed together.

        The region between the plates has **negative energy density** relative to the
        vacuum outside! This has been experimentally measured.

        **The problem with FTL applications:**

        1. **Scale:** The Casimir effect produces tiny amounts of negative energy.
           The Alcubierre drive would need about $-10^{64}$ kg worth—more than the
           mass of the observable universe!

        2. **Quantum inequalities:** Quantum mechanics seems to limit how much negative
           energy can exist and for how long. You can "borrow" negative energy, but
           you must "pay it back" quickly with positive energy.

        3. **Stability:** Exotic matter configurations tend to be unstable. A traversable
           wormhole might collapse the moment you try to enter it.

        **Energy requirements for warp drive:**

        | Version | Negative energy required |
        |---------|-------------------------|
        | Alcubierre (1994) | ~$10^{64}$ kg (mass of universe) |
        | Van Den Broeck (1999) | ~$10^{45}$ kg (mass of sun) |
        | Optimized (2012) | ~$10^{30}$ kg (mass of Jupiter) |
        | Theoretical minimum | Unknown, possibly small |

        Researchers have found ways to reduce the requirements, but it's still far
        beyond any foreseeable technology—and may be forbidden by deeper physics.
        """
    )
    return


@app.cell
def _(go, np):
    def create_exotic_matter_visualization():
        """Visualize the energy conditions and exotic matter."""

        # Energy density distribution for different scenarios
        x = np.linspace(-5, 5, 200)

        # Normal matter (positive everywhere)
        normal = np.exp(-x**2 / 2)

        # Casimir effect (negative between plates)
        casimir = np.where(np.abs(x) < 1, -0.3, 0) + 0.1 * np.exp(-x**2 / 4)

        # Warp bubble (negative at edges)
        warp = np.exp(-(x-2)**2 / 0.3) + np.exp(-(x+2)**2 / 0.3) - \
               0.8 * np.exp(-(x-1.5)**2 / 0.2) - 0.8 * np.exp(-(x+1.5)**2 / 0.2)

        # Wormhole throat (negative to keep it open)
        wormhole = np.exp(-x**2 / 0.5) - 1.5 * np.exp(-x**2 / 0.1)

        fig = go.Figure()

        # Normal matter
        fig.add_trace(go.Scatter(
            x=x, y=normal + 3,
            mode="lines",
            fill="tozeroy",
            line=dict(color="cyan", width=2),
            fillcolor="rgba(0, 255, 255, 0.3)",
            name="Normal matter (ρ > 0)",
        ))

        # Zero line for normal matter
        fig.add_hline(y=3, line_dash="dot", line_color="white", opacity=0.3)

        # Casimir effect
        fig.add_trace(go.Scatter(
            x=x, y=casimir + 1.5,
            mode="lines",
            fill="tozeroy",
            line=dict(color="yellow", width=2),
            fillcolor="rgba(255, 255, 0, 0.3)",
            name="Casimir effect",
        ))

        # Plates
        fig.add_vrect(x0=-1, x1=1, fillcolor="rgba(255,255,255,0.1)",
                     line_width=0, layer="below")
        fig.add_annotation(x=0, y=1.1, text="Between plates:<br>ρ < 0",
                          font=dict(color="yellow", size=10), showarrow=False)

        # Zero line for Casimir
        fig.add_hline(y=1.5, line_dash="dot", line_color="white", opacity=0.3)

        # Warp bubble
        fig.add_trace(go.Scatter(
            x=x, y=warp * 0.5,
            mode="lines",
            fill="tozeroy",
            line=dict(color="magenta", width=2),
            fillcolor="rgba(255, 0, 255, 0.3)",
            name="Warp bubble edges",
        ))

        # Zero line for warp
        fig.add_hline(y=0, line_dash="dot", line_color="white", opacity=0.3)

        # Annotations
        fig.add_annotation(x=-1.5, y=-0.4, text="Negative energy<br>(exotic matter)",
                          font=dict(color="magenta", size=10), showarrow=True,
                          arrowhead=2, ax=0, ay=-30)

        fig.update_layout(
            title=dict(
                text="<b>Exotic Matter:</b> Negative Energy Density<br><sub>Required for warp drives and wormholes</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Position", showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Energy density (offset for clarity)", showgrid=False,
                      showticklabels=False),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    exotic_matter_fig = create_exotic_matter_visualization()
    exotic_matter_fig
    return create_exotic_matter_visualization, exotic_matter_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Deep Dive: The Causality Problem

        Even if we could build a warp drive or wormhole, there's a deeper problem:
        **they can be turned into time machines**.

        **The wormhole time machine:**

        1. Create a wormhole with mouths A and B
        2. Leave mouth A stationary, accelerate mouth B to high speed and back
        3. Due to time dilation, less time passes at B than A
        4. Now the wormhole connects different times!
        5. Enter at A (2025), exit at B (2020)

        **The warp drive time machine:**

        1. Warp from Earth to a distant star at 10c (effective speed)
        2. Due to relativity of simultaneity, some observers see you arrive before you left
        3. Warp back from a reference frame where "now" at Earth is in your past
        4. Arrive at Earth before your original departure!

        **Hawking's Chronology Protection Conjecture:**

        Stephen Hawking proposed that the laws of physics conspire to prevent time machines.
        Whenever a time loop is about to form, quantum effects might cause the wormhole or
        warp bubble to be destroyed.

        The mechanism might involve:
        - Vacuum fluctuations building up around the time loop
        - Energy densities becoming infinite at the "chronology horizon"
        - Quantum gravity effects we don't yet understand

        > *"It seems there is a Chronology Protection Agency which prevents the appearance
        > of closed timelike curves and so makes the universe safe for historians."*
        > — Stephen Hawking
        """
    )
    return


@app.cell
def _(go, np):
    def create_causality_paradox_animation():
        """Visualize how warp drive could create a time loop."""
        n_frames = 50

        frames = []

        for i in range(n_frames):
            progress = i / n_frames

            frame_data = []

            # Spacetime diagram: x (space) vs t (time)
            # Earth worldline (stationary)
            frame_data.append(go.Scatter(
                x=[0, 0], y=[0, 5],
                mode="lines",
                line=dict(color="cyan", width=3),
                name="Earth",
            ))

            # Distant star worldline (stationary, 2 light-years away)
            frame_data.append(go.Scatter(
                x=[2, 2], y=[0, 5],
                mode="lines",
                line=dict(color="orange", width=3),
                name="Star (2 ly away)",
            ))

            # Light cones from origin
            frame_data.append(go.Scatter(
                x=[-5, 0, 5], y=[5, 0, 5],
                mode="lines",
                line=dict(color="yellow", width=1, dash="dash"),
                name="Light cone",
            ))

            # The paradox journey:
            # 1. Warp from Earth to star (appears FTL in Earth frame)
            # 2. Warp back in a boosted frame (appears to go backward in time)

            if progress < 0.3:
                # Depart Earth
                p = progress / 0.3
                ship_x = 0
                ship_y = p * 1
                frame_data.append(go.Scatter(
                    x=[ship_x], y=[ship_y],
                    mode="markers",
                    marker=dict(size=12, color="white", symbol="diamond"),
                    name="Ship",
                ))
            elif progress < 0.5:
                # Warp to star (FTL, nearly horizontal line)
                p = (progress - 0.3) / 0.2
                ship_x = p * 2
                ship_y = 1 + p * 0.2  # Nearly horizontal = FTL
                frame_data.append(go.Scatter(
                    x=[0, ship_x], y=[1, ship_y],
                    mode="lines",
                    line=dict(color="magenta", width=3),
                    name="Outbound (10c)",
                ))
                frame_data.append(go.Scatter(
                    x=[ship_x], y=[ship_y],
                    mode="markers",
                    marker=dict(size=12, color="white", symbol="diamond"),
                    name="Ship",
                ))
            elif progress < 0.6:
                # At star
                frame_data.append(go.Scatter(
                    x=[0, 2], y=[1, 1.2],
                    mode="lines",
                    line=dict(color="magenta", width=3),
                    name="Outbound (10c)",
                ))
                frame_data.append(go.Scatter(
                    x=[2], y=[1.2],
                    mode="markers",
                    marker=dict(size=12, color="white", symbol="diamond"),
                    name="Ship at star",
                ))
            else:
                # Return trip in boosted frame - goes backward in Earth time!
                p = (progress - 0.6) / 0.4
                ship_x = 2 - p * 2
                ship_y = 1.2 - p * 1.5  # Negative slope = backward in time!

                # Show full outbound path
                frame_data.append(go.Scatter(
                    x=[0, 2], y=[1, 1.2],
                    mode="lines",
                    line=dict(color="magenta", width=3),
                    name="Outbound (10c)",
                ))
                # Return path
                frame_data.append(go.Scatter(
                    x=[2, ship_x], y=[1.2, ship_y],
                    mode="lines",
                    line=dict(color="red", width=3),
                    name="Return (backward in time!)",
                ))
                frame_data.append(go.Scatter(
                    x=[ship_x], y=[ship_y],
                    mode="markers",
                    marker=dict(size=12, color="white", symbol="diamond"),
                    name="Ship",
                ))

                if progress > 0.95:
                    # Arrived before departure!
                    frame_data.append(go.Scatter(
                        x=[0.3], y=[0.5],
                        mode="text",
                        text=["ARRIVAL BEFORE<br>DEPARTURE!"],
                        textfont=dict(size=14, color="red"),
                        showlegend=False,
                    ))

            # Departure event marker
            frame_data.append(go.Scatter(
                x=[0], y=[1],
                mode="markers+text",
                marker=dict(size=8, color="green"),
                text=["Depart"],
                textposition="middle left",
                textfont=dict(size=10),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Causality Paradox:</b> FTL Creates Time Loops<br><sub>Warp out fast enough, return in a different frame → arrive before you left</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Space (light-years)", range=[-0.5, 3],
                          showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(title="Time (years)", range=[-0.5, 5],
                          showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, font=dict(size=10)),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 60, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    causality_paradox_fig = create_causality_paradox_animation()
    causality_paradox_fig
    return create_causality_paradox_animation, causality_paradox_fig


@app.cell
def _(mo):
    mo.accordion(
        {
            "Why do most physicists believe FTL is impossible?": mo.md(
                r"""
        Several independent lines of reasoning all point to the same conclusion:

        **1. Energy divergence:**
        The energy required to accelerate any massive object to c is infinite.
        This isn't a technological limitation—it's built into the fabric of spacetime.

        **2. Causality protection:**
        Every known FTL scheme, when analyzed carefully, leads to causal paradoxes.
        Many physicists believe there's a "chronology protection conjecture"—nature
        conspires to prevent time travel.

        **3. Quantum field theory:**
        In QFT, particles are excitations of fields. The structure of these fields
        is Lorentz-invariant, meaning c is built into the very definition of particles.
        Tachyonic fields (with imaginary mass) lead to vacuum instabilities.

        **4. Experimental evidence:**
        Despite a century of searching, no FTL phenomenon has ever been confirmed.
        Every apparent exception (quantum entanglement, phase velocities, etc.) turns
        out not to transmit information faster than light.

        **5. Consistency of physics:**
        If FTL were possible, it would unravel causality, thermodynamics, and the
        entire structure of physics. The laws we know work remarkably well—suggesting
        c really is a fundamental limit.
        """
            ),
            "What about quantum entanglement?": mo.md(
                r"""
        Quantum entanglement is often cited as "spooky action at a distance," but it
        doesn't allow FTL communication.

        When two particles are entangled and you measure one, the other's state is
        instantly determined—even if it's light-years away. This seems to violate
        relativity, but here's the catch:

        **You can't control the outcome of your measurement.**

        When Alice measures her particle, she gets a random result. Bob's particle
        instantly takes the correlated value, but Bob just sees a random result too.
        Neither can tell anything happened until they compare notes—which requires
        normal, slower-than-light communication.

        **No information travels faster than light.**

        The correlations are real and experimentally verified, but they can't be used
        to send messages. Nature is subtle: it allows "influence" without "signaling."

        This is one of the deepest mysteries of quantum mechanics, but it doesn't
        break relativity.
        """
            ),
            "Could the speed of light have been different?": mo.md(
                r"""
        This is a profound question about the nature of physical constants.

        **Option 1: c is arbitrary**
        Perhaps c could have been any value, and we just happen to live in a universe
        where it's 299,792,458 m/s. Other universes might have different values.

        **Option 2: c is necessary**
        Perhaps c emerges from deeper principles—the structure of spacetime itself—
        and couldn't be different. In this view, asking "what if c were different?"
        is like asking "what if 2+2=5?"

        **The anthropic perspective:**
        If c were very different, the universe might not support complex chemistry
        or life. Stars would burn differently, atoms would have different properties.
        We might only find ourselves in universes where c has life-compatible values.

        **The fine-structure constant:**
        What really matters isn't c alone, but dimensionless ratios like
        $\alpha = e^2/(4\pi\epsilon_0\hbar c) \approx 1/137$. This number determines
        atomic structure and chemistry. If it were significantly different, we wouldn't
        be here to ask the question.

        The fact that c has the value it does may be contingent, necessary, or selected
        by anthropic reasoning. We don't know which—yet.
        """
            ),
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Geometry of Impossibility

        | Question | Answer |
        |----------|--------|
        | Can we reach c? | No—requires infinite energy |
        | Can we exceed c? | Not by acceleration |
        | What happens at v > c? | Time/length become imaginary |
        | Do tachyons exist? | No evidence; would break causality |
        | Could c be different? | Maybe, but physics would change dramatically |
        | Are there loopholes? | Maybe (warp drives, wormholes) but require exotic matter |

        **Key insights:**

        1. **c isn't just a speed limit—it's the structure of spacetime.** It defines
           how space and time are woven together.

        2. **Everything moves through spacetime at c.** When you move through space,
           you "borrow" from your motion through time.

        3. **FTL doesn't mean "time goes backward"—it means time becomes imaginary.**
           The mathematics breaks down; ordinary concepts of cause and effect don't apply.

        4. **The barrier is geometric, not technological.** No amount of engineering
           can overcome the fundamental structure of reality.

        ---

        > *"The universe is not only queerer than we suppose, but queerer than we can suppose."*
        > — J.B.S. Haldane

        The speed of light isn't a limitation imposed from outside—it's a feature of
        spacetime itself. To ask "why can't we go faster?" is to ask "why is space space
        and time time?" These are the deepest questions in physics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References

        ### Feynman Lectures (Background)

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1963). *The Feynman Lectures on Physics, Volume I*.
          Addison-Wesley.
          - [Chapter 15: The Special Theory of Relativity](https://www.feynmanlectures.caltech.edu/I_15.html)
          - [Chapter 16: Relativistic Energy and Momentum](https://www.feynmanlectures.caltech.edu/I_16.html)
          - [Chapter 17: Space-Time](https://www.feynmanlectures.caltech.edu/I_17.html)

        ### Special Relativity

        - **Einstein, A.** (1905). "Zur Elektrodynamik bewegter Körper".
          Annalen der Physik, 17, 891-921.

        - **Minkowski, H.** (1908). Introduced 4D spacetime geometry.
          - Metric: $ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2$
          - Hyperbolic geometry of velocity addition

        ### Tachyons

        - **Bilaniuk, O.-M. P., Deshpande, V. K., & Sudarshan, E. C. G.** (1962).
          "'Meta' Relativity". American Journal of Physics, 30, 718.
          - First serious theoretical treatment of faster-than-light particles

        - **Feinberg, G.** (1967). "Possibility of Faster-Than-Light Particles".
          Physical Review, 159, 1089.
          - Named "tachyons" (from Greek *tachys*, swift)

        ### Wormholes

        - **Einstein, A. & Rosen, N.** (1935). "The Particle Problem in the General Theory of Relativity".
          Physical Review, 48, 73.
          - Original "Einstein-Rosen bridge" paper

        - **Morris, M. S. & Thorne, K. S.** (1988). "Wormholes in spacetime and their use for interstellar travel".
          American Journal of Physics, 56, 395.
          - Traversable wormhole requirements

        ### Warp Drives

        - **Alcubierre, M.** (1994). "The warp drive: hyper-fast travel within general relativity".
          Classical and Quantum Gravity, 11, L73.
          - Original Alcubierre metric paper

        ### Causality

        - **Hawking, S. W.** (1992). "Chronology protection conjecture".
          Physical Review D, 46, 603.
          - Why physics may forbid time machines

        ### Further Reading

        - Thorne, K. S. *Black Holes and Time Warps* — Popular science
        - Visser, M. *Lorentzian Wormholes: From Einstein to Hawking* — Technical treatment
        - Taylor, E. F. & Wheeler, J. A. *Spacetime Physics* — Special relativity foundations
        """
    )
    return


if __name__ == "__main__":
    app.run()
