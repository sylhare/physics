import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from physics_explorations.visualization import (
        COLORS,
        create_play_pause_buttons,
    )

    return COLORS, create_play_pause_buttons, go, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # The Fabric of Spacetime

        *An interactive exploration based on [Feynman Lectures on Physics, Chapters 15-17](https://www.feynmanlectures.caltech.edu/)*

        ---

        ## The Revolution of 1905

        In 1905, a 26-year-old patent clerk named Albert Einstein published a paper that
        would overturn 200 years of Newtonian physics. The paper's title was unassuming:
        *"On the Electrodynamics of Moving Bodies"*—but its consequences were revolutionary.

        Einstein started with two simple postulates:

        **1. The Principle of Relativity:**
        > The laws of physics are the same in all inertial (non-accelerating) reference frames.

        **2. The Constancy of Light Speed:**
        > The speed of light in vacuum is the same for all observers, regardless of their motion.

        The first postulate was already accepted—Newton would have agreed. The second was
        the bombshell. It seems to contradict everyday experience: if you're moving toward
        a light source, shouldn't you measure the light moving faster?

        **The answer is no.** And the consequences shake the foundations of space and time.

        To preserve the constancy of $c$, we must abandon:
        - Absolute time (clocks tick at different rates!)
        - Absolute space (lengths depend on motion!)
        - Absolute simultaneity (events can be simultaneous in one frame but not another!)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Time Dilation: Moving Clocks Run Slow

        The most startling consequence of Einstein's postulates is **time dilation**:
        a moving clock runs slower than a stationary one.

        **The light clock thought experiment:**

        Imagine a "clock" made of two mirrors with a light pulse bouncing between them.
        Each bounce is one "tick." This clock measures time by counting light bounces.

        Now imagine this clock is moving sideways. For a stationary observer:
        - The light must travel a *diagonal* path (longer than vertical)
        - But light still travels at speed $c$
        - Therefore, each tick takes *longer* for the stationary observer!

        **The math:**

        If the clock moves at velocity $v$, the time dilation factor is:

        $$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$

        A clock moving at velocity $v$ runs slower by factor $\gamma$:

        $$\Delta t_{moving} = \gamma \cdot \Delta t_{rest}$$

        At $v = 0.6c$: $\gamma = 1.25$ → Moving clock runs 25% slower
        At $v = 0.9c$: $\gamma = 2.29$ → Moving clock runs 2.3× slower
        At $v = 0.99c$: $\gamma = 7.09$ → Moving clock runs 7× slower!

        *The animation below shows the light clock thought experiment. Watch how the light
        path is longer in the "stationary" frame!*
        """
    )
    return


@app.cell
def _(go, np):
    def create_light_clock_animation():
        """Animate the light clock thought experiment showing time dilation."""
        n_frames = 60
        velocity = 0.5  # v/c

        # Gamma factor
        gamma = 1 / np.sqrt(1 - velocity**2)

        frames = []

        clock_height = 2.0  # Distance between mirrors

        for i in range(n_frames):
            t = i / n_frames

            # === Rest frame clock (left side) ===
            # Light bounces up and down
            rest_cycle = (2 * t) % 1  # Complete cycle
            if rest_cycle < 0.5:
                rest_light_y = rest_cycle * 2 * clock_height
            else:
                rest_light_y = (1 - rest_cycle) * 2 * clock_height

            # === Moving frame clock (right side) ===
            # Clock moves to the right
            move_x_offset = 4 + velocity * t * 4  # Moving position

            # Light takes diagonal path - slower apparent rate
            move_cycle = (2 * t / gamma) % 1
            if move_cycle < 0.5:
                move_light_y = move_cycle * 2 * clock_height
                move_light_x = move_x_offset + velocity * (move_cycle * gamma) * 2
            else:
                move_light_y = (1 - move_cycle) * 2 * clock_height
                move_light_x = move_x_offset + velocity * ((move_cycle - 0.5) * gamma + 0.5 * gamma) * 2

            # Rest frame elements
            frame_data = [
                # Rest clock mirrors
                go.Scatter(x=[-0.3, 0.3], y=[0, 0], mode="lines",
                          line=dict(color="silver", width=8), name="Bottom mirror (rest)"),
                go.Scatter(x=[-0.3, 0.3], y=[clock_height, clock_height], mode="lines",
                          line=dict(color="silver", width=8), name="Top mirror (rest)"),
                # Rest light pulse
                go.Scatter(x=[0], y=[rest_light_y], mode="markers",
                          marker=dict(size=15, color="yellow"), name="Light (rest frame)"),
                # Rest clock label
                go.Scatter(x=[0], y=[-0.5], mode="text",
                          text=["REST CLOCK"], textfont=dict(size=12)),

                # Moving clock mirrors (at current position)
                go.Scatter(x=[move_x_offset - 0.3, move_x_offset + 0.3], y=[0, 0], mode="lines",
                          line=dict(color="lightblue", width=8), name="Bottom mirror (moving)"),
                go.Scatter(x=[move_x_offset - 0.3, move_x_offset + 0.3], y=[clock_height, clock_height], mode="lines",
                          line=dict(color="lightblue", width=8), name="Top mirror (moving)"),
                # Moving light pulse
                go.Scatter(x=[move_light_x], y=[move_light_y], mode="markers",
                          marker=dict(size=15, color="cyan"), name="Light (moving frame)"),
                # Show diagonal path
                go.Scatter(x=[move_x_offset, move_light_x], y=[0, move_light_y], mode="lines",
                          line=dict(color="cyan", width=1, dash="dash"), name="Light path"),
                # Moving clock label
                go.Scatter(x=[move_x_offset], y=[-0.5], mode="text",
                          text=[f"MOVING at {velocity}c"], textfont=dict(size=12)),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text=f"<b>Light Clock:</b> Time Dilation Visualized (v = {velocity}c, γ = {gamma:.2f})<br><sub>Moving clock ticks slower because light travels a longer diagonal path</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-1.5, 10], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1, 3], scaleanchor="x", showgrid=False, zeroline=False, showticklabels=False),
                showlegend=False,
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.1,
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
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    light_clock_fig = create_light_clock_animation()
    light_clock_fig
    return (create_light_clock_animation, light_clock_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Gamma Factor: Gateway to Relativity

        The factor $\gamma$ (gamma) appears everywhere in special relativity:

        $$\begin{aligned}
        \gamma &= \frac{1}{\sqrt{1 - v^2/c^2}} \\
        &= \frac{1}{\sqrt{1 - \beta^2}}
        \end{aligned}$$

        where $\beta = v/c$ is velocity as a fraction of light speed.

        **Properties of gamma:**

        | Velocity ($v/c$) | $\gamma$ | Effect |
        |------------------|----------|--------|
        | 0 | 1.000 | No relativistic effects |
        | 0.1 | 1.005 | 0.5% effect |
        | 0.5 | 1.155 | 15% slower clocks |
        | 0.9 | 2.294 | Clocks run 2.3× slower |
        | 0.99 | 7.089 | Clocks run 7× slower |
        | 0.999 | 22.37 | Clocks run 22× slower |
        | 0.9999 | 70.71 | Clocks run 71× slower |

        **Key insight:** Relativistic effects are negligible at everyday speeds but become
        dramatic as $v \to c$. At $v = c$, gamma becomes infinite—which is why nothing
        with mass can reach light speed.

        *The interactive plot below shows how gamma grows. Use the slider to explore!*
        """
    )
    return


