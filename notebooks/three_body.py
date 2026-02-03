import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from physics_explorations.visualization import (
        COLORS,
        ANIMATION_SETTINGS,
        create_play_pause_buttons,
    )

    return ANIMATION_SETTINGS, COLORS, create_play_pause_buttons, go, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # The Three-Body Problem

        *An exploration of chaos, civilization, and the limits of prediction*

        ---

        ## A Story of Survival

        In Liu Cixin's acclaimed science fiction novel *The Three-Body Problem*, humanity
        makes contact with an alien civilization from a planet called Trisolaris. But Trisolaris
        is no ordinary world—it orbits in a system with **three suns**.

        The Trisolarans face an existential nightmare. Their planet's orbit is governed by
        the gravitational dance of three stars, creating a world of terrifying unpredictability:

        - **Stable Eras**: Brief periods when the planet settles into a predictable orbit
          around one sun. Civilization flourishes. Agriculture develops. Science advances.

        - **Chaotic Eras**: Without warning, the gravitational influence of the other suns
          disrupts the orbit. The planet might swing close to a sun (scorching everything)
          or drift far away (freezing the world). Civilizations collapse and must restart.

        The Trisolarans have risen and fallen nearly 200 times over millions of years,
        desperately trying to predict when chaos will strike. But here's the devastating
        truth they eventually discover: **it cannot be predicted**.

        Not because their mathematics is insufficient. Not because their computers are too slow.
        But because the three-body problem is fundamentally **chaotic**—tiny differences in
        initial conditions lead to wildly different outcomes.

        *This is not science fiction. This is real physics.*

        Let's explore why.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## What Is the Three-Body Problem?

        The **three-body problem** asks a deceptively simple question:

        > Given three masses moving under their mutual gravitational attraction,
        > can we predict their positions at any future time?

        For **two bodies**, the answer is yes! Newton solved this completely. Two objects
        orbiting each other follow perfect ellipses, forever. We can predict where Earth
        will be a million years from now with extraordinary precision.

        But add just **one more body**, and something strange happens: the problem becomes
        impossible to solve with a simple formula.

        **The mathematical reality:**

        For each body $i$, Newton's law gives us:

        $$m_i \frac{d^2\vec{r}_i}{dt^2} = \sum_{j \neq i} \frac{G m_i m_j}{|\vec{r}_j - \vec{r}_i|^3}(\vec{r}_j - \vec{r}_i)$$

        This is a system of 18 coupled, nonlinear differential equations (3 position components
        × 3 velocity components × 3 bodies, minus center of mass motion). While we can write
        down the equations easily, **no general closed-form solution exists**.

        We must simulate step by step, and here's where chaos enters.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Birth of Chaos Theory

        The three-body problem isn't just historically interesting—it gave birth to
        **chaos theory** itself.

        In 1887, King Oscar II of Sweden offered a prize for solving the problem. Henri Poincaré
        submitted a solution that initially seemed to work, but while preparing it for publication,
        he discovered a devastating error that led to an even greater insight.

        Poincaré found that the three-body system exhibits **sensitive dependence on initial
        conditions**—what we now call the "butterfly effect." Two systems starting with
        nearly identical positions and velocities will eventually diverge completely.

        **What this means for prediction:**

        | System | Predictability |
        |--------|----------------|
        | Two-body | Forever (perfect ellipses) |
        | Three-body | Limited (chaos dominates) |
        | Solar system | ~50 million years (before chaos) |

        Even our own solar system, with its many bodies, is chaotic on long timescales.
        We cannot predict whether Mercury will still be in orbit—or will have collided
        with the Sun or been ejected—in 5 billion years.

        *The animation below shows how three bodies of equal mass can dance in unpredictable ways.*
        """
    )
    return


@app.cell
def _(COLORS, go, np):
    def simulate_three_body(
        positions, velocities, masses, dt=0.001, n_steps=10000, G=1.0
    ):
        """Simulate three-body gravitational dynamics.

        Args:
            positions: Initial positions [(x1,y1), (x2,y2), (x3,y3)]
            velocities: Initial velocities [(vx1,vy1), (vx2,vy2), (vx3,vy3)]
            masses: Masses [m1, m2, m3]
            dt: Time step
            n_steps: Number of simulation steps
            G: Gravitational constant

        Returns:
            trajectories: List of (x_array, y_array) for each body
        """
        pos = np.array(positions, dtype=float)
        vel = np.array(velocities, dtype=float)
        m = np.array(masses, dtype=float)

        trajectories = [[pos[i].copy()] for i in range(3)]

        for _ in range(n_steps):
            # Calculate accelerations
            acc = np.zeros_like(pos)
            for i in range(3):
                for j in range(3):
                    if i != j:
                        r_vec = pos[j] - pos[i]
                        r_mag = np.sqrt(np.sum(r_vec**2))
                        if r_mag > 0.01:  # Softening to avoid singularities
                            acc[i] += G * m[j] * r_vec / (r_mag**3 + 0.001)

            # Velocity Verlet integration
            vel += acc * dt
            pos += vel * dt

            # Store positions
            for i in range(3):
                trajectories[i].append(pos[i].copy())

        # Convert to arrays
        for i in range(3):
            trajectories[i] = np.array(trajectories[i])

        return trajectories

    def create_three_body_animation(
        trajectories,
        body_colors,
        body_sizes,
        title="Three-Body System",
        n_frames=100,
        trail_length=80,
    ):
        """Create animated visualization of three-body motion."""
        # Downsample trajectories to n_frames
        total_points = len(trajectories[0])
        indices = np.linspace(0, total_points - 1, n_frames, dtype=int)

        frames = []
        for frame_idx, data_idx in enumerate(indices):
            frame_data = []

            for body_idx in range(3):
                traj = trajectories[body_idx]

                # Trail
                trail_start = max(0, data_idx - trail_length)
                trail_x = traj[trail_start : data_idx + 1, 0]
                trail_y = traj[trail_start : data_idx + 1, 1]

                frame_data.append(
                    go.Scatter(
                        x=trail_x,
                        y=trail_y,
                        mode="lines",
                        line={
                            "color": body_colors[body_idx],
                            "width": 2,
                        },
                        opacity=0.6,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

                # Current position
                frame_data.append(
                    go.Scatter(
                        x=[traj[data_idx, 0]],
                        y=[traj[data_idx, 1]],
                        mode="markers",
                        marker={
                            "size": body_sizes[body_idx],
                            "color": body_colors[body_idx],
                        },
                        showlegend=(frame_idx == 0),
                        name=f"Body {body_idx + 1}",
                        hoverinfo="skip",
                    )
                )

            frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

        # Calculate axis range
        all_x = np.concatenate([t[:, 0] for t in trajectories])
        all_y = np.concatenate([t[:, 1] for t in trajectories])
        margin = 0.2
        x_range = [all_x.min() - margin, all_x.max() + margin]
        y_range = [all_y.min() - margin, all_y.max() + margin]

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(text=f"<b>{title}</b>", font=dict(size=16)),
                xaxis={
                    "scaleanchor": "y",
                    "range": x_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                yaxis={
                    "range": y_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.12,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 30, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                        "mode": "loop",
                                    },
                                ],
                            },
                            {
                                "label": "Pause",
                                "method": "animate",
                                "args": [
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                        ],
                        "bgcolor": COLORS["paper"],
                        "font": {"color": COLORS["text"]},
                    }
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    # Figure-8 orbit (famous stable solution)
    # Initial conditions for the figure-8 three-body orbit
    p1 = 0.347111
    p2 = 0.532728

    positions_fig8 = [
        (-1.0, 0.0),
        (1.0, 0.0),
        (0.0, 0.0),
    ]
    velocities_fig8 = [
        (p1, p2),
        (p1, p2),
        (-2 * p1, -2 * p2),
    ]
    masses_fig8 = [1.0, 1.0, 1.0]

    trajectories_fig8 = simulate_three_body(
        positions_fig8, velocities_fig8, masses_fig8, dt=0.001, n_steps=12000
    )

    fig8_colors = [COLORS["gravity"], COLORS["quantum"], COLORS["wave"]]
    fig8_sizes = [20, 20, 20]

    fig8_animation = create_three_body_animation(
        trajectories_fig8,
        fig8_colors,
        fig8_sizes,
        title="The Figure-8 Orbit: A Rare Stable Solution",
        n_frames=180,
        trail_length=120,
    )

    return (
        create_three_body_animation,
        fig8_animation,
        fig8_colors,
        fig8_sizes,
        masses_fig8,
        p1,
        p2,
        positions_fig8,
        simulate_three_body,
        trajectories_fig8,
        velocities_fig8,
    )


@app.cell
def _(fig8_animation, mo):
    mo.vstack(
        [
            fig8_animation,
            mo.md(
                "**The Figure-8 Orbit:** This remarkable solution, discovered in 1993 by Christopher Moore, shows three equal masses chasing each other along a figure-8 path. All three bodies follow the *exact same curve* in space, just offset in time. This is one of very few known stable periodic solutions to the three-body problem."
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

        ## The Trisolaran Nightmare: Chaotic Orbits

        The figure-8 orbit above is beautiful but extraordinarily rare. Most three-body
        systems are **chaotic**—small perturbations grow exponentially, making long-term
        prediction impossible.

        In the Trisolaran system from the novel, the three suns have different masses and
        the planet is caught in their gravitational tug-of-war. The result is a world that
        can experience any of these fates:

        1. **Stable Era**: The planet temporarily orbits one sun while the other two are distant
        2. **Close Approach**: The planet swings dangerously close to a sun (extreme heat)
        3. **Ejection**: The planet is flung far from all suns (extreme cold)
        4. **Collision**: The planet crashes into a sun (destruction)

        The Trisolarans cannot predict which will happen next. They can only prepare for all possibilities.

        *The animation below shows a more realistic chaotic three-body system. Watch how
        the motions become increasingly unpredictable.*
        """
    )
    return


