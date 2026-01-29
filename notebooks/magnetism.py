import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # Magnetism and Electric Motors

        *An interactive exploration based on [Feynman Lectures on Physics, Volume II](https://www.feynmanlectures.caltech.edu/II_toc.html)*

        ---

        ## The Marriage of Electricity and Magnetism

        In 1820, Danish physicist Hans Christian Oersted made a discovery that would change the world:
        **a compass needle deflected when placed near a wire carrying electric current**.

        This was shocking. For centuries, electricity and magnetism had been considered completely
        separate phenomena. Lightning and static cling had nothing to do with lodestones and compasses—or
        so everyone thought.

        Oersted's discovery revealed a profound truth: **electricity and magnetism are two aspects of
        the same fundamental force**. This unification would eventually lead to:

        - Electric motors that power our civilization
        - Generators that produce our electricity
        - Transformers that distribute power across continents
        - The understanding that light itself is an electromagnetic wave

        > *"The force on an electric charge depends not only on where it is, but also on how fast
        > it is moving."* — Richard Feynman

        Let's explore this remarkable connection, from the basic physics of magnetic fields to the
        motors that move our world.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 1. The Magnetic Field

        ### What Creates a Magnetic Field?

        There are two sources of magnetic fields:

        1. **Moving electric charges** (currents)
        2. **Intrinsic magnetic moments** of particles (like electrons)

        The magnetic field $\mathbf{B}$ exerts a force on moving charges given by the **Lorentz force law**:

        $$\mathbf{F} = q\mathbf{v} \times \mathbf{B}$$

        This says: the force is perpendicular to both the velocity and the magnetic field, with
        magnitude $F = qvB\sin\theta$.

        **Key insight:** Unlike electric forces, magnetic forces do no work! The force is always
        perpendicular to the motion, so it changes the direction of velocity but not its magnitude.
        This is why magnetic fields can steer charged particles in circles but can't speed them up
        directly.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Magnetic field around a current-carrying wire
    def create_wire_field_animation():
        n_frames = 60
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi
            frame_data = []

            # The wire (vertical line at center)
            frame_data.append(go.Scatter3d(
                x=[0, 0], y=[0, 0], z=[-2, 2],
                mode="lines",
                line=dict(color="gold", width=10),
                name="Current-carrying wire",
            ))

            # Current direction indicator (moving charge)
            charge_z = -2 + (frame / n_frames) * 4
            if charge_z > 2:
                charge_z = charge_z - 4
            frame_data.append(go.Scatter3d(
                x=[0], y=[0], z=[charge_z],
                mode="markers",
                marker=dict(size=8, color="yellow", symbol="diamond"),
                name="Moving charge (current)",
            ))

            # Magnetic field lines (concentric circles)
            for r in [0.5, 1.0, 1.5]:
                theta = np.linspace(0, 2 * np.pi, 50)
                # Field lines rotate to show circulation
                theta_shifted = theta + t
                x_circle = r * np.cos(theta_shifted)
                y_circle = r * np.sin(theta_shifted)
                z_circle = np.zeros_like(theta)

                frame_data.append(go.Scatter3d(
                    x=x_circle, y=y_circle, z=z_circle,
                    mode="lines",
                    line=dict(color=f"rgba(0, 150, 255, {0.8 - r * 0.2})", width=4),
                    name=f"B field (r={r})" if r == 0.5 else None,
                    showlegend=(r == 0.5),
                ))

            # Field direction arrows
            n_arrows = 8
            for i in range(n_arrows):
                angle = t + i * 2 * np.pi / n_arrows
                r = 1.0
                x_arr = r * np.cos(angle)
                y_arr = r * np.sin(angle)

                # Arrow direction (tangent to circle, counterclockwise)
                dx = -0.2 * np.sin(angle)
                dy = 0.2 * np.cos(angle)

                frame_data.append(go.Cone(
                    x=[x_arr], y=[y_arr], z=[0],
                    u=[dx], v=[dy], w=[0],
                    colorscale=[[0, "cyan"], [1, "cyan"]],
                    showscale=False,
                    sizemode="absolute",
                    sizeref=0.15,
                ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Magnetic Field Around a Current-Carrying Wire</b><br><sub>Field lines form circles around the wire (right-hand rule)</sub>",
                    font=dict(size=14),
                ),
                scene=dict(
                    xaxis=dict(range=[-2, 2], showbackground=False),
                    yaxis=dict(range=[-2, 2], showbackground=False),
                    zaxis=dict(range=[-2.5, 2.5], showbackground=False, title="Wire"),
                    aspectmode="cube",
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
                ),
                showlegend=True,
                legend=dict(x=0, y=1),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    wire_field_fig = create_wire_field_animation()
    wire_field_fig
    return (create_wire_field_animation, wire_field_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Right-Hand Rule

        The direction of the magnetic field around a wire follows the **right-hand rule**:

        - Point your thumb in the direction of the current
        - Your fingers curl in the direction of the magnetic field

        The field strength decreases with distance from the wire:

        $$B = \frac{\mu_0 I}{2\pi r}$$

        where $\mu_0 = 4\pi \times 10^{-7}$ T·m/A is the **permeability of free space**, $I$ is
        the current, and $r$ is the distance from the wire.

        **Physical meaning:** The magnetic field wraps around the current like water swirling
        around a drain. The closer you are to the wire, the stronger the field. This simple
        geometry is the foundation of all electromagnets.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 2. Solenoids and Electromagnets

        ### Concentrating the Magnetic Field

        A single wire produces a weak, spread-out magnetic field. But if we coil the wire into
        a **solenoid** (a helix), something remarkable happens: the fields from each loop add up
        inside, creating a strong, uniform field.

        Inside a long solenoid:

        $$B = \mu_0 n I$$

        where $n$ is the number of turns per unit length.

        **Why this matters:** This is how we create controllable magnetic fields. By adjusting
        the current, we can turn the field on and off, or vary its strength. This is the basis
        of electromagnets, relays, and electric motors.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Magnetic field in a solenoid
    def create_solenoid_animation():
        n_frames = 60
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi
            frame_data = []

            # Solenoid coils
            n_turns = 10
            theta_coil = np.linspace(0, n_turns * 2 * np.pi, 200)
            x_coil = np.cos(theta_coil)
            y_coil = np.sin(theta_coil)
            z_coil = np.linspace(-3, 3, 200)

            frame_data.append(go.Scatter3d(
                x=x_coil, y=y_coil, z=z_coil,
                mode="lines",
                line=dict(color="orange", width=5),
                name="Solenoid coil",
            ))

            # Internal field lines (parallel, uniform)
            for offset in [-0.3, 0, 0.3]:
                # Animated flow along field lines
                z_field = np.linspace(-2.5, 2.5, 30)
                phase = t + offset * 5
                marker_pos = -2.5 + ((phase / (2 * np.pi)) * 5) % 5

                frame_data.append(go.Scatter3d(
                    x=[offset] * len(z_field),
                    y=[0] * len(z_field),
                    z=z_field,
                    mode="lines",
                    line=dict(color="cyan", width=3),
                    showlegend=(offset == 0),
                    name="B field (inside)" if offset == 0 else None,
                ))

                # Moving marker to show field direction
                frame_data.append(go.Scatter3d(
                    x=[offset], y=[0], z=[marker_pos],
                    mode="markers",
                    marker=dict(size=6, color="white", symbol="diamond"),
                    showlegend=False,
                ))

            # External field lines (returning loops)
            for side in [-1, 1]:
                for r_offset in [1.5, 2.0]:
                    # Curved return path
                    z_ext = np.linspace(-2.5, 2.5, 30)
                    x_ext = side * (1 + r_offset * np.exp(-z_ext**2 / 4))
                    y_ext = np.zeros_like(z_ext)

                    frame_data.append(go.Scatter3d(
                        x=x_ext, y=y_ext, z=z_ext,
                        mode="lines",
                        line=dict(color="rgba(0, 200, 255, 0.4)", width=2),
                        showlegend=False,
                    ))

            # Current direction indicators
            for i in range(4):
                z_pos = -2 + i * 1.5
                angle = t + i * np.pi / 2
                x_pos = np.cos(angle)
                y_pos = np.sin(angle)

                frame_data.append(go.Scatter3d(
                    x=[x_pos], y=[y_pos], z=[z_pos],
                    mode="markers",
                    marker=dict(size=5, color="yellow"),
                    showlegend=False,
                ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Magnetic Field in a Solenoid</b><br><sub>Uniform field inside, loops close outside</sub>",
                    font=dict(size=14),
                ),
                scene=dict(
                    xaxis=dict(range=[-3, 3], showbackground=False),
                    yaxis=dict(range=[-2, 2], showbackground=False),
                    zaxis=dict(range=[-4, 4], showbackground=False),
                    aspectmode="manual",
                    aspectratio=dict(x=1, y=0.7, z=1.3),
                    camera=dict(eye=dict(x=2, y=1, z=0.5)),
                ),
                showlegend=True,
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    solenoid_fig = create_solenoid_animation()
    solenoid_fig
    return (create_solenoid_animation, solenoid_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why the Field is Uniform Inside

        Inside the solenoid, each loop contributes a field in the same direction. The contributions
        add up to create a nearly uniform field parallel to the axis.

        Outside, the field lines must form closed loops (magnetic field lines always close on
        themselves—there are no magnetic monopoles). This means the external field spreads out
        and is much weaker.

        **Applications:**
        - **MRI machines** use superconducting solenoids to create powerful, uniform fields
        - **Particle accelerators** use solenoids to focus beams
        - **Electromagnets** in junkyards, door locks, and relays
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 3. Force on a Current-Carrying Wire

        ### The Foundation of Electric Motors

        When a current-carrying wire is placed in a magnetic field, it experiences a force:

        $$\mathbf{F} = I\mathbf{L} \times \mathbf{B}$$

        For a wire of length $L$ carrying current $I$ perpendicular to a field $B$:

        $$F = BIL$$

        **This is the principle behind every electric motor.** We use magnetic fields to push on
        wires carrying current, converting electrical energy into mechanical motion.

        The direction follows another right-hand rule:
        - Point fingers in direction of current
        - Curl toward direction of B field
        - Thumb points in direction of force
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Force on a current-carrying wire in a magnetic field
    def create_wire_force_animation():
        n_frames = 80
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames
            frame_data = []

            # Magnetic field (into the page, represented by X symbols)
            for x in np.linspace(-2, 2, 5):
                for y in np.linspace(-1.5, 1.5, 4):
                    frame_data.append(go.Scatter(
                        x=[x], y=[y],
                        mode="markers+text",
                        marker=dict(size=20, color="rgba(100, 100, 255, 0.3)", symbol="x"),
                        text=["B"],
                        textposition="top center",
                        textfont=dict(size=10, color="rgba(100, 100, 255, 0.5)"),
                        showlegend=False,
                    ))

            # Wire (moving due to force)
            wire_x = -1.5 + t * 3  # Wire moves to the right

            # Wire representation
            frame_data.append(go.Scatter(
                x=[wire_x, wire_x], y=[-1.5, 1.5],
                mode="lines",
                line=dict(color="orange", width=8),
                name="Wire (current up)",
            ))

            # Current direction arrow
            frame_data.append(go.Scatter(
                x=[wire_x], y=[0],
                mode="markers",
                marker=dict(size=15, color="yellow", symbol="triangle-up"),
                name="Current direction (I)",
            ))

            # Force arrow
            arrow_length = 0.5
            frame_data.append(go.Scatter(
                x=[wire_x, wire_x + arrow_length],
                y=[0.8, 0.8],
                mode="lines+markers",
                line=dict(color="red", width=4),
                marker=dict(size=[0, 12], color="red", symbol=["circle", "triangle-right"]),
                name="Force (F = IL × B)",
            ))

            # Annotations
            frame_data.append(go.Scatter(
                x=[2.5], y=[1.5],
                mode="text",
                text=["B field: into page (⊗)"],
                textfont=dict(size=12, color="blue"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[2.5], y=[1.0],
                mode="text",
                text=[f"Wire position: {wire_x:.1f}"],
                textfont=dict(size=12, color="orange"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Force on a Current-Carrying Wire</b><br><sub>F = IL × B pushes wire sideways</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3, 4], showgrid=True, zeroline=True, title="Position"),
                yaxis=dict(range=[-2, 2], showgrid=True, zeroline=True, scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.7, y=0.3),
                plot_bgcolor="rgba(240, 240, 255, 0.5)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    wire_force_fig = create_wire_force_animation()
    wire_force_fig
    return (create_wire_force_animation, wire_force_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Force

        In the animation above:
        - The **magnetic field B** points into the page (shown as ⊗ symbols)
        - The **current I** flows upward through the wire
        - The **force F** pushes the wire to the right

        Using the right-hand rule: current (up) × B (into page) = force (right).

        **The magnitude of the force** is $F = BIL$. To increase the force, we can:
        - Use a stronger magnetic field (bigger magnets)
        - Increase the current
        - Use more wire (more turns in a coil)

        This is exactly what we do in motors!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 4. Electromagnetic Induction

        ### Faraday's Revolutionary Discovery

        In 1831, Michael Faraday discovered the reverse effect: **a changing magnetic field
        induces an electric current**.

        This is described by **Faraday's Law**:

        $$\mathcal{E} = -\frac{d\Phi_B}{dt}$$

        where $\mathcal{E}$ is the induced electromotive force (EMF) and $\Phi_B = \int \mathbf{B} \cdot d\mathbf{A}$
        is the magnetic flux through a circuit.

        **In plain language:** If you change the magnetic field through a loop of wire—by moving
        a magnet, rotating the loop, or changing the field strength—you create a voltage that
        can drive a current.

        The negative sign is **Lenz's Law**: the induced current opposes the change that created it.
        This is nature's way of conserving energy.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Faraday's induction - magnet moving through coil
    def create_induction_animation():
        n_frames = 120
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi
            frame_data = []

            # Magnet position (oscillating)
            magnet_x = 2 * np.sin(t)

            # Coil (stationary)
            coil_theta = np.linspace(0, 2 * np.pi, 50)
            coil_y = 0.8 * np.cos(coil_theta)
            coil_z = 0.8 * np.sin(coil_theta)

            for x_offset in [-0.3, -0.1, 0.1, 0.3]:
                frame_data.append(go.Scatter3d(
                    x=[x_offset] * len(coil_theta),
                    y=coil_y,
                    z=coil_z,
                    mode="lines",
                    line=dict(color="orange", width=6),
                    showlegend=(x_offset == -0.3),
                    name="Coil" if x_offset == -0.3 else None,
                ))

            # Bar magnet
            frame_data.append(go.Scatter3d(
                x=[magnet_x - 0.8, magnet_x + 0.8],
                y=[0, 0],
                z=[0, 0],
                mode="lines",
                line=dict(color="red", width=20),
                name="Magnet",
            ))

            # N and S poles
            frame_data.append(go.Scatter3d(
                x=[magnet_x - 0.6], y=[0], z=[0.3],
                mode="text",
                text=["S"],
                textfont=dict(size=14, color="blue"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter3d(
                x=[magnet_x + 0.6], y=[0], z=[0.3],
                mode="text",
                text=["N"],
                textfont=dict(size=14, color="red"),
                showlegend=False,
            ))

            # Magnetic field lines from magnet
            for y_off in [-0.3, 0, 0.3]:
                field_x = np.linspace(magnet_x + 0.8, magnet_x + 2.5, 20)
                spread = (field_x - magnet_x - 0.8) * 0.3
                field_y = y_off * (1 + spread)
                field_z = np.zeros_like(field_x)

                frame_data.append(go.Scatter3d(
                    x=field_x, y=field_y, z=field_z,
                    mode="lines",
                    line=dict(color="rgba(255, 100, 100, 0.5)", width=2),
                    showlegend=False,
                ))

            # Induced current visualization (brightness based on rate of change)
            velocity = 2 * np.cos(t)  # d(position)/dt
            induced_emf = abs(velocity)  # Proportional to rate of flux change

            # Show current in coil wire (color intensity based on induced EMF)
            # Clamp alpha to avoid floating point issues with very small numbers
            alpha = max(0.0, min(induced_emf / 2, 1.0))
            current_color = f"rgba(255, 255, 0, {alpha:.3f})"
            frame_data.append(go.Scatter3d(
                x=[0.5], y=[0], z=[1.2],
                mode="text",
                text=[f"Induced EMF: {induced_emf:.2f} (arb. units)"],
                textfont=dict(size=12, color="yellow"),
                showlegend=False,
            ))

            # Current direction indicator (appears when EMF is significant)
            if induced_emf > 0.3:
                direction = "↻" if velocity > 0 else "↺"
                frame_data.append(go.Scatter3d(
                    x=[0], y=[1.2], z=[0],
                    mode="text",
                    text=[f"Current: {direction}"],
                    textfont=dict(size=14, color="cyan"),
                    showlegend=False,
                ))

            # Ammeter reading
            frame_data.append(go.Scatter3d(
                x=[0], y=[-1.5], z=[0],
                mode="markers+text",
                marker=dict(size=10, color=current_color),
                text=[f"v = {velocity:.2f}"],
                textposition="bottom center",
                textfont=dict(size=11, color="white"),
                name="Induced current",
                showlegend=(frame == 0),
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Electromagnetic Induction</b><br><sub>Moving magnet induces current in coil (Faraday's Law)</sub>",
                    font=dict(size=14),
                ),
                scene=dict(
                    xaxis=dict(range=[-4, 4], showbackground=False, title=""),
                    yaxis=dict(range=[-2, 2], showbackground=False, title=""),
                    zaxis=dict(range=[-1.5, 1.5], showbackground=False, title=""),
                    aspectmode="manual",
                    aspectratio=dict(x=2, y=1, z=0.75),
                    camera=dict(eye=dict(x=0, y=-2, z=0.5)),
                ),
                showlegend=True,
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 40, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    induction_fig = create_induction_animation()
    induction_fig
    return (create_induction_animation, induction_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Physics of Induction

        Watch the animation carefully:

        1. **When the magnet moves fastest** (center of oscillation), the induced EMF is maximum
        2. **When the magnet reverses direction** (ends of oscillation), the EMF is zero
        3. **The current direction reverses** when the magnet changes direction

        This is because $\mathcal{E} = -d\Phi_B/dt$. It's the **rate of change** of flux that
        matters, not the flux itself.

        **Lenz's Law in action:** When the north pole approaches, the coil creates a magnetic
        field that opposes the approach (like a north pole pushing back). When it recedes,
        the coil tries to maintain the flux (like a south pole attracting it). The induced
        current always opposes the change.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 5. The DC Motor

        ### Converting Electricity to Rotation

        Now we combine everything we've learned to build a motor!

        A **DC motor** consists of:
        1. **Permanent magnets** (or electromagnets) creating a magnetic field
        2. **Armature coil** that rotates in the field
        3. **Commutator** that reverses current direction every half-turn
        4. **Brushes** that maintain electrical contact with the spinning commutator

        The key insight: when current flows through the coil, one side is pushed up and the
        other down (by $\mathbf{F} = I\mathbf{L} \times \mathbf{B}$). This creates a **torque**
        that rotates the coil.

        The commutator is crucial: it reverses the current direction every half-turn, ensuring
        the torque always pushes in the same rotational direction.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: DC Motor operation
    def create_dc_motor_animation():
        n_frames = 120
        frames = []

        for frame in range(n_frames):
            angle = frame / n_frames * 4 * np.pi  # Two full rotations
            frame_data = []

            # Permanent magnets (N and S poles)
            # North pole (left)
            frame_data.append(go.Scatter(
                x=[-2.5, -1.5, -1.5, -2.5, -2.5],
                y=[-1, -1, 1, 1, -1],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 100, 100, 0.7)",
                line=dict(color="red", width=2),
                name="N pole",
            ))
            frame_data.append(go.Scatter(
                x=[-2], y=[0],
                mode="text",
                text=["N"],
                textfont=dict(size=20, color="white"),
                showlegend=False,
            ))

            # South pole (right)
            frame_data.append(go.Scatter(
                x=[1.5, 2.5, 2.5, 1.5, 1.5],
                y=[-1, -1, 1, 1, -1],
                mode="lines",
                fill="toself",
                fillcolor="rgba(100, 100, 255, 0.7)",
                line=dict(color="blue", width=2),
                name="S pole",
            ))
            frame_data.append(go.Scatter(
                x=[2], y=[0],
                mode="text",
                text=["S"],
                textfont=dict(size=20, color="white"),
                showlegend=False,
            ))

            # Magnetic field lines (horizontal, N to S)
            for y_offset in [-0.5, 0, 0.5]:
                frame_data.append(go.Scatter(
                    x=[-1.5, 1.5],
                    y=[y_offset, y_offset],
                    mode="lines",
                    line=dict(color="rgba(200, 200, 255, 0.5)", width=1, dash="dot"),
                    showlegend=False,
                ))

            # Rotating armature coil
            coil_length = 1.0
            coil_width = 0.6

            # Coil corners in local coordinates
            corners_local = np.array([
                [-coil_length, -coil_width],
                [coil_length, -coil_width],
                [coil_length, coil_width],
                [-coil_length, coil_width],
                [-coil_length, -coil_width],
            ])

            # Rotate
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotation = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            corners_rotated = corners_local @ rotation.T

            # Current direction depends on commutator position
            # Commutator reverses current every 180 degrees
            commutator_state = int((angle / np.pi) % 2)
            coil_color = "orange" if commutator_state == 0 else "yellow"

            frame_data.append(go.Scatter(
                x=corners_rotated[:, 0],
                y=corners_rotated[:, 1],
                mode="lines",
                line=dict(color=coil_color, width=6),
                name="Armature coil",
            ))

            # Current direction arrows on coil sides
            # Left side of coil
            left_center = rotation @ np.array([-coil_length, 0])
            # Right side of coil
            right_center = rotation @ np.array([coil_length, 0])

            # Force arrows (perpendicular to both current and B field)
            # B field is horizontal (left to right)
            # Current direction alternates with commutator
            if commutator_state == 0:
                # Current flows one way
                force_left = np.array([0, 0.4])  # Force up on left
                force_right = np.array([0, -0.4])  # Force down on right
            else:
                # Current reversed
                force_left = np.array([0, -0.4])
                force_right = np.array([0, 0.4])

            # Rotate force arrows with coil (they're relative to coil orientation)
            # Actually forces are in lab frame (up/down), not coil frame

            # Show force on left side (into page or out)
            left_y = left_center[1]
            if abs(np.cos(angle)) > 0.1:  # Only show when coil side is in field
                force_dir = 0.5 if (commutator_state == 0) else -0.5
                # Force is perpendicular to field and current
                frame_data.append(go.Scatter(
                    x=[left_center[0], left_center[0]],
                    y=[left_center[1], left_center[1] + force_dir * abs(np.cos(angle))],
                    mode="lines+markers",
                    line=dict(color="lime", width=3),
                    marker=dict(size=[0, 8], symbol=["circle", "triangle-up" if force_dir > 0 else "triangle-down"]),
                    name="Force" if frame == 0 else None,
                    showlegend=(frame == 0),
                ))

            # Commutator (split ring at bottom)
            comm_angle = angle
            comm_r = 0.3
            # Two half-rings
            theta1 = np.linspace(comm_angle, comm_angle + np.pi, 20)
            theta2 = np.linspace(comm_angle + np.pi, comm_angle + 2 * np.pi, 20)

            frame_data.append(go.Scatter(
                x=comm_r * np.cos(theta1),
                y=comm_r * np.sin(theta1) - 1.5,
                mode="lines",
                line=dict(color="gold", width=8),
                name="Commutator",
            ))
            frame_data.append(go.Scatter(
                x=comm_r * np.cos(theta2),
                y=comm_r * np.sin(theta2) - 1.5,
                mode="lines",
                line=dict(color="goldenrod", width=8),
                showlegend=False,
            ))

            # Brushes (stationary contacts)
            frame_data.append(go.Scatter(
                x=[-0.5, -0.35], y=[-1.5, -1.5],
                mode="lines",
                line=dict(color="gray", width=10),
                name="Brushes",
            ))
            frame_data.append(go.Scatter(
                x=[0.35, 0.5], y=[-1.5, -1.5],
                mode="lines",
                line=dict(color="gray", width=10),
                showlegend=False,
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[0], y=[2],
                mode="text",
                text=[f"Rotation: {np.degrees(angle) % 360:.0f}°"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))

            # Torque indicator
            torque = np.sin(angle) * (1 if commutator_state == 0 else -1)
            # With commutator, torque is always positive (same direction)
            effective_torque = abs(np.sin(angle))
            frame_data.append(go.Scatter(
                x=[0], y=[-2.3],
                mode="text",
                text=[f"Torque: {effective_torque:.2f} (always same direction!)"],
                textfont=dict(size=12, color="lime"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>DC Motor Operation</b><br><sub>Commutator reverses current to maintain rotation direction</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3, 2.5], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.8, y=1),
                plot_bgcolor="rgba(20, 20, 40, 1)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 40, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    dc_motor_fig = create_dc_motor_animation()
    dc_motor_fig
    return (create_dc_motor_animation, dc_motor_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### How the DC Motor Works

        Watch the animation and notice:

        1. **The coil rotates** because current-carrying wires in a magnetic field experience force
        2. **The commutator** (split ring) reverses the current direction every half-turn
        3. **The torque** is always in the same rotational direction (that's the commutator's job!)

        Without the commutator, the coil would oscillate back and forth instead of rotating
        continuously. The commutator is the key invention that makes DC motors work.

        **The torque varies** with angle: maximum when the coil is horizontal (wires perpendicular
        to field), zero when vertical (wires parallel to field). Real motors use multiple coils
        at different angles to smooth out the torque.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 6. The AC Induction Motor

        ### Tesla's Elegant Invention

        The **AC induction motor**, invented by Nikola Tesla in 1887, is perhaps the most
        important motor in the world. It powers:

        - Industrial machinery
        - Air conditioners and refrigerators
        - Electric vehicles (Tesla cars use AC induction motors!)
        - Fans, pumps, and compressors

        The genius of the induction motor: **it has no brushes or commutator**. The rotor
        isn't even connected to the power supply! Instead, it uses electromagnetic induction
        to create currents in the rotor.

        ### The Rotating Magnetic Field

        The key innovation is creating a **rotating magnetic field** using AC power. With
        three-phase AC (or clever wiring with single-phase), the magnetic field rotates
        around the stator, dragging the rotor along with it.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: AC Induction Motor with rotating magnetic field
    def create_ac_motor_animation():
        n_frames = 120
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi
            frame_data = []

            # Stator (outer ring with coils)
            stator_theta = np.linspace(0, 2 * np.pi, 100)
            stator_r_outer = 2.0
            stator_r_inner = 1.6

            frame_data.append(go.Scatter(
                x=stator_r_outer * np.cos(stator_theta),
                y=stator_r_outer * np.sin(stator_theta),
                mode="lines",
                line=dict(color="gray", width=3),
                name="Stator",
            ))
            frame_data.append(go.Scatter(
                x=stator_r_inner * np.cos(stator_theta),
                y=stator_r_inner * np.sin(stator_theta),
                mode="lines",
                line=dict(color="gray", width=3),
                showlegend=False,
            ))

            # Three-phase stator coils (at 0°, 120°, 240°)
            phases = [0, 2 * np.pi / 3, 4 * np.pi / 3]
            phase_colors = ["red", "green", "blue"]
            phase_names = ["Phase A", "Phase B", "Phase C"]

            for i, (phase, color, name) in enumerate(zip(phases, phase_colors, phase_names)):
                # Current in each phase (sinusoidal, offset by 120°)
                current = np.sin(t - phase)
                intensity = abs(current)

                # Coil position
                coil_angle = phase
                coil_x = 1.8 * np.cos(coil_angle)
                coil_y = 1.8 * np.sin(coil_angle)

                # Opposite coil
                opp_x = 1.8 * np.cos(coil_angle + np.pi)
                opp_y = 1.8 * np.sin(coil_angle + np.pi)

                frame_data.append(go.Scatter(
                    x=[coil_x, opp_x],
                    y=[coil_y, opp_y],
                    mode="markers",
                    marker=dict(size=15 + 10 * intensity,
                               color=color,
                               opacity=0.3 + 0.7 * intensity),
                    name=name,
                ))

            # Rotating magnetic field (the sum of all three phases)
            # The resultant field rotates at the AC frequency
            B_x = 0
            B_y = 0
            for i, phase in enumerate(phases):
                current = np.sin(t - phase)
                # Each coil contributes to field along its axis
                B_x += current * np.cos(phase)
                B_y += current * np.sin(phase)

            B_magnitude = np.sqrt(B_x**2 + B_y**2)
            B_angle = np.arctan2(B_y, B_x)

            # Show rotating B field vector
            frame_data.append(go.Scatter(
                x=[0, 1.2 * np.cos(B_angle)],
                y=[0, 1.2 * np.sin(B_angle)],
                mode="lines+markers",
                line=dict(color="yellow", width=5),
                marker=dict(size=[5, 12], color="yellow", symbol=["circle", "triangle-up"]),
                name="Rotating B field",
            ))

            # Rotor (squirrel cage - conducting bars)
            # Rotor lags slightly behind the field (slip)
            slip = 0.05  # 5% slip
            rotor_angle = t * (1 - slip)

            rotor_r = 1.4
            n_bars = 12

            for i in range(n_bars):
                bar_angle = rotor_angle + i * 2 * np.pi / n_bars
                bar_x = rotor_r * np.cos(bar_angle)
                bar_y = rotor_r * np.sin(bar_angle)

                # Induced current in bar depends on relative motion to B field
                relative_angle = bar_angle - B_angle
                induced_current = np.sin(relative_angle) * slip * 5  # Proportional to slip

                bar_alpha = min(1.0, 0.3 + 0.7 * abs(induced_current))
                bar_color = f"rgba(255, 165, 0, {bar_alpha:.3f})"

                frame_data.append(go.Scatter(
                    x=[bar_x * 0.3, bar_x],
                    y=[bar_y * 0.3, bar_y],
                    mode="lines",
                    line=dict(color=bar_color, width=6),
                    showlegend=(i == 0),
                    name="Rotor bars" if i == 0 else None,
                ))

            # Rotor end rings
            rotor_inner = np.linspace(0, 2 * np.pi, 50)
            frame_data.append(go.Scatter(
                x=0.3 * np.cos(rotor_inner),
                y=0.3 * np.sin(rotor_inner),
                mode="lines",
                line=dict(color="orange", width=4),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=rotor_r * np.cos(rotor_inner),
                y=rotor_r * np.sin(rotor_inner),
                mode="lines",
                line=dict(color="orange", width=4),
                showlegend=False,
            ))

            # Rotor position indicator
            frame_data.append(go.Scatter(
                x=[0, 0.8 * np.cos(rotor_angle)],
                y=[0, 0.8 * np.sin(rotor_angle)],
                mode="lines",
                line=dict(color="white", width=3, dash="dash"),
                name="Rotor position",
            ))

            # Info text
            frame_data.append(go.Scatter(
                x=[0], y=[2.8],
                mode="text",
                text=[f"Field angle: {np.degrees(B_angle) % 360:.0f}° | Rotor: {np.degrees(rotor_angle) % 360:.0f}° | Slip: {slip*100:.0f}%"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>AC Induction Motor</b><br><sub>Three-phase creates rotating field that drags rotor</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-2.5, 3.2], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.75, y=0.25),
                plot_bgcolor="rgba(20, 20, 40, 1)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 40, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    ac_motor_fig = create_ac_motor_animation()
    ac_motor_fig
    return (create_ac_motor_animation, ac_motor_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### How the Induction Motor Works

        The animation shows the key principles:

        1. **Three-phase AC** in the stator coils (red, green, blue) creates a rotating magnetic field
        2. **The field rotates** at the AC frequency (yellow arrow)
        3. **The rotor bars** (orange) have currents induced in them by the changing flux
        4. **These induced currents** experience forces that drag the rotor around

        **The slip is essential:** If the rotor caught up with the field, there would be no
        relative motion, no changing flux, no induced current, and no torque! The rotor must
        always lag behind the field by a few percent (the "slip").

        **Why it's so popular:**
        - No brushes = no sparks, no wear, no maintenance
        - Robust construction (no commutator to damage)
        - Works directly on AC power
        - Extremely reliable
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 7. The Stepper Motor

        ### Precise Digital Control

        **Stepper motors** move in discrete steps rather than continuous rotation. They're
        used wherever precise positioning is needed:

        - 3D printers
        - CNC machines
        - Camera focus mechanisms
        - Hard drive heads (older drives)
        - Robotic arms

        The motor has multiple coils that are energized in sequence. Each step moves the
        rotor by a fixed angle (commonly 1.8° = 200 steps per revolution).
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Stepper motor operation
    def create_stepper_animation():
        n_frames = 100
        frames = []

        steps_per_rev = 8  # Simplified for visualization
        step_angle = 2 * np.pi / steps_per_rev

        for frame in range(n_frames):
            # Current step (changes discretely)
            current_step = (frame // 12) % steps_per_rev
            target_angle = current_step * step_angle

            # Rotor angle (moves toward target with some dynamics)
            # Simple model: rotor snaps to position
            rotor_angle = target_angle

            frame_data = []

            # Stator with coils
            stator_r = 2.0

            # Four coil pairs (A, B, C, D) at 0°, 45°, 90°, 135°
            n_coils = 4
            coil_angles = [i * np.pi / 4 for i in range(n_coils)]
            coil_names = ["Coil A", "Coil B", "Coil C", "Coil D"]
            coil_colors = ["red", "green", "blue", "purple"]

            # Activation pattern: energize coils in sequence
            # Step 0: A, Step 1: A+B, Step 2: B, Step 3: B+C, etc.
            active_coils = []
            if current_step % 2 == 0:
                active_coils = [(current_step // 2) % n_coils]
            else:
                active_coils = [(current_step // 2) % n_coils, ((current_step // 2) + 1) % n_coils]

            for i, (angle, name, color) in enumerate(zip(coil_angles, coil_names, coil_colors)):
                is_active = i in active_coils
                intensity = 1.0 if is_active else 0.3

                # Coil representation
                coil_x = stator_r * np.cos(angle)
                coil_y = stator_r * np.sin(angle)
                opp_x = stator_r * np.cos(angle + np.pi)
                opp_y = stator_r * np.sin(angle + np.pi)

                frame_data.append(go.Scatter(
                    x=[coil_x], y=[coil_y],
                    mode="markers",
                    marker=dict(size=25, color=color, opacity=intensity,
                               symbol="square"),
                    name=name + (" (ON)" if is_active else ""),
                ))
                frame_data.append(go.Scatter(
                    x=[opp_x], y=[opp_y],
                    mode="markers",
                    marker=dict(size=25, color=color, opacity=intensity,
                               symbol="square"),
                    showlegend=False,
                ))

                # Magnetic field from active coils
                if is_active:
                    frame_data.append(go.Scatter(
                        x=[coil_x * 0.7, opp_x * 0.7],
                        y=[coil_y * 0.7, opp_y * 0.7],
                        mode="lines",
                        line=dict(color=color, width=2, dash="dot"),
                        showlegend=False,
                    ))

            # Rotor (permanent magnet with N/S poles)
            rotor_r = 1.2

            # Rotor body
            rotor_theta = np.linspace(0, 2 * np.pi, 50)
            frame_data.append(go.Scatter(
                x=0.8 * np.cos(rotor_theta),
                y=0.8 * np.sin(rotor_theta),
                mode="lines",
                fill="toself",
                fillcolor="rgba(100, 100, 100, 0.5)",
                line=dict(color="white", width=2),
                name="Rotor",
            ))

            # N pole (red)
            n_angle = rotor_angle
            frame_data.append(go.Scatter(
                x=[0, rotor_r * np.cos(n_angle)],
                y=[0, rotor_r * np.sin(n_angle)],
                mode="lines+markers+text",
                line=dict(color="red", width=8),
                marker=dict(size=[0, 15], color="red"),
                text=["", "N"],
                textposition="top center",
                textfont=dict(size=14, color="red"),
                showlegend=False,
            ))

            # S pole (blue)
            s_angle = rotor_angle + np.pi
            frame_data.append(go.Scatter(
                x=[0, rotor_r * np.cos(s_angle)],
                y=[0, rotor_r * np.sin(s_angle)],
                mode="lines+markers+text",
                line=dict(color="blue", width=8),
                marker=dict(size=[0, 15], color="blue"),
                text=["", "S"],
                textposition="bottom center",
                textfont=dict(size=14, color="blue"),
                showlegend=False,
            ))

            # Step counter
            frame_data.append(go.Scatter(
                x=[0], y=[2.8],
                mode="text",
                text=[f"Step: {current_step + 1}/{steps_per_rev} | Angle: {np.degrees(rotor_angle):.1f}°"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))

            # Active coils indicator
            active_names = [coil_names[i] for i in active_coils]
            frame_data.append(go.Scatter(
                x=[0], y=[-2.8],
                mode="text",
                text=[f"Active: {', '.join(active_names)}"],
                textfont=dict(size=12, color="yellow"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Stepper Motor</b><br><sub>Discrete steps by sequential coil activation</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3.2, 3.2], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.8, y=1),
                plot_bgcolor="rgba(20, 20, 40, 1)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    stepper_fig = create_stepper_animation()
    stepper_fig
    return (create_stepper_animation, stepper_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### How the Stepper Motor Works

        The animation shows **half-stepping** (energizing one or two coils at a time):

        1. **Coil A** energized → rotor aligns with A
        2. **Coils A and B** energized → rotor moves to halfway between
        3. **Coil B** energized → rotor aligns with B
        4. And so on...

        **Key advantages:**
        - **Open-loop control**: no feedback sensor needed (the motor "knows" where it is)
        - **Precise positioning**: moves exactly the commanded number of steps
        - **Holding torque**: maintains position when stopped (coils stay energized)

        **Trade-offs:**
        - Lower efficiency than DC motors
        - Can miss steps if overloaded
        - Resonance issues at certain speeds
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 8. The Generator

        ### Motors in Reverse

        A **generator** is simply a motor run backward. Instead of putting in electricity
        to get motion, we put in motion to get electricity.

        The physics is Faraday's law: rotating a coil in a magnetic field changes the
        magnetic flux through the coil, inducing an EMF:

        $$\mathcal{E} = NBA\omega\sin(\omega t)$$

        where $N$ is the number of turns, $B$ is the field strength, $A$ is the coil area,
        and $\omega$ is the angular velocity.

        This produces **alternating current** (AC) naturally! The voltage oscillates as
        the coil rotates.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: AC Generator
    def create_generator_animation():
        n_frames = 120
        frames = []

        # Store voltage history for the graph
        voltage_history = []

        for frame in range(n_frames):
            angle = frame / n_frames * 4 * np.pi  # Two full rotations
            frame_data = []

            # EMF = sin(angle)
            emf = np.sin(angle)
            voltage_history.append(emf)

            # Magnetic field (horizontal arrows)
            for y_pos in [-0.8, 0, 0.8]:
                frame_data.append(go.Scatter(
                    x=[-3, -2], y=[y_pos, y_pos],
                    mode="lines+markers",
                    line=dict(color="rgba(100, 100, 255, 0.5)", width=2),
                    marker=dict(size=[0, 8], symbol=["circle", "triangle-right"],
                               color="rgba(100, 100, 255, 0.5)"),
                    showlegend=(y_pos == 0),
                    name="B field" if y_pos == 0 else None,
                ))

            # Rotating coil
            coil_width = 1.5
            coil_height = 1.0

            # Project coil into page (we see it edge-on as it rotates)
            # When angle=0, coil is edge-on (vertical line)
            # When angle=90°, coil is face-on (rectangle)

            apparent_width = coil_width * abs(np.cos(angle))

            # Coil representation
            coil_x = [-apparent_width/2, apparent_width/2, apparent_width/2, -apparent_width/2, -apparent_width/2]
            coil_y = [-coil_height/2, -coil_height/2, coil_height/2, coil_height/2, -coil_height/2]

            frame_data.append(go.Scatter(
                x=coil_x, y=coil_y,
                mode="lines",
                line=dict(color="orange", width=4),
                fill="toself",
                fillcolor="rgba(255, 165, 0, 0.2)",
                name="Rotating coil",
            ))

            # Rotation axis (into page)
            frame_data.append(go.Scatter(
                x=[0], y=[0],
                mode="markers",
                marker=dict(size=10, color="white", symbol="circle"),
                name="Axis",
            ))

            # Slip rings and brushes
            frame_data.append(go.Scatter(
                x=[-0.3, 0.3], y=[-1.8, -1.8],
                mode="markers",
                marker=dict(size=15, color="gold", symbol="square"),
                name="Slip rings",
            ))

            # Output wires
            frame_data.append(go.Scatter(
                x=[-0.3, -0.3, -1], y=[-1.8, -2.5, -2.5],
                mode="lines",
                line=dict(color="red", width=3),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[0.3, 0.3, 1], y=[-1.8, -2.5, -2.5],
                mode="lines",
                line=dict(color="blue", width=3),
                showlegend=False,
            ))

            # Voltage graph (right side)
            time_axis = np.linspace(0, 4 * np.pi, len(voltage_history))
            frame_data.append(go.Scatter(
                x=2 + time_axis[-60:] / (4 * np.pi) * 2 if len(voltage_history) > 60 else 2 + time_axis / (4 * np.pi) * 2,
                y=[v * 0.8 for v in voltage_history[-60:]] if len(voltage_history) > 60 else [v * 0.8 for v in voltage_history],
                mode="lines",
                line=dict(color="lime", width=2),
                name="Output voltage",
            ))

            # Current voltage indicator
            frame_data.append(go.Scatter(
                x=[4.2], y=[emf * 0.8],
                mode="markers",
                marker=dict(size=10, color="lime"),
                showlegend=False,
            ))

            # Voltage axis
            frame_data.append(go.Scatter(
                x=[2, 4.2], y=[0, 0],
                mode="lines",
                line=dict(color="white", width=1, dash="dash"),
                showlegend=False,
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[0], y=[2],
                mode="text",
                text=[f"Angle: {np.degrees(angle) % 360:.0f}°"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[3], y=[1.5],
                mode="text",
                text=[f"EMF = {emf:.2f} V"],
                textfont=dict(size=12, color="lime"),
                showlegend=False,
            ))

            # Flux indicator
            flux = np.cos(angle)  # Flux is max when coil is face-on
            frame_data.append(go.Scatter(
                x=[0], y=[-3],
                mode="text",
                text=[f"Flux through coil: Φ = {flux:.2f} (max when face-on)"],
                textfont=dict(size=11, color="cyan"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>AC Generator</b><br><sub>Rotating coil in magnetic field produces alternating voltage</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3.5, 5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3.5, 2.5], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.7, y=1),
                plot_bgcolor="rgba(20, 20, 40, 1)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=0,
                        x=0.1,
                        buttons=[
                            dict(label="Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 40, "redraw": True},
                                             "fromcurrent": True}]),
                            dict(label="Pause",
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

    generator_fig = create_generator_animation()
    generator_fig
    return (create_generator_animation, generator_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### How the Generator Works

        Watch the animation:

        1. **The coil rotates** in the magnetic field (driven by external mechanical power)
        2. **The flux through the coil changes** as its orientation changes
        3. **Faraday's law** tells us this changing flux induces an EMF
        4. **The voltage oscillates** sinusoidally—this is AC power!

        **Key observation:** The EMF is maximum when the coil is edge-on (flux changing fastest)
        and zero when face-on (flux momentarily constant). This is why:

        $$\mathcal{E} = -\frac{d\Phi}{dt} = NBA\omega\sin(\omega t)$$

        The sine function comes from the geometry of rotation.

        **Note:** Unlike a DC motor, a generator uses **slip rings** (continuous rings) rather
        than a commutator. This preserves the AC nature of the output.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: From Oersted to Electric Vehicles

        | Discovery/Invention | Year | Key Principle | Application |
        |---------------------|------|---------------|-------------|
        | **Oersted** | 1820 | Current creates magnetic field | Electromagnets |
        | **Faraday** | 1831 | Changing flux induces EMF | Generators, transformers |
        | **DC Motor** | 1832 | $\mathbf{F} = I\mathbf{L} \times \mathbf{B}$ | Power tools, vehicles |
        | **AC Induction Motor** | 1887 | Rotating field induces rotor current | Industrial machinery |
        | **Stepper Motor** | 1960s | Sequential coil activation | Precision positioning |

        ### The Beautiful Unity

        All these devices—motors, generators, transformers—are manifestations of the same
        fundamental physics:

        1. **Moving charges create magnetic fields** (Ampère's law)
        2. **Changing magnetic fields create electric fields** (Faraday's law)
        3. **Magnetic fields exert forces on moving charges** (Lorentz force)

        These three principles, unified in Maxwell's equations, explain everything from
        compass needles to MRI machines, from bicycle dynamos to the electric grid.

        ---

        > *"The electrical force, like the gravitational force, decreases inversely as the
        > square of the distance... but the thing that is remarkable is that light turns out
        > to be part of the same thing—electricity and magnetism."*
        > — Richard Feynman

        The unification of electricity, magnetism, and light is one of the greatest
        achievements in the history of physics—and it all started with a compass needle
        deflecting near a wire.
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

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1964). *The Feynman Lectures on Physics, Volume II*.
          Addison-Wesley.
          - [Chapter 1: Electromagnetism](https://www.feynmanlectures.caltech.edu/II_01.html)
          - [Chapter 13: Magnetostatics](https://www.feynmanlectures.caltech.edu/II_13.html)
          - [Chapter 14: The Magnetic Field in Various Situations](https://www.feynmanlectures.caltech.edu/II_14.html)
          - [Chapter 16: Induced Currents](https://www.feynmanlectures.caltech.edu/II_16.html) — Motors and forces on wires
          - [Chapter 17: The Laws of Induction](https://www.feynmanlectures.caltech.edu/II_17.html) — Faraday's law, generators
          - [Chapter 34: The Magnetism of Matter](https://www.feynmanlectures.caltech.edu/II_34.html)
          - [Chapter 36: Ferromagnetism](https://www.feynmanlectures.caltech.edu/II_36.html)

        ### Mathematical Background

        - **Biot-Savart Law** (1820)
          - $d\mathbf{B} = \frac{\mu_0}{4\pi} \frac{I \, d\mathbf{l} \times \hat{\mathbf{r}}}{r^2}$
          - Magnetic field from a current element

        - **Ampère's Law**
          - $\oint \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{enc}$
          - Relates magnetic field to enclosed current

        - **Faraday's Law of Induction** (1831)
          - $\mathcal{E} = -\frac{d\Phi_B}{dt}$
          - Changing magnetic flux induces EMF

        - **Lorentz Force Law**
          - $\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$
          - Force on a charged particle

        - **Magnetic field of a solenoid**
          - $B = \mu_0 n I$ (inside, uniform)
          - $n$ = turns per unit length

        ### Key Constants

        - Permeability of free space: $\mu_0 = 4\pi \times 10^{-7}$ T·m/A
        - Permittivity of free space: $\epsilon_0 = 8.854 \times 10^{-12}$ F/m
        - Speed of light: $c = 1/\sqrt{\mu_0 \epsilon_0}$

        ### Historical References

        - **Oersted, H. C.** (1820). Discovery of electromagnetism.
        - **Faraday, M.** (1831). Discovery of electromagnetic induction.
        - **Maxwell, J. C.** (1865). Unified theory of electromagnetism.
        - **Tesla, N.** (1887). AC induction motor patent.

        ### Further Reading

        - Griffiths, D. J. *Introduction to Electrodynamics* — Standard undergraduate text
        - Purcell, E. M. & Morin, D. J. *Electricity and Magnetism* — Elegant treatment
        - Hughes, A. & Drury, B. *Electric Motors and Drives* — Engineering applications
        """
    )
    return


if __name__ == "__main__":
    app.run()
