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
        # The Motion of Charges in Electric and Magnetic Fields

        *An interactive exploration based on [Feynman Lectures on Physics, Volume II, Chapter 29](https://www.feynmanlectures.caltech.edu/II_29.html)*

        ---

        ## Steering the Invisible

        Charged particles are the workhorses of modern technology. We use electric and magnetic
        fields to push, steer, focus, and accelerate them in:

        - **Television and computer monitors** (older CRT displays)
        - **Electron microscopes** that see individual atoms
        - **Mass spectrometers** that identify molecules
        - **Particle accelerators** that probe the fundamental structure of matter
        - **Fusion reactors** that confine plasma at 100 million degrees

        The physics is elegantly simple: the **Lorentz force** governs everything.

        $$\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$$

        This single equation tells us how any charged particle responds to any combination
        of electric and magnetic fields. Let's explore its consequences.

        > *"The motion of a charged particle in given electric and magnetic fields can
        > always be worked out once we know the charge and mass of the particle."*
        > — Richard Feynman
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 1. Motion in a Uniform Electric Field

        ### The Simplest Case: Constant Acceleration

        In a uniform electric field $\mathbf{E}$, a charged particle experiences a constant force:

        $$\mathbf{F} = q\mathbf{E}$$

        This is exactly like gravity! The particle accelerates uniformly:

        $$\mathbf{a} = \frac{q\mathbf{E}}{m}$$

        **Key insight:** The acceleration depends on the **charge-to-mass ratio** $q/m$. This
        ratio is fundamental—it determines how responsive a particle is to electromagnetic fields.

        For an electron: $q/m = 1.76 \times 10^{11}$ C/kg (enormous!)

        This huge ratio is why electrons are so easy to deflect and accelerate. It's also why
        electron beams were used in old TV tubes—they could be steered quickly with small voltages.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Charged particle in uniform electric field (like a CRT)
    def create_electric_field_animation():
        n_frames = 80
        frames = []

        # Initial conditions
        v0_x = 2.0  # Initial horizontal velocity
        v0_y = 0.0  # No initial vertical velocity
        E_field = 1.5  # Electric field strength (pointing down, so positive charge deflects down)
        q_over_m = 1.0  # Normalized charge-to-mass ratio

        for frame in range(n_frames):
            t = frame / n_frames * 3.0  # Time
            frame_data = []

            # Particle position (parabolic trajectory)
            x = v0_x * t
            y = 2.0 - 0.5 * q_over_m * E_field * t**2  # Starts at y=2, deflects down

            # Velocity components
            v_x = v0_x
            v_y = -q_over_m * E_field * t

            # Electric field region (shaded area)
            frame_data.append(go.Scatter(
                x=[0, 6, 6, 0, 0],
                y=[3, 3, -1, -1, 3],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 255, 100, 0.1)",
                line=dict(color="rgba(255, 255, 0, 0.3)", width=1),
                name="E field region",
            ))

            # Electric field arrows (pointing down)
            for x_pos in [1, 2, 3, 4, 5]:
                for y_pos in [2.5, 1.5, 0.5, -0.5]:
                    frame_data.append(go.Scatter(
                        x=[x_pos, x_pos],
                        y=[y_pos, y_pos - 0.4],
                        mode="lines+markers",
                        line=dict(color="rgba(255, 200, 0, 0.4)", width=2),
                        marker=dict(size=[0, 6], symbol=["circle", "triangle-down"],
                                   color="rgba(255, 200, 0, 0.4)"),
                        showlegend=False,
                    ))

            # Capacitor plates
            frame_data.append(go.Scatter(
                x=[0, 6], y=[3.2, 3.2],
                mode="lines",
                line=dict(color="red", width=8),
                name="+ plate",
            ))
            frame_data.append(go.Scatter(
                x=[0, 6], y=[-1.2, -1.2],
                mode="lines",
                line=dict(color="blue", width=8),
                name="− plate",
            ))

            # Trajectory trace
            t_trace = np.linspace(0, t, 50)
            x_trace = v0_x * t_trace
            y_trace = 2.0 - 0.5 * q_over_m * E_field * t_trace**2

            frame_data.append(go.Scatter(
                x=x_trace, y=y_trace,
                mode="lines",
                line=dict(color="cyan", width=2, dash="dot"),
                name="Trajectory",
            ))

            # Particle
            frame_data.append(go.Scatter(
                x=[x], y=[y],
                mode="markers",
                marker=dict(size=15, color="cyan", symbol="circle",
                           line=dict(color="white", width=2)),
                name="Electron",
            ))

            # Velocity vector
            v_scale = 0.3
            frame_data.append(go.Scatter(
                x=[x, x + v_x * v_scale],
                y=[y, y + v_y * v_scale],
                mode="lines+markers",
                line=dict(color="lime", width=3),
                marker=dict(size=[0, 8], symbol=["circle", "triangle-right"],
                           color="lime"),
                name="Velocity",
            ))

            # Force vector
            f_scale = 0.5
            frame_data.append(go.Scatter(
                x=[x, x],
                y=[y, y - E_field * f_scale],
                mode="lines+markers",
                line=dict(color="red", width=3),
                marker=dict(size=[0, 8], symbol=["circle", "triangle-down"],
                           color="red"),
                name="Force (qE)",
            ))

            # Info display
            frame_data.append(go.Scatter(
                x=[7], y=[2.5],
                mode="text",
                text=[f"t = {t:.2f}"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[7], y=[2.0],
                mode="text",
                text=[f"vₓ = {v_x:.2f}"],
                textfont=dict(size=11, color="lime"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[7], y=[1.5],
                mode="text",
                text=[f"vᵧ = {v_y:.2f}"],
                textfont=dict(size=11, color="lime"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Electron in Uniform Electric Field</b><br><sub>Parabolic trajectory (like projectile motion)</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-0.5, 8], showgrid=True, zeroline=False, title="x position"),
                yaxis=dict(range=[-2, 4], showgrid=True, zeroline=False, title="y position",
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.75, y=0.15),
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

    electric_field_fig = create_electric_field_animation()
    electric_field_fig
    return (create_electric_field_animation, electric_field_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Trajectory

        The animation shows an electron entering a uniform electric field (between capacitor plates).
        The motion is exactly analogous to projectile motion under gravity:

        - **Horizontal motion**: Constant velocity (no horizontal force)
        - **Vertical motion**: Constant acceleration toward the positive plate

        The trajectory is a **parabola**, described by:

        $$y = y_0 + v_{y0}t - \frac{1}{2}\frac{qE}{m}t^2$$

        **This is how old CRT televisions worked:** Electrons were shot horizontally, then deflected
        vertically by electric (or magnetic) fields to paint the image on the phosphor screen.
        By varying the deflection voltage rapidly, the beam could be steered to any point on the screen.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 2. Motion in a Uniform Magnetic Field

        ### The Circular Dance

        A magnetic field does something fundamentally different from an electric field.
        The force is always **perpendicular** to the velocity:

        $$\mathbf{F} = q\mathbf{v} \times \mathbf{B}$$

        This has profound consequences:

        1. **The magnetic force does no work** (force ⊥ velocity)
        2. **Speed remains constant** (only direction changes)
        3. **The path is circular** (constant centripetal acceleration)

        The radius of this circular motion is found by balancing magnetic force with centripetal force:

        $$qvB = \frac{mv^2}{r} \implies r = \frac{mv}{qB}$$

        This is called the **cyclotron radius** or **Larmor radius**.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Charged particle in uniform magnetic field (circular motion)
    def create_magnetic_circular_animation():
        n_frames = 120
        frames = []

        # Parameters
        B = 1.0  # Magnetic field strength (into page)
        q_over_m = 1.0  # Charge-to-mass ratio
        v = 2.0  # Speed

        # Cyclotron radius
        r = v / (q_over_m * B)

        # Cyclotron frequency
        omega = q_over_m * B

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi / omega * 1.5  # 1.5 complete orbits
            frame_data = []

            # Particle position (circular motion)
            # Starting at (r, 0) moving counterclockwise (for positive charge, B into page)
            theta = omega * t
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # Velocity (tangent to circle)
            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

            # Magnetic field indicators (X symbols for "into page")
            for bx in np.linspace(-4, 4, 5):
                for by in np.linspace(-4, 4, 5):
                    frame_data.append(go.Scatter(
                        x=[bx], y=[by],
                        mode="markers",
                        marker=dict(size=12, color="rgba(100, 100, 255, 0.3)",
                                   symbol="x"),
                        showlegend=False,
                    ))

            # Trajectory trace
            theta_trace = np.linspace(0, theta, 100)
            x_trace = r * np.cos(theta_trace)
            y_trace = r * np.sin(theta_trace)

            frame_data.append(go.Scatter(
                x=x_trace, y=y_trace,
                mode="lines",
                line=dict(color="cyan", width=2, dash="dot"),
                name="Trajectory",
            ))

            # Reference circle
            theta_circle = np.linspace(0, 2 * np.pi, 100)
            frame_data.append(go.Scatter(
                x=r * np.cos(theta_circle),
                y=r * np.sin(theta_circle),
                mode="lines",
                line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                name="Cyclotron orbit",
            ))

            # Particle
            frame_data.append(go.Scatter(
                x=[x], y=[y],
                mode="markers",
                marker=dict(size=18, color="cyan", symbol="circle",
                           line=dict(color="white", width=2)),
                name="Charged particle",
            ))

            # Velocity vector
            v_scale = 0.4
            frame_data.append(go.Scatter(
                x=[x, x + vx * v_scale],
                y=[y, y + vy * v_scale],
                mode="lines+markers",
                line=dict(color="lime", width=3),
                marker=dict(size=[0, 10], symbol=["circle", "arrow"],
                           color="lime", angle=np.degrees(np.arctan2(vy, vx))),
                name="Velocity v",
            ))

            # Force vector (toward center)
            f_scale = 0.5
            fx = -x / r  # Points toward center
            fy = -y / r
            frame_data.append(go.Scatter(
                x=[x, x + fx * f_scale * v],
                y=[y, y + fy * f_scale * v],
                mode="lines+markers",
                line=dict(color="red", width=3),
                marker=dict(size=[0, 10], symbol=["circle", "arrow"],
                           color="red"),
                name="Force F = qv×B",
            ))

            # Center point
            frame_data.append(go.Scatter(
                x=[0], y=[0],
                mode="markers",
                marker=dict(size=8, color="yellow", symbol="cross"),
                name="Center",
            ))

            # Radius line
            frame_data.append(go.Scatter(
                x=[0, x], y=[0, y],
                mode="lines",
                line=dict(color="yellow", width=1, dash="dash"),
                name=f"r = mv/qB = {r:.2f}",
            ))

            # Info box
            frame_data.append(go.Scatter(
                x=[3.5], y=[3.5],
                mode="text",
                text=[f"θ = {np.degrees(theta):.0f}°"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[3.5], y=[3.0],
                mode="text",
                text=[f"|v| = {v:.2f} (constant!)"],
                textfont=dict(size=11, color="lime"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[3.5], y=[2.5],
                mode="text",
                text=["B field: into page ⊗"],
                textfont=dict(size=11, color="rgba(100, 100, 255, 0.8)"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Circular Motion in Magnetic Field</b><br><sub>Force always perpendicular to velocity → circular path</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-5, 5], showgrid=True, zeroline=True, title="x"),
                yaxis=dict(range=[-5, 5], showgrid=True, zeroline=True, title="y",
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.02, y=0.98),
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

    magnetic_circular_fig = create_magnetic_circular_animation()
    magnetic_circular_fig
    return (create_magnetic_circular_animation, magnetic_circular_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Cyclotron Frequency

        Something remarkable emerges from the circular motion: the **frequency of revolution
        is independent of the particle's speed!**

        The period is:
        $$T = \frac{2\pi r}{v} = \frac{2\pi m}{qB}$$

        The cyclotron frequency is:
        $$f_c = \frac{qB}{2\pi m} \quad \text{or} \quad \omega_c = \frac{qB}{m}$$

        **Why this matters:** A faster particle travels in a bigger circle, but it also moves
        faster around that circle. These effects exactly cancel, so all particles with the same
        $q/m$ orbit at the same frequency regardless of their energy.

        This is the key insight behind the **cyclotron** particle accelerator!

        | Particle | Cyclotron frequency in 1 Tesla field |
        |----------|-------------------------------------|
        | Electron | 28 GHz (microwave) |
        | Proton | 15 MHz (radio) |
        | Alpha | 7.6 MHz |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 3. The Mass Spectrometer

        ### Weighing Atoms with Magnetism

        The mass spectrometer is one of the most important analytical instruments in science.
        It can identify atoms and molecules by their mass with extraordinary precision.

        **The principle is elegant:**

        1. **Ionize** the sample (remove or add electrons to create charged particles)
        2. **Accelerate** the ions through a known voltage $V$
        3. **Bend** them in a magnetic field
        4. **Detect** where they land

        The kinetic energy after acceleration:
        $$\frac{1}{2}mv^2 = qV \implies v = \sqrt{\frac{2qV}{m}}$$

        The radius in the magnetic field:
        $$r = \frac{mv}{qB} = \frac{m}{qB}\sqrt{\frac{2qV}{m}} = \frac{1}{B}\sqrt{\frac{2mV}{q}}$$

        **Key result:** The radius depends on $\sqrt{m/q}$. Heavier ions curve less and land
        farther from the entrance.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Mass spectrometer separating isotopes
    def create_mass_spectrometer_animation():
        n_frames = 100
        frames = []

        # Parameters
        B = 1.0  # Magnetic field
        V = 1.0  # Accelerating voltage
        q = 1.0  # Charge (same for all)

        # Three different masses (e.g., isotopes)
        masses = [1.0, 1.1, 1.2]  # Representing e.g., C-12, C-13, C-14
        colors = ["cyan", "lime", "orange"]
        labels = ["m = 1.0 (light)", "m = 1.1 (medium)", "m = 1.2 (heavy)"]

        for frame in range(n_frames):
            progress = frame / n_frames
            frame_data = []

            # Ion source
            frame_data.append(go.Scatter(
                x=[-3.5, -3, -3, -3.5, -3.5],
                y=[-0.5, -0.5, 0.5, 0.5, -0.5],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 100, 100, 0.3)",
                line=dict(color="red", width=2),
                name="Ion source",
            ))

            # Accelerating region
            frame_data.append(go.Scatter(
                x=[-3, -2, -2, -3, -3],
                y=[-0.3, -0.3, 0.3, 0.3, -0.3],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 255, 0, 0.1)",
                line=dict(color="yellow", width=1),
                name="Accelerator (V)",
            ))

            # Magnetic field region (semicircle area)
            theta_region = np.linspace(-np.pi/2, np.pi/2, 50)
            r_region = 4
            x_region = np.concatenate([[-2], -2 + r_region * np.cos(theta_region), [-2]])
            y_region = np.concatenate([[r_region], r_region * np.sin(theta_region), [-r_region]])

            frame_data.append(go.Scatter(
                x=x_region, y=y_region,
                mode="lines",
                fill="toself",
                fillcolor="rgba(100, 100, 255, 0.1)",
                line=dict(color="rgba(100, 100, 255, 0.3)", width=1),
                name="B field region",
            ))

            # Magnetic field indicators
            for bx in np.linspace(-1, 2, 4):
                for by in np.linspace(-2, 2, 5):
                    if bx**2 + by**2 < 12:
                        frame_data.append(go.Scatter(
                            x=[bx], y=[by],
                            mode="markers",
                            marker=dict(size=8, color="rgba(100, 100, 255, 0.3)",
                                       symbol="x"),
                            showlegend=False,
                        ))

            # Detector plate
            frame_data.append(go.Scatter(
                x=[-2.1, -2.1], y=[-3.5, -1],
                mode="lines",
                line=dict(color="white", width=6),
                name="Detector",
            ))

            # Particle trajectories
            for i, (m, color, label) in enumerate(zip(masses, colors, labels)):
                # Velocity after acceleration
                v = np.sqrt(2 * q * V / m)

                # Cyclotron radius
                r = m * v / (q * B)

                # Trajectory: semicircle
                # Starts at (-2, 0) going right, curves down
                theta_max = np.pi * min(progress * 1.2, 1.0)  # Animate the arc
                theta_traj = np.linspace(np.pi/2, np.pi/2 - theta_max, 50)

                x_traj = -2 + r * np.cos(theta_traj)
                y_traj = r + r * np.sin(theta_traj)

                frame_data.append(go.Scatter(
                    x=x_traj, y=y_traj,
                    mode="lines",
                    line=dict(color=color, width=3),
                    name=label,
                ))

                # Particle marker (at end of trajectory)
                if progress > 0.1:
                    x_particle = x_traj[-1]
                    y_particle = y_traj[-1]
                    frame_data.append(go.Scatter(
                        x=[x_particle], y=[y_particle],
                        mode="markers",
                        marker=dict(size=12, color=color),
                        showlegend=False,
                    ))

                # Landing position indicator
                if progress > 0.95:
                    landing_y = r + r * np.sin(np.pi/2 - np.pi)  # = r - r = 0? No...
                    # Actually landing at y = r - r = 0 when theta = -pi/2
                    landing_y = 0  # All land at y where x = -2 - 2r... wait
                    # Let me recalculate. Center at (-2, r). When theta = -pi/2:
                    # x = -2 + r*cos(-pi/2) = -2 + 0 = -2
                    # y = r + r*sin(-pi/2) = r - r = 0
                    # Hmm, they all land at y=0? That's not right for a spectrometer.

                    # Let me fix the geometry. Standard mass spec: ions enter horizontally,
                    # curve in semicircle, land on detector on opposite side.
                    # If entering at (-2, 0) going +x direction, B into page (positive charge):
                    # Force initially in -y direction. So curves down.
                    # Center at (-2, -r). After semicircle (theta = pi), lands at (-2, -2r).

                    landing_y = -2 * r
                    frame_data.append(go.Scatter(
                        x=[-2.3], y=[landing_y],
                        mode="text",
                        text=[f"r={r:.2f}"],
                        textfont=dict(size=10, color=color),
                        showlegend=False,
                    ))

            # Formula display
            frame_data.append(go.Scatter(
                x=[2], y=[3],
                mode="text",
                text=["r = (1/B)√(2mV/q)"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[2], y=[2.5],
                mode="text",
                text=["Heavier ions → larger radius"],
                textfont=dict(size=11, color="yellow"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Mass Spectrometer</b><br><sub>Separating ions by mass using magnetic deflection</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-5, 4], showgrid=False, zeroline=False),
                yaxis=dict(range=[-4, 4], showgrid=False, zeroline=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.6, y=0.95),
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

    mass_spec_fig = create_mass_spectrometer_animation()
    mass_spec_fig
    return (create_mass_spectrometer_animation, mass_spec_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Applications of Mass Spectrometry

        The mass spectrometer has revolutionized many fields:

        **Chemistry & Biochemistry:**
        - Identifying unknown compounds
        - Determining molecular structure
        - Proteomics (identifying proteins)

        **Medicine:**
        - Drug testing
        - Newborn screening for metabolic disorders
        - Cancer biomarker detection

        **Forensics:**
        - Detecting trace evidence
        - Identifying explosives and drugs

        **Archaeology & Geology:**
        - Carbon-14 dating
        - Determining isotope ratios in ancient samples

        **Space Science:**
        - Analyzing atmospheres of planets and moons
        - Mass spectrometers on Mars rovers

        The precision is remarkable: modern instruments can distinguish masses differing by
        less than one part in a million!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 4. The Cyclotron

        ### Accelerating Particles to High Energies

        The **cyclotron**, invented by Ernest Lawrence in 1930, was the first practical
        particle accelerator. It exploits the fact that cyclotron frequency is independent
        of energy.

        **How it works:**

        1. Ions start at the center between two D-shaped electrodes ("dees")
        2. An oscillating voltage accelerates them each time they cross the gap
        3. The magnetic field bends them in semicircles
        4. They spiral outward, gaining energy with each crossing
        5. When they reach the edge, they're extracted at high energy

        The key insight: the AC frequency is fixed at $f_c = qB/(2\pi m)$. The particles
        automatically stay in sync because faster particles take bigger circles but still
        complete each semicircle in the same time!
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Cyclotron accelerator
    def create_cyclotron_animation():
        n_frames = 200
        frames = []

        # Parameters
        B = 1.0
        q_over_m = 1.0
        omega_c = q_over_m * B  # Cyclotron frequency
        energy_gain = 0.1  # Energy gained per gap crossing

        for frame in range(n_frames):
            t = frame / n_frames * 8 * np.pi / omega_c  # Multiple orbits
            frame_data = []

            # Calculate particle trajectory (spiral)
            # Energy increases discretely at gap crossings
            n_crossings = int(omega_c * t / np.pi)  # Number of gap crossings
            current_energy = 0.5 + n_crossings * energy_gain
            v = np.sqrt(2 * current_energy)
            r = v / (q_over_m * B)

            # Angle within current semicircle
            theta = omega_c * t

            # Position
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # Draw the dees
            theta_dee = np.linspace(0, np.pi, 50)
            r_dee = 4.0

            # Upper dee (D1)
            x_d1 = np.concatenate([[0], r_dee * np.cos(theta_dee), [0]])
            y_d1 = np.concatenate([[0], r_dee * np.sin(theta_dee), [0]])

            # Voltage oscillation
            voltage_phase = omega_c * t
            v_d1 = np.sin(voltage_phase)
            color_d1 = "rgba(255, 100, 100, 0.3)" if v_d1 > 0 else "rgba(100, 100, 255, 0.3)"
            color_d2 = "rgba(100, 100, 255, 0.3)" if v_d1 > 0 else "rgba(255, 100, 100, 0.3)"

            frame_data.append(go.Scatter(
                x=x_d1, y=y_d1,
                mode="lines",
                fill="toself",
                fillcolor=color_d1,
                line=dict(color="gray", width=2),
                name="Dee 1",
            ))

            # Lower dee (D2)
            x_d2 = np.concatenate([[0], r_dee * np.cos(theta_dee + np.pi), [0]])
            y_d2 = np.concatenate([[0], r_dee * np.sin(theta_dee + np.pi), [0]])

            frame_data.append(go.Scatter(
                x=x_d2, y=y_d2,
                mode="lines",
                fill="toself",
                fillcolor=color_d2,
                line=dict(color="gray", width=2),
                name="Dee 2",
            ))

            # Gap region
            frame_data.append(go.Scatter(
                x=[-0.3, 0.3, 0.3, -0.3, -0.3],
                y=[-4.2, -4.2, 4.2, 4.2, -4.2],
                mode="lines",
                line=dict(color="yellow", width=1, dash="dash"),
                name="Acceleration gap",
            ))

            # Spiral trajectory trace
            t_trace = np.linspace(0, t, 300)
            x_trace = []
            y_trace = []
            for tt in t_trace:
                n_cross = int(omega_c * tt / np.pi)
                e = 0.5 + n_cross * energy_gain
                v_t = np.sqrt(2 * e)
                r_t = v_t / (q_over_m * B)
                theta_t = omega_c * tt
                x_trace.append(r_t * np.cos(theta_t))
                y_trace.append(r_t * np.sin(theta_t))

            frame_data.append(go.Scatter(
                x=x_trace, y=y_trace,
                mode="lines",
                line=dict(color="cyan", width=1),
                name="Spiral path",
            ))

            # Particle
            frame_data.append(go.Scatter(
                x=[x], y=[y],
                mode="markers",
                marker=dict(size=12, color="cyan",
                           line=dict(color="white", width=2)),
                name="Particle",
            ))

            # Magnetic field indicators (around edge)
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                bx = 4.5 * np.cos(angle)
                by = 4.5 * np.sin(angle)
                frame_data.append(go.Scatter(
                    x=[bx], y=[by],
                    mode="markers",
                    marker=dict(size=10, color="rgba(100, 100, 255, 0.4)",
                               symbol="x"),
                    showlegend=False,
                ))

            # Info display
            frame_data.append(go.Scatter(
                x=[0], y=[5.5],
                mode="text",
                text=[f"Orbits: {n_crossings//2} | Energy: {current_energy:.2f} | Radius: {r:.2f}"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))

            # Voltage indicator
            frame_data.append(go.Scatter(
                x=[5], y=[0],
                mode="text",
                text=[f"V = {v_d1:.2f}"],
                textfont=dict(size=11, color="yellow"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Cyclotron</b><br><sub>Particles spiral outward, gaining energy at each gap crossing</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-6, 6], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-5.5, 6], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.75, y=0.2),
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
                                 args=[None, {"frame": {"duration": 30, "redraw": True},
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

    cyclotron_fig = create_cyclotron_animation()
    cyclotron_fig
    return (create_cyclotron_animation, cyclotron_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Cyclotron's Limitations

        The cyclotron works beautifully up to a point, but it has a fundamental limitation:
        **relativistic effects**.

        As particles approach the speed of light, their mass increases:
        $$m = \gamma m_0 = \frac{m_0}{\sqrt{1 - v^2/c^2}}$$

        This means the cyclotron frequency decreases:
        $$\omega = \frac{qB}{\gamma m_0}$$

        The particles fall out of sync with the fixed AC frequency!

        **Solutions:**
        - **Synchrocyclotron**: Decrease the AC frequency as particles speed up
        - **Synchrotron**: Increase the magnetic field as particles speed up (used in modern accelerators like the LHC)
        - **Isochronous cyclotron**: Shape the magnetic field to compensate

        Lawrence's first cyclotron (1930) was 4 inches in diameter and accelerated protons
        to 80 keV. Today's largest synchrotron (LHC) is 27 km in circumference and reaches
        6.5 TeV—almost 100 million times more energy!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 5. The Velocity Selector

        ### Crossed Electric and Magnetic Fields

        When electric and magnetic fields are perpendicular to each other AND to the particle
        velocity, something interesting happens. The forces can cancel!

        For a particle moving with velocity $v$ in the x-direction:
        - Electric force: $F_E = qE$ (let's say in +y direction)
        - Magnetic force: $F_B = qvB$ (in -y direction if B is in z)

        The forces balance when:
        $$qE = qvB \implies v = \frac{E}{B}$$

        **Only particles with this specific velocity pass through undeflected!**

        This is called a **velocity selector** or **Wien filter**. It's used to:
        - Select particles of known velocity for experiments
        - Filter ion beams in mass spectrometers
        - Measure the charge-to-mass ratio of particles
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Velocity selector (crossed E and B fields)
    def create_velocity_selector_animation():
        n_frames = 100
        frames = []

        # Fields
        E = 1.0  # Electric field (pointing up)
        B = 1.0  # Magnetic field (into page)
        v_select = E / B  # Selected velocity

        # Three particles with different velocities
        velocities = [v_select * 0.7, v_select, v_select * 1.3]
        colors = ["orange", "lime", "cyan"]
        labels = ["Too slow (deflects up)", "Just right (passes)", "Too fast (deflects down)"]

        for frame in range(n_frames):
            t = frame / n_frames * 4.0
            frame_data = []

            # Selector region
            frame_data.append(go.Scatter(
                x=[0, 5, 5, 0, 0],
                y=[-2, -2, 2, 2, -2],
                mode="lines",
                fill="toself",
                fillcolor="rgba(100, 100, 100, 0.2)",
                line=dict(color="gray", width=2),
                name="Selector region",
            ))

            # Electric field arrows
            for x_pos in [0.5, 1.5, 2.5, 3.5, 4.5]:
                frame_data.append(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[-1.5, -0.8],
                    mode="lines+markers",
                    line=dict(color="rgba(255, 200, 0, 0.5)", width=2),
                    marker=dict(size=[0, 6], symbol=["circle", "triangle-up"],
                               color="rgba(255, 200, 0, 0.5)"),
                    showlegend=(x_pos == 0.5),
                    name="E field (up)" if x_pos == 0.5 else None,
                ))

            # Magnetic field indicators
            for x_pos in [1, 2, 3, 4]:
                for y_pos in [-1, 0, 1]:
                    frame_data.append(go.Scatter(
                        x=[x_pos], y=[y_pos],
                        mode="markers",
                        marker=dict(size=10, color="rgba(100, 100, 255, 0.4)",
                                   symbol="x"),
                        showlegend=False,
                    ))

            # Plates
            frame_data.append(go.Scatter(
                x=[0, 5], y=[2.2, 2.2],
                mode="lines",
                line=dict(color="red", width=6),
                name="+ plate",
            ))
            frame_data.append(go.Scatter(
                x=[0, 5], y=[-2.2, -2.2],
                mode="lines",
                line=dict(color="blue", width=6),
                name="− plate",
            ))

            # Particle trajectories
            for v, color, label in zip(velocities, colors, labels):
                # Net acceleration
                # F_E = qE (up), F_B = qvB (down for positive charge, v in +x, B into page)
                # a = (E - vB) * (q/m), let q/m = 1
                a = E - v * B

                # Position
                x = v * t
                if x > 5.5:
                    x = 5.5
                    t_eff = 5.5 / v
                else:
                    t_eff = t

                y = 0.5 * a * t_eff**2

                # Trajectory trace
                t_trace = np.linspace(0, t_eff, 50)
                x_trace = v * t_trace
                y_trace = 0.5 * a * t_trace**2

                frame_data.append(go.Scatter(
                    x=x_trace, y=y_trace,
                    mode="lines",
                    line=dict(color=color, width=3),
                    name=label,
                ))

                # Particle
                frame_data.append(go.Scatter(
                    x=[x], y=[y],
                    mode="markers",
                    marker=dict(size=12, color=color,
                               line=dict(color="white", width=1)),
                    showlegend=False,
                ))

            # Exit slit
            frame_data.append(go.Scatter(
                x=[5.5, 5.5], y=[-0.3, -2.5],
                mode="lines",
                line=dict(color="white", width=4),
                name="Exit slit",
            ))
            frame_data.append(go.Scatter(
                x=[5.5, 5.5], y=[0.3, 2.5],
                mode="lines",
                line=dict(color="white", width=4),
                showlegend=False,
            ))

            # Formula
            frame_data.append(go.Scatter(
                x=[2.5], y=[3],
                mode="text",
                text=["v = E/B passes through"],
                textfont=dict(size=12, color="lime"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[7], y=[1],
                mode="text",
                text=["B: into page ⊗"],
                textfont=dict(size=10, color="rgba(100, 100, 255, 0.8)"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Velocity Selector</b><br><sub>Only particles with v = E/B pass through undeflected</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-1, 8], showgrid=False, zeroline=False),
                yaxis=dict(range=[-3, 3.5], showgrid=False, zeroline=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.55, y=0.25),
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

    velocity_selector_fig = create_velocity_selector_animation()
    velocity_selector_fig
    return (create_velocity_selector_animation, velocity_selector_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### How the Velocity Selector Works

        Watch the three particles in the animation:

        - **Orange (too slow)**: Magnetic force < Electric force → deflects up
        - **Green (just right)**: Forces balance → goes straight through
        - **Cyan (too fast)**: Magnetic force > Electric force → deflects down

        **The math:**

        Electric force (upward): $F_E = qE$

        Magnetic force (downward for $v$ rightward, $B$ into page): $F_B = qvB$

        Net force: $F_{net} = q(E - vB)$

        - If $v < E/B$: net force up (slow particles curve toward + plate)
        - If $v = E/B$: net force zero (selected velocity passes through)
        - If $v > E/B$: net force down (fast particles curve toward − plate)

        **Historical note:** J.J. Thomson used this principle in 1897 to measure $e/m$ for
        electrons, proving they were a fundamental particle!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 6. Magnetic Bottles and Plasma Confinement

        ### Trapping Charged Particles

        A uniform magnetic field makes particles go in circles, but they can still escape
        along the field lines. How do we trap them completely?

        The answer is a **magnetic bottle** (or magnetic mirror). By making the field
        stronger at the ends, we can reflect particles back!

        **The physics:** When a particle spirals into a region of stronger field, it experiences
        a force that pushes it back. This is because the field lines converge, creating a
        component of force opposite to the particle's motion along the field.

        The condition for reflection is related to the **pitch angle** $\alpha$ (angle between
        velocity and field direction):

        $$\sin^2\alpha_0 = \frac{B_0}{B_{max}}$$

        Particles with larger pitch angles (more perpendicular motion) get reflected. Those
        with smaller pitch angles (moving mostly along the field) can escape through the ends.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Magnetic bottle / mirror confinement
    def create_magnetic_bottle_animation():
        n_frames = 150
        frames = []

        # Bottle parameters
        L = 6  # Length of bottle
        r_center = 1.5  # Radius at center (weak field)
        r_end = 0.5  # Radius at ends (strong field)

        for frame in range(n_frames):
            t = frame / n_frames * 4 * np.pi
            frame_data = []

            # Draw bottle shape (field lines)
            z_bottle = np.linspace(-L/2, L/2, 100)
            # Bottle radius varies: wider in middle, narrow at ends
            r_bottle = r_end + (r_center - r_end) * np.cos(np.pi * z_bottle / L)**2

            # Upper and lower boundaries
            frame_data.append(go.Scatter(
                x=z_bottle, y=r_bottle,
                mode="lines",
                line=dict(color="rgba(100, 200, 255, 0.5)", width=2),
                name="Field boundary",
            ))
            frame_data.append(go.Scatter(
                x=z_bottle, y=-r_bottle,
                mode="lines",
                line=dict(color="rgba(100, 200, 255, 0.5)", width=2),
                showlegend=False,
            ))

            # Field lines (curved)
            for r_frac in [0.3, 0.5, 0.7, 0.9]:
                r_line = r_frac * r_bottle
                frame_data.append(go.Scatter(
                    x=z_bottle, y=r_line,
                    mode="lines",
                    line=dict(color="rgba(100, 100, 255, 0.3)", width=1),
                    showlegend=False,
                ))
                frame_data.append(go.Scatter(
                    x=z_bottle, y=-r_line,
                    mode="lines",
                    line=dict(color="rgba(100, 100, 255, 0.3)", width=1),
                    showlegend=False,
                ))

            # Particle motion (bouncing back and forth)
            # Simplified: sinusoidal z motion, circular xy motion
            omega_z = 1.0  # Bounce frequency
            omega_c = 8.0  # Cyclotron frequency (fast rotation)

            z = 2.0 * np.sin(omega_z * t)  # Bounces between z = ±2
            # Cyclotron radius varies with field strength
            # B ~ 1/r_bottle^2, so cyclotron radius ~ r_bottle^2
            local_r = r_end + (r_center - r_end) * np.cos(np.pi * z / L)**2
            gyro_radius = 0.3 * (local_r / r_center)**2

            # Position in xy plane (spiraling)
            x_offset = gyro_radius * np.cos(omega_c * t)
            y_offset = gyro_radius * np.sin(omega_c * t)

            # Particle trace (recent history)
            t_trace = np.linspace(max(0, t - 1.5), t, 80)
            z_trace = 2.0 * np.sin(omega_z * t_trace)
            x_trace = []
            y_trace = []
            for tt, zz in zip(t_trace, z_trace):
                lr = r_end + (r_center - r_end) * np.cos(np.pi * zz / L)**2
                gr = 0.3 * (lr / r_center)**2
                x_trace.append(gr * np.cos(omega_c * tt))
                y_trace.append(zz)  # Plot z on y-axis for side view

            frame_data.append(go.Scatter(
                x=y_trace, y=x_trace,
                mode="lines",
                line=dict(color="cyan", width=2),
                name="Particle path",
            ))

            # Current particle position (shown from side: z on x-axis, gyro motion on y)
            frame_data.append(go.Scatter(
                x=[z], y=[x_offset],
                mode="markers",
                marker=dict(size=12, color="yellow",
                           line=dict(color="white", width=2)),
                name="Trapped particle",
            ))

            # Mirror points indicator
            frame_data.append(go.Scatter(
                x=[-2.5, 2.5], y=[0, 0],
                mode="markers+text",
                marker=dict(size=10, color="red", symbol="x"),
                text=["Mirror", "Mirror"],
                textposition=["bottom center", "bottom center"],
                textfont=dict(size=10, color="red"),
                name="Mirror points",
            ))

            # Field strength indicator
            B_strength = (r_center / local_r)**2
            frame_data.append(go.Scatter(
                x=[4], y=[1.2],
                mode="text",
                text=[f"B ∝ 1/r² (stronger at ends)"],
                textfont=dict(size=11, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[4], y=[0.8],
                mode="text",
                text=[f"Local B: {B_strength:.1f}× center"],
                textfont=dict(size=10, color="cyan"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Magnetic Bottle</b><br><sub>Particle trapped by magnetic mirrors at ends</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-4, 5.5], showgrid=False, zeroline=False, title="z (along field)"),
                yaxis=dict(range=[-2, 2], showgrid=False, zeroline=False, title="Perpendicular",
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.7, y=0.95),
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

    magnetic_bottle_fig = create_magnetic_bottle_animation()
    magnetic_bottle_fig
    return (create_magnetic_bottle_animation, magnetic_bottle_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Applications of Magnetic Confinement

        **Fusion Energy:**

        The most ambitious application is **nuclear fusion**. To fuse hydrogen into helium
        (like the Sun does), we need temperatures of 100 million degrees. At this temperature,
        matter is plasma—a gas of free electrons and ions.

        No material container can hold such hot plasma. But magnetic fields can!

        The two main approaches:
        - **Tokamak**: A donut-shaped (toroidal) magnetic bottle (ITER, under construction)
        - **Stellarator**: A twisted donut with complex coil geometry

        **The Van Allen Radiation Belts:**

        Earth itself is a giant magnetic bottle! Charged particles from the Sun get trapped
        in Earth's magnetic field, bouncing between the poles. These are the Van Allen belts.

        When particles "leak" out of the trap near the poles and hit the atmosphere, they
        create the **aurora borealis** (northern lights) and **aurora australis** (southern lights).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 7. The Hall Effect

        ### Measuring Magnetic Fields with Voltage

        When current flows through a conductor in a magnetic field, the charges get deflected
        to one side. This creates a voltage perpendicular to both the current and field—the
        **Hall voltage**.

        For a conductor of width $w$ with current density $J$ in a field $B$:

        $$V_H = \frac{IB}{nqt}$$

        where $n$ is the charge carrier density and $t$ is the thickness.

        **Why it matters:**
        - **Hall sensors** measure magnetic field strength in countless devices
        - Reveals whether charge carriers are positive or negative
        - Measures carrier density in semiconductors
        - Used in anti-lock brakes, computer keyboards, smartphones
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Hall effect
    def create_hall_effect_animation():
        n_frames = 80
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 2 * np.pi
            frame_data = []

            # Conductor slab
            frame_data.append(go.Scatter(
                x=[-2, 2, 2, -2, -2],
                y=[-1, -1, 1, 1, -1],
                mode="lines",
                fill="toself",
                fillcolor="rgba(200, 150, 100, 0.3)",
                line=dict(color="orange", width=2),
                name="Conductor",
            ))

            # Current direction (left to right)
            frame_data.append(go.Scatter(
                x=[-2.5, -1.5],
                y=[0, 0],
                mode="lines+markers",
                line=dict(color="yellow", width=4),
                marker=dict(size=[0, 12], symbol=["circle", "triangle-right"],
                           color="yellow"),
                name="Current I →",
            ))

            # Magnetic field (into page)
            for x_pos in [-1, 0, 1]:
                for y_pos in [-0.5, 0.5]:
                    frame_data.append(go.Scatter(
                        x=[x_pos], y=[y_pos],
                        mode="markers",
                        marker=dict(size=15, color="rgba(100, 100, 255, 0.5)",
                                   symbol="x"),
                        showlegend=False,
                    ))

            frame_data.append(go.Scatter(
                x=[0], y=[1.8],
                mode="text",
                text=["B into page ⊗"],
                textfont=dict(size=12, color="rgba(100, 100, 255, 0.8)"),
                showlegend=False,
            ))

            # Moving electrons (current carriers)
            n_electrons = 8
            for i in range(n_electrons):
                # Electrons move right to left (opposite to current)
                phase = t + i * 2 * np.pi / n_electrons
                x_e = 1.8 - (phase % (2 * np.pi)) / (2 * np.pi) * 3.6

                # Deflected toward top (negative charge, v left, B into page → F up)
                # Build up creates E field that eventually balances
                deflection = 0.3 * np.sin(phase * 2)  # Small oscillation showing deflection

                frame_data.append(go.Scatter(
                    x=[x_e], y=[deflection],
                    mode="markers",
                    marker=dict(size=8, color="cyan", symbol="circle"),
                    showlegend=(i == 0),
                    name="Electrons (moving ←)" if i == 0 else None,
                ))

            # Charge buildup on edges
            # Top edge: negative (electrons accumulate)
            frame_data.append(go.Scatter(
                x=np.linspace(-1.8, 1.8, 10),
                y=[1.05] * 10,
                mode="markers+text",
                marker=dict(size=8, color="cyan"),
                text=["−"] * 10,
                textposition="top center",
                textfont=dict(size=10, color="cyan"),
                name="− charge buildup",
            ))

            # Bottom edge: positive (electron deficit)
            frame_data.append(go.Scatter(
                x=np.linspace(-1.8, 1.8, 10),
                y=[-1.05] * 10,
                mode="markers+text",
                marker=dict(size=8, color="red"),
                text=["+"] * 10,
                textposition="bottom center",
                textfont=dict(size=10, color="red"),
                name="+ charge deficit",
            ))

            # Hall voltage indicator
            frame_data.append(go.Scatter(
                x=[2.5, 2.5],
                y=[-1, 1],
                mode="lines+markers",
                line=dict(color="lime", width=3),
                marker=dict(size=[8, 8], color=["red", "cyan"]),
                name="Hall voltage V_H",
            ))

            frame_data.append(go.Scatter(
                x=[2.8], y=[0],
                mode="text",
                text=["V_H"],
                textfont=dict(size=14, color="lime"),
                showlegend=False,
            ))

            # Electric field from charge separation
            frame_data.append(go.Scatter(
                x=[0, 0],
                y=[0.6, -0.6],
                mode="lines+markers",
                line=dict(color="rgba(255, 100, 100, 0.7)", width=2, dash="dash"),
                marker=dict(size=[0, 8], symbol=["circle", "triangle-down"],
                           color="rgba(255, 100, 100, 0.7)"),
                name="E field (Hall)",
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Hall Effect</b><br><sub>Magnetic deflection creates transverse voltage</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3.5, 4], showgrid=False, zeroline=False),
                yaxis=dict(range=[-2, 2.5], showgrid=False, zeroline=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.6, y=0.25),
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
                                 args=[None, {"frame": {"duration": 60, "redraw": True},
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

    hall_effect_fig = create_hall_effect_animation()
    hall_effect_fig
    return (create_hall_effect_animation, hall_effect_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Hall Effect

        The animation shows what happens step by step:

        1. **Current flows** through the conductor (conventional current right, electrons left)
        2. **Magnetic force** deflects electrons upward ($\mathbf{F} = q\mathbf{v} \times \mathbf{B}$)
        3. **Charges accumulate**: negative at top, positive at bottom
        4. **Electric field develops** between the charged edges
        5. **Equilibrium**: Electric force balances magnetic force, current flows straight

        **The Hall voltage** tells us:
        - **Sign of carriers**: If $V_H$ is positive on top, carriers are negative (electrons)
        - **Carrier density**: $n = IB/(V_H q t)$
        - **Field strength**: Used in Hall effect sensors

        **Historical note:** Edwin Hall discovered this effect in 1879, providing the first
        direct evidence that electric current in metals is carried by negative charges!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 8. Aurora Borealis: Nature's Light Show

        ### Earth's Magnetic Bottle in Action

        The **aurora** (northern and southern lights) is a spectacular demonstration of
        charged particle motion in magnetic fields on a planetary scale.

        **How it works:**

        1. **Solar wind** (plasma from the Sun) streams toward Earth
        2. Most is deflected by Earth's magnetic field (the magnetosphere)
        3. Some particles get trapped in the **Van Allen belts**
        4. Particles bounce between magnetic mirrors near the poles
        5. Near the poles, field lines dip into the atmosphere
        6. Particles collide with nitrogen and oxygen, exciting the atoms
        7. The atoms emit light as they de-excite: **green, red, purple, blue**

        The colors depend on which atoms are excited and at what altitude:
        - **Green** (most common): Oxygen at 100-300 km
        - **Red**: Oxygen above 300 km
        - **Blue/Purple**: Nitrogen
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Charged particles in Earth's magnetic field (aurora)
    def create_aurora_animation():
        n_frames = 120
        frames = []

        for frame in range(n_frames):
            t = frame / n_frames * 4 * np.pi
            frame_data = []

            # Earth
            theta_earth = np.linspace(0, 2 * np.pi, 100)
            r_earth = 1.0
            frame_data.append(go.Scatter(
                x=r_earth * np.cos(theta_earth),
                y=r_earth * np.sin(theta_earth),
                mode="lines",
                fill="toself",
                fillcolor="rgba(50, 100, 200, 0.5)",
                line=dict(color="blue", width=2),
                name="Earth",
            ))

            # Magnetic field lines (dipole approximation)
            for L in [2, 3, 4, 5]:  # L-shells
                theta_field = np.linspace(-np.pi/2 * 0.9, np.pi/2 * 0.9, 100)
                r_field = L * np.cos(theta_field)**2
                x_field = r_field * np.cos(theta_field)
                y_field = r_field * np.sin(theta_field)

                frame_data.append(go.Scatter(
                    x=x_field, y=y_field,
                    mode="lines",
                    line=dict(color="rgba(100, 150, 255, 0.3)", width=1),
                    showlegend=(L == 3),
                    name="Magnetic field" if L == 3 else None,
                ))

            # Trapped particle bouncing
            L_particle = 3
            bounce_freq = 0.5
            gyro_freq = 8

            # Latitude oscillation
            lat = 0.7 * np.sin(bounce_freq * t)  # Bounces between ±0.7 rad (~40°)
            r_particle = L_particle * np.cos(lat)**2

            # Add gyration
            gyro_radius = 0.15 * (1 + 0.5 * abs(np.sin(lat)))  # Larger near equator
            gyro_x = gyro_radius * np.cos(gyro_freq * t)
            gyro_y = gyro_radius * np.sin(gyro_freq * t)

            x_particle = r_particle * np.cos(lat) + gyro_x * np.sin(lat)
            y_particle = r_particle * np.sin(lat) + gyro_y

            # Particle trace
            t_trace = np.linspace(max(0, t - 2), t, 60)
            x_trace = []
            y_trace = []
            for tt in t_trace:
                lat_t = 0.7 * np.sin(bounce_freq * tt)
                r_t = L_particle * np.cos(lat_t)**2
                gx = 0.15 * (1 + 0.5 * abs(np.sin(lat_t))) * np.cos(gyro_freq * tt)
                gy = 0.15 * (1 + 0.5 * abs(np.sin(lat_t))) * np.sin(gyro_freq * tt)
                x_trace.append(r_t * np.cos(lat_t) + gx * np.sin(lat_t))
                y_trace.append(r_t * np.sin(lat_t) + gy)

            frame_data.append(go.Scatter(
                x=x_trace, y=y_trace,
                mode="lines",
                line=dict(color="yellow", width=2),
                name="Trapped particle",
            ))

            frame_data.append(go.Scatter(
                x=[x_particle], y=[y_particle],
                mode="markers",
                marker=dict(size=10, color="yellow",
                           line=dict(color="white", width=1)),
                showlegend=False,
            ))

            # Aurora regions (near poles)
            # Northern aurora
            aurora_intensity = (1 + np.sin(t * 2)) / 2  # Pulsing
            aurora_theta_n = np.linspace(np.pi/2 - 0.4, np.pi/2 + 0.4, 20)
            aurora_r_n = 1.05 + 0.1 * aurora_intensity
            frame_data.append(go.Scatter(
                x=aurora_r_n * np.cos(aurora_theta_n),
                y=aurora_r_n * np.sin(aurora_theta_n),
                mode="lines",
                line=dict(color=f"rgba(100, 255, 100, {0.3 + 0.5 * aurora_intensity})",
                         width=8),
                name="Aurora",
            ))

            # Southern aurora
            aurora_theta_s = np.linspace(-np.pi/2 - 0.4, -np.pi/2 + 0.4, 20)
            frame_data.append(go.Scatter(
                x=aurora_r_n * np.cos(aurora_theta_s),
                y=aurora_r_n * np.sin(aurora_theta_s),
                mode="lines",
                line=dict(color=f"rgba(100, 255, 100, {0.3 + 0.5 * aurora_intensity})",
                         width=8),
                showlegend=False,
            ))

            # Solar wind (incoming particles from right)
            for i in range(5):
                sw_x = 6 - (t * 0.5 + i) % 3
                sw_y = -2 + i
                if sw_x > 4:
                    frame_data.append(go.Scatter(
                        x=[sw_x], y=[sw_y],
                        mode="markers",
                        marker=dict(size=6, color="orange"),
                        showlegend=(i == 0),
                        name="Solar wind" if i == 0 else None,
                    ))

            # Magnetosphere boundary (approximate)
            theta_mag = np.linspace(np.pi/2, 3*np.pi/2, 50)
            r_mag = 5 / (1 + 0.5 * np.cos(theta_mag - np.pi))
            frame_data.append(go.Scatter(
                x=r_mag * np.cos(theta_mag),
                y=r_mag * np.sin(theta_mag),
                mode="lines",
                line=dict(color="rgba(255, 255, 255, 0.2)", width=1, dash="dash"),
                name="Magnetopause",
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[0], y=[0],
                mode="text",
                text=["N"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[0], y=[1.6],
                mode="text",
                text=["North"],
                textfont=dict(size=10, color="white"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Aurora: Earth's Magnetic Bottle</b><br><sub>Charged particles trapped in Van Allen belts create light shows at the poles</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-6, 7], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-4, 4], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.75, y=0.95),
                plot_bgcolor="rgba(0, 0, 20, 1)",
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

    aurora_fig = create_aurora_animation()
    aurora_fig
    return (create_aurora_animation, aurora_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Physics of Aurora

        The animation shows the key features:

        1. **Solar wind** (orange particles) streams from the Sun
        2. **Magnetosphere** deflects most particles around Earth
        3. **Trapped particles** spiral along field lines, bouncing between hemispheres
        4. **Aurora** glows where particles enter the atmosphere near the poles

        **The Van Allen Belts:**

        There are two main radiation belts:
        - **Inner belt** (1,000-6,000 km): Mostly protons, very stable
        - **Outer belt** (13,000-60,000 km): Mostly electrons, varies with solar activity

        **Space weather hazard:** During solar storms, these belts can become so intense
        that satellites are damaged and astronauts must shelter in shielded areas.

        **Historical note:** The Van Allen belts were discovered in 1958 by James Van Allen
        using data from the first American satellite, Explorer 1. It was the first major
        scientific discovery of the space age!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Lorentz Force at Work

        | Application | Physics Principle | Key Equation |
        |-------------|-------------------|--------------|
        | **CRT displays** | E-field deflection | $\mathbf{a} = q\mathbf{E}/m$ |
        | **Cyclotron motion** | B-field bending | $r = mv/(qB)$ |
        | **Mass spectrometer** | Mass-dependent radius | $r \propto \sqrt{m}$ |
        | **Cyclotron accelerator** | Constant frequency | $\omega_c = qB/m$ |
        | **Velocity selector** | Crossed fields balance | $v = E/B$ |
        | **Magnetic bottle** | Mirror reflection | $\sin^2\alpha = B_0/B_{max}$ |
        | **Hall effect** | Transverse voltage | $V_H = IB/(nqt)$ |
        | **Aurora** | Planetary magnetic trap | Dipole field + atmosphere |

        All of these phenomena follow from a single equation:

        $$\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$$

        **The remarkable unity of physics:** From laboratory mass spectrometers to planetary
        auroras, from television tubes to fusion reactors, the motion of charged particles
        is governed by this one elegant law.

        ---

        > *"The same equations have the same solutions. This is why, having studied one
        > phenomenon—let's call it a cyclotron—you can then apply the same mathematics to
        > something else that looks entirely different."*
        > — Richard Feynman
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References

        ### Primary Source

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1964). *The Feynman Lectures on Physics, Volume II*.
          Addison-Wesley.
          - [Chapter 29: The Motion of Charges in Electric and Magnetic Fields](https://www.feynmanlectures.caltech.edu/II_29.html)
          - Topics: uniform fields, momentum analysis, magnetic lenses, electron microscope,
            accelerator guide fields, alternating-gradient focusing, crossed fields

        ### Related Feynman Lectures

        - [Chapter 13: Magnetostatics](https://www.feynmanlectures.caltech.edu/II_13.html) — Magnetic force basics
        - [Chapter 14: The Magnetic Field in Various Situations](https://www.feynmanlectures.caltech.edu/II_14.html)
        - [Chapter 16: Induced Currents](https://www.feynmanlectures.caltech.edu/II_16.html) — Motors and induction
        - [Chapter 17: The Laws of Induction](https://www.feynmanlectures.caltech.edu/II_17.html) — Betatron (section 17-4)

        ### Mathematical Background

        - **Lorentz Force Law**
          - $\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$
          - Combines electric and magnetic forces on a charged particle

        - **Cyclotron Motion**
          - Radius: $r = mv/(qB)$ (Larmor radius)
          - Frequency: $\omega_c = qB/m$ (cyclotron frequency)
          - Period: $T = 2\pi m/(qB)$
          - Independent of velocity (non-relativistic)

        - **Mass Spectrometer**
          - After acceleration through voltage $V$: $v = \sqrt{2qV/m}$
          - Radius in magnetic field: $r = (1/B)\sqrt{2mV/q}$

        - **Velocity Selector**
          - Crossed E and B fields
          - Selected velocity: $v = E/B$

        - **Hall Effect**
          - Hall voltage: $V_H = IB/(nqt)$
          - $n$ = carrier density, $t$ = thickness

        - **Magnetic Mirror**
          - Reflection condition: $\sin^2\alpha_0 = B_0/B_{max}$
          - Particles with small pitch angles escape ("loss cone")

        ### Historical References

        - **J.J. Thomson** (1897): Used crossed fields to measure $e/m$ for electrons
        - **E.O. Lawrence** (1930): Invented the cyclotron, Nobel Prize 1939
        - **E.H. Hall** (1879): Discovered the Hall effect
        - **J.A. Van Allen** (1958): Discovered Earth's radiation belts

        ### Further Reading

        - Griffiths, D. J. *Introduction to Electrodynamics* — Chapters on particle dynamics
        - Jackson, J. D. *Classical Electrodynamics* — Advanced treatment
        - Chen, F. F. *Introduction to Plasma Physics* — Magnetic confinement
        - Parks, G. K. *Physics of Space Plasmas* — Van Allen belts and aurora
        """
    )
    return


if __name__ == "__main__":
    app.run()
