import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import polars as pl

    return go, mo, np, pl


@app.cell
def _(mo):
    mo.md(
        r"""
        # The Theory of Gravitation

        *An interactive exploration based on [Feynman Lectures on Physics, Chapter 7](https://www.feynmanlectures.caltech.edu/I_07.html)*

        ---

        ## The Beauty of Gravitation

        Feynman called gravitation *"the greatest of all the discoveries"* in physics.
        Why? Because a single, simple law explains everything from a falling apple to the
        motion of galaxies billions of light-years away.

        The story unfolds across three centuries of human curiosity:

        **Tycho Brahe** (1546-1601) spent his life making the most precise astronomical
        observations anyone had ever achieved—night after night, year after year, recording
        the positions of planets with painstaking accuracy. He didn't know what the data meant,
        but he knew it mattered.

        **Johannes Kepler** (1571-1630) inherited Tycho's data and spent *years* trying to
        make sense of it. After countless failed attempts with circles and epicycles, he
        discovered three elegant laws that described *how* the planets moved—but not *why*.

        **Isaac Newton** (1643-1727) asked the deeper question: What *force* could produce
        Kepler's laws? His answer—the Law of Universal Gravitation—unified the heavens and
        the Earth under one principle.

        > *"If I have seen further, it is by standing on the shoulders of giants."* — Newton

        Let's explore each piece of this magnificent puzzle.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Kepler's First Law: The Law of Ellipses

        > *Each planet moves in an ellipse with the Sun at one focus.*

        Before Kepler, everyone assumed planetary orbits must be circles—the "perfect" shape.
        This wasn't just aesthetic preference; it was philosophical dogma going back to the
        ancient Greeks. Circles were "divine," and the heavens must be perfect.

        Kepler tried for years to fit Mars's orbit to a circle. It never quite worked.
        The error was tiny—just 8 arc-minutes (about 1/4 the width of the Moon as seen from Earth)—but
        Kepler trusted Tycho's data over 2,000 years of philosophical tradition.

        That tiny discrepancy led him to a revolutionary idea: **orbits are ellipses**.

        **What is an ellipse?**

        An ellipse is like a "stretched circle" with two special points called *foci* (singular: focus).
        The defining property: for any point on the ellipse, the sum of distances to the two foci is constant:

        $$r_1 + r_2 = 2a$$

        where $a$ is the semi-major axis (half the longest diameter).

        **Why does this matter?**

        The Sun sits at one focus—not at the center! This means:
        - The planet is sometimes closer to the Sun (**perihelion**)
        - The planet is sometimes farther from the Sun (**aphelion**)
        - This varying distance has real consequences for climate and orbital speed

        The polar equation, with the Sun at the origin, is:

        $$r = \frac{a(1-e^2)}{1 + e\cos\theta}$$

        **In the animation below, verify Kepler's discovery:**
        - The **gold circle** is the Sun (at one focus)
        - The **gray ×** marks the other focus (empty—nothing there!)
        - The **orange dashed line** is $r_1$ (distance to Sun)
        - The **green dashed line** is $r_2$ (distance to other focus)
        - Watch how $r_1 + r_2$ stays constant as the planet orbits—this is the definition of an ellipse!

        *Click Play to see the orbit in motion.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_ellipse_animation(e: float = 0.5, a: float = 1.0, n_frames: int = 120):
        """Create animated ellipse with planet motion."""
        # Generate ellipse
        theta = np.linspace(0, 2 * np.pi, 200)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x_ellipse = r * np.cos(theta)
        y_ellipse = r * np.sin(theta)

        # Focus positions
        c = a * e  # Distance from center to focus
        focus1 = (0, 0)  # Sun at origin (one focus)
        focus2 = (-2 * c, 0)  # Other focus

        # Planet trajectory with correct timing (Kepler's equation)
        M_values = np.linspace(0, 2 * np.pi, n_frames, endpoint=False)
        x_planet = []
        y_planet = []

        for M in M_values:
            # Solve Kepler's equation iteratively
            E = M
            for _ in range(20):
                E = M + e * np.sin(E)
            # True anomaly
            theta_true = 2 * np.arctan2(
                np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)
            )
            r_val = a * (1 - e**2) / (1 + e * np.cos(theta_true))
            x_planet.append(r_val * np.cos(theta_true))
            y_planet.append(r_val * np.sin(theta_true))

        # Create figure
        fig = go.Figure(
            data=[
                # Ellipse orbit
                go.Scatter(
                    x=x_ellipse,
                    y=y_ellipse,
                    mode="lines",
                    line={"color": "lightblue", "width": 2},
                    name="Orbit",
                ),
                # Sun at focus 1
                go.Scatter(
                    x=[focus1[0]],
                    y=[focus1[1]],
                    mode="markers",
                    marker={"size": 22, "color": "gold", "symbol": "circle"},
                    name="Sun (Focus 1)",
                ),
                # Focus 2 marker
                go.Scatter(
                    x=[focus2[0]],
                    y=[focus2[1]],
                    mode="markers",
                    marker={"size": 12, "color": "gray", "symbol": "x"},
                    name="Focus 2 (empty)",
                ),
                # Planet (initial position)
                go.Scatter(
                    x=[x_planet[0]],
                    y=[y_planet[0]],
                    mode="markers",
                    marker={"size": 14, "color": "steelblue"},
                    name="Planet",
                ),
                # Radius vector to sun
                go.Scatter(
                    x=[0, x_planet[0]],
                    y=[0, y_planet[0]],
                    mode="lines",
                    line={"color": "orange", "width": 2, "dash": "dash"},
                    name="r₁ (to Sun)",
                ),
                # Radius vector to focus 2
                go.Scatter(
                    x=[focus2[0], x_planet[0]],
                    y=[focus2[1], y_planet[0]],
                    mode="lines",
                    line={"color": "green", "width": 2, "dash": "dash"},
                    name="r₂ (to Focus 2)",
                ),
            ],
            layout=go.Layout(
                title=dict(
                    text="<b>Kepler's First Law:</b> Elliptical Orbit",
                    font=dict(size=16),
                ),
                xaxis={"scaleanchor": "y", "range": [-2.5, 2], "title": "x (AU)"},
                yaxis={"range": [-1.5, 1.5], "title": "y (AU)"},
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.15,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "▶ Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 50, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                    },
                                ],
                            },
                            {
                                "label": "⏸ Pause",
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
                        ],
                    }
                ],
                margin=dict(b=80),
            ),
            frames=[
                go.Frame(
                    data=[
                        go.Scatter(x=x_ellipse, y=y_ellipse),
                        go.Scatter(x=[focus1[0]], y=[focus1[1]]),
                        go.Scatter(x=[focus2[0]], y=[focus2[1]]),
                        go.Scatter(x=[x_planet[i]], y=[y_planet[i]]),
                        go.Scatter(x=[0, x_planet[i]], y=[0, y_planet[i]]),
                        go.Scatter(
                            x=[focus2[0], x_planet[i]], y=[focus2[1], y_planet[i]]
                        ),
                    ],
                    name=str(i),
                )
                for i in range(n_frames)
            ],
        )

        return fig

    ellipse_fig = create_ellipse_animation(e=0.6)
    ellipse_fig
    return (create_ellipse_animation, ellipse_fig)


@app.cell
def _(mo):
    mo.accordion(
        {
            "Why Ellipses? (Derivation)": mo.md(
                r"""
        Newton proved that an inverse-square force law *necessarily* produces conic section
        orbits (ellipse, parabola, or hyperbola). Here's the essence of the proof:

        **Step 1: Conservation of Angular Momentum**

        For any central force (pointing toward a fixed point), there's no torque:
        $$\vec{\tau} = \vec{r} \times \vec{F} = 0$$

        So angular momentum is conserved:
        $$L = mr^2\dot{\theta} = \text{constant}$$

        **Step 2: The Orbit Equation**

        Using the substitution $u = 1/r$ and converting to $\theta$ as the independent variable,
        the equation of motion becomes:

        $$\frac{d^2u}{d\theta^2} + u = \frac{GMm^2}{L^2}$$

        This is a simple harmonic oscillator equation with a constant offset. The solution is:

        $$u = \frac{1}{r} = \frac{GMm^2}{L^2}\left(1 + e\cos(\theta - \theta_0)\right)$$

        **Step 3: Recognize the Ellipse**

        Rearranging gives the polar equation of a conic section:
        $$r = \frac{L^2/(GMm^2)}{1 + e\cos\theta} = \frac{a(1-e^2)}{1 + e\cos\theta}$$

        The eccentricity $e$ is determined by the total energy:
        $$e = \sqrt{1 + \frac{2EL^2}{G^2M^2m^3}}$$

        - $E < 0$: Bound orbit → $e < 1$ → **Ellipse**
        - $E = 0$: Escape trajectory → $e = 1$ → **Parabola**
        - $E > 0$: Unbound → $e > 1$ → **Hyperbola**
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

        ## Kepler's Second Law: Equal Areas in Equal Times

        > *The radius vector from the Sun to a planet sweeps out equal areas in equal times.*

        This was Feynman's favorite of Kepler's laws because it reveals something *deep* about
        nature that Kepler himself couldn't have known: the **conservation of angular momentum**.

        **What does this law actually say?**

        Imagine drawing a line from the Sun to a planet. As the planet moves, this line sweeps
        out a pie-slice shaped area. Kepler discovered that the planet sweeps out *equal areas*
        in *equal time intervals*—no matter where it is in its orbit.

        **The surprising consequence:**

        Watch the planet in the animation below. Notice something strange?

        - Near **perihelion** (closest to Sun): the planet races along at high speed
        - Near **aphelion** (farthest from Sun): the planet crawls slowly

        This isn't random—it's mathematically required! Since the planet is closer at perihelion,
        it must move faster to sweep out the same area as when it's far away and moving slowly.

        **The physics behind it:**

        Angular momentum $L = mvr$ must stay constant (there's no torque from a central force).
        When $r$ is small, $v$ must be large. When $r$ is large, $v$ must be small:

        $$\frac{dA}{dt} = \frac{1}{2}r^2\frac{d\theta}{dt} = \frac{L}{2m} = \text{constant}$$

        **Real-world example:** Earth moves fastest in January (perihelion) and slowest in July
        (aphelion). Northern hemisphere winter is actually shorter than summer by about 5 days
        because of this effect!

        *Click Play to watch the areas being swept out. Each colored wedge represents the same
        time interval. Notice how the wedges near perihelion (right side, near Sun) are short
        and fat, while those near aphelion (left side, far from Sun) are long and thin—but
        they have equal areas!*
        """
    )
    return


@app.cell
def _(go, np):
    def create_equal_areas_animation(e: float = 0.6, n_wedges: int = 8):
        """Create animation showing equal areas swept in equal times."""
        a = 1.0
        n_frames = n_wedges * 15  # 15 frames per wedge

        # Generate ellipse
        theta_orbit = np.linspace(0, 2 * np.pi, 200)
        r_orbit = a * (1 - e**2) / (1 + e * np.cos(theta_orbit))
        x_ellipse = r_orbit * np.cos(theta_orbit)
        y_ellipse = r_orbit * np.sin(theta_orbit)

        # Calculate planet positions for each frame using Kepler's equation
        M_values = np.linspace(0, 2 * np.pi, n_frames, endpoint=False)
        positions = []
        theta_values = []

        for M in M_values:
            E = M
            for _ in range(20):
                E = M + e * np.sin(E)
            theta_true = 2 * np.arctan2(
                np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)
            )
            r_val = a * (1 - e**2) / (1 + e * np.cos(theta_true))
            positions.append((r_val * np.cos(theta_true), r_val * np.sin(theta_true)))
            theta_values.append(theta_true)

        # Wedge colors - distinct colors
        colors = [
            "rgba(231, 76, 60, 0.5)",    # red
            "rgba(52, 152, 219, 0.5)",   # blue
            "rgba(241, 196, 15, 0.5)",   # yellow
            "rgba(46, 204, 113, 0.5)",   # green
            "rgba(155, 89, 182, 0.5)",   # purple
            "rgba(230, 126, 34, 0.5)",   # orange
            "rgba(26, 188, 156, 0.5)",   # teal
            "rgba(236, 112, 99, 0.5)",   # coral
        ]

        def create_wedge(theta_start, theta_end, color):
            """Create a filled wedge polygon."""
            if theta_end < theta_start:
                theta_end += 2 * np.pi

            n_arc = 40
            arc_theta = np.linspace(theta_start, theta_end, n_arc)
            arc_r = a * (1 - e**2) / (1 + e * np.cos(arc_theta))
            arc_x = arc_r * np.cos(arc_theta)
            arc_y = arc_r * np.sin(arc_theta)

            wedge_x = np.concatenate([[0], arc_x, [0]])
            wedge_y = np.concatenate([[0], arc_y, [0]])

            return go.Scatter(
                x=wedge_x,
                y=wedge_y,
                fill="toself",
                fillcolor=color,
                line={"color": "rgba(0,0,0,0.4)", "width": 1},
                showlegend=False,
                hoverinfo="skip",
            )

        # Create frames
        frames = []
        frames_per_wedge = n_frames // n_wedges

        for frame_idx in range(n_frames):
            wedge_idx = frame_idx // frames_per_wedge
            frame_in_wedge = frame_idx % frames_per_wedge

            frame_data = []

            # Add completed wedges
            for w in range(wedge_idx):
                start_frame = w * frames_per_wedge
                end_frame = (w + 1) * frames_per_wedge - 1
                frame_data.append(create_wedge(
                    theta_values[start_frame],
                    theta_values[end_frame],
                    colors[w % len(colors)]
                ))

            # Add current partial wedge
            if frame_in_wedge > 0:
                start_frame = wedge_idx * frames_per_wedge
                frame_data.append(create_wedge(
                    theta_values[start_frame],
                    theta_values[frame_idx],
                    colors[wedge_idx % len(colors)]
                ))

            # Add orbit
            frame_data.append(go.Scatter(
                x=x_ellipse,
                y=y_ellipse,
                mode="lines",
                line={"color": "lightblue", "width": 3},
                showlegend=False,
                hoverinfo="skip",
            ))

            # Add sun
            frame_data.append(go.Scatter(
                x=[0],
                y=[0],
                mode="markers",
                marker={"size": 24, "color": "gold"},
                showlegend=False,
                hoverinfo="skip",
            ))

            # Add planet
            frame_data.append(go.Scatter(
                x=[positions[frame_idx][0]],
                y=[positions[frame_idx][1]],
                mode="markers",
                marker={"size": 14, "color": "steelblue"},
                showlegend=False,
                hoverinfo="skip",
            ))

            # Add radius vector
            frame_data.append(go.Scatter(
                x=[0, positions[frame_idx][0]],
                y=[0, positions[frame_idx][1]],
                mode="lines",
                line={"color": "white", "width": 2},
                showlegend=False,
                hoverinfo="skip",
            ))

            frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

        # Initial state
        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Kepler's Second Law:</b> Equal Areas in Equal Times<br><sub>Each colored wedge = same time interval</sub>",
                    font=dict(size=16),
                ),
                xaxis={"scaleanchor": "y", "range": [-2.5, 2], "title": "x (AU)"},
                yaxis={"range": [-1.5, 1.5], "title": "y (AU)"},
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.15,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "▶ Play",
                                "method": "animate",
                                "args": [
                                    None,
                                    {
                                        "frame": {"duration": 60, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0},
                                    },
                                ],
                            },
                            {
                                "label": "⏸ Pause",
                                "method": "animate",
                                "args": [
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                            {
                                "label": "↺ Reset",
                                "method": "animate",
                                "args": [
                                    ["0"],
                                    {
                                        "frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                    },
                                ],
                            },
                        ],
                    }
                ],
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    equal_areas_fig = create_equal_areas_animation()
    equal_areas_fig
    return (create_equal_areas_animation, equal_areas_fig)


@app.cell
def _(mo):
    mo.accordion(
        {
            "The Deep Truth: Angular Momentum Conservation": mo.md(
                r"""
        Feynman emphasized that this law is more fundamental than it first appears.
        It doesn't depend on the *specific* force law at all!

        **For ANY central force** (one that always points toward a fixed center):

        $$\vec{\tau} = \vec{r} \times \vec{F} = 0$$

        No torque means angular momentum is conserved:
        $$\vec{L} = m\vec{r} \times \vec{v} = \text{constant}$$

        The area swept out in time $dt$ is half the parallelogram formed by $\vec{r}$ and $d\vec{r}$:
        $$dA = \frac{1}{2}|\vec{r} \times d\vec{r}| = \frac{1}{2}|\vec{r} \times \vec{v}|\,dt = \frac{L}{2m}\,dt$$

        Therefore:
        $$\boxed{\frac{dA}{dt} = \frac{L}{2m} = \text{constant}}$$

        This works for gravity ($1/r^2$), springs ($-kr$), or any other central force!
        The equal-area law is really a statement about **symmetry**: the rotational
        symmetry of a central force implies conservation of angular momentum.
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

        ## Kepler's Third Law: The Harmonic Law

        > *The square of a planet's orbital period is proportional to the cube of its
        semi-major axis.*

        $$T^2 = \frac{4\pi^2}{GM}a^3$$

        This is arguably the most powerful of Kepler's laws because it connects *time* to *space*
        with a precise mathematical relationship that holds across the entire solar system.

        **What makes this remarkable?**

        Consider the range of scales involved:
        - **Mercury:** 0.39 AU from Sun, orbits in 88 days
        - **Saturn:** 9.5 AU from Sun, orbits in 29 years

        Saturn is 24× farther from the Sun and takes 122× longer to orbit. These numbers seem
        unrelated—until you notice that $24^3 \approx 13,824$ and $122^2 \approx 14,884$.
        They're nearly equal! That's Kepler's Third Law in action.

        **Why is $T^2/a^3$ the same for all planets?**

        The ratio $T^2/a^3 = 4\pi^2/(GM)$ depends only on the Sun's mass $M$, not on the planet.
        This means:
        - All planets orbiting the Sun have the same $T^2/a^3$ ratio
        - If you discovered a new planet, you could predict its orbital period from its distance
        - Different stars with different masses would have different ratios

        **Newton's insight:** This law let Newton work backwards to *deduce* that gravity must
        follow an inverse-square law! If gravity were $1/r^3$ or $1/r$, the relationship between
        $T$ and $a$ would be different.

        *Hover over the points to see the data. Notice how perfectly all six planets align on
        the theoretical line—this is how we know the law is correct!*
        """
    )
    return


@app.cell
def _(go, np, pl):
    # Planetary data (real values)
    planets_data = pl.DataFrame(
        {
            "Planet": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn"],
            "a (AU)": [0.387, 0.723, 1.000, 1.524, 5.203, 9.537],
            "T (years)": [0.241, 0.615, 1.000, 1.881, 11.86, 29.46],
            "Eccentricity": [0.206, 0.007, 0.017, 0.093, 0.048, 0.054],
        }
    )

    # Calculate T² and a³
    planets_analyzed = planets_data.with_columns(
        [
            (pl.col("T (years)") ** 2).round(2).alias("T² (years²)"),
            (pl.col("a (AU)") ** 3).round(2).alias("a³ (AU³)"),
            ((pl.col("T (years)") ** 2) / (pl.col("a (AU)") ** 3)).round(3).alias("T²/a³"),
        ]
    )

    # Extract for plotting
    a_cubed = planets_analyzed["a³ (AU³)"].to_numpy()
    T_squared = planets_analyzed["T² (years²)"].to_numpy()
    names = planets_analyzed["Planet"].to_list()

    # Theoretical line (T² = a³ when using AU and years)
    a_theory = np.linspace(0, 900, 100)
    T_theory = a_theory

    kepler3_fig = go.Figure()

    # Theoretical line
    kepler3_fig.add_trace(
        go.Scatter(
            x=a_theory,
            y=T_theory,
            mode="lines",
            name="Theory: T² = a³",
            line={"color": "red", "dash": "dash", "width": 2},
        )
    )

    # Planet data points
    kepler3_fig.add_trace(
        go.Scatter(
            x=a_cubed,
            y=T_squared,
            mode="markers+text",
            name="Observed Data",
            text=names,
            textposition="top center",
            textfont=dict(size=11),
            marker={"size": 14, "color": "steelblue", "line": {"width": 2, "color": "white"}},
            hovertemplate="<b>%{text}</b><br>a³ = %{x:.2f} AU³<br>T² = %{y:.2f} years²<extra></extra>",
        )
    )

    kepler3_fig.update_layout(
        title=dict(
            text="<b>Kepler's Third Law:</b> T² vs a³<br><sub>All planets fall on the same line!</sub>",
            font=dict(size=16),
        ),
        xaxis_title="Semi-major axis cubed, a³ (AU³)",
        yaxis_title="Period squared, T² (years²)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="closest",
    )

    kepler3_fig
    return (
        T_squared,
        T_theory,
        a_cubed,
        a_theory,
        kepler3_fig,
        names,
        planets_analyzed,
        planets_data,
    )


@app.cell
def _(mo, planets_analyzed):
    mo.vstack(
        [
            mo.md(
                r"""
                **Planetary Data Table**

                Notice the last column: $T^2/a^3 \approx 1.00$ for every planet! This constant ratio
                is what Kepler discovered empirically, and what Newton explained theoretically.
                """
            ),
            mo.ui.table(planets_analyzed, selection=None),
        ]
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "Derivation: Why T² ∝ a³?": mo.md(
                r"""
        For a circular orbit (a good approximation for most planets), the derivation is elegant:

        **Step 1: Balance of forces**

        Gravitational pull provides the centripetal acceleration:
        $$\frac{mv^2}{r} = \frac{GMm}{r^2}$$

        **Step 2: Express velocity in terms of period**

        For a circular orbit, the planet travels circumference $2\pi r$ in time $T$:
        $$v = \frac{2\pi r}{T}$$

        **Step 3: Substitute and simplify**

        $$\frac{m(2\pi r/T)^2}{r} = \frac{GMm}{r^2}$$

        $$\frac{4\pi^2 r}{T^2} = \frac{GM}{r^2}$$

        $$T^2 = \frac{4\pi^2}{GM}r^3$$

        **Step 4: Generalize to ellipses**

        Newton showed that for elliptical orbits, $r$ is replaced by the semi-major axis $a$:
        $$\boxed{T^2 = \frac{4\pi^2}{GM}a^3}$$

        The factor $4\pi^2/GM$ is the *same* for all planets orbiting the Sun—that's why
        they all fall on the same line! Different stars have different masses $M$, so their
        planetary systems would have different slopes.
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

        ## Newton's Law of Universal Gravitation

        Here comes Newton's great synthesis—the law that unified terrestrial and celestial physics:

        $$F = G\frac{m_1 m_2}{r^2}$$

        **The word "Universal" is key.** Newton claimed that the *same* force that makes an apple
        fall from a tree also keeps the Moon in orbit, holds galaxies together, and governs the
        motion of everything with mass in the universe. This was a radical idea—before Newton,
        people thought earthly and heavenly physics were completely different.

        **Understanding the equation:**

        - $F$ = gravitational force (in Newtons)
        - $G$ = gravitational constant ($6.67 \times 10^{-11}$ N⋅m²/kg²)—remarkably small!
        - $m_1, m_2$ = the two masses attracting each other
        - $r$ = distance between their centers

        **Why inverse-square ($1/r^2$)?**

        The inverse-square dependence is not arbitrary—it's deeply connected to the geometry of
        3D space. Imagine gravity as "field lines" radiating outward from a mass. The number of
        lines is fixed, but they spread over the surface of an expanding sphere. Since a sphere's
        surface area grows as $r^2$, the density of lines (and thus the field strength) falls as $1/r^2$.

        **What makes $1/r^2$ mathematically special?**

        As Feynman emphasized, the inverse-square law is the *only* power law that:
        1. Produces closed, repeating elliptical orbits (orbits that return exactly to their starting point)
        2. Makes Kepler's Third Law ($T^2 \propto a^3$) work out exactly
        3. Allows Newton to prove that a spherical shell acts gravitationally as if all its mass were at the center

        If gravity were $1/r$ or $1/r^3$, planetary orbits would slowly precess (rotate) or spiral—they
        wouldn't be stable ellipses.

        *The plot below compares different power laws on a log-log scale. Only $1/r^2$ produces
        the stable, closed orbits we observe.*
        """
    )
    return


@app.cell
def _(go, np):
    # Compare different power laws
    r = np.linspace(0.5, 5, 100)

    inv_r1 = 1 / r
    inv_r2 = 1 / r**2
    inv_r3 = 1 / r**3

    inverse_square_fig = go.Figure()

    inverse_square_fig.add_trace(
        go.Scatter(
            x=r,
            y=inv_r1,
            mode="lines",
            name="1/r — orbits precess",
            line={"color": "gray", "dash": "dot", "width": 2},
        )
    )

    inverse_square_fig.add_trace(
        go.Scatter(
            x=r,
            y=inv_r2,
            mode="lines",
            name="1/r² — stable ellipses!",
            line={"color": "red", "width": 4},
        )
    )

    inverse_square_fig.add_trace(
        go.Scatter(
            x=r,
            y=inv_r3,
            mode="lines",
            name="1/r³ — unstable",
            line={"color": "gray", "dash": "dash", "width": 2},
        )
    )

    inverse_square_fig.update_layout(
        title=dict(
            text="<b>Why Inverse-Square is Special</b><br><sub>Only 1/r² produces stable, closed planetary orbits</sub>",
            font=dict(size=16),
        ),
        xaxis_title="Distance r (log scale)",
        yaxis_title="Force magnitude (log scale)",
        yaxis_type="log",
        xaxis_type="log",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
    )

    inverse_square_fig
    return (inv_r1, inv_r2, inv_r3, inverse_square_fig, r)


@app.cell
def _(mo):
    mo.accordion(
        {
            "Newton's Apple-and-Moon Calculation": mo.md(
                r"""
        This is the calculation that changed history. Newton asked: if gravity follows an
        inverse-square law, can the *same* force explain both the falling apple and the
        orbiting Moon?

        **The Moon's orbital data:**
        - Distance from Earth: $r_{moon} \approx 60 \times R_{Earth} \approx 384,000$ km
        - Orbital period: $T \approx 27.3$ days $\approx 2.36 \times 10^6$ seconds

        **Calculate the Moon's centripetal acceleration:**
        $$a_{moon} = \frac{4\pi^2 r}{T^2} = \frac{4\pi^2 \times 3.84 \times 10^8}{(2.36 \times 10^6)^2} \approx 0.00272 \text{ m/s}^2$$

        **If gravity follows inverse-square, predict from surface gravity:**
        $$\frac{a_{moon}}{g_{surface}} = \left(\frac{R_{Earth}}{r_{moon}}\right)^2 = \frac{1}{60^2} = \frac{1}{3600}$$

        $$a_{moon} = \frac{9.8}{3600} \approx 0.00272 \text{ m/s}^2$$

        **It matches!**

        The same force that makes an apple fall at 9.8 m/s² makes the Moon "fall" toward
        Earth at 1/3600 of that rate. The Moon doesn't crash into Earth because it's also
        moving sideways fast enough to keep missing!

        This was the moment physics unified the heavens and the Earth.
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

        ## Newton's Cannon: The Unity of Falling and Orbiting

        This is one of Newton's most brilliant thought experiments, published in his *Principia* (1687).
        It demolishes the intuitive barrier between "falling" and "orbiting."

        **The setup:** Imagine a cannon on a very high mountain—so high it's above the atmosphere
        (no air resistance). Fire the cannon horizontally with increasing velocities.

        **What happens at each velocity?**

        1. **Low velocity (red):** The cannonball falls to Earth in a parabolic arc, just like
           any projectile. Gravity pulls it down faster than it moves forward.

        2. **Medium velocity (yellow):** The cannonball travels farther before hitting the ground.
           It's still falling, but now Earth's curvature matters—the ground curves away slightly.

        3. **Orbital velocity (green):** Here's the magic! The cannonball falls toward Earth,
           but Earth's surface curves away at exactly the same rate. The ball keeps falling but
           never gets closer—it's in a circular orbit! For Earth, this is about 7.9 km/s (17,500 mph).

        4. **Above orbital velocity (blue):** The cannonball has too much energy for a circle.
           It swings out into an elliptical orbit, going farther from Earth before falling back.

        **The profound insight:**

        > **Orbiting IS falling.** The Moon is falling toward Earth right now—it just keeps missing.

        An astronaut on the Space Station is in continuous free-fall, falling toward Earth at
        the same rate as their spacecraft. That's why they float—not because there's "no gravity"
        (gravity is 90% as strong up there), but because everything around them is falling together.

        *Click "Fire Cannon" to watch cannonballs launched at increasing velocities. Each trajectory
        appears in sequence—watch how they transition from falling to orbiting!*
        """
    )
    return


@app.cell
def _(go, np):
    def create_newtons_cannon_animated():
        """Create animated visualization of Newton's cannon thought experiment."""
        R = 1.0
        g = 1.0

        # Draw Earth (fewer points)
        theta_earth = np.linspace(0, 2 * np.pi, 60)
        x_earth = R * np.cos(theta_earth)
        y_earth = R * np.sin(theta_earth)

        # Cannon position
        cannon_height = 1.1 * R
        x_cannon, y_cannon = 0, cannon_height

        # Circular orbit velocity at cannon height
        v_circular = np.sqrt(g * R**2 / cannon_height)

        # Different launch velocities (fewer trajectories)
        velocities = [0.4, 0.7, 1.0, 1.15]
        colors = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db"]

        # Pre-calculate all trajectories with fewer points
        all_trajectories = []
        max_points = 80  # Limit points per trajectory

        for v_frac in velocities:
            v0 = v_frac * v_circular
            x, y = x_cannon, y_cannon
            vx, vy = v0, 0
            dt = 0.02  # Larger time step
            x_traj = [x]
            y_traj = [y]

            for step in range(500):
                r = np.sqrt(x**2 + y**2)
                if r < R:
                    break
                if r > 4:
                    break
                if step > 50 and abs(y - cannon_height) < 0.1 and x > 0.1:
                    break
                if len(x_traj) >= max_points:
                    break

                a_mag = g * R**2 / r**2
                ax = -a_mag * x / r
                ay = -a_mag * y / r
                vx += ax * dt
                vy += ay * dt
                x += vx * dt
                y += vy * dt
                x_traj.append(x)
                y_traj.append(y)

            all_trajectories.append((np.array(x_traj), np.array(y_traj)))

        # Create frames - one frame per trajectory (show them appearing one by one)
        frames = []

        for traj_idx in range(len(all_trajectories) + 1):
            frame_data = [
                # Earth
                go.Scatter(x=x_earth, y=y_earth, mode="lines", fill="toself",
                           fillcolor="rgba(100, 180, 255, 0.4)", line={"color": "steelblue", "width": 2},
                           hoverinfo="skip"),
                # Cannon
                go.Scatter(x=[x_cannon], y=[y_cannon], mode="markers",
                           marker={"size": 12, "color": "black", "symbol": "triangle-right"},
                           hoverinfo="skip"),
            ]

            # Add trajectories up to current index
            for idx in range(traj_idx):
                px, py = all_trajectories[idx]
                frame_data.append(go.Scatter(x=px, y=py, mode="lines",
                                              line={"color": colors[idx], "width": 3},
                                              hoverinfo="skip"))

            frames.append(go.Frame(data=frame_data, name=str(traj_idx)))

        # Initial frame - just Earth and cannon
        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Newton's Cannon:</b> From Falling to Orbiting<br><sub>Click Play to fire at increasing velocities</sub>",
                    font=dict(size=16),
                ),
                xaxis={"scaleanchor": "y", "range": [-2.5, 2.5], "showgrid": False, "zeroline": False, "showticklabels": False},
                yaxis={"range": [-2.5, 2.5], "showgrid": False, "zeroline": False, "showticklabels": False},
                showlegend=False,
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.08,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "▶ Fire Cannon",
                                "method": "animate",
                                "args": [None, {"frame": {"duration": 800, "redraw": True},
                                               "fromcurrent": True, "transition": {"duration": 300}}],
                            },
                            {
                                "label": "↺ Reset",
                                "method": "animate",
                                "args": [["0"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                            },
                        ],
                    }
                ],
                margin=dict(b=60),
                annotations=[
                    dict(x=1.9, y=1.7, text="<b>Velocity:</b>", showarrow=False, font=dict(size=10)),
                    dict(x=1.9, y=1.4, text="<span style='color:#e74c3c'>■</span> Slow", showarrow=False, font=dict(size=9)),
                    dict(x=1.9, y=1.2, text="<span style='color:#f1c40f'>■</span> Medium", showarrow=False, font=dict(size=9)),
                    dict(x=1.9, y=1.0, text="<span style='color:#2ecc71'>■</span> Orbital", showarrow=False, font=dict(size=9)),
                    dict(x=1.9, y=0.8, text="<span style='color:#3498db'>■</span> Fast", showarrow=False, font=dict(size=9)),
                ],
            ),
            frames=frames,
        )

        return fig

    cannon_fig = create_newtons_cannon_animated()
    cannon_fig
    return (cannon_fig, create_newtons_cannon_animated)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Interactive Explorer: How Eccentricity Shapes an Orbit

        Eccentricity $e$ is the single number that describes an orbit's shape. It ranges from 0 to 1
        for bound orbits:

        | Eccentricity | Shape | Example |
        |--------------|-------|---------|
        | $e = 0$ | Perfect circle | Venus ($e = 0.007$) |
        | $e = 0.2$ | Slightly elliptical | Mercury ($e = 0.206$) |
        | $e = 0.5$ | Noticeably elongated | — |
        | $e = 0.97$ | Extremely elongated | Halley's Comet |
        | $e = 1$ | Parabola (escape) | Some comets |
        | $e > 1$ | Hyperbola (unbound) | Interstellar objects |

        **How eccentricity affects the orbit:**

        For an orbit with semi-major axis $a$ and eccentricity $e$:
        - **Perihelion** (closest approach): $r_{min} = a(1-e)$
        - **Aphelion** (farthest point): $r_{max} = a(1+e)$
        - **Ratio**: $r_{max}/r_{min} = (1+e)/(1-e)$

        **Why eccentricity matters:**

        High eccentricity means extreme temperature variations! A comet with $e = 0.97$ might
        swing from beyond Neptune's orbit (freezing) to inside Mercury's orbit (searing) and back.
        Earth's small eccentricity ($e = 0.017$) keeps our climate relatively stable.

        *Use the slider below to see how eccentricity transforms a circle into increasingly
        elongated ellipses. Watch how the perihelion and aphelion distances change!*
        """
    )
    return


@app.cell
def _(mo):
    eccentricity_slider = mo.ui.slider(
        start=0,
        stop=0.95,
        step=0.05,
        value=0.5,
        label="Eccentricity (e)",
        show_value=True,
    )
    mo.hstack([mo.md("**Adjust eccentricity:**"), eccentricity_slider], justify="start", gap=1)
    return (eccentricity_slider,)


@app.cell
def _(eccentricity_slider, go, np):
    def plot_orbit_with_eccentricity(e):
        """Plot an orbit with given eccentricity."""
        a = 1.0

        theta = np.linspace(0, 2 * np.pi, 200)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        r_perihelion = a * (1 - e)
        r_aphelion = a * (1 + e)
        c = a * e
        b = a * np.sqrt(1 - e**2)

        fig = go.Figure()

        # Orbit
        fig.add_trace(
            go.Scatter(
                x=x, y=y,
                mode="lines",
                line={"color": "lightblue", "width": 3},
                name="Orbit",
                hoverinfo="skip",
            )
        )

        # Sun
        fig.add_trace(
            go.Scatter(
                x=[0], y=[0],
                mode="markers",
                marker={"size": 24, "color": "gold"},
                name="Sun (focus)",
            )
        )

        # Second focus
        fig.add_trace(
            go.Scatter(
                x=[-2 * c], y=[0],
                mode="markers",
                marker={"size": 10, "color": "gray", "symbol": "x"},
                name="Empty focus",
            )
        )

        # Perihelion
        fig.add_trace(
            go.Scatter(
                x=[r_perihelion], y=[0],
                mode="markers",
                marker={"size": 12, "color": "#e74c3c"},
                name=f"Perihelion: {r_perihelion:.2f} AU",
            )
        )

        # Aphelion
        fig.add_trace(
            go.Scatter(
                x=[-r_aphelion], y=[0],
                mode="markers",
                marker={"size": 12, "color": "#3498db"},
                name=f"Aphelion: {r_aphelion:.2f} AU",
            )
        )

        # Semi-major axis
        fig.add_trace(
            go.Scatter(
                x=[-r_aphelion, r_perihelion], y=[0, 0],
                mode="lines",
                line={"color": "green", "dash": "dash", "width": 2},
                name=f"Semi-major axis: {a:.2f} AU",
            )
        )

        ratio = r_aphelion / r_perihelion if r_perihelion > 0.01 else float('inf')

        fig.update_layout(
            title=dict(
                text=f"<b>Orbit with e = {e:.2f}</b><br><sub>Semi-minor axis b = {b:.2f} AU | Aphelion/Perihelion = {ratio:.1f}×</sub>",
                font=dict(size=16),
            ),
            xaxis={"scaleanchor": "y", "range": [-2.5, 2], "title": "x (AU)"},
            yaxis={"range": [-1.5, 1.5], "title": "y (AU)"},
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10)),
        )

        return fig

    orbit_explorer_fig = plot_orbit_with_eccentricity(eccentricity_slider.value)
    orbit_explorer_fig
    return (orbit_explorer_fig, plot_orbit_with_eccentricity)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Tidal Forces: Gravity's Gradient

        The Moon's gravity isn't uniform across Earth—it's slightly stronger on the side
        facing the Moon and slightly weaker on the far side. This **differential pull**,
        or *tidal force*, stretches Earth along the Earth-Moon line.

        **But why TWO bulges? Why is there a bulge on the far side, away from the Moon?**

        This is one of the most commonly misunderstood phenomena in physics. The far-side bulge
        is NOT caused by the Sun—it's caused by the Moon itself! Here's the key insight:

        Think about it from Earth's reference frame (which is accelerating toward the Moon):
        - The **near side** of Earth is pulled toward the Moon *more strongly* than average → water bulges toward Moon
        - The **center** of Earth is pulled with average force → this is our reference
        - The **far side** is pulled *less strongly* than Earth's center → relative to Earth's center, this water is "left behind"

        In other words: the Moon pulls Earth's center away from the far-side water, creating a bulge there too!

        The tidal force is the *difference* between the Moon's pull at each location and its pull at Earth's center.
        This creates a stretching effect along the Earth-Moon line.

        *Click Play to watch Earth rotate under the tidal bulges—notice how any point experiences two high tides per day.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_tidal_animation():
        """Create animated diagram showing Earth rotating under tidal bulges."""
        R = 1.0
        bulge = 0.25
        moon_distance = 4.5
        n_frames = 60

        # Base shapes
        theta = np.linspace(0, 2 * np.pi, 100)

        # Tidal bulge (fixed relative to Moon)
        x_bulge = (R + bulge * np.cos(2 * theta)) * np.cos(theta)
        y_bulge = (R + bulge * np.cos(2 * theta)) * np.sin(theta)

        # Moon
        moon_theta = np.linspace(0, 2 * np.pi, 50)
        moon_r = 0.3
        moon_x = moon_distance + moon_r * np.cos(moon_theta)
        moon_y = moon_r * np.sin(moon_theta)

        # Create frames for Earth rotation
        frames = []
        for i in range(n_frames):
            rotation_angle = 2 * np.pi * i / n_frames

            # Earth's surface features rotate
            earth_theta = theta + rotation_angle
            x_earth = R * 0.85 * np.cos(earth_theta)
            y_earth = R * 0.85 * np.sin(earth_theta)

            # A marker point on Earth's surface (like a coastal city)
            marker_angle = rotation_angle
            marker_r = R + bulge * np.cos(2 * marker_angle)  # On the water surface
            marker_x = marker_r * np.cos(marker_angle)
            marker_y = marker_r * np.sin(marker_angle)

            # Continent markers (rotate with Earth)
            continent_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
            cont_x = [0.6 * np.cos(a + rotation_angle) for a in continent_angles]
            cont_y = [0.6 * np.sin(a + rotation_angle) for a in continent_angles]

            frame_data = [
                # Ocean bulge (fixed)
                go.Scatter(x=x_bulge, y=y_bulge, mode="lines", fill="toself",
                           fillcolor="rgba(65, 105, 225, 0.3)", line={"color": "royalblue", "width": 2}),
                # Earth interior (rotating)
                go.Scatter(x=x_earth, y=y_earth, mode="lines", fill="toself",
                           fillcolor="rgba(139, 119, 101, 0.6)", line={"color": "sienna", "width": 1}),
                # Continent markers
                go.Scatter(x=cont_x, y=cont_y, mode="markers",
                           marker={"size": 12, "color": "forestgreen", "symbol": "circle"}),
                # Coastal city marker
                go.Scatter(x=[marker_x], y=[marker_y], mode="markers",
                           marker={"size": 10, "color": "red", "symbol": "star"}),
                # Moon
                go.Scatter(x=moon_x, y=moon_y, mode="lines", fill="toself",
                           fillcolor="rgba(200, 200, 200, 0.8)", line={"color": "gray", "width": 1}),
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        # Initial frame
        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Tidal Animation:</b> Earth Rotates Under the Bulges<br><sub>Red star = coastal city experiencing two high tides per rotation</sub>",
                    font=dict(size=16),
                ),
                xaxis={"scaleanchor": "y", "range": [-3, 6], "showgrid": False, "zeroline": False, "showticklabels": False},
                yaxis={"range": [-2.5, 2.5], "showgrid": False, "zeroline": False, "showticklabels": False},
                showlegend=False,
                updatemenus=[
                    {
                        "type": "buttons",
                        "showactive": False,
                        "y": -0.08,
                        "x": 0.5,
                        "xanchor": "center",
                        "buttons": [
                            {
                                "label": "▶ Play",
                                "method": "animate",
                                "args": [None, {"frame": {"duration": 80, "redraw": True},
                                               "fromcurrent": True, "transition": {"duration": 0}}],
                            },
                            {
                                "label": "⏸ Pause",
                                "method": "animate",
                                "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                            },
                        ],
                    }
                ],
                margin=dict(b=60),
                annotations=[
                    dict(x=-1.3, y=-1.8, text="Far-side bulge<br>(Moon pulls Earth away)", showarrow=False, font=dict(size=10)),
                    dict(x=1.3, y=-1.8, text="Near-side bulge<br>(Moon pulls water)", showarrow=False, font=dict(size=10)),
                    dict(x=moon_distance, y=-0.8, text="Moon", showarrow=False, font=dict(size=11, color="gray")),
                ],
            ),
            frames=frames,
        )

        return fig

    tidal_fig = create_tidal_animation()
    tidal_fig
    return (create_tidal_animation, tidal_fig)


@app.cell
def _(mo):
    mo.accordion(
        {
            "The Physics of Two Bulges (Detailed Explanation)": mo.md(
                r"""
        The two-bulge phenomenon confuses many people. Let's work through it carefully.

        **The Key: Tidal force is DIFFERENTIAL gravity**

        The Moon exerts gravitational force on every part of Earth, but the strength varies:
        - At Earth's center: $F_{center} = \frac{GMm}{r^2}$
        - At the near side (distance $r - R$): $F_{near} = \frac{GMm}{(r-R)^2}$ — **stronger**
        - At the far side (distance $r + R$): $F_{far} = \frac{GMm}{(r+R)^2}$ — **weaker**

        **The tidal force at each point is the difference from the center:**

        $$F_{tidal,near} = F_{near} - F_{center} \approx +\frac{2GMmR}{r^3}$$ (toward Moon)

        $$F_{tidal,far} = F_{far} - F_{center} \approx -\frac{2GMmR}{r^3}$$ (away from Moon!)

        **Why does "weaker pull" create an outward bulge?**

        Earth's center accelerates toward the Moon. The far-side water accelerates *less*
        (weaker pull), so relative to Earth's center, it lags behind—creating a bulge
        pointing away from the Moon.

        It's like being in an elevator that suddenly accelerates upward: you feel pressed
        into the floor (near side), but a helium balloon would seem to move toward the
        ceiling (far side)—not because something pushes it up, but because it doesn't
        accelerate as much as its surroundings.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Why does the Moon cause stronger tides than the Sun?**

        The Sun is 27 million times more massive than the Moon, but 390 times farther away.
        Tidal force depends on the *gradient* of gravity—how fast it changes with distance:

        $$F_{tidal} \propto \frac{M}{r^3}$$

        Since tidal force goes as $1/r^3$ (not $1/r^2$ like gravity itself):

        $$\frac{F_{tide,Sun}}{F_{tide,Moon}} = \frac{M_{Sun}}{M_{Moon}} \times \left(\frac{r_{Moon}}{r_{Sun}}\right)^3 \approx \frac{27,000,000}{390^3} \approx 0.46$$

        The Moon wins! Solar tides are about half as strong as lunar tides.

        When the Sun and Moon align (new moon or full moon), we get **spring tides**—extra high and low.
        When they're at right angles (quarter moons), we get **neap tides**—more moderate.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Einstein's Refinement: General Relativity

        Newton's theory worked spectacularly for over 200 years—it predicted the existence of
        Neptune before anyone saw it! But tiny discrepancies remained, and Einstein showed that
        Newton's theory was an *approximation* of a deeper truth.

        **The conceptual revolution:**

        Newton described gravity as a force acting instantaneously across space—but *how* does
        the Sun "know" where Earth is? Einstein's answer: gravity isn't a force at all!

        Instead, mass and energy **curve spacetime itself**. Objects in free fall (including
        orbiting planets) are simply following the straightest possible paths through curved
        spacetime. The Earth doesn't feel a "force" from the Sun—it's following a geodesic
        through the spacetime geometry the Sun creates.

        **Where Newton fails and Einstein succeeds:**

        | Phenomenon | Newton | Einstein | What We Observe |
        |------------|--------|----------|-----------------|
        | Mercury's orbit | Precesses 532"/century | Adds 43"/century | 575"/century ✓ |
        | Light near Sun | Not bent | Bent by 1.75" | Confirmed in 1919 eclipse ✓ |
        | Clocks in gravity | Run at same rate | Tick slower | GPS satellites need 38 μs/day correction ✓ |
        | Gravitational waves | None predicted | Ripples in spacetime | Detected by LIGO in 2015 ✓ |
        | Black holes | Undefined | Complete theory | Imaged by Event Horizon Telescope 2019 ✓ |

        **Mercury's perihelion puzzle:**

        Mercury's elliptical orbit slowly rotates (precesses) around the Sun. Newton's theory,
        accounting for all other planets' gravitational tugs, predicts 532 arcseconds per century.
        But astronomers measured 575 arcseconds—a discrepancy of 43 arcseconds that no one
        could explain. Einstein's first test of General Relativity was showing it predicted
        exactly those missing 43 arcseconds!

        **The relationship between Newton and Einstein:**

        As Feynman emphasized: Newton isn't *wrong*—his theory is what you get from Einstein's
        when gravity is weak and speeds are slow (compared to light). For throwing baseballs,
        launching rockets, even planning interplanetary missions, Newton is plenty accurate and
        much easier to calculate. Einstein only matters for extreme precision or extreme gravity.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary: The Laws of Gravitation

        | Law | Mathematical Form | Physical Meaning |
        |-----|-------------------|------------------|
        | **Kepler I** | $r = \dfrac{a(1-e^2)}{1+e\cos\theta}$ | Orbits are ellipses with Sun at one focus |
        | **Kepler II** | $\dfrac{dA}{dt} = \dfrac{L}{2m}$ | Equal areas swept in equal times |
        | **Kepler III** | $T^2 = \dfrac{4\pi^2}{GM}a^3$ | Period² ∝ distance³ |
        | **Newton** | $F = G\dfrac{m_1 m_2}{r^2}$ | Universal gravitation |

        ---

        Feynman closed his lecture on gravitation with a reflection on the nature of
        scientific understanding:

        > *"Nature uses only the longest threads to weave her patterns, so each small piece
        of her fabric reveals the organization of the entire tapestry."*

        The same law that governs an apple's fall describes the dance of binary pulsars
        billions of light-years away. That's the power—and the beauty—of physics.
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

        - **Feynman, R. P., Leighton, R. B., & Sands, M.** (1963). *The Feynman Lectures on Physics, Volume I*.
          [Chapter 7: The Theory of Gravitation](https://www.feynmanlectures.caltech.edu/I_07.html).
          Addison-Wesley.

        ### Mathematical Background

        - **Kepler's Laws of Planetary Motion**
          - First Law (1609): Planets move in ellipses with the Sun at one focus
          - Second Law (1609): Equal areas are swept in equal times
          - Third Law (1619): $T^2 \propto a^3$ for all planets
          - Original work: *Astronomia Nova* (1609) and *Harmonices Mundi* (1619)

        - **Newton's Law of Universal Gravitation** (1687)
          - $F = G\frac{m_1 m_2}{r^2}$
          - Original work: *Philosophiæ Naturalis Principia Mathematica*
          - Gravitational constant $G = 6.674 \times 10^{-11}$ N⋅m²/kg²

        - **Conic Sections and Orbital Mechanics**
          - Eccentricity: $e = 0$ (circle), $0 < e < 1$ (ellipse), $e = 1$ (parabola), $e > 1$ (hyperbola)
          - Orbit equation: $r = \frac{a(1-e^2)}{1 + e\cos\theta}$

        ### Further Reading

        - **Feynman Lectures**: [Chapter 9: Newton's Laws of Dynamics](https://www.feynmanlectures.caltech.edu/I_09.html)
        - **Feynman Lectures**: [Chapter 13: Work and Potential Energy](https://www.feynmanlectures.caltech.edu/I_13.html)
        - Goldstein, H. *Classical Mechanics* (3rd ed.) — Chapters on central force motion
        - Misner, Thorne, & Wheeler. *Gravitation* — For general relativistic treatment
        """
    )
    return


if __name__ == "__main__":
    app.run()
