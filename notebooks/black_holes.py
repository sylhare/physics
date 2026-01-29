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
        # Black Holes: Where Spacetime Breaks Down

        *An interactive exploration based on [Feynman Lectures on Physics, Volume II, Chapter 42: Curved Space](https://www.feynmanlectures.caltech.edu/II_42.html) and general relativity*

        ---

        ## The Ultimate Extreme

        Black holes are regions of spacetime where gravity is so strong that **nothing—not even
        light—can escape**. They represent the most extreme predictions of Einstein's general
        relativity, where our intuitions about space, time, and causality break down completely.

        What makes black holes so fascinating:

        - **The event horizon**: A one-way boundary in spacetime
        - **Time and space swap roles**: Inside a black hole, falling inward is as inevitable as aging
        - **Infinite time dilation**: Time stops at the horizon (from an outside observer's view)
        - **The singularity**: Where density becomes infinite and physics breaks down
        - **Information paradox**: What happens to information that falls in?

        > *"Black holes ain't so black."* — Stephen Hawking

        Let's explore these cosmic monsters and understand what they tell us about the
        nature of spacetime itself.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 1. The Schwarzschild Radius

        ### When Escape Velocity Reaches Light Speed

        Every massive object has a theoretical "point of no return" radius. If you compressed
        the object smaller than this radius, not even light could escape.

        This is the **Schwarzschild radius**, named after Karl Schwarzschild who found the
        first exact solution to Einstein's equations in 1916 (while serving in WWI!):

        $$r_s = \frac{2GM}{c^2}$$

        **In plain language:** The Schwarzschild radius is proportional to mass. Double the mass,
        double the radius. For the Sun, it's about 3 km. For Earth, it's about 9 mm!

        | Object | Mass | Schwarzschild Radius |
        |--------|------|---------------------|
        | Earth | 6 × 10²⁴ kg | 9 mm |
        | Sun | 2 × 10³⁰ kg | 3 km |
        | Sagittarius A* | 4 × 10⁶ M☉ | 12 million km |
        | M87* | 6.5 × 10⁹ M☉ | 19 billion km |

        If an object is compressed within its Schwarzschild radius, it becomes a **black hole**.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Schwarzschild radius and escape velocity
    def create_schwarzschild_animation():
        n_frames = 100
        frames = []

        # Show object being compressed
        r_initial = 3.0
        r_schwarzschild = 1.0  # Normalized

        for frame in range(n_frames):
            progress = frame / n_frames
            frame_data = []

            # Current radius of the collapsing star
            if progress < 0.7:
                r_current = r_initial - (r_initial - r_schwarzschild * 1.5) * (progress / 0.7)
            else:
                # Collapse accelerates
                remaining = (progress - 0.7) / 0.3
                r_current = r_schwarzschild * 1.5 - (r_schwarzschild * 1.5 - r_schwarzschild * 0.3) * remaining

            # Schwarzschild radius (constant, shown as dashed circle)
            theta = np.linspace(0, 2 * np.pi, 100)
            frame_data.append(go.Scatter(
                x=r_schwarzschild * np.cos(theta),
                y=r_schwarzschild * np.sin(theta),
                mode="lines",
                line=dict(color="red", width=2, dash="dash"),
                name=f"Event horizon (r_s = {r_schwarzschild})",
            ))

            # Collapsing star
            frame_data.append(go.Scatter(
                x=r_current * np.cos(theta),
                y=r_current * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 200, 100, 0.5)" if r_current > r_schwarzschild else "rgba(50, 50, 50, 0.9)",
                line=dict(color="orange" if r_current > r_schwarzschild else "black", width=2),
                name="Collapsing star",
            ))

            # Light rays trying to escape
            n_rays = 8
            for i in range(n_rays):
                angle = i * 2 * np.pi / n_rays
                start_r = r_current * 0.9

                # Ray length depends on whether inside horizon
                if r_current > r_schwarzschild:
                    # Light can escape (gets dimmer as we approach horizon)
                    escape_factor = (r_current - r_schwarzschild) / (r_initial - r_schwarzschild)
                    ray_length = 1.5 * escape_factor + 0.3
                    ray_color = f"rgba(255, 255, 0, {0.3 + 0.7 * escape_factor})"
                else:
                    # Light cannot escape - rays curve back
                    ray_length = 0.2
                    ray_color = "rgba(255, 0, 0, 0.5)"

                x_start = start_r * np.cos(angle)
                y_start = start_r * np.sin(angle)
                x_end = (start_r + ray_length) * np.cos(angle)
                y_end = (start_r + ray_length) * np.sin(angle)

                frame_data.append(go.Scatter(
                    x=[x_start, x_end],
                    y=[y_start, y_end],
                    mode="lines",
                    line=dict(color=ray_color, width=2),
                    showlegend=(i == 0),
                    name="Light rays" if i == 0 else None,
                ))

            # Escape velocity indicator
            if r_current > r_schwarzschild:
                v_escape = min(1.0, np.sqrt(r_schwarzschild / r_current))
            else:
                v_escape = 1.0  # Already beyond c

            frame_data.append(go.Scatter(
                x=[3.5], y=[2],
                mode="text",
                text=[f"v_escape = {v_escape:.2f}c"],
                textfont=dict(size=14, color="yellow" if v_escape < 1 else "red"),
                showlegend=False,
            ))

            # Status
            if r_current > r_schwarzschild:
                status = "Star collapsing..."
            else:
                status = "BLACK HOLE FORMED!"

            frame_data.append(go.Scatter(
                x=[0], y=[3.5],
                mode="text",
                text=[status],
                textfont=dict(size=16, color="white" if r_current > r_schwarzschild else "red"),
                showlegend=False,
            ))

            # Radius indicator
            frame_data.append(go.Scatter(
                x=[3.5], y=[1.5],
                mode="text",
                text=[f"r = {r_current:.2f} r_s"],
                textfont=dict(size=12, color="orange"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Gravitational Collapse to Black Hole</b><br><sub>When r < r_s, light cannot escape</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-4, 5], showgrid=False, zeroline=False, scaleanchor="y"),
                yaxis=dict(range=[-4, 4], showgrid=False, zeroline=False),
                showlegend=True,
                legend=dict(x=0.7, y=0.3),
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

    schwarzschild_fig = create_schwarzschild_animation()
    schwarzschild_fig
    return (create_schwarzschild_animation, schwarzschild_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Physics of the Event Horizon

        The animation shows a star collapsing. As it shrinks:

        1. **Escape velocity increases** as $v_{escape} = \sqrt{2GM/r}$
        2. **Light struggles more** to escape (shown dimmer)
        3. **At the Schwarzschild radius**, escape velocity equals $c$
        4. **Inside the horizon**, even light falls back in

        **Important clarification:** The event horizon isn't a physical surface—it's a
        **boundary in spacetime**. An astronaut falling through would notice nothing special
        at that moment. But they could never return or send signals back out.

        The name "Schwarzschild" means "black shield" in German—a fitting name for the
        boundary that shields us from seeing what's inside!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 2. Light Cones and Causality

        ### How Spacetime Diagrams Reveal Black Hole Physics

        To understand black holes properly, we need **spacetime diagrams**. These show
        both space (horizontal) and time (vertical) together.

        **Light cones** are crucial: they show all possible paths light can take from
        an event. Since nothing travels faster than light, your entire future must lie
        within your future light cone.

        In flat spacetime (far from gravity):
        - Light cones are symmetric, tilted at 45°
        - You can move left or right freely
        - Time always moves "up"

        Near a black hole, **light cones tilt toward the singularity**. This tilting
        is the geometric way of saying "gravity pulls everything in."
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Light cones tilting near a black hole
    def create_light_cone_animation():
        n_frames = 80
        frames = []

        # Schwarzschild radius
        r_s = 2.0

        for frame in range(n_frames):
            # Observer falling toward black hole
            progress = frame / n_frames
            r_observer = 6.0 - progress * 5.5  # From r=6 to r=0.5

            frame_data = []

            # Draw the event horizon
            frame_data.append(go.Scatter(
                x=[r_s, r_s],
                y=[-3, 8],
                mode="lines",
                line=dict(color="red", width=3),
                name="Event horizon",
            ))

            # Singularity
            frame_data.append(go.Scatter(
                x=[0, 0],
                y=[-3, 8],
                mode="lines",
                line=dict(color="white", width=4),
                name="Singularity (r=0)",
            ))

            # Draw light cones at various positions
            positions = [5.5, 4.5, 3.5, 2.5, 1.5, 0.5]
            times = [0, 1.5, 3, 4.5, 6, 7.5]

            for r, t in zip(positions, times):
                # Light cone tilt increases as we approach horizon
                # At infinity: 45°, at horizon: 90° (fully tilted inward)
                if r > r_s:
                    # Outside horizon: tilt factor
                    tilt = 1 - np.sqrt(1 - r_s / r)
                    tilt = min(tilt * 2, 0.9)  # Exaggerate for visibility
                else:
                    # Inside horizon: light cone tilted past vertical
                    tilt = 1.0 + (r_s - r) / r_s * 0.5

                # Light cone edges
                cone_height = 1.0
                # Right edge angle from vertical
                right_angle = np.pi / 4 * (1 - tilt)  # 45° at infinity, 0° at horizon
                # Left edge
                left_angle = np.pi / 4 * (1 + tilt)  # Tilts more than 45° toward center

                if r > r_s:
                    # Outside: both edges point somewhat outward and inward
                    x_right = r + cone_height * np.sin(right_angle)
                    x_left = r - cone_height * np.sin(left_angle)
                    color = "rgba(255, 255, 100, 0.6)"
                else:
                    # Inside: entire cone tilts toward singularity
                    x_right = r - cone_height * 0.3
                    x_left = r - cone_height * 0.8
                    color = "rgba(255, 100, 100, 0.6)"

                # Draw light cone
                frame_data.append(go.Scatter(
                    x=[x_left, r, x_right],
                    y=[t + cone_height, t, t + cone_height],
                    mode="lines",
                    fill="toself",
                    fillcolor=color,
                    line=dict(color="yellow" if r > r_s else "red", width=2),
                    showlegend=False,
                ))

                # Event point
                frame_data.append(go.Scatter(
                    x=[r], y=[t],
                    mode="markers",
                    marker=dict(size=8, color="white"),
                    showlegend=False,
                ))

            # Observer's current position
            t_observer = progress * 7.5
            frame_data.append(go.Scatter(
                x=[r_observer], y=[t_observer],
                mode="markers",
                marker=dict(size=15, color="cyan", symbol="star",
                           line=dict(color="white", width=2)),
                name="Falling observer",
            ))

            # Worldline of observer
            r_trace = np.linspace(6.0, r_observer, 50)
            t_trace = np.linspace(0, t_observer, 50)
            frame_data.append(go.Scatter(
                x=r_trace, y=t_trace,
                mode="lines",
                line=dict(color="cyan", width=2, dash="dot"),
                name="Observer's worldline",
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[5], y=[-2],
                mode="text",
                text=["Outside: can escape"],
                textfont=dict(size=11, color="yellow"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[1], y=[-2],
                mode="text",
                text=["Inside: must fall to r=0"],
                textfont=dict(size=11, color="red"),
                showlegend=False,
            ))

            # Current radius
            status = f"r = {r_observer:.2f}" + (" (outside)" if r_observer > r_s else " (INSIDE!)")
            frame_data.append(go.Scatter(
                x=[5], y=[8.5],
                mode="text",
                text=[status],
                textfont=dict(size=14, color="cyan" if r_observer > r_s else "red"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Light Cones Near a Black Hole</b><br><sub>Cones tilt inward; inside horizon, all futures lead to singularity</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-0.5, 7], title="Radius r", showgrid=True,
                          gridcolor="rgba(100,100,100,0.3)"),
                yaxis=dict(range=[-3, 9], title="Time t", showgrid=True,
                          gridcolor="rgba(100,100,100,0.3)"),
                showlegend=True,
                legend=dict(x=0.65, y=0.35),
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

    light_cone_fig = create_light_cone_animation()
    light_cone_fig
    return (create_light_cone_animation, light_cone_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Light Cone Diagram

        This diagram reveals the deep truth about black holes:

        **Outside the horizon (yellow cones):**
        - Light cones tilt toward the center but still allow escape
        - An observer can fire rockets and move outward
        - Signals can be sent to infinity

        **At the horizon:**
        - The outward edge of the light cone becomes vertical
        - Light aimed directly outward hovers at the horizon forever
        - This is the "point of no return"

        **Inside the horizon (red cones):**
        - The entire light cone points toward r = 0
        - **All possible futures lead to the singularity**
        - Moving "outward" is as impossible as moving backward in time

        **The profound insight:** Inside a black hole, the radial direction becomes timelike.
        Falling toward the singularity isn't like falling down—it's like aging. You can't
        avoid it any more than you can avoid tomorrow.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 3. Gravitational Time Dilation

        ### Time Slows Near Massive Objects

        One of the most striking predictions of general relativity is **gravitational time
        dilation**: clocks run slower in stronger gravitational fields.

        Near a Schwarzschild black hole, a clock at radius $r$ runs slower by a factor:

        $$\frac{d\tau}{dt} = \sqrt{1 - \frac{r_s}{r}}$$

        where $d\tau$ is proper time (what the local clock measures) and $dt$ is coordinate
        time (what a distant observer measures).

        **Key observations:**
        - At $r = \infty$: clocks run normally
        - As $r \to r_s$: the factor approaches zero
        - At the horizon: time appears to stop (from outside)

        This is why we say an object falling into a black hole appears to "freeze" at the
        horizon from an outside perspective—we never see it cross!
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Gravitational time dilation near black hole
    def create_time_dilation_animation():
        n_frames = 120
        frames = []

        r_s = 1.0  # Schwarzschild radius

        for frame in range(n_frames):
            t = frame / n_frames * 4 * np.pi
            frame_data = []

            # Black hole
            theta_bh = np.linspace(0, 2 * np.pi, 100)
            frame_data.append(go.Scatter(
                x=r_s * np.cos(theta_bh),
                y=r_s * np.sin(theta_bh),
                mode="lines",
                fill="toself",
                fillcolor="black",
                line=dict(color="red", width=2),
                name="Event horizon",
            ))

            # Clocks at different radii
            radii = [1.2, 1.5, 2.0, 3.0, 5.0]
            colors = ["red", "orange", "yellow", "lime", "cyan"]

            for r, color in zip(radii, colors):
                # Time dilation factor
                gamma = np.sqrt(1 - r_s / r)

                # Clock tick rate (slower near horizon)
                local_time = t * gamma

                # Clock position
                x_clock = r
                y_clock = 0

                # Draw clock face
                clock_r = 0.2
                clock_theta = np.linspace(0, 2 * np.pi, 30)
                frame_data.append(go.Scatter(
                    x=x_clock + clock_r * np.cos(clock_theta),
                    y=y_clock + clock_r * np.sin(clock_theta),
                    mode="lines",
                    line=dict(color=color, width=2),
                    showlegend=False,
                ))

                # Clock hand
                hand_angle = local_time  # Rotates with local time
                hand_x = x_clock + clock_r * 0.8 * np.sin(hand_angle)
                hand_y = y_clock + clock_r * 0.8 * np.cos(hand_angle)

                frame_data.append(go.Scatter(
                    x=[x_clock, hand_x],
                    y=[y_clock, hand_y],
                    mode="lines",
                    line=dict(color=color, width=3),
                    showlegend=False,
                ))

                # Time dilation label
                frame_data.append(go.Scatter(
                    x=[x_clock], y=[y_clock - 0.4],
                    mode="text",
                    text=[f"γ={gamma:.2f}"],
                    textfont=dict(size=10, color=color),
                    showlegend=False,
                ))

            # Reference clock at infinity (top)
            ref_x, ref_y = 0, 3
            clock_r = 0.3
            frame_data.append(go.Scatter(
                x=ref_x + clock_r * np.cos(clock_theta),
                y=ref_y + clock_r * np.sin(clock_theta),
                mode="lines",
                line=dict(color="white", width=2),
                name="Reference clock (r=∞)",
            ))

            # Reference hand (runs at full speed)
            hand_x = ref_x + clock_r * 0.8 * np.sin(t)
            hand_y = ref_y + clock_r * 0.8 * np.cos(t)
            frame_data.append(go.Scatter(
                x=[ref_x, hand_x],
                y=[ref_y, hand_y],
                mode="lines",
                line=dict(color="white", width=3),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[ref_x], y=[ref_y + 0.5],
                mode="text",
                text=["t (coordinate time)"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))

            # Formula
            frame_data.append(go.Scatter(
                x=[4], y=[2.5],
                mode="text",
                text=["dτ/dt = √(1 - r_s/r)"],
                textfont=dict(size=12, color="white"),
                showlegend=False,
            ))

            # Explanation
            frame_data.append(go.Scatter(
                x=[4], y=[-2],
                mode="text",
                text=["Closer to horizon = slower time"],
                textfont=dict(size=11, color="yellow"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Gravitational Time Dilation</b><br><sub>Clocks run slower near the event horizon</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-1, 6.5], showgrid=False, zeroline=False),
                yaxis=dict(range=[-3, 4], showgrid=False, zeroline=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.65, y=0.95),
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

    time_dilation_fig = create_time_dilation_animation()
    time_dilation_fig
    return (create_time_dilation_animation, time_dilation_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The "Frozen Star" Effect

        Watch the clocks in the animation:
        - **White clock** (at infinity): Runs normally
        - **Cyan clock** (far away): Almost normal
        - **Red clock** (near horizon): Almost stopped!

        **From a distant observer's perspective:**

        An astronaut falling into a black hole would appear to slow down as they approach
        the horizon. Their clock would tick slower and slower. Light from them would be
        increasingly redshifted. They would appear to asymptotically approach the horizon
        but never quite reach it—frozen in time at the edge forever.

        **From the astronaut's perspective:**

        They notice nothing unusual at the horizon! Their clock keeps ticking normally.
        They cross the horizon in finite proper time and continue falling toward the
        singularity. The asymmetry comes from the one-way nature of the horizon—signals
        can't get back out.

        **This is real physics:** GPS satellites must correct for gravitational time dilation
        (and special relativistic effects) or navigation errors would accumulate at ~10 km/day!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 4. Gravitational Redshift

        ### Light Losing Energy to Gravity

        When light climbs out of a gravitational well, it loses energy. Since a photon's
        energy is $E = hf$, losing energy means lower frequency—the light is **redshifted**.

        The gravitational redshift formula near a black hole:

        $$\frac{f_{observed}}{f_{emitted}} = \sqrt{1 - \frac{r_s}{r}}$$

        **At the horizon**, the redshift becomes infinite—light is redshifted to zero
        frequency (infinite wavelength). This is another way of seeing why nothing can
        escape: any light emitted at the horizon has zero energy by the time it reaches
        a distant observer.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Gravitational redshift
    def create_redshift_animation():
        n_frames = 100
        frames = []

        r_s = 1.0

        for frame in range(n_frames):
            progress = frame / n_frames
            frame_data = []

            # Black hole
            theta = np.linspace(0, 2 * np.pi, 100)
            frame_data.append(go.Scatter(
                x=r_s * np.cos(theta),
                y=r_s * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor="black",
                line=dict(color="red", width=2),
                name="Black hole",
            ))

            # Emitter at different radii (moves closer over time)
            r_emit = 4.0 - progress * 2.8  # From r=4 to r=1.2

            # Redshift factor
            z_factor = 1 / np.sqrt(1 - r_s / r_emit) - 1  # Redshift z

            # Wavelength stretching
            lambda_emit = 500  # nm (green light)
            lambda_obs = lambda_emit * (1 + z_factor)

            # Convert wavelength to color
            # Simplified: 400nm=violet, 500nm=green, 600nm=orange, 700nm=red, >700nm=infrared
            if lambda_obs < 450:
                color = "violet"
            elif lambda_obs < 495:
                color = "blue"
            elif lambda_obs < 570:
                color = "green"
            elif lambda_obs < 590:
                color = "yellow"
            elif lambda_obs < 650:
                color = "orange"
            elif lambda_obs < 750:
                color = "red"
            else:
                color = "darkred"

            # Emitter position
            emit_x = r_emit
            emit_y = 0

            frame_data.append(go.Scatter(
                x=[emit_x], y=[emit_y],
                mode="markers",
                marker=dict(size=15, color="green", symbol="star"),
                name="Light source (green)",
            ))

            # Light wave traveling outward
            wave_positions = np.linspace(r_emit, 6, 50)
            wave_y = 0.2 * np.sin(2 * np.pi * (wave_positions - r_emit) / (0.3 * (1 + z_factor)) - progress * 10)

            frame_data.append(go.Scatter(
                x=wave_positions, y=wave_y,
                mode="lines",
                line=dict(color=color, width=3),
                name="Light wave (observed)",
            ))

            # Observer
            frame_data.append(go.Scatter(
                x=[6], y=[0],
                mode="markers",
                marker=dict(size=20, color="white", symbol="circle"),
                name="Observer",
            ))

            # Info display
            frame_data.append(go.Scatter(
                x=[3.5], y=[2.5],
                mode="text",
                text=[f"r/r_s = {r_emit/r_s:.2f}"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[3.5], y=[2.0],
                mode="text",
                text=[f"Redshift z = {z_factor:.2f}"],
                textfont=dict(size=12, color="orange"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[3.5], y=[1.5],
                mode="text",
                text=[f"λ_obs = {lambda_obs:.0f} nm"],
                textfont=dict(size=12, color=color),
                showlegend=False,
            ))

            # Color bar showing redshift
            colors_bar = ["green", "yellow", "orange", "red", "darkred"]
            for i, c in enumerate(colors_bar):
                frame_data.append(go.Scatter(
                    x=[5 + i * 0.3], y=[-2],
                    mode="markers",
                    marker=dict(size=20, color=c, symbol="square"),
                    showlegend=False,
                ))

            frame_data.append(go.Scatter(
                x=[5], y=[-2.6],
                mode="text",
                text=["Emitted"],
                textfont=dict(size=10, color="green"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[6.2], y=[-2.6],
                mode="text",
                text=["→ Observed"],
                textfont=dict(size=10, color="darkred"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Gravitational Redshift</b><br><sub>Light loses energy escaping gravity; redshifts to infinity at horizon</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-0.5, 7.5], showgrid=False, zeroline=False),
                yaxis=dict(range=[-3.5, 3], showgrid=False, zeroline=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.01, y=0.99),
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

    redshift_fig = create_redshift_animation()
    redshift_fig
    return (create_redshift_animation, redshift_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Redshift in Action

        Watch what happens to green light as its source approaches the black hole:

        - **Far from the horizon**: Light is slightly redshifted (still green-yellow)
        - **Closer**: Light becomes orange, then red
        - **Near the horizon**: Light is deeply redshifted into infrared

        **At the horizon itself**, the redshift would be infinite—the light would have
        zero frequency and zero energy. This is consistent with our other pictures:
        - Time dilation: infinite time to receive the signal
        - Light cones: outward light just hovers at the horizon
        - Escape velocity: equals c, so light can't escape

        **Observational evidence:** Astronomers observe gravitational redshift from:
        - White dwarf stars (mild redshift)
        - Neutron stars (stronger redshift)
        - Gas falling into black holes (extreme redshift and Doppler effects)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 5. Spacetime Curvature

        ### The Rubber Sheet Analogy (and Its Limits)

        You've probably seen the "bowling ball on a rubber sheet" analogy for gravity.
        A heavy ball creates a depression, and smaller balls roll toward it.

        This analogy captures one truth: **mass curves spacetime**, and objects follow
        the curves. But it's misleading in important ways:

        - It only shows space curvature, not time curvature
        - It requires "gravity" to make balls roll down
        - It's 2D, hiding the full 4D picture

        **The better picture:** Spacetime curvature means that straight lines (geodesics)
        aren't what you'd expect. Near a mass, "straight ahead in time" curves toward the mass.
        Objects fall not because of a force, but because falling is the straightest
        possible path through curved spacetime!

        > *"Matter tells spacetime how to curve, and spacetime tells matter how to move."*
        > — John Wheeler
        """
    )
    return


@app.cell
def _(go, np):
    # Visualization: Embedding diagram of curved space
    def create_embedding_diagram():
        # Create a 3D embedding of 2D curved space (Flamm's paraboloid)
        r_s = 1.0

        # Radial coordinate
        r = np.linspace(r_s * 1.01, 6, 100)
        theta = np.linspace(0, 2 * np.pi, 60)

        R, Theta = np.meshgrid(r, theta)

        # Flamm's paraboloid: z = 2*sqrt(r_s*(r - r_s))
        Z = 2 * np.sqrt(r_s * (R - r_s))

        # Convert to Cartesian
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)

        # Create the surface
        fig = go.Figure()

        # Curved space surface
        fig.add_trace(go.Surface(
            x=X, y=Y, z=-Z,  # Negative Z to show "well"
            colorscale=[[0, 'darkblue'], [0.5, 'blue'], [1, 'cyan']],
            showscale=False,
            opacity=0.8,
            name="Curved spacetime",
        ))

        # Event horizon circle
        theta_eh = np.linspace(0, 2 * np.pi, 100)
        x_eh = r_s * np.cos(theta_eh)
        y_eh = r_s * np.sin(theta_eh)
        z_eh = np.zeros_like(theta_eh)

        fig.add_trace(go.Scatter3d(
            x=x_eh, y=y_eh, z=z_eh,
            mode="lines",
            line=dict(color="red", width=8),
            name="Event horizon",
        ))

        # Add some geodesics (paths of falling objects)
        for phi_start in [0, np.pi/2, np.pi, 3*np.pi/2]:
            r_path = np.linspace(5, r_s * 1.05, 50)
            x_path = r_path * np.cos(phi_start)
            y_path = r_path * np.sin(phi_start)
            z_path = -2 * np.sqrt(r_s * (r_path - r_s))

            fig.add_trace(go.Scatter3d(
                x=x_path, y=y_path, z=z_path,
                mode="lines",
                line=dict(color="yellow", width=4),
                showlegend=bool(phi_start == 0),
                name="Falling geodesic" if phi_start == 0 else None,
            ))

        # Add radial grid lines
        for phi in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            r_line = np.linspace(r_s * 1.01, 6, 30)
            x_line = r_line * np.cos(phi)
            y_line = r_line * np.sin(phi)
            z_line = -2 * np.sqrt(r_s * (r_line - r_s))

            fig.add_trace(go.Scatter3d(
                x=x_line, y=y_line, z=z_line,
                mode="lines",
                line=dict(color="rgba(255,255,255,0.3)", width=1),
                showlegend=False,
            ))

        fig.update_layout(
            title=dict(
                text="<b>Flamm's Paraboloid: Embedding of Schwarzschild Geometry</b><br><sub>Space curves into a 'well' around the black hole (time dimension not shown)</sub>",
                font=dict(size=14),
            ),
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=""),
                yaxis=dict(showbackground=False, showticklabels=False, title=""),
                zaxis=dict(showbackground=False, showticklabels=False, title="Embedding depth"),
                camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=0.5),
            ),
            showlegend=True,
            legend=dict(x=0.7, y=0.9),
            paper_bgcolor="rgba(0,0,20,1)",
            plot_bgcolor="rgba(0,0,20,1)",
        )

        return fig

    embedding_fig = create_embedding_diagram()
    embedding_fig
    return (create_embedding_diagram, embedding_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Embedding Diagram

        This is **Flamm's paraboloid**, a way of visualizing the spatial geometry
        outside a black hole.

        **What it shows:**
        - The "depth" represents how much space is curved
        - The red circle is the event horizon
        - Yellow lines show paths of falling objects (geodesics)
        - The funnel gets infinitely deep at the horizon

        **What it doesn't show:**
        - Time curvature (which is equally important!)
        - The interior of the black hole
        - The singularity at r = 0

        **Why objects fall:** In this picture, a "straight line" (geodesic) on this
        curved surface curves toward the center. Objects don't fall because of a force—they
        follow the straightest possible path, and that path leads inward.

        The equation for this surface is:
        $$z = 2\sqrt{r_s(r - r_s)}$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 6. Inside the Black Hole

        ### Where Space Becomes Time

        The most mind-bending aspect of black holes is what happens **inside** the horizon.
        The Schwarzschild metric changes character: the $r$ coordinate becomes timelike
        and the $t$ coordinate becomes spacelike!

        **What this means physically:**
        - Outside: you can choose to move left or right (in space), but must move forward in time
        - Inside: you can choose earlier or later (in the $t$ coordinate), but must move toward r = 0

        **The singularity isn't a place—it's a time.** Once inside, reaching r = 0 is
        as inevitable as reaching tomorrow. You can't avoid it any more than you can
        stop time.

        **How long until the singularity?**

        For an observer falling from rest at the horizon, the proper time to reach
        the singularity is:

        $$\tau = \frac{\pi G M}{c^3} = \frac{\pi r_s}{2c}$$

        For a stellar black hole (3 solar masses): about 50 microseconds!

        For a supermassive black hole (4 million solar masses): about 60 seconds.
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Interior of black hole (Kruskal-like diagram)
    def create_interior_animation():
        n_frames = 100
        frames = []

        for frame in range(n_frames):
            progress = frame / n_frames
            frame_data = []

            # Draw regions
            # Region I: Outside (right)
            frame_data.append(go.Scatter(
                x=[0, 4, 4, 0],
                y=[0, 4, -4, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 100, 200, 0.2)",
                line=dict(color="rgba(0,100,200,0.5)", width=1),
                name="Region I (our universe)",
            ))

            # Region II: Inside (future)
            frame_data.append(go.Scatter(
                x=[0, 4, -4, 0],
                y=[0, 4, 4, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(100, 0, 0, 0.3)",
                line=dict(color="rgba(100,0,0,0.5)", width=1),
                name="Region II (inside BH)",
            ))

            # Singularity (future)
            sing_x = np.linspace(-3, 3, 100)
            sing_y = np.sqrt(sing_x**2 + 1) * 2  # Hyperbola
            frame_data.append(go.Scatter(
                x=sing_x, y=sing_y,
                mode="lines",
                line=dict(color="white", width=4),
                name="Singularity (r=0)",
            ))

            # Horizons (45° lines)
            frame_data.append(go.Scatter(
                x=[-4, 4], y=[-4, 4],
                mode="lines",
                line=dict(color="red", width=2),
                name="Event horizon",
            ))
            frame_data.append(go.Scatter(
                x=[-4, 4], y=[4, -4],
                mode="lines",
                line=dict(color="red", width=2, dash="dash"),
                showlegend=False,
            ))

            # Infalling observer worldline
            # Start outside, cross horizon, hit singularity
            t_param = np.linspace(0, progress * 3, 50)
            # Simplified trajectory
            x_obs = 3 - t_param * 0.5
            y_obs = t_param * 1.2

            # Clip to singularity
            valid = y_obs < np.sqrt(x_obs**2 + 1) * 2
            x_obs = x_obs[valid]
            y_obs = y_obs[valid]

            if len(x_obs) > 0:
                frame_data.append(go.Scatter(
                    x=x_obs, y=y_obs,
                    mode="lines",
                    line=dict(color="cyan", width=3),
                    name="Falling observer",
                ))

                # Current position
                frame_data.append(go.Scatter(
                    x=[x_obs[-1]], y=[y_obs[-1]],
                    mode="markers",
                    marker=dict(size=12, color="cyan", symbol="star"),
                    showlegend=False,
                ))

                # Light cone at current position
                cone_size = 0.5
                cx, cy = x_obs[-1], y_obs[-1]

                # Inside horizon, light cone tilts toward singularity
                if cx < cy:  # Inside
                    frame_data.append(go.Scatter(
                        x=[cx - cone_size, cx, cx + cone_size],
                        y=[cy + cone_size, cy, cy + cone_size],
                        mode="lines",
                        fill="toself",
                        fillcolor="rgba(255, 100, 100, 0.4)",
                        line=dict(color="red", width=2),
                        name="Light cone (tilted!)",
                    ))
                else:  # Outside
                    frame_data.append(go.Scatter(
                        x=[cx - cone_size, cx, cx + cone_size],
                        y=[cy + cone_size, cy, cy + cone_size],
                        mode="lines",
                        fill="toself",
                        fillcolor="rgba(255, 255, 100, 0.4)",
                        line=dict(color="yellow", width=2),
                        name="Light cone",
                    ))

            # Labels
            frame_data.append(go.Scatter(
                x=[2.5], y=[-2],
                mode="text",
                text=["OUTSIDE"],
                textfont=dict(size=14, color="cyan"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[0], y=[3],
                mode="text",
                text=["INSIDE"],
                textfont=dict(size=14, color="red"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[0], y=[5],
                mode="text",
                text=["Singularity: inevitable future"],
                textfont=dict(size=11, color="white"),
                showlegend=False,
            ))

            # Status
            if len(x_obs) > 0 and x_obs[-1] < y_obs[-1]:
                status = "INSIDE: falling toward singularity"
                status_color = "red"
            else:
                status = "Outside: can still escape"
                status_color = "cyan"

            frame_data.append(go.Scatter(
                x=[0], y=[-3.5],
                mode="text",
                text=[status],
                textfont=dict(size=12, color=status_color),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Kruskal Diagram: Inside the Black Hole</b><br><sub>Once inside, the singularity is your inevitable future</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-4.5, 4.5], title="Space", showgrid=True,
                          gridcolor="rgba(100,100,100,0.2)"),
                yaxis=dict(range=[-4, 6], title="Time", showgrid=True,
                          gridcolor="rgba(100,100,100,0.2)", scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.65, y=0.3),
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

    interior_fig = create_interior_animation()
    interior_fig
    return (create_interior_animation, interior_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Kruskal Diagram Explained

        This diagram shows the **causal structure** of a black hole spacetime:

        **The regions:**
        - **Blue (Region I)**: Our universe, outside the black hole
        - **Red (Region II)**: Inside the black hole (future of the horizon)
        - **White curve**: The singularity at r = 0

        **The key insight:** The singularity is a horizontal line at the top—it's a
        **moment in time**, not a place in space. Once you cross the horizon (the 45°
        red line), the singularity is in your future just like tomorrow is in yours.

        **Watch the light cone:** Outside, it points upward (toward the future).
        Inside, it tilts so that the entire cone points toward the singularity.
        There's no direction you can go—no matter how you fire your rockets—that
        doesn't lead to the singularity.

        **The inevitability:** Trying to avoid the singularity once inside is like
        trying to avoid next Tuesday. The harder you try (more acceleration), the
        faster you get there (time dilation works against you).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 7. Types of Black Holes

        ### From Stellar Corpses to Cosmic Monsters

        Black holes come in different sizes and can have different properties:

        **By mass:**

        | Type | Mass | Formation | Example |
        |------|------|-----------|---------|
        | **Stellar** | 3-100 M☉ | Core collapse of massive stars | Cygnus X-1 |
        | **Intermediate** | 100-10⁵ M☉ | Mergers? Still mysterious | HLX-1 |
        | **Supermassive** | 10⁵-10¹⁰ M☉ | Unknown; grow with galaxies | Sgr A*, M87* |
        | **Primordial** | Any (theoretical) | Early universe density fluctuations | None confirmed |

        **By properties:**

        - **Schwarzschild**: Non-rotating, no charge (simplest)
        - **Kerr**: Rotating (most realistic for astrophysical black holes)
        - **Reissner-Nordström**: Charged, non-rotating
        - **Kerr-Newman**: Rotating and charged

        Real astrophysical black holes are expected to be nearly pure Kerr solutions—they
        rotate (from the angular momentum of infalling matter) and any charge quickly
        neutralizes.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualization: Rotating black hole (Kerr) with ergosphere
    def create_kerr_black_hole():
        # Parameters
        M = 1  # Mass
        a = 0.9  # Spin parameter (0 to 1)

        # Event horizon radius (outer)
        r_plus = M + np.sqrt(M**2 - a**2)
        # Ergosphere radius at equator
        r_ergo_eq = 2 * M

        fig = go.Figure()

        # Ergosphere (oblate spheroid)
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 30)
        U, V = np.meshgrid(u, v)

        # Ergosphere boundary: r = M + sqrt(M^2 - a^2 cos^2(theta))
        r_ergo = M + np.sqrt(M**2 - a**2 * np.cos(V)**2)

        X_ergo = r_ergo * np.sin(V) * np.cos(U)
        Y_ergo = r_ergo * np.sin(V) * np.sin(U)
        Z_ergo = r_ergo * np.cos(V)

        fig.add_trace(go.Surface(
            x=X_ergo, y=Y_ergo, z=Z_ergo,
            colorscale=[[0, 'rgba(255,100,100,0.3)'], [1, 'rgba(255,100,100,0.3)']],
            showscale=False,
            opacity=0.3,
            name="Ergosphere",
        ))

        # Event horizon (smaller sphere/oblate)
        X_eh = r_plus * np.sin(V) * np.cos(U)
        Y_eh = r_plus * np.sin(V) * np.sin(U)
        Z_eh = r_plus * np.cos(V)

        fig.add_trace(go.Surface(
            x=X_eh, y=Y_eh, z=Z_eh,
            colorscale=[[0, 'black'], [1, 'darkgray']],
            showscale=False,
            opacity=1.0,
            name="Event horizon",
        ))

        # Ring singularity (at equator, radius a)
        theta_ring = np.linspace(0, 2 * np.pi, 100)
        fig.add_trace(go.Scatter3d(
            x=a * np.cos(theta_ring),
            y=a * np.sin(theta_ring),
            z=np.zeros(100),
            mode="lines",
            line=dict(color="white", width=6),
            name="Ring singularity",
        ))

        # Rotation direction arrows
        for z_pos in [0.5, -0.5]:
            for theta_arr in np.linspace(0, 2 * np.pi, 4, endpoint=False):
                r_arr = r_plus + 0.3
                x_arr = r_arr * np.cos(theta_arr)
                y_arr = r_arr * np.sin(theta_arr)
                # Tangent direction (counterclockwise)
                dx = -0.3 * np.sin(theta_arr)
                dy = 0.3 * np.cos(theta_arr)

                fig.add_trace(go.Cone(
                    x=[x_arr], y=[y_arr], z=[z_pos],
                    u=[dx], v=[dy], w=[0],
                    colorscale=[[0, 'cyan'], [1, 'cyan']],
                    showscale=False,
                    sizemode="absolute",
                    sizeref=0.15,
                    name="Rotation" if theta_arr == 0 and z_pos == 0.5 else None,
                    showlegend=bool(theta_arr == 0 and z_pos == 0.5),
                ))

        # Spin axis
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[-2.5, 2.5],
            mode="lines",
            line=dict(color="yellow", width=3, dash="dash"),
            name="Spin axis",
        ))

        fig.update_layout(
            title=dict(
                text="<b>Kerr Black Hole (Rotating)</b><br><sub>Spin creates ergosphere where space itself is dragged around</sub>",
                font=dict(size=14),
            ),
            scene=dict(
                xaxis=dict(range=[-3, 3], showbackground=False, title=""),
                yaxis=dict(range=[-3, 3], showbackground=False, title=""),
                zaxis=dict(range=[-3, 3], showbackground=False, title=""),
                aspectmode="cube",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1)),
            ),
            showlegend=True,
            legend=dict(x=0.7, y=0.9),
            paper_bgcolor="rgba(0,0,20,1)",
        )

        return fig

    kerr_fig = create_kerr_black_hole()
    kerr_fig
    return (create_kerr_black_hole, kerr_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Kerr Black Hole

        Rotating black holes have fascinating additional features:

        **The ergosphere** (red region):
        - A region outside the event horizon where space is dragged around
        - You cannot stay stationary here—you're forced to rotate with the black hole
        - Named from Greek "ergo" (work) because energy can be extracted from it

        **Frame dragging:**
        - Space itself rotates around the black hole
        - This effect exists around any rotating mass (Earth too, very weakly)
        - Confirmed by Gravity Probe B in 2011

        **The ring singularity:**
        - Unlike Schwarzschild's point singularity, Kerr has a ring
        - The ring has radius $a = J/(Mc)$ where $J$ is angular momentum
        - Theoretical possibility of passing through the ring to other regions

        **The Penrose process:**
        - You can extract energy from a rotating black hole
        - Send in a particle that splits; one piece falls in with negative energy
        - The other escapes with more energy than the original!
        - Could theoretically extract up to 29% of the black hole's mass as energy
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 8. Hawking Radiation

        ### Black Holes Aren't Completely Black

        In 1974, Stephen Hawking made a stunning discovery: **black holes emit radiation
        and slowly evaporate!**

        **The mechanism (simplified):**

        Quantum mechanics allows particle-antiparticle pairs to briefly pop into existence
        everywhere in space (vacuum fluctuations). Near the horizon:

        1. A pair forms just outside the horizon
        2. One particle falls in (negative energy)
        3. The other escapes (positive energy—the Hawking radiation)
        4. The black hole loses mass

        **The temperature:**
        $$T_H = \frac{\hbar c^3}{8\pi G M k_B} = \frac{1.227 \times 10^{23} \text{ K} \cdot \text{kg}}{M}$$

        **Key insight:** Smaller black holes are hotter! A stellar black hole is colder than
        the cosmic microwave background, so it absorbs more than it emits. But a tiny primordial
        black hole would glow brightly and eventually explode.

        | Black Hole Mass | Temperature | Lifetime |
        |-----------------|-------------|----------|
        | Solar mass | 60 nanokelvin | 10⁶⁷ years |
        | Moon mass | 2.7 K | 10⁵⁰ years |
        | Mountain (10¹² kg) | 120 billion K | 1 second |
        """
    )
    return


@app.cell
def _(go, np):
    # Animation: Hawking radiation concept
    def create_hawking_animation():
        n_frames = 120
        frames = []

        r_s = 1.0

        for frame in range(n_frames):
            t = frame / n_frames * 4 * np.pi
            frame_data = []

            # Black hole (shrinking very slowly to show evaporation concept)
            shrink_factor = 1 - 0.1 * (frame / n_frames)
            r_current = r_s * shrink_factor

            theta = np.linspace(0, 2 * np.pi, 100)
            frame_data.append(go.Scatter(
                x=r_current * np.cos(theta),
                y=r_current * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor="black",
                line=dict(color="red", width=2),
                name="Black hole",
            ))

            # Virtual particle pairs appearing and one escaping
            n_pairs = 5
            for i in range(n_pairs):
                phase = t + i * 2 * np.pi / n_pairs
                # Pair appears at random position near horizon
                angle = phase * 1.3
                r_pair = r_current * 1.1

                x_center = r_pair * np.cos(angle)
                y_center = r_pair * np.sin(angle)

                # Animation cycle for each pair
                cycle = (phase % (2 * np.pi)) / (2 * np.pi)

                if cycle < 0.3:
                    # Pair appears
                    separation = cycle / 0.3 * 0.15
                    # Particle (escaping)
                    frame_data.append(go.Scatter(
                        x=[x_center + separation * np.cos(angle)],
                        y=[y_center + separation * np.sin(angle)],
                        mode="markers",
                        marker=dict(size=8, color="cyan"),
                        showlegend=(i == 0 and cycle > 0.1),
                        name="Escaping particle" if i == 0 else None,
                    ))
                    # Antiparticle (falling in)
                    frame_data.append(go.Scatter(
                        x=[x_center - separation * np.cos(angle)],
                        y=[y_center - separation * np.sin(angle)],
                        mode="markers",
                        marker=dict(size=8, color="red"),
                        showlegend=(i == 0 and cycle > 0.1),
                        name="Falling antiparticle" if i == 0 else None,
                    ))
                elif cycle < 0.8:
                    # Separation phase
                    progress = (cycle - 0.3) / 0.5
                    # Escaping particle moves out
                    r_escape = r_pair + progress * 1.5
                    frame_data.append(go.Scatter(
                        x=[r_escape * np.cos(angle)],
                        y=[r_escape * np.sin(angle)],
                        mode="markers",
                        marker=dict(size=8, color="cyan"),
                        showlegend=False,
                    ))
                    # Falling particle moves in
                    r_fall = r_pair - progress * (r_pair - r_current * 0.5)
                    if r_fall > r_current * 0.3:
                        frame_data.append(go.Scatter(
                            x=[r_fall * np.cos(angle)],
                            y=[r_fall * np.sin(angle)],
                            mode="markers",
                            marker=dict(size=8, color="red"),
                            showlegend=False,
                        ))

            # Thermal glow around horizon
            glow_r = np.linspace(r_current, r_current + 0.3, 10)
            for gr in glow_r:
                alpha_raw = 0.3 * (1 - (gr - r_current) / 0.3) * (0.5 + 0.5 * np.sin(t * 3))
                alpha = max(0.0, min(1.0, alpha_raw))
                frame_data.append(go.Scatter(
                    x=gr * np.cos(theta),
                    y=gr * np.sin(theta),
                    mode="lines",
                    line=dict(color=f"rgba(255, 200, 100, {alpha:.2f})", width=2),
                    showlegend=False,
                ))

            # Temperature indicator (increases as BH shrinks)
            T_relative = 1 / shrink_factor
            frame_data.append(go.Scatter(
                x=[3], y=[1.5],
                mode="text",
                text=[f"T ∝ 1/M (hotter as it shrinks!)"],
                textfont=dict(size=11, color="orange"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[3], y=[1.0],
                mode="text",
                text=[f"Relative T: {T_relative:.2f}"],
                textfont=dict(size=12, color="yellow"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[3], y=[-1.5],
                mode="text",
                text=["Virtual pairs form at horizon"],
                textfont=dict(size=10, color="white"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[3], y=[-2],
                mode="text",
                text=["One escapes, one falls in"],
                textfont=dict(size=10, color="white"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Hawking Radiation</b><br><sub>Virtual particle pairs at horizon → black hole slowly evaporates</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-2.5, 4.5], showgrid=False, zeroline=False),
                yaxis=dict(range=[-2.5, 2.5], showgrid=False, zeroline=False, scaleanchor="x"),
                showlegend=True,
                legend=dict(x=0.65, y=0.95),
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

    hawking_fig = create_hawking_animation()
    hawking_fig
    return (create_hawking_animation, hawking_fig)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Information Paradox

        Hawking radiation creates one of the deepest puzzles in physics: the
        **black hole information paradox**.

        **The problem:**

        1. Quantum mechanics says information is never destroyed
        2. If you throw a book into a black hole, the information seems trapped
        3. But Hawking radiation is thermal (random)—it carries no information
        4. When the black hole evaporates completely, where did the information go?

        **Proposed solutions:**

        - **Information is lost**: Violates quantum mechanics (Hawking's original view)
        - **Information escapes gradually**: Encoded subtly in radiation correlations
        - **Remnants**: A tiny stable remnant stores all the information
        - **Firewalls**: Drama at the horizon (controversial)
        - **Holography**: Information is encoded on the horizon surface

        This paradox connects quantum mechanics, gravity, and thermodynamics in ways
        we don't fully understand. Solving it may require a complete theory of quantum gravity.

        > *"Not only does God play dice, but he sometimes throws them where they cannot be seen."*
        > — Stephen Hawking
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: Black Holes and Causality

        | Concept | Key Equation | Physical Meaning |
        |---------|--------------|------------------|
        | **Schwarzschild radius** | $r_s = 2GM/c^2$ | Boundary where escape velocity = c |
        | **Event horizon** | Surface at $r = r_s$ | One-way membrane; causally disconnects inside from outside |
        | **Time dilation** | $d\tau/dt = \sqrt{1-r_s/r}$ | Time stops at horizon (from outside view) |
        | **Gravitational redshift** | $f_{obs}/f_{emit} = \sqrt{1-r_s/r}$ | Light loses all energy escaping from horizon |
        | **Light cones** | Tilt toward singularity | Inside: all futures lead to r=0 |
        | **Hawking temperature** | $T = \hbar c^3/(8\pi GMk_B)$ | Black holes radiate; smaller = hotter |

        **The deep lessons:**

        1. **Gravity is geometry.** Black holes aren't objects that "pull" things in—they're
           regions where spacetime is so curved that all paths lead inward.

        2. **The horizon is about causality, not force.** Nothing special happens locally
           at the horizon—it's only globally that we see it's a point of no return.

        3. **Space and time are unified.** Inside a black hole, the distinction between
           "trying to escape" and "trying to stop time" vanishes.

        4. **Classical and quantum meet.** Hawking radiation shows that a complete
           understanding requires quantum gravity—still an open frontier.

        ---

        > *"The black holes of nature are the most perfect macroscopic objects there are
        > in the universe: the only elements in their construction are our concepts of
        > space and time."*
        > — Subrahmanyan Chandrasekhar
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## References

        ### Feynman Lectures Background

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1964). *The Feynman Lectures on Physics, Volume II*.
          Addison-Wesley.
          - [Chapter 42: Curved Space](https://www.feynmanlectures.caltech.edu/II_42.html) — Introduction to curved geometry and gravity
          - [Chapter 17: Space-Time (Vol. I)](https://www.feynmanlectures.caltech.edu/I_17.html) — Special relativistic spacetime

        - **Feynman, R. P.** (1995). *Feynman Lectures on Gravitation*. Addison-Wesley.
          - Advanced treatment of gravity as a field theory

        ### General Relativity and Black Holes

        - **Schwarzschild, K.** (1916). "Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie".
          First exact solution to Einstein's equations; defines the black hole metric.

        - **Kerr, R. P.** (1963). "Gravitational Field of a Spinning Mass".
          Physical Review Letters, 11, 237.
          Solution for rotating black holes.

        - **Penrose, R.** (1965). "Gravitational Collapse and Space-Time Singularities".
          Physical Review Letters, 14, 57.
          Proved singularities are inevitable (Nobel Prize 2020).

        ### Key Equations

        - **Schwarzschild radius**: $r_s = \frac{2GM}{c^2}$
          - Sun: 3 km, Earth: 9 mm

        - **Gravitational time dilation**: $\frac{d\tau}{dt} = \sqrt{1 - \frac{r_s}{r}}$

        - **Gravitational redshift**: $\frac{\lambda_{obs}}{\lambda_{emit}} = \frac{1}{\sqrt{1 - r_s/r}}$

        - **Hawking temperature**: $T_H = \frac{\hbar c^3}{8\pi G M k_B} \approx \frac{6 \times 10^{-8}}{M/M_\odot}$ K

        - **Schwarzschild metric**:
          $$ds^2 = -\left(1-\frac{r_s}{r}\right)c^2 dt^2 + \frac{dr^2}{1-r_s/r} + r^2 d\Omega^2$$

        ### Hawking Radiation

        - **Hawking, S. W.** (1974). "Black hole explosions?". Nature, 248, 30.
          Original paper predicting black hole evaporation.

        - **Hawking, S. W.** (1975). "Particle Creation by Black Holes".
          Communications in Mathematical Physics, 43, 199.
          Full derivation of black hole thermodynamics.

        ### Information Paradox

        - **Hawking, S. W.** (1976). "Breakdown of Predictability in Gravitational Collapse".
          Physical Review D, 14, 2460.
          States the information paradox.

        - **Susskind, L.** (2008). *The Black Hole War*. Little, Brown.
          Popular account of the paradox and proposed resolutions.

        ### Observational Evidence

        - **Event Horizon Telescope Collaboration** (2019). "First M87 Event Horizon Telescope Results".
          Astrophysical Journal Letters, 875, L1.
          First image of a black hole shadow.

        - **LIGO/Virgo** (2016). "Observation of Gravitational Waves from a Binary Black Hole Merger".
          Physical Review Letters, 116, 061102.
          First direct detection of black hole mergers.

        ### Further Reading

        - Thorne, K. S. *Black Holes and Time Warps* — Excellent popular science book
        - Carroll, S. *Spacetime and Geometry* — Graduate textbook on GR
        - Wald, R. M. *General Relativity* — Advanced textbook
        - Misner, Thorne, Wheeler. *Gravitation* — The comprehensive reference
        """
    )
    return


if __name__ == "__main__":
    app.run()
