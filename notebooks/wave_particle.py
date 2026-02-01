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
        # The Wave-Particle Duality

        *An interactive exploration based on [Feynman Lectures on Physics, Volume III](https://www.feynmanlectures.caltech.edu/III_01.html)*

        ---

        ## The Central Mystery of Quantum Mechanics

        > *"We choose to examine a phenomenon which is impossible, absolutely impossible,
        > to explain in any classical way, and which has in it the heart of quantum mechanics.
        > In reality, it contains the only mystery."*
        > — Richard Feynman

        Light behaves like a wave—it diffracts, interferes, and bends around corners.
        But light also behaves like a stream of particles (photons)—it comes in discrete
        packets that can knock electrons out of metals.

        So which is it? Wave or particle?

        **The answer is neither—and both.** This notebook explores the experiments that
        revealed this fundamental strangeness at the heart of nature.

        $$E = h\nu \quad \text{(photon energy)}$$
        $$p = \frac{h}{\lambda} \quad \text{(photon momentum)}$$

        where $h = 6.626 \times 10^{-34}$ J·s is Planck's constant.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Wave Behavior: Interference

        When waves meet, they **interfere**. If two wave crests meet, they add up
        (constructive interference). If a crest meets a trough, they cancel
        (destructive interference).

        This is easily demonstrated with water waves, sound waves, and light waves.
        It's the hallmark of wave behavior—particles don't do this!

        **Young's double-slit experiment (1801):**

        Thomas Young shone light through two narrow slits and observed alternating
        bright and dark bands on a screen—an **interference pattern**. This proved
        light was a wave, settling a century-long debate.

        The bright bands occur where:
        $$d \sin\theta = m\lambda \quad (m = 0, \pm 1, \pm 2, ...)$$

        *The animation below shows two wave sources creating an interference pattern.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_wave_interference_animation():
        """Animate two-source wave interference."""
        n_frames = 50

        # Grid for wave visualization
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        # Two sources
        source1 = (-2, 0)
        source2 = (2, 0)

        frames = []

        for i in range(n_frames):
            t = 2 * np.pi * i / n_frames

            # Distance from each source (use maximum to avoid sqrt of negative due to float precision)
            r1 = np.sqrt(np.maximum(0, (X - source1[0])**2 + (Y - source1[1])**2))
            r2 = np.sqrt(np.maximum(0, (X - source2[0])**2 + (Y - source2[1])**2))

            # Wave from each source (circular waves)
            # Add small epsilon to avoid sqrt(0) warnings
            k = 1.5  # wave number
            wave1 = np.sin(k * r1 - t) / (np.sqrt(r1 + 1e-10) + 0.5)
            wave2 = np.sin(k * r2 - t) / (np.sqrt(r2 + 1e-10) + 0.5)

            # Superposition
            total_wave = wave1 + wave2

            frame_data = [
                go.Heatmap(
                    x=x, y=y, z=total_wave,
                    colorscale="RdBu",
                    zmin=-1.5, zmax=1.5,
                    showscale=False,
                ),
                # Source markers
                go.Scatter(
                    x=[source1[0], source2[0]],
                    y=[source1[1], source2[1]],
                    mode="markers",
                    marker=dict(size=12, color="yellow", line=dict(color="black", width=2)),
                    name="Sources (slits)",
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Wave Interference:</b> Two Sources Creating Patterns<br><sub>Bright and dark bands form where waves add or cancel</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="", showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(title="", showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
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

    wave_interference_fig = create_wave_interference_animation()
    wave_interference_fig
    return create_wave_interference_animation, wave_interference_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Particle Behavior: The Photoelectric Effect

        In 1887, Heinrich Hertz noticed something strange: ultraviolet light could knock
        electrons out of metal surfaces. This **photoelectric effect** couldn't be explained
        by wave theory.

        **The puzzle:**

        - Classical wave theory predicted that brighter light (more energy) should eject
          faster electrons. Instead, brightness only affected *how many* electrons came out.
        - The *speed* of ejected electrons depended only on the light's **frequency** (color).
        - Below a certain frequency, no electrons came out—no matter how bright the light!

        **Einstein's explanation (1905):**

        Light comes in discrete packets—**photons**—each carrying energy $E = h\nu$.

        - A photon either has enough energy to eject an electron, or it doesn't
        - More photons (brighter light) = more electrons, not faster electrons
        - Higher frequency = more energy per photon = faster electrons

        $$K_{max} = h\nu - \phi$$

        where $\phi$ is the **work function** (minimum energy to free an electron).

        Einstein won the Nobel Prize for this explanation—not for relativity!

        *The animation below shows photons ejecting electrons from a metal surface.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_photoelectric_animation():
        """Animate the photoelectric effect."""
        n_frames = 80
        np.random.seed(42)

        frames = []

        # Precompute random photon arrivals and electron ejections
        n_photons = 15
        photon_starts = np.random.uniform(0, n_frames * 0.7, n_photons)
        photon_x_start = np.random.uniform(-1.5, 1.5, n_photons)

        for i in range(n_frames):
            frame_data = []

            # Metal surface
            frame_data.append(go.Scatter(
                x=[-2, 2, 2, -2, -2],
                y=[-0.5, -0.5, -2, -2, -0.5],
                fill="toself",
                fillcolor="rgba(150, 150, 150, 0.8)",
                line=dict(color="gray", width=2),
                name="Metal surface",
            ))

            # Incoming photons
            photon_x = []
            photon_y = []
            for j, (start, x_pos) in enumerate(zip(photon_starts, photon_x_start)):
                if start <= i < start + 20:
                    progress = (i - start) / 20
                    y_pos = 3 - progress * 3.5
                    if y_pos > -0.5:
                        photon_x.append(x_pos)
                        photon_y.append(y_pos)

            if photon_x:
                frame_data.append(go.Scatter(
                    x=photon_x, y=photon_y,
                    mode="markers",
                    marker=dict(size=10, color="yellow",
                               line=dict(color="orange", width=2),
                               symbol="star"),
                    name="Photons (hν)",
                ))

            # Ejected electrons
            electron_x = []
            electron_y = []
            for j, (start, x_pos) in enumerate(zip(photon_starts, photon_x_start)):
                if i > start + 20:
                    progress = (i - start - 20) / 30
                    if progress < 1.5:
                        # Electron ejected upward with some spread
                        e_y = -0.5 + progress * 2.5
                        e_x = x_pos + 0.3 * np.sin(j) * progress
                        electron_x.append(e_x)
                        electron_y.append(e_y)

            if electron_x:
                frame_data.append(go.Scatter(
                    x=electron_x, y=electron_y,
                    mode="markers",
                    marker=dict(size=8, color="blue",
                               line=dict(color="lightblue", width=1)),
                    name="Ejected electrons",
                ))

            # Energy level annotation
            frame_data.append(go.Scatter(
                x=[2.5], y=[2],
                mode="text",
                text=[f"Photon energy: E = hν"],
                textposition="middle left",
                textfont=dict(size=12, color="yellow"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Photoelectric Effect:</b> Photons Ejecting Electrons<br><sub>Each photon can eject one electron if hν > work function</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-3, 4], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-2.5, 4], showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                plot_bgcolor="rgba(0,0,30,0.9)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
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

    photoelectric_fig = create_photoelectric_animation()
    photoelectric_fig
    return create_photoelectric_animation, photoelectric_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Double-Slit Experiment: Where It Gets Strange

        Here's where classical intuition breaks down completely.

        **With waves:** Shine light through two slits → interference pattern (bright and dark bands).
        This makes sense—waves interfere.

        **With particles:** Shoot bullets through two slits → two piles (no interference).
        Particles just go through one slit or the other.

        **With electrons (or photons)?** This is where Feynman says the "only mystery" lies.

        **The experiment:**

        1. Fire electrons one at a time through two slits
        2. Each electron hits the detector at a specific point—like a particle
        3. But after many electrons... an **interference pattern** builds up!

        > *"Each electron goes through both slits simultaneously"*

        This isn't metaphorical. If you try to detect which slit the electron went through,
        the interference pattern **disappears**—you get two piles like classical particles.

        The act of measurement changes the outcome.

        *The animation below shows single particles building up an interference pattern.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_double_slit_animation():
        """Animate particles building up an interference pattern."""
        n_frames = 120
        np.random.seed(123)

        # Generate detection positions following interference pattern
        def interference_probability(x, d=2, wavelength=1):
            """Probability distribution for double-slit interference."""
            # Simplified interference pattern
            return (np.cos(np.pi * d * x / wavelength) ** 2) * np.exp(-x**2 / 50)

        # Sample from this distribution
        x_range = np.linspace(-8, 8, 300)
        probs = interference_probability(x_range)
        probs = probs / probs.sum()

        n_total_particles = 300
        all_x_positions = np.random.choice(x_range, size=n_total_particles, p=probs)
        all_y_positions = np.random.uniform(-0.3, 0.3, n_total_particles)

        frames = []

        for i in range(n_frames):
            # How many particles have landed so far
            n_landed = min(int(i * n_total_particles / n_frames), n_total_particles)

            # Current particle in flight
            in_flight = i % 8 < 6  # Particle visible for part of cycle
            flight_progress = (i % 8) / 6

            frame_data = []

            # Barrier with slits
            frame_data.append(go.Scatter(
                x=[-10, -1, -1, -10],
                y=[3, 3, 3.3, 3.3],
                fill="toself",
                fillcolor="rgba(80, 80, 80, 0.9)",
                line=dict(color="gray", width=1),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[1, 10, 10, 1],
                y=[3, 3, 3.3, 3.3],
                fill="toself",
                fillcolor="rgba(80, 80, 80, 0.9)",
                line=dict(color="gray", width=1),
                showlegend=False,
            ))
            # Middle barrier
            frame_data.append(go.Scatter(
                x=[-0.3, 0.3, 0.3, -0.3],
                y=[3, 3, 3.3, 3.3],
                fill="toself",
                fillcolor="rgba(80, 80, 80, 0.9)",
                line=dict(color="gray", width=1),
                name="Barrier with two slits",
            ))

            # Detection screen
            frame_data.append(go.Scatter(
                x=[-8, 8],
                y=[-1, -1],
                mode="lines",
                line=dict(color="white", width=3),
                name="Detector screen",
            ))

            # Particle source
            frame_data.append(go.Scatter(
                x=[0], y=[6],
                mode="markers",
                marker=dict(size=15, color="cyan", symbol="diamond"),
                name="Particle source",
            ))

            # Particle in flight
            if in_flight and n_landed < n_total_particles:
                if flight_progress < 0.4:
                    # Before slits
                    p_y = 6 - flight_progress * 7
                    p_x = 0
                else:
                    # After slits - heading to detection point
                    target_x = all_x_positions[n_landed]
                    p_x = target_x * (flight_progress - 0.4) / 0.6
                    p_y = 3 - (flight_progress - 0.4) / 0.6 * 4

                frame_data.append(go.Scatter(
                    x=[p_x], y=[p_y],
                    mode="markers",
                    marker=dict(size=8, color="yellow"),
                    name="Particle in flight",
                ))

            # Landed particles
            if n_landed > 0:
                frame_data.append(go.Scatter(
                    x=all_x_positions[:n_landed],
                    y=-1 + all_y_positions[:n_landed],
                    mode="markers",
                    marker=dict(size=4, color="cyan", opacity=0.7),
                    name=f"Detected particles: {n_landed}",
                ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Double-Slit Experiment:</b> Single Particles Build Interference<br><sub>Each particle lands at one spot, but the pattern emerges statistically</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-10, 10], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-2, 7], showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.08,
                        x=0.5,
                        xanchor="center",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
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

    double_slit_fig = create_double_slit_animation()
    double_slit_fig
    return create_double_slit_animation, double_slit_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Which Slit? The Measurement Problem

        Here's where it gets truly bizarre. What if we try to catch the electron
        in the act—watching which slit it goes through?

        **When we don't measure which slit:** Interference pattern appears

        **When we DO measure which slit:** Interference pattern **vanishes**—we get
        two blobs like classical particles!

        > *"It is as if the electron knows whether we're watching."*

        But it's not consciousness or magic. The act of detecting which slit the electron
        passes through requires interacting with it—and that interaction destroys the
        delicate quantum superposition.

        **Feynman's summary:**

        - If the paths are *distinguishable*, add **probabilities** (like particles): $P = P_1 + P_2$
        - If the paths are *indistinguishable*, add **amplitudes** (like waves): $\psi = \psi_1 + \psi_2$, then $P = |\psi|^2$

        The interference comes from the cross terms when you square the sum of amplitudes.
        When you measure which path, you collapse the superposition and lose those terms.

        *The animation below compares behavior with and without "which-path" detection.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_measurement_comparison():
        """Show interference vs no interference when measuring."""
        x = np.linspace(-8, 8, 200)

        # Interference pattern (not measured)
        interference = (np.cos(np.pi * x / 2) ** 2) * np.exp(-x**2 / 30)
        interference = interference / interference.max()

        # No interference (measured - just two Gaussians)
        no_interference = 0.5 * (np.exp(-(x + 2)**2 / 4) + np.exp(-(x - 2)**2 / 4))
        no_interference = no_interference / no_interference.max()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x, y=interference,
            mode="lines",
            line=dict(color="cyan", width=3),
            name="Not measured (interference)",
            fill="tozeroy",
            fillcolor="rgba(0, 255, 255, 0.3)",
        ))

        fig.add_trace(go.Scatter(
            x=x, y=-no_interference,
            mode="lines",
            line=dict(color="orange", width=3),
            name="Measured (no interference)",
            fill="tozeroy",
            fillcolor="rgba(255, 165, 0, 0.3)",
        ))

        # Add slit positions
        fig.add_vline(x=-2, line_dash="dot", line_color="white", opacity=0.5)
        fig.add_vline(x=2, line_dash="dot", line_color="white", opacity=0.5)

        fig.update_layout(
            title=dict(
                text="<b>The Measurement Effect:</b> Watching Destroys Interference<br><sub>Top: paths indistinguishable | Bottom: paths measured</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Position on screen", showgrid=False),
            yaxis=dict(title="Detection probability", showgrid=False, zeroline=True),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor="rgba(0,0,30,0.9)",
        )

        return fig

    measurement_fig = create_measurement_comparison()
    measurement_fig
    return create_measurement_comparison, measurement_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## de Broglie's Insight: Matter Waves

        If light (waves) can behave like particles, could particles behave like waves?

        In 1924, Louis de Broglie made a bold proposal in his PhD thesis: **all matter
        has a wavelength**. This wasn't just speculation—it was a logical extension of
        Einstein's photon idea, run in reverse.

        **The reasoning:**

        Einstein showed that light waves carry momentum in discrete packets: $p = h/\lambda$.
        De Broglie asked: if waves have particle properties, do particles have wave properties?

        He proposed the inverse relation:

        $$\begin{aligned}
        \lambda &= \frac{h}{p} \\
        &= \frac{h}{mv}
        \end{aligned}$$

        **What the equation tells us:**

        - $\lambda$ is the wavelength associated with any particle
        - $h$ is Planck's constant ($6.626 \times 10^{-34}$ J·s)—incredibly tiny!
        - $p = mv$ is the particle's momentum (mass × velocity)

        **Why we don't see baseballs diffract:**

        For everyday objects, this wavelength is absurdly small. A baseball moving at
        40 m/s has a wavelength of about $10^{-34}$ meters—that's 10 billion billion
        times smaller than a proton! No experiment could ever detect this.

        But for electrons, the wavelength is significant—comparable to atomic spacings:

        | Particle | Speed | de Broglie wavelength |
        |----------|-------|----------------------|
        | Electron (100 eV) | 6×10⁶ m/s | 0.12 nm (atomic scale!) |
        | Neutron (thermal) | 2200 m/s | 0.18 nm |
        | Baseball | 40 m/s | 10⁻³⁴ m (unmeasurable) |

        **Experimental confirmation:**

        In 1927, Davisson and Germer scattered electrons off a nickel crystal and
        observed diffraction patterns—exactly as predicted by de Broglie's formula!
        The crystal lattice acted like a diffraction grating for electron waves.

        This earned de Broglie the Nobel Prize and established that wave-particle
        duality applies to **all matter**, not just light. Every particle—electron,
        proton, atom, even you—has a wavelength. It's just usually far too small to matter.
        """
    )
    return


@app.cell
def _(go, np):
    def create_debroglie_animation():
        """Animate de Broglie wavelength for different masses."""
        n_frames = 80

        frames = []

        for i in range(n_frames):
            t = 2 * np.pi * i / n_frames
            x = np.linspace(0, 10, 200)

            # Three "particles" with different masses (different wavelengths)
            # Electron - short wavelength but visible
            lambda_electron = 1.0
            wave_electron = np.sin(2 * np.pi * x / lambda_electron - t) * np.exp(-((x - 5)**2) / 20)

            # Proton - shorter wavelength (1836x mass means smaller λ = h/mv)
            lambda_proton = 0.3
            wave_proton = np.sin(2 * np.pi * x / lambda_proton - t) * np.exp(-((x - 5)**2) / 20)

            # "Baseball" - essentially flat (wavelength too small)
            wave_baseball = 0.8 * np.exp(-((x - 5 - 0.1 * np.sin(t))**2) / 0.5)

            frame_data = [
                go.Scatter(
                    x=x, y=wave_electron + 2.5,
                    mode="lines",
                    line=dict(color="cyan", width=2),
                    name="Electron (λ = 0.12 nm)",
                ),
                go.Scatter(
                    x=x, y=wave_proton,
                    mode="lines",
                    line=dict(color="yellow", width=2),
                    name="Proton (λ = 0.07 pm)",
                ),
                go.Scatter(
                    x=x, y=wave_baseball - 2.5,
                    mode="lines",
                    line=dict(color="orange", width=3),
                    name="Baseball (λ ≈ 0)",
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>de Broglie Wavelength:</b> λ = h/p<br><sub>Heavier particles have shorter wavelengths (less wave-like)</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Position", showgrid=False),
                yaxis=dict(title="Wave amplitude", showgrid=False, zeroline=False,
                          range=[-4, 4], showticklabels=False),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                plot_bgcolor="rgba(0,0,30,0.9)",
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
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
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

    debroglie_fig = create_debroglie_animation()
    debroglie_fig
    return create_debroglie_animation, debroglie_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Uncertainty Principle

        Wave-particle duality leads directly to Heisenberg's uncertainty principle—one
        of the most profound statements in all of physics.

        **The wave connection:**

        Think about what it means for a particle to "be" a wave:

        - A pure sine wave has a **definite wavelength** (and thus definite momentum,
          via $p = h/\lambda$), but it extends forever—it has **no definite position**.
        - A localized wave packet (definite position) must be built from a superposition
          of many wavelengths—so it has **no definite momentum**.

        This isn't a quirk of waves; it's mathematics. You cannot have a function that's
        both sharply localized AND has only one frequency component.

        **The mathematical statement:**

        $$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$$

        **What each symbol means:**

        - $\Delta x$ = uncertainty in position (how "spread out" the particle is)
        - $\Delta p$ = uncertainty in momentum (how "spread out" its velocity is)
        - $\hbar = h/2\pi \approx 1.05 \times 10^{-34}$ J·s (the "reduced" Planck constant)
        - The $\geq$ means the product can never be smaller than $\hbar/2$

        **What this means physically:**

        - If you know exactly where a particle is ($\Delta x \to 0$), you know nothing
          about its momentum ($\Delta p \to \infty$)
        - If you know exactly how fast it's moving ($\Delta p \to 0$), you have no idea
          where it is ($\Delta x \to \infty$)
        - Most real situations are somewhere in between

        **This isn't about measurement errors!**

        A common misconception: "We disturb the particle when we measure it."

        The truth is deeper: the particle doesn't *have* a definite position AND momentum
        simultaneously. These properties are not just unknown—they're **undefined**.
        Asking "where is the electron AND how fast is it moving?" is like asking
        "what's north of the North Pole?"

        **Feynman's perspective:**

        > *"The uncertainty principle 'protects' quantum mechanics. If you could measure
        > both position and momentum precisely, you could determine which slit the
        > electron went through without disturbing the interference pattern. Nature
        > doesn't allow this."*
        """
    )
    return


@app.cell
def _(go, np):
    def create_uncertainty_visualization():
        """Visualize position-momentum uncertainty tradeoff."""
        x = np.linspace(-10, 10, 300)

        fig = go.Figure()

        # Well-localized (uncertain momentum)
        psi_localized = np.exp(-x**2 / 2)
        fig.add_trace(go.Scatter(
            x=x, y=psi_localized + 3,
            mode="lines", fill="tozeroy",
            line=dict(color="cyan", width=2),
            fillcolor="rgba(0, 255, 255, 0.3)",
            name="Localized: Δx small, Δp large",
        ))

        # Medium spread
        psi_medium = np.exp(-x**2 / 8)
        fig.add_trace(go.Scatter(
            x=x, y=psi_medium,
            mode="lines", fill="tozeroy",
            line=dict(color="yellow", width=2),
            fillcolor="rgba(255, 255, 0, 0.3)",
            name="Medium: Δx medium, Δp medium",
        ))

        # Spread out (definite momentum)
        psi_spread = 0.5 * np.exp(-x**2 / 50)
        fig.add_trace(go.Scatter(
            x=x, y=psi_spread - 2,
            mode="lines", fill="tozeroy",
            line=dict(color="orange", width=2),
            fillcolor="rgba(255, 165, 0, 0.3)",
            name="Delocalized: Δx large, Δp small",
        ))

        fig.update_layout(
            title=dict(
                text="<b>Uncertainty Principle:</b> Δx · Δp ≥ ℏ/2<br><sub>Position and momentum cannot both be precisely defined</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Position", showgrid=False),
            yaxis=dict(title="Probability amplitude |ψ|²", showgrid=False,
                      showticklabels=False, zeroline=False),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            plot_bgcolor="rgba(0,0,30,0.9)",
        )

        return fig

    uncertainty_fig = create_uncertainty_visualization()
    uncertainty_fig
    return create_uncertainty_visualization, uncertainty_fig


@app.cell
def _(mo):
    mo.accordion(
        {
            "How does this connect to the double-slit experiment?": mo.md(
                r"""
        The uncertainty principle explains why measuring "which slit" destroys interference:

        To determine which slit an electron went through, you need to localize it to within
        the slit separation $d$. This means $\Delta x \approx d$.

        By the uncertainty principle: $\Delta p \geq \hbar / (2d)$

        This momentum uncertainty causes the electron's trajectory to become uncertain by an
        angle $\Delta \theta \approx \Delta p / p$.

        The interference fringes have angular spacing $\theta_{fringe} \approx \lambda / d$.

        Using de Broglie: $\lambda = h/p$, so $\theta_{fringe} \approx h / (pd)$

        Comparing: $\Delta \theta \approx \hbar / (pd) \approx \theta_{fringe}$

        The measurement uncertainty is exactly enough to wash out the fringes!
        Nature is consistent—you can't cheat the uncertainty principle.
        """
            ),
            "Philosophical implications": mo.md(
                r"""
        Wave-particle duality raises deep questions about the nature of reality:

        **Copenhagen interpretation:** The wave function represents our knowledge, not
        reality. Before measurement, the electron doesn't have a definite position—it's
        meaningless to ask "where is it?"

        **Many-worlds interpretation:** The electron goes through both slits, and the
        universe splits. In one branch you detect it at slit A, in another at slit B.

        **Pilot wave theory:** The electron is always a particle, but it's guided by a
        real wave that goes through both slits.

        **Feynman's pragmatism:**
        > *"Do not keep saying to yourself, 'But how can it be like that?' because you
        > will go down the drain into a blind alley from which nobody has yet escaped.
        > Nobody knows how it can be like that."*

        The mathematics works. The predictions match experiments to extraordinary precision.
        Whether we can "understand" it in classical terms may be asking the wrong question.
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

        ## Probability Amplitudes: The Quantum Rule

        Feynman developed a beautiful way to think about quantum mechanics using
        **probability amplitudes**.

        **Classical probability:** The probability of A *or* B happening is $P(A) + P(B)$

        **Quantum mechanics:** We add **amplitudes** (complex numbers), then square:

        $$\begin{aligned}
        P &= |\psi_A + \psi_B|^2 \\
        &= |\psi_A|^2 + |\psi_B|^2 + 2\text{Re}(\psi_A^* \psi_B)
        \end{aligned}$$

        That last term—the **interference term**—is what makes quantum mechanics different.
        It can be positive (constructive) or negative (destructive).

        **The path integral formulation:**

        Feynman showed that a particle's amplitude to go from A to B is the sum over
        **all possible paths**, each weighted by $e^{iS/\hbar}$ where $S$ is the classical action.

        $$\psi(B) = \sum_{\text{paths}} e^{iS[\text{path}]/\hbar}$$

        For macroscopic objects, nearby paths have very different phases and cancel out—
        except near the classical path, where $S$ is stationary. This is why baseballs
        follow Newton's laws while electrons do strange things.
        """
    )
    return


@app.cell
def _(go, np):
    def create_path_integral_animation():
        """Visualize Feynman path integral concept."""
        n_frames = 60
        np.random.seed(42)

        frames = []

        # Generate multiple paths from A to B
        n_paths = 15
        n_points = 50

        start = np.array([0, 0])
        end = np.array([10, 0])

        for i in range(n_frames):
            t = i / n_frames
            frame_data = []

            # Draw paths with varying "craziness"
            for path_idx in range(n_paths):
                # Classical-ish path has less deviation
                deviation = 0.5 + path_idx * 0.3

                x = np.linspace(0, 10, n_points)
                # Random walk-like path
                np.random.seed(42 + path_idx)
                y_offsets = np.cumsum(np.random.randn(n_points) * deviation * 0.1)
                # Force to start and end at 0
                y = y_offsets - y_offsets[0] - (y_offsets[-1] - y_offsets[0]) * np.linspace(0, 1, n_points)

                # Phase based on "action" (roughly path length)
                path_length = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
                phase = path_length * 2 + 2 * np.pi * t * 3

                # Color based on phase
                color = f"hsla({(phase * 30) % 360}, 70%, 50%, 0.5)"

                frame_data.append(go.Scatter(
                    x=x, y=y,
                    mode="lines",
                    line=dict(color=color, width=1.5),
                    showlegend=False,
                ))

            # Classical path (straight line, emphasized)
            frame_data.append(go.Scatter(
                x=[0, 10], y=[0, 0],
                mode="lines",
                line=dict(color="white", width=3),
                name="Classical path",
            ))

            # Start and end points
            frame_data.append(go.Scatter(
                x=[0, 10], y=[0, 0],
                mode="markers+text",
                marker=dict(size=15, color=["green", "red"]),
                text=["A", "B"],
                textposition="top center",
                textfont=dict(size=14, color="white"),
                name="Endpoints",
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Feynman Path Integral:</b> Sum Over All Paths<br><sub>Each path contributes with phase e<sup>iS/ℏ</sup> — crazy paths cancel out</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                          range=[-4, 4], scaleanchor="x"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                plot_bgcolor="rgba(0,0,30,0.95)",
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

    path_integral_fig = create_path_integral_animation()
    path_integral_fig
    return create_path_integral_animation, path_integral_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Wave-Particle Duality

        | Aspect | Wave behavior | Particle behavior |
        |--------|--------------|-------------------|
        | **Evidence** | Interference, diffraction | Photoelectric effect, discrete detection |
        | **When observed** | Paths indistinguishable | Paths measured/distinguishable |
        | **Math** | Add amplitudes, then square | Add probabilities directly |
        | **Formula** | $P = |\psi_1 + \psi_2|^2$ | $P = P_1 + P_2$ |

        **Key insights:**

        1. **Complementarity:** Wave and particle are complementary descriptions. Which
           you see depends on what you measure.

        2. **Measurement matters:** The act of observation fundamentally affects the system.

        3. **Probability is fundamental:** Quantum mechanics predicts probabilities, not
           definite outcomes. This isn't ignorance—it's nature.

        4. **Everything is quantum:** Electrons, photons, atoms, even large molecules
           show wave-particle duality. The classical world emerges from quantum mechanics
           in the limit of large systems.

        ---

        > *"The more you see how strangely Nature behaves, the harder it is to make a model
        > that explains how even the simplest phenomena actually work. So theoretical physics
        > has given up on that."*
        > — Richard Feynman

        *This is the foundation upon which all of quantum mechanics is built. From here,
        we can understand atoms, molecules, solids, lasers, transistors—the entire modern world.*
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

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1965). *The Feynman Lectures on Physics, Volume III*.
          Addison-Wesley.
          - [Chapter 1: Quantum Behavior](https://www.feynmanlectures.caltech.edu/III_01.html) — The double-slit experiment
          - [Chapter 2: The Relation of Wave and Particle Viewpoints](https://www.feynmanlectures.caltech.edu/III_02.html)
          - [Chapter 3: Probability Amplitudes](https://www.feynmanlectures.caltech.edu/III_03.html)

        ### Key Experiments

        - **Young's Double-Slit Experiment** (1801)
          - Thomas Young demonstrated wave interference of light
          - Fringe spacing: $\Delta y = \lambda L / d$

        - **Photoelectric Effect** (Einstein, 1905)
          - Light comes in quanta (photons) with energy $E = h\nu$
          - Nobel Prize 1921
          - Planck's constant: $h = 6.626 \times 10^{-34}$ J⋅s

        - **Electron Diffraction** (Davisson & Germer, 1927)
          - Confirmed de Broglie's matter wave hypothesis
          - Nobel Prize 1937

        ### Mathematical Framework

        - **de Broglie Wavelength** (1924)
          - $\lambda = h/p = h/(mv)$
          - Matter has wave-like properties
          - Nobel Prize 1929

        - **Heisenberg Uncertainty Principle** (1927)
          - $\Delta x \cdot \Delta p \geq \hbar/2$
          - $\Delta E \cdot \Delta t \geq \hbar/2$
          - Reduced Planck constant: $\hbar = h/(2\pi) = 1.055 \times 10^{-34}$ J⋅s

        - **Feynman Path Integral** (1948)
          - Amplitude: $\langle x_f | x_i \rangle = \int \mathcal{D}[x(t)] \, e^{iS[x]/\hbar}$
          - Sum over all possible paths
          - Action: $S = \int L \, dt$

        ### Further Reading

        - **Feynman Lectures**: [Volume III, Chapter 4: Identical Particles](https://www.feynmanlectures.caltech.edu/III_04.html)
        - Feynman, R. P. *QED: The Strange Theory of Light and Matter* — Popular introduction
        - Sakurai, J. J. *Modern Quantum Mechanics* — Graduate-level treatment
        - Griffiths, D. J. *Introduction to Quantum Mechanics* — Undergraduate textbook
        """
    )
    return


if __name__ == "__main__":
    app.run()