@app.cell
def _(COLORS, create_three_body_animation, simulate_three_body):
    # Chaotic system simulation
    positions_chaos = [
        (0.0, 0.0),
        (1.5, 0.0),
        (0.5, 1.2),
    ]
    velocities_chaos = [
        (0.0, 0.3),
        (-0.3, -0.2),
        (0.3, -0.1),
    ]
    masses_chaos = [1.0, 0.8, 0.6]

    trajectories_chaos = simulate_three_body(
        positions_chaos, velocities_chaos, masses_chaos, dt=0.002, n_steps=15000
    )

    chaos_colors = [COLORS["gravity"], COLORS["photon"], COLORS["secondary"]]
    chaos_sizes = [24, 20, 18]

    chaos_animation = create_three_body_animation(
        trajectories_chaos,
        chaos_colors,
        chaos_sizes,
        title="Chaotic Three-Body Motion",
        n_frames=120,
        trail_length=100,
    )

    return (
        chaos_animation,
        chaos_colors,
        chaos_sizes,
        masses_chaos,
        positions_chaos,
        trajectories_chaos,
        velocities_chaos,
    )


@app.cell
def _(chaos_animation, mo):
    mo.vstack(
        [
            chaos_animation,
            mo.md(
                "**Chaotic Motion:** Three bodies with unequal masses (shown by size) interact gravitationally. Notice how the system alternates between close encounters and wider separations. The orange 'sun' dominates gravitationally, but the other bodies can temporarily escape its influence before being pulled back."
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

        ## Sensitive Dependence: The Butterfly Effect

        The defining feature of chaos is **sensitive dependence on initial conditions**.
        Two systems that start nearly identically will eventually diverge completely.

        Let's demonstrate this dramatically. We'll simulate two three-body systems that
        differ by only **0.0001** in one initial position—roughly the width of a human hair
        compared to a football field.

        Watch how the systems initially follow nearly identical paths, then gradually diverge
        until they bear no resemblance to each other.

        This is why the Trisolarans cannot predict their fate: even if they could measure
        their suns' positions to extraordinary precision, unmeasurably tiny errors would
        eventually dominate their predictions.
        """
    )
    return


@app.cell
def _(COLORS, go, np, simulate_three_body):
    def create_butterfly_effect_animation():
        """Show two nearly-identical systems diverging."""
        # Base initial conditions
        positions_base = [
            (0.0, 0.0),
            (1.0, 0.0),
            (0.5, 0.866),
        ]
        velocities_base = [
            (0.2, 0.3),
            (-0.3, 0.1),
            (0.1, -0.4),
        ]
        masses = [1.0, 1.0, 1.0]

        # Perturbed initial conditions (tiny difference)
        epsilon = 0.0001
        positions_perturbed = [
            (0.0 + epsilon, 0.0),
            (1.0, 0.0),
            (0.5, 0.866),
        ]

        # Simulate both
        traj_base = simulate_three_body(
            positions_base, velocities_base, masses, dt=0.001, n_steps=8000
        )
        traj_perturbed = simulate_three_body(
            positions_perturbed, velocities_base, masses, dt=0.001, n_steps=8000
        )

        # Create animation showing both systems
        n_frames = 100
        total_points = len(traj_base[0])
        indices = np.linspace(0, total_points - 1, n_frames, dtype=int)

        # Calculate divergence over time
        divergence = []
        for idx in indices:
            total_div = 0
            for body in range(3):
                dx = traj_base[body][idx, 0] - traj_perturbed[body][idx, 0]
                dy = traj_base[body][idx, 1] - traj_perturbed[body][idx, 1]
                total_div += np.sqrt(dx**2 + dy**2)
            divergence.append(total_div / 3)

        frames = []
        for frame_idx, data_idx in enumerate(indices):
            frame_data = []

            # System 1 (base) - solid colors
            colors_base = [COLORS["quantum"], COLORS["wave"], COLORS["particle"]]
            for body in range(3):
                # Trail
                trail_start = max(0, data_idx - 80)
                frame_data.append(
                    go.Scatter(
                        x=traj_base[body][trail_start : data_idx + 1, 0],
                        y=traj_base[body][trail_start : data_idx + 1, 1],
                        mode="lines",
                        line={"color": colors_base[body], "width": 2},
                        opacity=0.7,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )
                # Body
                frame_data.append(
                    go.Scatter(
                        x=[traj_base[body][data_idx, 0]],
                        y=[traj_base[body][data_idx, 1]],
                        mode="markers",
                        marker={"size": 16, "color": colors_base[body]},
                        name=f"System A - Body {body + 1}" if frame_idx == 0 else None,
                        showlegend=(frame_idx == 0 and body == 0),
                        hoverinfo="skip",
                    )
                )

            # System 2 (perturbed) - dashed/lighter
            colors_perturbed = [
                COLORS["secondary"],
                COLORS["tertiary"],
                COLORS["accent2"],
            ]
            for body in range(3):
                # Trail
                trail_start = max(0, data_idx - 80)
                frame_data.append(
                    go.Scatter(
                        x=traj_perturbed[body][trail_start : data_idx + 1, 0],
                        y=traj_perturbed[body][trail_start : data_idx + 1, 1],
                        mode="lines",
                        line={"color": colors_perturbed[body], "width": 2, "dash": "dot"},
                        opacity=0.7,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )
                # Body
                frame_data.append(
                    go.Scatter(
                        x=[traj_perturbed[body][data_idx, 0]],
                        y=[traj_perturbed[body][data_idx, 1]],
                        mode="markers",
                        marker={
                            "size": 14,
                            "color": colors_perturbed[body],
                            "symbol": "diamond",
                        },
                        name=f"System B - Body {body + 1}" if frame_idx == 0 else None,
                        showlegend=(frame_idx == 0 and body == 0),
                        hoverinfo="skip",
                    )
                )

            frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

        # Axis range
        all_x = np.concatenate(
            [t[:, 0] for t in traj_base] + [t[:, 0] for t in traj_perturbed]
        )
        all_y = np.concatenate(
            [t[:, 1] for t in traj_base] + [t[:, 1] for t in traj_perturbed]
        )
        margin = 0.3
        x_range = [all_x.min() - margin, all_x.max() + margin]
        y_range = [all_y.min() - margin, all_y.max() + margin]

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Butterfly Effect:</b> Initial difference = 0.0001",
                    font=dict(size=16),
                ),
                xaxis={
                    "scaleanchor": "y",
                    "range": x_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                yaxis={
                    "range": y_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10),
                ),
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.12,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 40, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                    },
                                ],
                            },
                            {
                                "label": "Pause",
                                "method": "animate",
                                "args": [
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                        ],
                        "bgcolor": COLORS["paper"],
                        "font": {"color": COLORS["text"]},
                    }
                ],
                margin=dict(b=80),
                annotations=[
                    dict(
                        x=0.5,
                        y=-0.22,
                        xref="paper",
                        yref="paper",
                        text="Circles = System A | Diamonds = System B (started 0.0001 apart)",
                        showarrow=False,
                        font=dict(size=11, color=COLORS["text_secondary"]),
                    )
                ],
            ),
            frames=frames,
        )

        return fig

    butterfly_fig = create_butterfly_effect_animation()
    return (butterfly_fig, create_butterfly_effect_animation)


@app.cell
def _(butterfly_fig, mo):
    mo.vstack(
        [
            butterfly_fig,
            mo.md(
                "**The Butterfly Effect:** Two identical three-body systems—except one body starts just 0.0001 units away. At first they move together (solid circles and dotted diamonds overlap). But tiny differences amplify exponentially. By the end, the systems have completely different configurations. This is why long-term prediction is fundamentally impossible."
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

        ## The Trisolaran Star System: A Planet Among Three Suns

        Let's simulate something closer to the scenario in the novel: a small planet
        (like Trisolaris) orbiting in a system dominated by three massive stars.

        The suns are much more massive than the planet, so they primarily interact with
        each other while the planet is swept along by their combined gravitational field.

        Watch how the planet can experience:
        - Periods of relative stability (orbiting one sun)
        - Chaotic transitions (gravitational handoffs between suns)
        - Close approaches (scorching heat)
        - Far excursions (freezing cold)
        """
    )
    return


@app.cell
def _(COLORS, go, np):
    def simulate_trisolaris(dt=0.0005, n_steps=30000):
        """Simulate a planet in a triple-star system."""
        # Three suns - hierarchical system (binary pair + distant third)
        # Using normalized units
        sun_positions = np.array([
            [-0.5, 0.0],   # Sun 1 (binary pair)
            [0.5, 0.0],    # Sun 2 (binary pair)
            [2.5, 0.0],    # Sun 3 (distant)
        ])
        sun_velocities = np.array([
            [0.0, -0.4],
            [0.0, 0.4],
            [0.0, -0.15],
        ])
        sun_masses = np.array([1.0, 1.0, 0.8])

        # Planet - starts orbiting the binary pair
        planet_pos = np.array([0.0, 1.2])
        planet_vel = np.array([0.6, 0.0])
        planet_mass = 0.0001  # Negligible mass

        # Storage
        sun_trajectories = [[pos.copy()] for pos in sun_positions]
        planet_trajectory = [planet_pos.copy()]

        G = 1.0

        for _ in range(n_steps):
            # Sun-sun forces
            sun_acc = np.zeros_like(sun_positions)
            for i in range(3):
                for j in range(3):
                    if i != j:
                        r_vec = sun_positions[j] - sun_positions[i]
                        r_mag = np.sqrt(np.sum(r_vec**2)) + 0.01
                        sun_acc[i] += G * sun_masses[j] * r_vec / (r_mag**3)

            # Planet acceleration (from all suns)
            planet_acc = np.zeros(2)
            for j in range(3):
                r_vec = sun_positions[j] - planet_pos
                r_mag = np.sqrt(np.sum(r_vec**2)) + 0.01
                planet_acc += G * sun_masses[j] * r_vec / (r_mag**3)

            # Update suns
            sun_velocities += sun_acc * dt
            sun_positions += sun_velocities * dt

            # Update planet
            planet_vel += planet_acc * dt
            planet_pos += planet_vel * dt

            # Store
            for i in range(3):
                sun_trajectories[i].append(sun_positions[i].copy())
            planet_trajectory.append(planet_pos.copy())

        # Convert to arrays
        for i in range(3):
            sun_trajectories[i] = np.array(sun_trajectories[i])
        planet_trajectory = np.array(planet_trajectory)

        return sun_trajectories, planet_trajectory

    def create_trisolaris_animation(sun_trajs, planet_traj, n_frames=200):
        """Create animation of Trisolaran system."""
        total_points = len(planet_traj)
        indices = np.linspace(0, total_points - 1, n_frames, dtype=int)

        sun_colors = ["#FFD700", "#FFA500", "#FF6347"]  # Gold, Orange, Tomato (suns)
        sun_sizes = [28, 28, 24]
        planet_color = COLORS["quantum"]
        planet_size = 10

        frames = []
        for frame_idx, data_idx in enumerate(indices):
            frame_data = []

            # Sun trails and positions
            for sun_idx in range(3):
                traj = sun_trajs[sun_idx]
                trail_start = max(0, data_idx - 150)

                # Trail
                frame_data.append(
                    go.Scatter(
                        x=traj[trail_start : data_idx + 1, 0],
                        y=traj[trail_start : data_idx + 1, 1],
                        mode="lines",
                        line={"color": sun_colors[sun_idx], "width": 2},
                        opacity=0.4,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

                # Sun
                frame_data.append(
                    go.Scatter(
                        x=[traj[data_idx, 0]],
                        y=[traj[data_idx, 1]],
                        mode="markers",
                        marker={
                            "size": sun_sizes[sun_idx],
                            "color": sun_colors[sun_idx],
                            "line": {"width": 2, "color": "white"},
                        },
                        name=f"Sun {sun_idx + 1}" if frame_idx == 0 else None,
                        showlegend=(frame_idx == 0),
                        hoverinfo="skip",
                    )
                )

            # Planet trail
            trail_start = max(0, data_idx - 200)
            frame_data.append(
                go.Scatter(
                    x=planet_traj[trail_start : data_idx + 1, 0],
                    y=planet_traj[trail_start : data_idx + 1, 1],
                    mode="lines",
                    line={"color": planet_color, "width": 1.5},
                    opacity=0.6,
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

            # Planet
            frame_data.append(
                go.Scatter(
                    x=[planet_traj[data_idx, 0]],
                    y=[planet_traj[data_idx, 1]],
                    mode="markers",
                    marker={
                        "size": planet_size,
                        "color": planet_color,
                        "symbol": "circle",
                    },
                    name="Trisolaris" if frame_idx == 0 else None,
                    showlegend=(frame_idx == 0),
                    hoverinfo="skip",
                )
            )

            frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

        # Axis range
        all_x = np.concatenate([t[:, 0] for t in sun_trajs] + [planet_traj[:, 0]])
        all_y = np.concatenate([t[:, 1] for t in sun_trajs] + [planet_traj[:, 1]])
        margin = 0.5
        x_range = [all_x.min() - margin, all_x.max() + margin]
        y_range = [all_y.min() - margin, all_y.max() + margin]

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Trisolaran System:</b> A Planet Among Three Suns",
                    font=dict(size=16),
                ),
                xaxis={
                    "scaleanchor": "y",
                    "range": x_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                yaxis={
                    "range": y_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.12,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 25, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                    },
                                ],
                            },
                            {
                                "label": "Pause",
                                "method": "animate",
                                "args": [
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                        ],
                        "bgcolor": COLORS["paper"],
                        "font": {"color": COLORS["text"]},
                    }
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    sun_trajectories, planet_trajectory = simulate_trisolaris()
    trisolaris_fig = create_trisolaris_animation(sun_trajectories, planet_trajectory)

    return (
        create_trisolaris_animation,
        planet_trajectory,
        simulate_trisolaris,
        sun_trajectories,
        trisolaris_fig,
    )


@app.cell
def _(mo, trisolaris_fig):
    mo.vstack(
        [
            trisolaris_fig,
            mo.md(
                "**The Trisolaran System (Chaotic):** Three suns (gold, orange, red) orbit each other while a small blue planet tries to survive. The two closer suns form a binary pair, while the third orbits farther out. The planet's fate depends on the complex gravitational dance—sometimes stable, sometimes chaotic. This is the reality the Trisolarans face."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### But Wait—Can a Trisolaran System Ever Be Stable?

        Yes! Real triple-star systems with planets do exist. The key is **hierarchy**:

        - The planet must orbit much closer to one star (or a tight binary) than the
          distance to the third star
        - The "stability zone" requires the planet's orbit to be less than ~1/3 the
          distance to the perturbing star

        Examples like **Alpha Centauri** show this is possible. Below is a stable configuration
        where the planet safely orbits the binary pair while the third sun stays far away.
        """
    )
    return


@app.cell
def _(COLORS, go, np):
    def simulate_stable_trisolaris(dt=0.0003, n_steps=50000):
        """Simulate a STABLE planet in a triple-star system.

        Key to stability:
        - Tight binary pair (separation ~1)
        - Third star far away (distance ~8, giving ratio > 5:1)
        - Planet in circumbinary orbit at ~2x binary separation
        """
        # Tight binary pair
        binary_sep = 0.8
        sun_positions = np.array([
            [-binary_sep/2, 0.0],   # Sun 1 (binary)
            [binary_sep/2, 0.0],    # Sun 2 (binary)
            [8.0, 0.0],             # Sun 3 (distant - 10x binary separation)
        ])

        # Binary orbital velocity (circular orbit around center of mass)
        v_binary = np.sqrt(1.0 / binary_sep) * 0.7
        # Third star velocity (slow orbit around system)
        v_third = np.sqrt(2.0 / 8.0) * 0.5

        sun_velocities = np.array([
            [0.0, -v_binary],
            [0.0, v_binary],
            [0.0, v_third],
        ])
        sun_masses = np.array([1.0, 1.0, 0.6])

        # Planet in stable circumbinary orbit
        # Orbital radius should be > 2x binary separation for stability
        planet_radius = 2.0
        planet_orbital_v = np.sqrt(2.0 / planet_radius) * 0.95  # Slightly less than circular

        planet_pos = np.array([planet_radius, 0.0])
        planet_vel = np.array([0.0, planet_orbital_v])

        # Storage (sample every 5 steps to reduce memory)
        sun_trajectories = [[pos.copy()] for pos in sun_positions]
        planet_trajectory = [planet_pos.copy()]

        G = 1.0
        sample_rate = 5

        for step in range(n_steps):
            # Sun-sun forces
            sun_acc = np.zeros_like(sun_positions)
            for i in range(3):
                for j in range(3):
                    if i != j:
                        r_vec = sun_positions[j] - sun_positions[i]
                        r_mag = np.sqrt(np.sum(r_vec**2)) + 0.001
                        sun_acc[i] += G * sun_masses[j] * r_vec / (r_mag**3)

            # Planet acceleration (from all suns)
            planet_acc = np.zeros(2)
            for j in range(3):
                r_vec = sun_positions[j] - planet_pos
                r_mag = np.sqrt(np.sum(r_vec**2)) + 0.001
                planet_acc += G * sun_masses[j] * r_vec / (r_mag**3)

            # Velocity Verlet integration
            sun_velocities += sun_acc * dt
            sun_positions += sun_velocities * dt
            planet_vel += planet_acc * dt
            planet_pos += planet_vel * dt

            # Store periodically
            if step % sample_rate == 0:
                for i in range(3):
                    sun_trajectories[i].append(sun_positions[i].copy())
                planet_trajectory.append(planet_pos.copy())

        # Convert to arrays
        for i in range(3):
            sun_trajectories[i] = np.array(sun_trajectories[i])
        planet_trajectory = np.array(planet_trajectory)

        return sun_trajectories, planet_trajectory

    def create_stable_trisolaris_animation(sun_trajs, planet_traj, n_frames=250):
        """Create animation of stable Trisolaran system."""
        total_points = len(planet_traj)
        indices = np.linspace(0, total_points - 1, n_frames, dtype=int)

        sun_colors = ["#FFD700", "#FFA500", "#FF6347"]
        sun_sizes = [26, 26, 22]
        planet_color = COLORS["quantum"]
        planet_size = 12

        frames = []
        for frame_idx, data_idx in enumerate(indices):
            frame_data = []

            # Sun trails and positions
            for sun_idx in range(3):
                traj = sun_trajs[sun_idx]
                trail_start = max(0, data_idx - 200)

                # Trail
                frame_data.append(
                    go.Scatter(
                        x=traj[trail_start : data_idx + 1, 0],
                        y=traj[trail_start : data_idx + 1, 1],
                        mode="lines",
                        line={"color": sun_colors[sun_idx], "width": 2},
                        opacity=0.4,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

                # Sun
                frame_data.append(
                    go.Scatter(
                        x=[traj[data_idx, 0]],
                        y=[traj[data_idx, 1]],
                        mode="markers",
                        marker={
                            "size": sun_sizes[sun_idx],
                            "color": sun_colors[sun_idx],
                            "line": {"width": 2, "color": "white"},
                        },
                        name=f"Sun {sun_idx + 1}" if frame_idx == 0 else None,
                        showlegend=(frame_idx == 0),
                        hoverinfo="skip",
                    )
                )

            # Planet trail (longer for stable orbit visibility)
            trail_start = max(0, data_idx - 300)
            frame_data.append(
                go.Scatter(
                    x=planet_traj[trail_start : data_idx + 1, 0],
                    y=planet_traj[trail_start : data_idx + 1, 1],
                    mode="lines",
                    line={"color": planet_color, "width": 2},
                    opacity=0.7,
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

            # Planet
            frame_data.append(
                go.Scatter(
                    x=[planet_traj[data_idx, 0]],
                    y=[planet_traj[data_idx, 1]],
                    mode="markers",
                    marker={
                        "size": planet_size,
                        "color": planet_color,
                        "symbol": "circle",
                        "line": {"width": 1, "color": "white"},
                    },
                    name="Trisolaris" if frame_idx == 0 else None,
                    showlegend=(frame_idx == 0),
                    hoverinfo="skip",
                )
            )

            frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

        # Axis range - focus on inner system but show distant sun
        inner_x = np.concatenate([sun_trajs[0][:, 0], sun_trajs[1][:, 0], planet_traj[:, 0]])
        inner_y = np.concatenate([sun_trajs[0][:, 1], sun_trajs[1][:, 1], planet_traj[:, 1]])
        margin = 1.0
        x_min = min(inner_x.min() - margin, -4)
        x_max = max(inner_x.max() + margin, sun_trajs[2][:, 0].max() + 1)
        y_range = [inner_y.min() - margin, inner_y.max() + margin]

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Stable Trisolaran System:</b> Hierarchy Creates Order<br><sub>Planet safely orbits the binary while the third sun stays distant</sub>",
                    font=dict(size=16),
                ),
                xaxis={
                    "scaleanchor": "y",
                    "range": [x_min, x_max],
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                yaxis={
                    "range": y_range,
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False,
                },
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["paper"],
                font=dict(color=COLORS["text"]),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.12,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 30, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                        "mode": "loop",
                                    },
                                ],
                            },
                            {
                                "label": "Pause",
                                "method": "animate",
                                "args": [
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                        ],
                        "bgcolor": COLORS["paper"],
                        "font": {"color": COLORS["text"]},
                    }
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    stable_sun_trajs, stable_planet_traj = simulate_stable_trisolaris()
    stable_trisolaris_fig = create_stable_trisolaris_animation(stable_sun_trajs, stable_planet_traj)

    return (
        create_stable_trisolaris_animation,
        simulate_stable_trisolaris,
        stable_planet_traj,
        stable_sun_trajs,
        stable_trisolaris_fig,
    )


@app.cell
def _(mo, stable_trisolaris_fig):
    mo.vstack(
        [
            stable_trisolaris_fig,
            mo.md(
                "**Stable Trisolaran Configuration:** The secret is hierarchy! The planet (blue) orbits the tight binary pair (gold and orange suns) at a safe distance, while the third sun (red) is far enough away that its gravitational perturbations are gentle. This is how real planets survive in triple-star systems like Alpha Centauri. The planet experiences predictable **Stable Eras** indefinitely."
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

        ## Possible Outcomes: How Three-Body Systems Can End

        Over long timescales, three-body systems don't dance forever. They typically evolve
        toward one of several end states:

        | Outcome | Description | Probability |
        |---------|-------------|-------------|
        | **Ejection** | One body gains enough energy to escape | Most common |
        | **Collision** | Two bodies merge | Less common |
        | **Stable hierarchy** | Binary pair + distant third | Temporary |
        | **Periodic orbit** | Like figure-8 | Extremely rare |

        The most common fate is **ejection**: the lightest body gets progressively more
        energy from close encounters until it escapes to infinity, leaving behind a
        stable binary pair.

        Let's see different scenarios unfold.
        """
    )
    return


@app.cell
def _(COLORS, create_three_body_animation, simulate_three_body):
    # Scenario 1: Ejection case
    positions_eject = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.3, 0.5),
    ]
    velocities_eject = [
        (0.0, 0.2),
        (0.0, -0.3),
        (0.5, 0.1),
    ]
    masses_eject = [1.0, 1.0, 0.3]  # Light third body

    trajectories_eject = simulate_three_body(
        positions_eject, velocities_eject, masses_eject, dt=0.002, n_steps=12000
    )

    eject_colors = [COLORS["gravity"], COLORS["photon"], COLORS["particle"]]
    eject_sizes = [22, 22, 14]

    eject_animation = create_three_body_animation(
        trajectories_eject,
        eject_colors,
        eject_sizes,
        title="Scenario: Ejection of the Lightest Body",
        n_frames=100,
        trail_length=80,
    )

    return (
        eject_animation,
        eject_colors,
        eject_sizes,
        masses_eject,
        positions_eject,
        trajectories_eject,
        velocities_eject,
    )


@app.cell
def _(eject_animation, mo):
    mo.vstack(
        [
            eject_animation,
            mo.md(
                "**Ejection Scenario:** Two massive bodies (orange and gold) dominate, while a lighter body (pink) gets progressively more energy from close encounters. Eventually, the light body may gain enough energy to escape entirely, leaving a stable binary behind. This is the most common long-term fate of three-body systems."
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(COLORS, create_three_body_animation, np, simulate_three_body):
    # Scenario 2: Hierarchical system - tight binary + distant third
    # Binary separation
    binary_sep = 0.5
    # Third body distance (must be >> binary_sep for stability)
    third_dist = 5.0

    # Binary orbital velocity: v = sqrt(G*m_other / separation)
    v_binary = np.sqrt(1.0 / binary_sep) * 0.7

    # Third body orbital velocity around binary center of mass
    # Total binary mass = 2.0, so v = sqrt(2.0 / distance)
    v_third = np.sqrt(2.0 / third_dist) * 0.95

    positions_hier = [
        (-binary_sep/2, 0.0),
        (binary_sep/2, 0.0),
        (third_dist, 0.0),
    ]
    velocities_hier = [
        (0.0, -v_binary),
        (0.0, v_binary),
        (0.0, v_third),
    ]
    masses_hier = [1.0, 1.0, 0.6]

    trajectories_hier = simulate_three_body(
        positions_hier, velocities_hier, masses_hier, dt=0.0008, n_steps=25000
    )

    hier_colors = [COLORS["gravity"], COLORS["photon"], COLORS["wave"]]
    hier_sizes = [22, 22, 18]

    hier_animation = create_three_body_animation(
        trajectories_hier,
        hier_colors,
        hier_sizes,
        title="Scenario: Hierarchical System (Binary + Distant Third)",
        n_frames=180,
        trail_length=150,
    )

    return (
        hier_animation,
        hier_colors,
        hier_sizes,
        masses_hier,
        positions_hier,
        trajectories_hier,
        velocities_hier,
    )


@app.cell
def _(hier_animation, mo):
    mo.vstack(
        [
            hier_animation,
            mo.md(
                "**Hierarchical System:** A close binary pair (orange and gold) with a distant third body (green) orbiting them both. This configuration can be stable for long periods—the third body 'sees' the binary as roughly a single mass. Many real triple-star systems have this structure. But perturbations can eventually destabilize even these systems."
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

        ## Why Can't We Solve It?

        The three-body problem isn't just *hard*—it's fundamentally different from the two-body problem.

        **Two-Body Problem:**
        - 10 conserved quantities (energy, momentum, angular momentum)
        - 12 degrees of freedom
        - Enough constraints to solve completely
        - Solution: Conic sections (ellipse, parabola, hyperbola)

        **Three-Body Problem:**
        - Same 10 conserved quantities
        - 18 degrees of freedom
        - Not enough constraints!
        - No general closed-form solution

        The mathematics says: you cannot write down a formula that takes the initial positions
        and velocities and outputs the positions at any future time. You *must* integrate
        step by step, accumulating errors as you go.

        **Poincaré's Insight:**

        Henri Poincaré proved that the three-body problem is *non-integrable*—there are no
        additional hidden conserved quantities waiting to be discovered. The chaos is
        intrinsic to the system, not a failure of our mathematics.

        This was a profound shift in physics: some systems are fundamentally unpredictable,
        not because we lack knowledge, but because nature itself doesn't "know" the distant
        future of such systems.
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "Special Solutions That Do Exist": mo.md(
                r"""
        While no *general* solution exists, mathematicians have found special cases:

        **Lagrange Points (1772):**
        Three bodies at the vertices of an equilateral triangle, rotating together.
        This is where we park space telescopes like James Webb!

        **Euler's Collinear Solutions (1767):**
        Three bodies in a line, rotating around their center of mass.
        Unstable but mathematically exact.

        **The Figure-8 (1993):**
        Three equal masses chasing each other along a figure-8 path.
        Discovered by Christopher Moore, proven stable by Chenciner and Montgomery (2000).

        **Periodic Orbits:**
        Thousands of periodic solutions have been found numerically, but they form
        a set of measure zero—if you pick initial conditions randomly, you will
        *never* land on one. They're mathematical curiosities, not physical attractors.

        **The Sitnikov Problem:**
        A restricted case where one body oscillates perpendicular to two others
        in circular orbit. Shows beautiful chaos in a simplified setting.
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

        ## Practical Implications: Our Solar System

        You might wonder: if three bodies are chaotic, how does our solar system
        survive with eight planets plus countless smaller objects?

        The answer is **hierarchy and timescales**:

        1. **The Sun dominates**: It contains 99.8% of the solar system's mass.
           Planets primarily interact with the Sun, not each other.

        2. **Resonances provide stability**: Jupiter and Saturn have a 5:2 orbital
           resonance that actually stabilizes the inner solar system.

        3. **Chaos is slow**: Our solar system *is* chaotic, but on timescales of
           ~50 million years. Short-term predictions are extremely accurate.

        **What we can and cannot predict:**

        | Prediction | Confidence |
        |------------|------------|
        | Tomorrow's planetary positions | Perfect (microsecond accuracy) |
        | Positions in 100 years | Excellent |
        | Positions in 10 million years | Good |
        | Positions in 100 million years | Uncertain |
        | Positions in 5 billion years | Unknown (Mercury might be ejected!) |

        The Trisolarans face a much harsher version: their chaos timescale might be
        only centuries or millennia, not millions of years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Profound Lesson

        The three-body problem teaches us something deep about the nature of physical law:

        > **Deterministic does not mean predictable.**

        Newton's laws are completely deterministic—given exact initial conditions, the
        future is uniquely determined. And yet, in chaotic systems, we cannot access that
        future because:

        1. We cannot measure initial conditions with infinite precision
        2. Small errors grow exponentially
        3. Eventually, our predictions become worthless

        This isn't a failure of physics—it's a discovery *about* physics. Some systems
        have inherent limits to predictability built into their dynamics.

        **For the Trisolarans**, this means their civilization will forever live in
        uncertainty. They cannot predict when their next Chaotic Era will begin, only
        that it will. They can prepare, adapt, and survive—but never truly know their fate.

        **For us**, the three-body problem reminds us that even in a universe governed
        by elegant mathematical laws, complexity and unpredictability can emerge from
        the simplest ingredients: three masses and gravity.

        ---

        *"The universe is not only queerer than we suppose, but queerer than we can suppose."*
        — J.B.S. Haldane
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References

        ### The Novel

        - **Liu Cixin** (2008). *The Three-Body Problem* (三体). Translated by Ken Liu (2014).
          Winner of the Hugo Award for Best Novel, 2015.

        ### Physics & Mathematics

        - **Poincaré, H.** (1890). "Sur le problème des trois corps et les équations de la dynamique."
          *Acta Mathematica* 13: 1–270. The foundational work on chaos theory.

        - **Moore, C.** (1993). "Braids in classical dynamics." *Physical Review Letters* 70: 3675.
          Discovery of the figure-8 orbit.

        - **Chenciner, A. & Montgomery, R.** (2000). "A remarkable periodic solution of the three-body
          problem in the case of equal masses." *Annals of Mathematics* 152: 881–901.

        - **Valtonen, M. & Karttunen, H.** (2006). *The Three-Body Problem*. Cambridge University Press.
          Comprehensive treatment of the mathematics and astronomy.

        ### Further Reading

        - **Feynman, R. P.** *The Feynman Lectures on Physics*, Chapter 9: Newton's Laws of Dynamics.
          [feynmanlectures.caltech.edu](https://www.feynmanlectures.caltech.edu/I_09.html)

        - **Gleick, J.** (1987). *Chaos: Making a New Science*. Accessible introduction to chaos theory.

        - **Wisdom, J.** (1987). "Chaotic behaviour in the solar system." *Proceedings of the Royal Society*
          A 413: 109–129. On long-term chaos in our own solar system.
        """
    )
    return


if __name__ == "__main__":
    app.run()
