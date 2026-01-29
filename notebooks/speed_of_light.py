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
        # The Speed of Light

        *An interactive exploration based on [Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/)*

        ---

        ## Why Does the Speed of Light Matter?

        The speed of light, denoted $c$, is arguably the most important constant in physics.
        It's not just "how fast light travels"—it's the **cosmic speed limit**, the conversion
        factor between space and time, and the key to understanding why $E = mc^2$.

        $$c = 299,792,458 \text{ m/s}$$

        This is exact—not measured, but *defined*. Since 1983, the meter itself is defined as
        the distance light travels in 1/299,792,458 of a second!

        But how did we discover this value? The story spans four centuries of increasingly
        clever experiments, culminating in one of the most precise measurements in all of science.

        **What makes $c$ special:**
        - It's the same for all observers, regardless of their motion (Einstein's postulate)
        - Nothing with mass can reach it; nothing with mass can even get close without infinite energy
        - It connects electricity and magnetism: $c = 1/\sqrt{\epsilon_0 \mu_0}$
        - It sets the scale for all of special relativity
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The First Measurement: Rømer and Jupiter's Moons (1676)

        Before Rømer, many scientists believed light traveled instantaneously. Galileo tried
        to measure it with lanterns on hilltops—but light was far too fast for human reaction times.

        **Ole Rømer's brilliant insight:** Use the solar system as a laboratory!

        Rømer studied Io, one of Jupiter's moons, which orbits Jupiter every 42.5 hours like
        clockwork. He noticed something strange: when Earth was moving *away* from Jupiter,
        Io's eclipses (when it passes behind Jupiter) seemed to come later than predicted.
        When Earth moved *toward* Jupiter, they came early.

        **The explanation:** Light takes time to travel! When Earth is farther from Jupiter,
        the light announcing Io's eclipse has farther to travel, so we see it later.

        **Rømer's calculation:**
        - The maximum delay was about 22 minutes (we now know it's closer to 16.6 minutes)
        - This delay corresponds to light crossing Earth's orbital diameter
        - Earth's orbital diameter ≈ 300 million km

        $$c \approx \frac{300,000,000 \text{ km}}{1000 \text{ s}} \approx 300,000 \text{ km/s}$$

        Not bad for the 17th century! Modern value: 299,792 km/s.

        *The animation below shows how Earth's changing distance from Jupiter affects when we see Io's eclipses.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_romer_animation():
        """Animate Rømer's observation of Jupiter's moons."""
        n_frames = 80

        # Orbits (not to scale, for visualization)
        theta = np.linspace(0, 2 * np.pi, 100)

        # Earth orbit (inner)
        earth_orbit_r = 1.0
        earth_orbit_x = earth_orbit_r * np.cos(theta)
        earth_orbit_y = earth_orbit_r * np.sin(theta)

        # Jupiter orbit (outer) - Jupiter moves slower
        jupiter_orbit_r = 2.5
        jupiter_orbit_x = jupiter_orbit_r * np.cos(theta)
        jupiter_orbit_y = jupiter_orbit_r * np.sin(theta)

        # Create frames
        frames = []
        for i in range(n_frames):
            # Earth completes ~1 orbit while Jupiter moves ~1/12 of orbit
            earth_angle = 2 * np.pi * i / n_frames
            jupiter_angle = 2 * np.pi * i / (n_frames * 12) + np.pi  # Start opposite side

            earth_x = earth_orbit_r * np.cos(earth_angle)
            earth_y = earth_orbit_r * np.sin(earth_angle)

            jupiter_x = jupiter_orbit_r * np.cos(jupiter_angle)
            jupiter_y = jupiter_orbit_r * np.sin(jupiter_angle)

            # Distance between Earth and Jupiter
            distance = np.sqrt((jupiter_x - earth_x)**2 + (jupiter_y - earth_y)**2)

            # Light ray from Jupiter to Earth
            light_x = [jupiter_x, earth_x]
            light_y = [jupiter_y, earth_y]

            frame_data = [
                # Sun
                go.Scatter(x=[0], y=[0], mode="markers",
                          marker=dict(size=20, color="gold"), name="Sun"),
                # Earth orbit
                go.Scatter(x=earth_orbit_x, y=earth_orbit_y, mode="lines",
                          line=dict(color="lightblue", width=1, dash="dot"), name="Earth orbit"),
                # Jupiter orbit
                go.Scatter(x=jupiter_orbit_x, y=jupiter_orbit_y, mode="lines",
                          line=dict(color="lightyellow", width=1, dash="dot"), name="Jupiter orbit"),
                # Earth
                go.Scatter(x=[earth_x], y=[earth_y], mode="markers",
                          marker=dict(size=12, color="steelblue"), name="Earth"),
                # Jupiter
                go.Scatter(x=[jupiter_x], y=[jupiter_y], mode="markers",
                          marker=dict(size=16, color="orange"), name="Jupiter"),
                # Light path
                go.Scatter(x=light_x, y=light_y, mode="lines",
                          line=dict(color="yellow", width=2, dash="dash"),
                          name=f"Light path: {distance:.2f} AU"),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Rømer's Method:</b> Earth-Jupiter Distance Changes<br><sub>Watch how the light travel time varies as Earth orbits</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(scaleanchor="y", range=[-3.5, 3.5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False, showticklabels=False),
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
                                 args=[None, {"frame": {"duration": 100, "redraw": True},
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

    romer_fig = create_romer_animation()
    romer_fig
    return (create_romer_animation, romer_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Fizeau's Rotating Wheel (1849)

        The first *terrestrial* measurement of light speed came from Hippolyte Fizeau.
        His ingenious method: use a spinning toothed wheel to chop a light beam into pulses,
        then measure how fast the wheel must spin so that the returning light is blocked.

        **How it worked:**

        1. A light beam passes through a gap between two teeth of a spinning wheel
        2. The light travels to a mirror 8.6 km away and reflects back
        3. By the time it returns, the wheel has rotated slightly
        4. If the wheel spins at just the right speed, the next *tooth* blocks the returning light

        **The calculation:**

        - Distance to mirror and back: $2 \times 8.6$ km $= 17.2$ km
        - The wheel had 720 teeth, so gaps were separated by $1/720$ of a rotation
        - Light was blocked when the wheel spun at 12.6 rotations/second
        - Time for light to travel: $\frac{1}{720 \times 12.6} = \frac{1}{9072}$ seconds

        $$c = \frac{17,200 \text{ m}}{1/9072 \text{ s}} \approx 313,000 \text{ km/s}$$

        Within 5% of the modern value—remarkable for a tabletop experiment!

        *The animation below shows how the rotating wheel method works.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_fizeau_animation():
        """Animate Fizeau's rotating wheel experiment."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            rotation = 2 * np.pi * i / 20  # Wheel rotation

            # Toothed wheel (8 teeth for visibility)
            n_teeth = 8
            wheel_theta = np.linspace(0, 2 * np.pi, 200)
            wheel_r = 0.5 + 0.15 * np.sin(n_teeth * (wheel_theta + rotation))
            wheel_x = wheel_r * np.cos(wheel_theta) - 2
            wheel_y = wheel_r * np.sin(wheel_theta)

            # Check if light can pass (simplified)
            tooth_phase = (n_teeth * rotation) % (2 * np.pi)
            light_passes = np.sin(tooth_phase) > 0

            # Mirror
            mirror_x = [2, 2]
            mirror_y = [-0.3, 0.3]

            # Light beam (only if passing through gap)
            if light_passes:
                # Outgoing light
                light_out_x = [-1.5, 2]
                light_out_y = [0, 0]
                # Return light (slightly offset for visibility)
                pulse_pos = (i % 15) / 15  # Animate pulse position
                if pulse_pos < 0.5:
                    light_ret_x = [-1.5 + pulse_pos * 7, -1.5 + pulse_pos * 7 + 0.3]
                    light_ret_y = [0.05, 0.05]
                else:
                    light_ret_x = [2 - (pulse_pos - 0.5) * 7, 2 - (pulse_pos - 0.5) * 7 + 0.3]
                    light_ret_y = [0.05, 0.05]
                light_color = "yellow"
            else:
                light_out_x = [-1.5, -1.3]
                light_out_y = [0, 0]
                light_ret_x = []
                light_ret_y = []
                light_color = "rgba(255,255,0,0.3)"

            frame_data = [
                # Wheel
                go.Scatter(x=wheel_x, y=wheel_y, mode="lines", fill="toself",
                          fillcolor="rgba(100,100,100,0.5)", line=dict(color="gray", width=2),
                          name="Toothed wheel"),
                # Light source
                go.Scatter(x=[-3], y=[0], mode="markers",
                          marker=dict(size=15, color="white", line=dict(color="yellow", width=2)),
                          name="Light source"),
                # Mirror
                go.Scatter(x=mirror_x, y=mirror_y, mode="lines",
                          line=dict(color="silver", width=8), name="Mirror (8.6 km away)"),
                # Outgoing light
                go.Scatter(x=light_out_x, y=light_out_y, mode="lines",
                          line=dict(color=light_color, width=4), name="Light beam"),
            ]

            if light_ret_x:
                frame_data.append(
                    go.Scatter(x=light_ret_x, y=light_ret_y, mode="lines",
                              line=dict(color="yellow", width=4), name="Returning light")
                )

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Fizeau's Rotating Wheel:</b> First Terrestrial Measurement<br><sub>Light passes through gap, reflects, returns—will it pass through the next gap?</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-4, 3], showgrid=False, zeroline=False, showticklabels=False),
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
                plot_bgcolor="rgba(0,0,30,0.9)",
            ),
            frames=frames,
        )

        return fig

    fizeau_fig = create_fizeau_animation()
    fizeau_fig
    return (create_fizeau_animation, fizeau_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Foucault's Rotating Mirror (1850)

        Just a year after Fizeau, Léon Foucault improved the method using a rotating *mirror*
        instead of a toothed wheel. This allowed for much shorter distances and higher precision.

        **The key insight:**

        A rotating mirror changes angle while light travels to a distant fixed mirror and back.
        The returning beam hits the rotating mirror at a slightly different angle, causing a
        measurable deflection in the final image.

        **Advantages over Fizeau's method:**
        - Could work with shorter distances (just 20 meters in Foucault's setup!)
        - Gave a continuous measurement, not just "blocked" or "not blocked"
        - Could detect smaller differences in light speed

        **Foucault's result:** $c \approx 298,000$ km/s

        **Historical importance:** Foucault also showed that light travels *slower* in water
        than in air—a crucial test that proved light was a wave, not a particle (in the
        classical sense). Newton's particle theory predicted light should travel *faster*
        in denser media!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Maxwell's Theoretical Prediction (1865)

        While experimentalists were refining their measurements, James Clerk Maxwell made a
        stunning theoretical discovery. He unified electricity and magnetism into four elegant
        equations and found they predicted electromagnetic waves that travel at:

        $$c = \frac{1}{\sqrt{\epsilon_0 \mu_0}}$$

        where:
        - $\epsilon_0$ = permittivity of free space (from electrostatics)
        - $\mu_0$ = permeability of free space (from magnetostatics)

        **The shocking result:** When Maxwell plugged in the measured values of $\epsilon_0$
        and $\mu_0$ (from completely separate experiments with capacitors and inductors),
        he got $c \approx 310,000$ km/s—almost exactly the measured speed of light!

        Maxwell's conclusion: **Light is an electromagnetic wave.**

        > *"We can scarcely avoid the conclusion that light consists in the transverse
        > undulations of the same medium which is the cause of electric and magnetic phenomena."*
        > — James Clerk Maxwell, 1865

        This was one of the great unifications in physics history—optics, electricity, and
        magnetism were all aspects of the same phenomenon.
        """
    )
    return


@app.cell
def _(go, np):
    # Show the relationship c = 1/sqrt(ε₀μ₀)
    def create_em_wave_animation():
        """Animate an electromagnetic wave showing E and B fields."""
        n_frames = 60
        frames = []

        for i in range(n_frames):
            phase = 2 * np.pi * i / n_frames

            # Wave propagation
            x = np.linspace(0, 4 * np.pi, 200)

            # E field (vertical)
            E = np.sin(x - phase)

            # B field (horizontal, perpendicular to E)
            B = np.sin(x - phase)

            frame_data = [
                # E field
                go.Scatter3d(
                    x=x, y=np.zeros_like(x), z=E,
                    mode="lines",
                    line=dict(color="red", width=4),
                    name="Electric field (E)"
                ),
                # B field
                go.Scatter3d(
                    x=x, y=B, z=np.zeros_like(x),
                    mode="lines",
                    line=dict(color="blue", width=4),
                    name="Magnetic field (B)"
                ),
                # Propagation axis
                go.Scatter3d(
                    x=[0, 4*np.pi], y=[0, 0], z=[0, 0],
                    mode="lines",
                    line=dict(color="white", width=2, dash="dash"),
                    name="Direction of propagation"
                ),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Electromagnetic Wave:</b> E and B Fields Perpendicular<br><sub>Light is oscillating electric and magnetic fields traveling at speed c</sub>",
                    font=dict(size=16),
                ),
                scene=dict(
                    xaxis=dict(title="Propagation direction", showgrid=False),
                    yaxis=dict(title="B field", showgrid=False),
                    zaxis=dict(title="E field", showgrid=False),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
                ),
                showlegend=True,
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
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
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

    em_wave_fig = create_em_wave_animation()
    em_wave_fig
    return (create_em_wave_animation, em_wave_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Michelson's Precision Measurements (1879-1926)

        Albert Michelson dedicated much of his career to measuring the speed of light with
        ever-increasing precision. His rotating mirror experiments achieved accuracies that
        stood for decades.

        **Michelson's 1926 measurement:**
        - Used an octagonal rotating mirror
        - Light path of 35 km (between Mount Wilson and Mount San Antonio in California)
        - Result: $c = 299,796 \pm 4$ km/s

        **The method:**

        An octagonal mirror rotating at precisely the right speed would reflect the returning
        light beam at exactly the same angle as the outgoing beam. By measuring the rotation
        speed needed, Michelson could calculate $c$ with unprecedented accuracy.

        **Fun fact:** For his work on precision optical measurements, Michelson became the
        first American to win the Nobel Prize in Physics (1907).
        """
    )
    return


@app.cell
def _(go, np):
    # Historical measurements comparison
    measurements = {
        "Rømer (1676)": 220000,
        "Bradley (1729)": 301000,
        "Fizeau (1849)": 315000,
        "Foucault (1850)": 298000,
        "Michelson (1879)": 299910,
        "Michelson (1926)": 299796,
        "Modern (defined)": 299792.458,
    }

    years = [1676, 1729, 1849, 1850, 1879, 1926, 1983]
    values = list(measurements.values())
    names = list(measurements.keys())

    modern_c = 299792.458

    history_fig = go.Figure()

    # Measurements
    history_fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode="markers+text",
        text=names,
        textposition="top center",
        marker=dict(size=12, color="steelblue"),
        name="Measurements"
    ))

    # Modern value line
    history_fig.add_hline(y=modern_c, line_dash="dash", line_color="red",
                         annotation_text=f"Modern value: {modern_c} km/s")

    history_fig.update_layout(
        title=dict(
            text="<b>Historical Measurements of the Speed of Light</b><br><sub>Four centuries of increasing precision</sub>",
            font=dict(size=16),
        ),
        xaxis_title="Year",
        yaxis_title="Speed of light (km/s)",
        yaxis=dict(range=[200000, 350000]),
        showlegend=False,
    )

    history_fig
    return history_fig, measurements, modern_c, names, values, years


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Modern Definition (1983)

        Today, we don't *measure* the speed of light—we *define* it:

        $$c = 299,792,458 \text{ m/s exactly}$$

        This might seem circular, but it's actually clever. The second is defined by atomic
        clocks (the frequency of cesium-133 atoms), and the meter is defined as the distance
        light travels in exactly $1/299,792,458$ of a second.

        **Why define it this way?**

        1. We can measure time (atomic clocks) far more precisely than distance
        2. It makes $c$ exact by definition, eliminating measurement uncertainty
        3. Length measurements become time measurements, which are more precise

        **The philosophical shift:**

        Before 1983: "How far does light travel in one second?"
        After 1983: "How long does it take light to travel one meter?"

        The answer to the second question is *defined* to be exactly $1/299,792,458$ seconds.
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "Why is c the same for all observers? (Preview of Special Relativity)": mo.md(
                r"""
        Here's the mystery that led Einstein to special relativity:

        **The problem:**

        If you're on a train moving at 100 km/h and throw a ball forward at 50 km/h, someone
        on the ground sees the ball moving at 150 km/h. Velocities add.

        But light doesn't work this way! If you're on a spaceship moving at 0.5c and shine
        a flashlight forward, you measure the light moving at $c$. And someone "stationary"
        also measures that same light moving at $c$—not $1.5c$!

        **Einstein's postulate (1905):**

        > *The speed of light in vacuum is the same for all observers, regardless of their motion.*

        This isn't intuitive—it seems to violate basic addition. But experiment after experiment
        confirms it. The resolution requires abandoning our intuitive notions of absolute time
        and absolute space.

        **The Michelson-Morley experiment (1887):**

        Michelson and Morley tried to detect Earth's motion through the supposed "luminiferous
        ether" by measuring tiny differences in light speed. They found *nothing*—light speed
        was the same in all directions, regardless of Earth's motion through space.

        This "null result" was one of the most important experiments in physics history,
        paving the way for Einstein's special theory of relativity.

        *Continue to the next notebook to explore what happens when we take the constancy
        of c seriously...*
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

        ## Summary: Measuring the Unmeasurable

        | Method | Year | Result (km/s) | Key Innovation |
        |--------|------|---------------|----------------|
        | **Rømer** | 1676 | ~220,000 | Used Jupiter's moons as a cosmic clock |
        | **Bradley** | 1729 | ~301,000 | Stellar aberration (tilting telescopes) |
        | **Fizeau** | 1849 | ~315,000 | First terrestrial measurement (toothed wheel) |
        | **Foucault** | 1850 | ~298,000 | Rotating mirror (shorter distances) |
        | **Maxwell** | 1865 | ~310,000 | *Theoretical*—from $\epsilon_0$ and $\mu_0$ |
        | **Michelson** | 1926 | 299,796 | Precision rotating mirrors |
        | **Modern** | 1983 | 299,792.458 | *Defined exactly* |

        **Key insights:**

        1. Light has a finite speed—it takes time to travel across the universe
        2. This speed is enormous by everyday standards (~1 billion km/h)
        3. Maxwell showed light is an electromagnetic wave, connecting optics to electricity
        4. The constancy of $c$ for all observers leads to special relativity

        ---

        > *"The speed of light is not just a number—it's the speed of causality, the cosmic
        > speed limit that shapes the structure of spacetime itself."*

        *Continue to the **Spacetime** notebook to explore Einstein's revolutionary conclusions...*
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

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1963). *The Feynman Lectures on Physics*.
          Addison-Wesley.
          - [Volume I, Chapter 15: The Special Theory of Relativity](https://www.feynmanlectures.caltech.edu/I_15.html)
            (discusses the constancy of $c$)
          - [Volume II, Chapter 18: The Maxwell Equations](https://www.feynmanlectures.caltech.edu/II_18.html)

        ### Historical Measurements

        - **Rømer, O.** (1676). First measurement using Jupiter's moon Io.
          Estimated $c \approx 220{,}000$ km/s.

        - **Fizeau, H.** (1849). Toothed wheel method.
          Result: $c \approx 315{,}000$ km/s.

        - **Foucault, L.** (1850). Rotating mirror method.
          Result: $c \approx 298{,}000$ km/s.

        - **Michelson, A. A.** (1926). Precision rotating mirror.
          Result: $c = 299{,}796$ km/s.

        ### Maxwell's Theoretical Prediction

        - **Maxwell, J. C.** (1865). "A Dynamical Theory of the Electromagnetic Field".
          Philosophical Transactions of the Royal Society, 155, 459-512.
          - Predicted $c = 1/\sqrt{\epsilon_0 \mu_0}$
          - Connected light to electromagnetic waves

        ### Modern Definition

        - **SI Definition** (1983): The speed of light is *exactly*
          $c = 299{,}792{,}458$ m/s by definition.
          - The meter is now defined as the distance light travels in $1/299{,}792{,}458$ seconds

        ### Key Constants

        - Vacuum permittivity: $\epsilon_0 = 8.854 \times 10^{-12}$ F/m
        - Vacuum permeability: $\mu_0 = 4\pi \times 10^{-7}$ H/m
        - Speed of light: $c = 1/\sqrt{\epsilon_0 \mu_0} = 299{,}792{,}458$ m/s

        ### Further Reading

        - **Feynman Lectures**: [Volume I, Chapter 17: Space-Time](https://www.feynmanlectures.caltech.edu/I_17.html)
        - Galison, P. *Einstein's Clocks, Poincaré's Maps* — Historical context
        """
    )
    return


if __name__ == "__main__":
    app.run()