@app.cell
def _(mo):
    velocity_slider = mo.ui.slider(
        start=0,
        stop=0.99,
        step=0.01,
        value=0.5,
        label="Velocity (v/c)",
        show_value=True,
    )
    mo.hstack([mo.md("**Set velocity as fraction of light speed:**"), velocity_slider], justify="start", gap=1)
    return (velocity_slider,)


@app.cell
def _(go, np, velocity_slider):
    v = velocity_slider.value
    if v >= 1:
        v = 0.999
    gamma_val = 1 / np.sqrt(1 - v**2)

    # Plot gamma vs velocity
    velocities = np.linspace(0, 0.99, 100)
    gammas = 1 / np.sqrt(1 - velocities**2)

    gamma_fig = go.Figure()

    # Gamma curve
    gamma_fig.add_trace(go.Scatter(
        x=velocities,
        y=gammas,
        mode="lines",
        line=dict(color="steelblue", width=3),
        name="γ(v)"
    ))

    # Current point
    gamma_fig.add_trace(go.Scatter(
        x=[v],
        y=[gamma_val],
        mode="markers",
        marker=dict(size=15, color="red"),
        name=f"Current: γ = {gamma_val:.3f}"
    ))

    gamma_fig.update_layout(
        title=dict(
            text=f"<b>The Gamma Factor</b><br><sub>At v = {v}c: γ = {gamma_val:.3f} → clocks run {gamma_val:.2f}× slower, lengths contract to {1/gamma_val:.2%}</sub>",
            font=dict(size=16),
        ),
        xaxis_title="Velocity (v/c)",
        yaxis_title="Gamma (γ)",
        yaxis=dict(range=[0, 10]),
        showlegend=True,
    )

    gamma_fig
    return gamma_fig, gamma_val, gammas, v, velocities


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Length Contraction: Moving Objects Shrink

        If time dilates, what about space? Einstein showed that lengths in the direction
        of motion **contract**:

        $$\begin{aligned}
        L_{moving} &= \frac{L_{rest}}{\gamma} \\
        &= L_{rest}\sqrt{1 - v^2/c^2}
        \end{aligned}$$

        A meter stick moving at $v = 0.9c$ appears only 44 cm long to a stationary observer!

        **The key insight:** This isn't an optical illusion or mechanical compression.
        The object really *is* shorter in that reference frame. But here's the twist:
        an observer moving with the object sees it as normal length—and sees *you* as
        contracted!

        **Who's right?** Both observers are correct in their own reference frames.
        There is no absolute "true length"—length depends on relative motion.

        *The animation below shows a spaceship moving at different velocities.
        Watch how it contracts in the direction of motion!*
        """
    )
    return


@app.cell
def _(go, np):
    def create_length_contraction_animation():
        """Animate length contraction of a spaceship."""
        n_frames = 60

        # Spaceship shape (at rest)
        ship_length = 2.0
        ship_height = 0.5

        frames = []

        for i in range(n_frames):
            # Velocity oscillates
            t = i / n_frames
            v = 0.8 * np.sin(2 * np.pi * t)  # Oscillate between -0.8c and +0.8c

            if abs(v) > 0.01:
                gamma = 1 / np.sqrt(1 - v**2)
                contracted_length = ship_length / gamma
            else:
                gamma = 1
                contracted_length = ship_length

            # Ship shape (contracted in x)
            ship_x = [-contracted_length/2, contracted_length/2, contracted_length/2,
                      contracted_length/2 + 0.3, contracted_length/2, contracted_length/2,
                      -contracted_length/2, -contracted_length/2]
            ship_y = [-ship_height/2, -ship_height/2, -ship_height/4,
                      0, ship_height/4, ship_height/2,
                      ship_height/2, -ship_height/2]

            # Reference grid
            grid_x = []
            grid_y = []
            for gx in np.arange(-3, 4, 0.5):
                grid_x.extend([gx, gx, None])
                grid_y.extend([-1.5, 1.5, None])

            frame_data = [
                # Reference grid
                go.Scatter(x=grid_x, y=grid_y, mode="lines",
                          line=dict(color="rgba(100,100,100,0.3)", width=1),
                          name="Reference grid"),
                # Spaceship
                go.Scatter(x=ship_x, y=ship_y, mode="lines", fill="toself",
                          fillcolor="rgba(100,150,255,0.5)",
                          line=dict(color="steelblue", width=2),
                          name=f"Spaceship (L = {contracted_length:.2f})"),
                # Velocity indicator
                go.Scatter(x=[0], y=[-1.2], mode="text",
                          text=[f"v = {v:.2f}c, γ = {gamma:.2f}"],
                          textfont=dict(size=14)),
                # Rest length reference
                go.Scatter(x=[-ship_length/2, ship_length/2], y=[1.0, 1.0], mode="lines",
                          line=dict(color="red", width=2, dash="dash"),
                          name=f"Rest length = {ship_length}"),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Length Contraction:</b> Moving Objects Shrink<br><sub>Red dashed line shows rest length; ship contracts at high velocity</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False),
                yaxis=dict(range=[-1.5, 1.5], scaleanchor="x", showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.1,
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
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    contraction_fig = create_length_contraction_animation()
    contraction_fig
    return (contraction_fig, create_length_contraction_animation)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Relativity of Simultaneity

        Perhaps the most mind-bending consequence: **events that are simultaneous in one
        frame may not be simultaneous in another**.

        **Einstein's train thought experiment:**

        Imagine a train moving at high speed. Lightning strikes both ends of the train
        simultaneously (in the ground frame). A person standing exactly in the middle
        of the platform sees both flashes at the same time.

        But what about a passenger in the middle of the train?

        - The train is moving *toward* the light from the front strike
        - The train is moving *away* from the light from the rear strike
        - Since light speed is constant, the passenger sees the front flash *first*!

        For the train passenger, the front strike happened *before* the rear strike.
        Neither observer is wrong—simultaneity is relative.

        **The profound implication:**

        There is no universal "now" that everyone agrees on. What is "now" for you may
        be "past" or "future" for someone moving relative to you. This isn't a failure
        of clocks—it's a fundamental feature of spacetime.

        *The animation below shows the train thought experiment.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_simultaneity_animation():
        """Animate the relativity of simultaneity with Einstein's train."""
        n_frames = 60

        frames = []
        train_length = 4.0
        train_velocity = 0.5

        for i in range(n_frames):
            t = i / n_frames * 2 - 0.5  # Time from -0.5 to 1.5

            # Train position
            train_x = train_velocity * t * 3

            # Lightning strikes at t=0 at both ends (in ground frame)
            if t >= 0:
                # Light expands from both ends
                light_radius = t * 3  # Light expansion (c = 1 for simplicity scaled)

                # Front light
                front_strike_x = train_length / 2
                front_light_left = max(front_strike_x - light_radius, -5)
                front_light_right = min(front_strike_x + light_radius, 5)

                # Rear light
                rear_strike_x = -train_length / 2
                rear_light_left = max(rear_strike_x - light_radius, -5)
                rear_light_right = min(rear_strike_x + light_radius, 5)
            else:
                front_light_left = front_light_right = train_length / 2
                rear_light_left = rear_light_right = -train_length / 2

            # Train observer position (moves with train)
            observer_x = train_x

            # Ground observer (stationary at center)
            ground_observer_x = 0

            frame_data = [
                # Ground (platform)
                go.Scatter(x=[-5, 5], y=[-0.3, -0.3], mode="lines",
                          line=dict(color="gray", width=10), name="Platform"),

                # Train
                go.Scatter(x=[train_x - train_length/2, train_x + train_length/2,
                             train_x + train_length/2, train_x - train_length/2,
                             train_x - train_length/2],
                          y=[0.1, 0.1, 0.6, 0.6, 0.1], mode="lines", fill="toself",
                          fillcolor="rgba(100,150,200,0.5)",
                          line=dict(color="steelblue", width=2), name="Train"),

                # Train observer
                go.Scatter(x=[observer_x], y=[0.35], mode="markers",
                          marker=dict(size=15, color="blue", symbol="circle"),
                          name="Train observer"),

                # Ground observer
                go.Scatter(x=[ground_observer_x], y=[-0.5], mode="markers",
                          marker=dict(size=15, color="green", symbol="circle"),
                          name="Ground observer"),

                # Lightning strike points (fixed in ground frame)
                go.Scatter(x=[train_length/2, -train_length/2], y=[0.8, 0.8], mode="markers",
                          marker=dict(size=10, color="yellow", symbol="star"),
                          name="Strike points"),
            ]

            # Add light waves after t=0
            if t >= 0:
                # Front light wave
                frame_data.append(go.Scatter(
                    x=[front_light_left, front_light_right],
                    y=[0.35, 0.35], mode="lines",
                    line=dict(color="yellow", width=4),
                    name="Light from front"
                ))
                # Rear light wave
                frame_data.append(go.Scatter(
                    x=[rear_light_left, rear_light_right],
                    y=[0.35, 0.35], mode="lines",
                    line=dict(color="orange", width=4),
                    name="Light from rear"
                ))

            # Check if light has reached observers
            if t >= 0:
                front_reached_train = observer_x <= front_strike_x + light_radius and observer_x >= front_strike_x - light_radius
                rear_reached_train = observer_x <= rear_strike_x + light_radius and observer_x >= rear_strike_x - light_radius

                status = []
                if front_reached_train and rear_reached_train:
                    status.append("Train observer: Both reached")
                elif front_reached_train:
                    status.append("Train observer: Front first!")
                elif rear_reached_train:
                    status.append("Train observer: Rear first!")

                if abs(ground_observer_x - front_strike_x) <= light_radius and abs(ground_observer_x - rear_strike_x) <= light_radius:
                    status.append("Ground observer: Simultaneous!")

                if status:
                    frame_data.append(go.Scatter(
                        x=[0], y=[1.2], mode="text",
                        text=["<br>".join(status)],
                        textfont=dict(size=12)
                    ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Relativity of Simultaneity:</b> Einstein's Train<br><sub>Lightning strikes both ends simultaneously in ground frame—but not for train observer!</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1, 1.5], showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=9)),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.1,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 100, "redraw": True},
                                            "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate"}]),
                            dict(label="↺ Reset",
                                 method="animate",
                                 args=[["0"], {"frame": {"duration": 0, "redraw": True},
                                              "mode": "immediate"}]),
                        ],
                    )
                ],
                margin=dict(b=60),
            ),
            frames=frames,
        )

        return fig

    simultaneity_fig = create_simultaneity_animation()
    simultaneity_fig
    return (create_simultaneity_animation, simultaneity_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Spacetime Diagrams: Visualizing Relativity

        **Minkowski spacetime** combines space and time into a single geometric structure.
        In a spacetime diagram:

        - **Vertical axis:** Time (usually $ct$ so both axes have units of distance)
        - **Horizontal axis:** Space (one dimension)
        - **World lines:** The path an object traces through spacetime
        - **Light cones:** The boundary of what can causally affect or be affected by an event

        **Key features:**

        - A stationary object traces a vertical line (moving through time, not space)
        - Light rays travel at 45° angles (since $c = 1$ in natural units)
        - The **light cone** divides spacetime into past, future, and "elsewhere"
        - Events outside your light cone cannot affect you (faster-than-light communication is impossible)

        *The interactive diagram below shows spacetime structure.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_spacetime_diagram():
        """Create an interactive spacetime diagram."""
        # Light cone
        t_future = np.linspace(0, 3, 50)
        t_past = np.linspace(-3, 0, 50)

        # Future light cone
        future_right_x = t_future
        future_right_t = t_future
        future_left_x = -t_future
        future_left_t = t_future

        # Past light cone
        past_right_x = -t_past
        past_right_t = t_past
        past_left_x = t_past
        past_left_t = t_past

        fig = go.Figure()

        # Elsewhere regions (shaded)
        fig.add_trace(go.Scatter(
            x=[-4, 0, -4, -4],
            y=[0, 0, 4, 0],
            fill="toself",
            fillcolor="rgba(150,150,150,0.2)",
            line=dict(width=0),
            name="Elsewhere (spacelike)",
            hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=[4, 0, 4, 4],
            y=[0, 0, 4, 0],
            fill="toself",
            fillcolor="rgba(150,150,150,0.2)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=[-4, 0, -4, -4],
            y=[0, 0, -4, 0],
            fill="toself",
            fillcolor="rgba(150,150,150,0.2)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=[4, 0, 4, 4],
            y=[0, 0, -4, 0],
            fill="toself",
            fillcolor="rgba(150,150,150,0.2)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Future light cone
        fig.add_trace(go.Scatter(
            x=np.concatenate([future_right_x, future_left_x[::-1]]),
            y=np.concatenate([future_right_t, future_left_t[::-1]]),
            fill="toself",
            fillcolor="rgba(255,200,100,0.3)",
            line=dict(color="orange", width=2),
            name="Future light cone"
        ))

        # Past light cone
        fig.add_trace(go.Scatter(
            x=np.concatenate([past_right_x, past_left_x[::-1]]),
            y=np.concatenate([past_right_t, past_left_t[::-1]]),
            fill="toself",
            fillcolor="rgba(100,150,255,0.3)",
            line=dict(color="blue", width=2),
            name="Past light cone"
        ))

        # Light rays (45° lines)
        fig.add_trace(go.Scatter(
            x=[-3, 3], y=[-3, 3], mode="lines",
            line=dict(color="yellow", width=2, dash="dash"),
            name="Light ray"
        ))
        fig.add_trace(go.Scatter(
            x=[3, -3], y=[-3, 3], mode="lines",
            line=dict(color="yellow", width=2, dash="dash"),
            showlegend=False
        ))

        # World line of stationary observer
        fig.add_trace(go.Scatter(
            x=[0, 0], y=[-3, 3], mode="lines",
            line=dict(color="white", width=3),
            name="Stationary observer"
        ))

        # World line of moving observer (v = 0.5c)
        v = 0.5
        fig.add_trace(go.Scatter(
            x=[-1.5, 1.5], y=[-3, 3], mode="lines",
            line=dict(color="cyan", width=3),
            name=f"Moving observer (v={v}c)"
        ))

        # Origin event
        fig.add_trace(go.Scatter(
            x=[0], y=[0], mode="markers",
            marker=dict(size=12, color="red"),
            name="Event (here, now)"
        ))

        # Labels
        fig.add_annotation(x=0, y=2.5, text="FUTURE", showarrow=False, font=dict(size=14, color="orange"))
        fig.add_annotation(x=0, y=-2.5, text="PAST", showarrow=False, font=dict(size=14, color="blue"))
        fig.add_annotation(x=2.5, y=0, text="ELSEWHERE", showarrow=False, font=dict(size=12, color="gray"))
        fig.add_annotation(x=-2.5, y=0, text="ELSEWHERE", showarrow=False, font=dict(size=12, color="gray"))

        fig.update_layout(
            title=dict(
                text="<b>Spacetime Diagram:</b> Light Cones and Causality<br><sub>Only events inside your light cone can affect you or be affected by you</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Space (x)", range=[-4, 4], zeroline=True, zerolinecolor="white", zerolinewidth=1),
            yaxis=dict(title="Time (ct)", range=[-4, 4], zeroline=True, zerolinecolor="white", zerolinewidth=1, scaleanchor="x"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=9)),
            plot_bgcolor="rgba(0,0,30,0.9)",
        )

        return fig

    spacetime_fig = create_spacetime_diagram()
    spacetime_fig
    return (create_spacetime_diagram, spacetime_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Spacetime Interval: What Everyone Agrees On

        In ordinary geometry, the distance between two points is invariant—everyone measures
        the same distance regardless of how they orient their axes.

        In spacetime, the analogous invariant is the **spacetime interval**:

        $$s^2 = c^2\Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$$

        or in one spatial dimension:

        $$s^2 = c^2\Delta t^2 - \Delta x^2$$

        **The remarkable fact:** While different observers disagree about $\Delta t$ and
        $\Delta x$ separately, they all agree on $s^2$!

        **Three types of intervals:**

        | Interval | Condition | Physical meaning |
        |----------|-----------|------------------|
        | **Timelike** ($s^2 > 0$) | Time separation dominates | Events can be causally connected |
        | **Spacelike** ($s^2 < 0$) | Space separation dominates | Events cannot influence each other |
        | **Lightlike** ($s^2 = 0$) | On the light cone | Connected by a light signal |

        For timelike intervals, the **proper time** $\tau$ (time measured by a clock traveling
        between the events) is:

        $$\begin{aligned}
        \tau &= \frac{s}{c} \\
        &= \sqrt{\Delta t^2 - \Delta x^2/c^2}
        \end{aligned}$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## E = mc²: Mass-Energy Equivalence

        Einstein's most famous equation emerges naturally from special relativity.
        The total energy of a particle is:

        $$\begin{aligned}
        E &= \gamma mc^2 \\
        &= \frac{mc^2}{\sqrt{1 - v^2/c^2}}
        \end{aligned}$$

        At rest ($v = 0$, $\gamma = 1$):

        $$E_0 = mc^2$$

        This is the **rest energy**—energy stored in mass itself. A 1 kg object contains:

        $$\begin{aligned}
        E &= (1 \text{ kg})(3 \times 10^8 \text{ m/s})^2 \\
        &= 9 \times 10^{16} \text{ J}
        \end{aligned}$$

        That's equivalent to about 21 megatons of TNT—from a single kilogram!

        **The kinetic energy** is the excess over rest energy:

        $$\begin{aligned}
        KE &= E - E_0 \\
        &= (\gamma - 1)mc^2
        \end{aligned}$$

        At low speeds, this reduces to the familiar $KE = \frac{1}{2}mv^2$.

        **The full energy-momentum relation:**

        $$E^2 = (pc)^2 + (mc^2)^2$$

        For massless particles (like photons): $E = pc$
        For particles at rest: $E = mc^2$
        """
    )
    return


@app.cell
def _(go, np):
    # E vs v showing rest energy and kinetic energy
    v_range = np.linspace(0, 0.99, 100)
    gamma_range = 1 / np.sqrt(1 - v_range**2)

    # Normalize to rest mass energy
    total_energy = gamma_range  # E/mc²
    kinetic_energy = gamma_range - 1  # KE/mc²
    rest_energy = np.ones_like(v_range)  # E₀/mc² = 1

    # Classical kinetic energy for comparison (normalized)
    classical_ke = 0.5 * v_range**2  # ½v²/c² (normalized)

    energy_fig = go.Figure()

    # Rest energy
    energy_fig.add_trace(go.Scatter(
        x=v_range, y=rest_energy,
        mode="lines", fill="tozeroy",
        fillcolor="rgba(100,100,255,0.3)",
        line=dict(color="blue", width=2),
        name="Rest energy (mc²)"
    ))

    # Total energy
    energy_fig.add_trace(go.Scatter(
        x=v_range, y=total_energy,
        mode="lines",
        line=dict(color="red", width=3),
        name="Total energy (γmc²)"
    ))

    # Classical KE for comparison
    energy_fig.add_trace(go.Scatter(
        x=v_range, y=1 + classical_ke,
        mode="lines",
        line=dict(color="green", width=2, dash="dash"),
        name="Classical prediction"
    ))

    energy_fig.update_layout(
        title=dict(
            text="<b>E = γmc²:</b> Energy vs Velocity<br><sub>Energy approaches infinity as v→c (blue = rest energy, gap = kinetic energy)</sub>",
            font=dict(size=16),
        ),
        xaxis_title="Velocity (v/c)",
        yaxis_title="Energy (units of mc²)",
        yaxis=dict(range=[0, 8]),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )

    energy_fig
    return (
        classical_ke,
        energy_fig,
        gamma_range,
        kinetic_energy,
        rest_energy,
        total_energy,
        v_range,
    )


@app.cell
def _(mo):
    mo.accordion(
        {
            "Why can't anything reach the speed of light?": mo.md(
                r"""
        The energy equation $E = \gamma mc^2$ provides the answer:

        As $v \to c$, $\gamma \to \infty$, so $E \to \infty$.

        **It would take infinite energy to accelerate any massive object to light speed.**

        This isn't just a practical limitation—it's a fundamental law of nature. No matter
        how much energy you add, you can get closer and closer to $c$ but never reach it.

        **What about massless particles?**

        Photons and gravitational waves travel at exactly $c$—but they're massless and *always*
        travel at $c$. They can't slow down! For massless particles, the energy-momentum
        relation gives $E = pc$, which works at any energy without requiring $v < c$.

        **The cosmic speed limit:**

        The speed $c$ isn't just "how fast light happens to travel"—it's the speed of causality,
        the maximum speed at which any information or influence can propagate through spacetime.
        It appears in the structure of spacetime itself.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The New View of Space and Time

        Einstein's special relativity replaces Newton's absolute space and time with a
        unified **spacetime** where:

        | Newtonian View | Relativistic View |
        |----------------|-------------------|
        | Time is absolute | Time is relative (dilates with motion) |
        | Space is absolute | Space is relative (contracts with motion) |
        | Simultaneity is absolute | Simultaneity is relative |
        | Velocities add simply | Velocities add via Lorentz formula |
        | Mass is constant | Relativistic mass increases with speed |
        | $E = \frac{1}{2}mv^2$ | $E = \gamma mc^2$ |

        **The key equations:**

        $$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$

        $$\Delta t' = \gamma \Delta t$$ (time dilation)

        $$L' = L/\gamma$$ (length contraction)

        $$s^2 = c^2\Delta t^2 - \Delta x^2$$ (invariant interval)

        $$E = \gamma mc^2$$ (total energy)

        $$E^2 = (pc)^2 + (mc^2)^2$$ (energy-momentum relation)

        ---

        > *"The distinction between past, present, and future is only a stubbornly persistent
        > illusion."* — Albert Einstein

        Space and time are not the fixed stage on which physics plays out—they are dynamic,
        interwoven, and depend on the observer's motion. The speed of light isn't just a number;
        it's the thread that stitches space and time into the fabric of spacetime.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References

        ### Primary Sources

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1963). *The Feynman Lectures on Physics, Volume I*.
          Addison-Wesley.
          - [Chapter 15: The Special Theory of Relativity](https://www.feynmanlectures.caltech.edu/I_15.html)
          - [Chapter 16: Relativistic Energy and Momentum](https://www.feynmanlectures.caltech.edu/I_16.html)
          - [Chapter 17: Space-Time](https://www.feynmanlectures.caltech.edu/I_17.html)

        ### Mathematical Background

        - **Lorentz Transformation** (1904)
          - $t' = \gamma(t - vx/c^2)$, $x' = \gamma(x - vt)$
          - Lorentz factor: $\gamma = 1/\sqrt{1 - v^2/c^2}$

        - **Time Dilation**: $\Delta t' = \gamma \Delta t$
          - Moving clocks run slow by factor $\gamma$
          - Experimentally confirmed with muon decay, GPS satellites

        - **Length Contraction**: $L' = L/\gamma$
          - Moving objects contract along direction of motion

        - **Spacetime Interval** (invariant):
          - $s^2 = c^2\Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$
          - Timelike ($s^2 > 0$), spacelike ($s^2 < 0$), lightlike ($s^2 = 0$)

        - **Mass-Energy Equivalence** (Einstein, 1905)
          - $E = mc^2$ (rest energy)
          - $E = \gamma mc^2$ (total energy)
          - $E^2 = (pc)^2 + (mc^2)^2$ (energy-momentum relation)

        ### Original Papers

        - Einstein, A. (1905). "Zur Elektrodynamik bewegter Körper" (*On the Electrodynamics of Moving Bodies*).
          Annalen der Physik, 17, 891-921.
        - Minkowski, H. (1908). "Die Grundgleichungen für die elektromagnetischen Vorgänge in bewegten Körpern".
          This work introduced the concept of 4-dimensional spacetime.

        ### Further Reading

        - Taylor, E. F. & Wheeler, J. A. *Spacetime Physics* — Excellent introduction
        - Rindler, W. *Introduction to Special Relativity* — More mathematical treatment
        """
    )
    return


if __name__ == "__main__":
    app.run()
