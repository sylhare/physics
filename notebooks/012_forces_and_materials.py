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
        create_play_pause_buttons,
        get_plotly_config,
    )

    return (
        COLORS,
        create_play_pause_buttons,
        get_plotly_config,
        go,
        mo,
        np,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Forces, Friction, and the Strength of Materials

        *A hands-on tour of the ideas that decide whether a shelf holds your books or
        quietly sags to the floor — built in the spirit of the
        [Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/).*

        ---

        ## Why should you care how a plank bends?

        Look around the room you're in. A table holds up a laptop. A shelf holds up books.
        A door hangs from two small hinges. A ladder leans against a wall without sliding out.
        Every one of these is a little conspiracy of **forces** that happen to cancel out — and
        the whole game of understanding structures is learning to see those forces even though
        nothing is moving.

        Feynman liked to say that the interesting thing about physics is not the equations but
        the *habit of looking*. So that's what we'll practice. We'll start with the simplest
        possible question — *what is a push?* — and by the end we'll be able to look at a beam,
        a bracket, or a leaning ladder and say, with reasons: *this will hold*, or *this is where
        it breaks*.

        We'll build up in layers, each one leaning on the one before:

        1. **Force** — a push or a pull, and why direction matters
        2. **Equilibrium** — how a still object is secretly a tug-of-war that ties
        3. **The moment** — forces that *turn* things, and the magic of the lever
        4. **Constraints and reactions** — how a table, a pin, or a wall pushes back
        5. **Friction** — the sideways force that lets us walk, and stops boxes from sliding
        6. **Stress and strain** — what a force feels like *inside* the material
        7. **Everyday materials** — steel, aluminium, concrete, wood, rubber, compared honestly
        8. **Beams** — why *shape* beats *material*, and why a plank is stiff on its edge
        9. **Stress concentration** — where a shape secretly breaks first
        10. **Buckling** — why a long thin thing folds instead of crushing

        Nothing here needs more than school algebra. Every number is a real, measured one, and
        every claim links to where you can check it. Let's go and look.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 1. What is a force?

        A **force** is just a push or a pull. That sounds too simple to be worth a name, but
        the subtle part is that a force is not a single number — it's an **arrow**. To describe
        one completely you need three things:

        - **How hard** it pushes (its magnitude, measured in *newtons*, N — roughly the weight
          of a small apple resting in your hand),
        - **Which way** it points (its direction),
        - **Where** it acts (its point of application — pushing a door near the hinge is not the
          same as pushing near the handle, as we'll see).

        Because forces are arrows, several forces acting on the same object combine the way arrows
        do: you lay them tip-to-tail and see where you end up. If they cancel out perfectly, the
        object doesn't accelerate — that's Newton's whole story in one line,
        $\vec{F}_{\text{net}} = m\vec{a}$. When $\vec{F}_{\text{net}} = 0$, either the object sits
        still or it coasts at constant velocity. Feynman's Chapter on the
        [Characteristics of Force](https://www.feynmanlectures.caltech.edu/I_12.html) is the
        classic tour of this idea.

        There's one more piece that trips everyone up at first: **every push comes with an equal
        push back** (Newton's third law). When a book presses down on a table, the table presses
        *up* on the book, exactly as hard. That returning push has a name — the **normal force** —
        and it's the reason the book doesn't fall through the wood.

        The picture below is a *free-body diagram*: we mentally cut the object out of the world and
        draw only the arrows acting **on it**. This one habit — draw the object, draw every arrow —
        is the single most useful thing in all of mechanics.
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo):
    def free_body_diagram():
        fig = go.Figure()

        # Ground line
        fig.add_trace(
            go.Scatter(
                x=[-1, 5],
                y=[1, 1],
                mode="lines",
                line={"color": COLORS["text_secondary"], "width": 3},
                name="Ground",
                hoverinfo="skip",
            )
        )

        # The box (a filled rectangle)
        fig.add_trace(
            go.Scatter(
                x=[1, 3, 3, 1, 1],
                y=[1, 1, 2, 2, 1],
                mode="lines",
                fill="toself",
                fillcolor="rgba(96, 165, 250, 0.25)",
                line={"color": COLORS["quantum"], "width": 2},
                name="Book / box",
                hoverinfo="skip",
            )
        )

        arrows = [
            # (tail_x, tail_y, head_x, head_y, color, label, lx, ly)
            (2.0, 1.5, 2.0, 0.35, COLORS["gravity"], "Weight  W (gravity pulls down)", 2.05, 0.5),
            (2.0, 2.0, 2.0, 3.1, COLORS["primary"], "Normal  N (table pushes up)", 2.05, 3.2),
            (0.1, 1.5, 1.0, 1.5, COLORS["secondary"], "Push  P (you push sideways)", -0.9, 1.7),
            (3.0, 1.15, 2.2, 1.15, COLORS["electric"], "Friction  f (resists sliding)", 3.1, 1.15),
        ]

        annotations = []
        for tx, ty, hx, hy, color, label, lx, ly in arrows:
            annotations.append(
                {
                    "x": hx,
                    "y": hy,
                    "ax": tx,
                    "ay": ty,
                    "xref": "x",
                    "yref": "y",
                    "axref": "x",
                    "ayref": "y",
                    "showarrow": True,
                    "arrowhead": 2,
                    "arrowsize": 1.4,
                    "arrowwidth": 3.5,
                    "arrowcolor": color,
                }
            )
            annotations.append(
                {
                    "x": lx,
                    "y": ly,
                    "text": label,
                    "showarrow": False,
                    "font": {"color": color, "size": 12},
                    "xanchor": "left",
                }
            )

        fig.update_layout(
            title={
                "text": "<b>A Free-Body Diagram</b><br><sub>Every force on the box, drawn as an arrow</sub>"
            },
            xaxis={"range": [-1, 5], "showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={
                "range": [-0.2, 3.6],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            showlegend=True,
            annotations=annotations,
            height=520,
        )
        return fig

    fbd_plot = mo.ui.plotly(free_body_diagram(), config=get_plotly_config())
    mo.output.replace(fbd_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 2. Equilibrium: a still object is a tug-of-war that ties

        Here is the first big idea, and it's almost embarrassingly powerful:

        > If an object is not accelerating, **all the forces on it add up to exactly zero.**

        That's it. A book on a table isn't experiencing *no* forces — gravity is yanking it down
        the whole time. It's just that the table pushes up *equally hard*, so the arrows cancel and
        the book stays put. We say the book is in **equilibrium**.

        This turns a static, boring picture into a puzzle we can *solve*. Whenever something holds
        still, we can write "up-forces = down-forces" and "left-forces = right-forces" and often
        that's enough to find a force we couldn't otherwise see.

        Let's do a real example that hides a nasty surprise. Hang a weight from two ropes that meet
        at the top, each making an angle $\theta$ with the *horizontal*. By symmetry each rope pulls
        with the same tension $T$. Only the vertical parts of those pulls fight gravity, so:

        $$2\,T\sin\theta = W \quad\Longrightarrow\quad T = \frac{W}{2\sin\theta}$$

        Now watch what that formula *does*. When the ropes hang steeply ($\theta$ near $90°$),
        $\sin\theta \approx 1$ and each rope carries about half the weight — sensible. But as the
        ropes get **flatter** ($\theta \to 0$), $\sin\theta \to 0$ and the tension **blows up toward
        infinity**. A nearly-horizontal rope has to pull enormously hard to produce any upward
        component at all.

        This is why a clothesline sags, why you can't pull a rope perfectly straight no matter how
        strong you are, and why a slightly drooping cable is far safer than a taut one. *Drag the
        slider and watch the tension climb as the ropes flatten out.*
        """
    )
    return


@app.cell
def _(mo):
    rope_angle = mo.ui.slider(
        start=5,
        stop=85,
        step=1,
        value=45,
        label="Rope angle θ (degrees from horizontal)",
        show_value=True,
    )
    mo.hstack([mo.md("**Flatten the ropes:**"), rope_angle], justify="start", gap=1)
    return (rope_angle,)


@app.cell
def _(COLORS, get_plotly_config, go, mo, np, rope_angle):
    def two_rope_figure(theta_deg):
        theta = np.radians(theta_deg)
        weight = 100.0  # newtons
        tension = weight / (2 * np.sin(theta))

        # Geometry: knot at origin, ropes go up-left and up-right to anchors
        span = 2.0
        anchor_y = span * np.tan(theta)
        left_anchor = (-span, anchor_y)
        right_anchor = (span, anchor_y)

        fig = go.Figure()

        # Ceiling
        fig.add_trace(
            go.Scatter(
                x=[-span - 0.5, span + 0.5],
                y=[anchor_y, anchor_y],
                mode="lines",
                line={"color": COLORS["text_secondary"], "width": 4},
                name="Ceiling",
                hoverinfo="skip",
            )
        )
        # Ropes
        for anchor in (left_anchor, right_anchor):
            fig.add_trace(
                go.Scatter(
                    x=[0, anchor[0]],
                    y=[0, anchor[1]],
                    mode="lines",
                    line={"color": COLORS["primary"], "width": 4},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
        # The weight
        fig.add_trace(
            go.Scatter(
                x=[0],
                y=[-0.35],
                mode="markers",
                marker={"size": 34, "color": COLORS["gravity"], "symbol": "square"},
                name="Weight W = 100 N",
            )
        )

        color = COLORS["wave"] if tension <= weight else COLORS["secondary"]
        fig.update_layout(
            title={
                "text": f"<b>Two Ropes Holding One Weight</b><br>"
                f"<sub>θ = {theta_deg}°  →  each rope tension T = {tension:.0f} N "
                f"({tension / weight:.1f}× the whole weight)</sub>"
            },
            xaxis={"range": [-3, 3], "showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={
                "range": [-1, max(anchor_y, 1) + 0.3],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 0,
                    "y": max(anchor_y, 1) + 0.15,
                    "text": f"<b>T = {tension:.0f} N per rope</b>",
                    "showarrow": False,
                    "font": {"color": color, "size": 15},
                }
            ],
            height=520,
        )
        return fig

    rope_plot = mo.ui.plotly(two_rope_figure(rope_angle.value), config=get_plotly_config())
    mo.output.replace(rope_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 3. The moment: forces that *turn* things

        So far our forces have pushed objects around. But there's a second thing a force can do:
        it can make something **rotate**. Push a door near its hinge and it barely swings; push at
        the handle, far from the hinge, and it opens easily. Same door, same hand — what changed?

        The *distance from the pivot*. The turning effect of a force is called its **moment**
        (or **torque**), and it's simply the force multiplied by the perpendicular distance from
        the pivot to the line of the force:

        $$\text{moment} = \text{force} \times \text{lever arm} \qquad \tau = F \, d$$

        This one little product explains a huge amount of daily life. A long wrench loosens a stuck
        bolt a short wrench can't touch. A door handle is placed as far from the hinge as possible.
        A seesaw balances a heavy child close to the middle against a light child far out.

        And here is the second law of equilibrium, the twin of the first: for something that isn't
        spinning up,

        > the **turning effects** must also cancel — clockwise moments = anticlockwise moments.

        A balanced seesaw is exactly this statement: $W_1 d_1 = W_2 d_2$. The heavy side wins unless
        the light side sits farther out to make up for it with a longer lever arm. *Slide the block
        on the right in and out and watch the beam tip until the two moments match.*
        """
    )
    return


@app.cell
def _(mo):
    seesaw_pos = mo.ui.slider(
        start=0.5,
        stop=3.5,
        step=0.1,
        value=1.2,
        label="Distance of right block from pivot, d₂ (m)",
        show_value=True,
    )
    mo.hstack([mo.md("**Move the right block:**"), seesaw_pos], justify="start", gap=1)
    return (seesaw_pos,)


@app.cell
def _(COLORS, get_plotly_config, go, mo, np, seesaw_pos):
    def seesaw_figure(d2):
        d1 = 2.0  # left block fixed 2 m from pivot
        w1 = w2 = 1.0  # equal-weight blocks

        left_moment = w1 * d1
        right_moment = w2 * d2
        net = right_moment - left_moment  # >0 means right side sinks

        # Tilt the beam: clockwise (right sinks) for net > 0
        tilt = np.clip(-8.0 * net, -16, 16)
        phi = np.radians(tilt)
        length = 4.0

        def rotate(x):
            return x * np.cos(phi), x * np.sin(phi)

        lx, ly = rotate(-d1)
        rx, ry = rotate(d2)
        beam_lx, beam_ly = rotate(-length)
        beam_rx, beam_ry = rotate(length)

        fig = go.Figure()

        # Pivot (triangle)
        fig.add_trace(
            go.Scatter(
                x=[-0.4, 0.4, 0],
                y=[-0.8, -0.8, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(160,160,160,0.5)",
                line={"color": COLORS["text_secondary"], "width": 2},
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Beam
        fig.add_trace(
            go.Scatter(
                x=[beam_lx, beam_rx],
                y=[beam_ly, beam_ry],
                mode="lines",
                line={"color": COLORS["primary"], "width": 8},
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Blocks
        fig.add_trace(
            go.Scatter(
                x=[lx],
                y=[ly + 0.25],
                mode="markers",
                marker={"size": 26, "color": COLORS["gravity"], "symbol": "square"},
                name=f"Left block  (d₁ = {d1:.1f} m)",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[rx],
                y=[ry + 0.25],
                mode="markers",
                marker={"size": 26, "color": COLORS["tertiary"], "symbol": "square"},
                name=f"Right block  (d₂ = {d2:.1f} m)",
            )
        )

        if abs(net) < 0.05:
            verdict = "BALANCED  —  W·d₁ = W·d₂"
            vcolor = COLORS["wave"]
        elif net > 0:
            verdict = "Right side sinks  —  its lever arm is longer"
            vcolor = COLORS["secondary"]
        else:
            verdict = "Left side sinks  —  its lever arm is longer"
            vcolor = COLORS["secondary"]

        fig.update_layout(
            title={
                "text": f"<b>The Seesaw: Balancing Moments</b><br>"
                f"<sub>left moment = {left_moment:.1f}  |  right moment = {right_moment:.1f}  →  {verdict}</sub>"
            },
            xaxis={
                "range": [-4.5, 4.5],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "range": [-1.2, 2.2],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 0,
                    "y": 2.0,
                    "text": f"<b>{verdict}</b>",
                    "showarrow": False,
                    "font": {"color": vcolor, "size": 14},
                }
            ],
            height=480,
        )
        return fig

    seesaw_plot = mo.ui.plotly(seesaw_figure(seesaw_pos.value), config=get_plotly_config())
    mo.output.replace(seesaw_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 4. Constraints and reactions: how the world pushes back

        A structure only stands because something *holds it in place*. The floor stops the table
        from falling. A hinge stops the door from flying off. A bracket stops the shelf from
        rotating down. Each of these is a **constraint** — a connection that forbids some motion —
        and wherever a constraint forbids a motion, it does so by supplying a **reaction force**
        (or a reaction moment) exactly big enough to make the equilibrium equations balance.

        Engineers-in-spirit sort supports by *what they can push with*:

        - A **roller** (or a smooth floor) can only push **perpendicular** to the surface. It
          supplies one reaction — the normal force. Think of a can rolling on a table: the table
          holds it up but can't stop it rolling sideways.
        - A **pin** (a hinge, a bolt through a hole) can push in **any direction**, so it supplies
          two reactions (horizontal and vertical) — but it lets the piece *rotate* freely, so it
          supplies **no moment**. A door hinge is exactly this.
        - A **fixed** (built-in) support, like a beam cemented into a wall or a flagpole in the
          ground, forbids *everything*: it supplies two reaction forces **and** a reaction moment.

        Knowing which reactions a support can provide is how you figure out whether a structure is
        even *solvable* — and where the loads actually go. Here's the cleanest example: a beam
        resting on two supports with a load somewhere in the middle. The two upward reactions must
        (a) add up to the load, and (b) balance its moment. Put the load right over one support and
        that support takes nearly all of it. The math is pure lever again:

        $$R_{\text{left}} = W\,\frac{L - a}{L}, \qquad R_{\text{right}} = W\,\frac{a}{L}$$

        *Slide the load along the beam and watch the reactions hand the weight back and forth.*
        """
    )
    return


@app.cell
def _(mo):
    load_pos = mo.ui.slider(
        start=0.5,
        stop=5.5,
        step=0.1,
        value=2.0,
        label="Load position a (m from left support)",
        show_value=True,
    )
    mo.hstack([mo.md("**Move the load:**"), load_pos], justify="start", gap=1)
    return (load_pos,)


@app.cell
def _(COLORS, get_plotly_config, go, mo, load_pos):
    def beam_reactions_figure(a):
        span = 6.0
        load = 10.0  # kN
        r_left = load * (span - a) / span
        r_right = load * a / span

        fig = go.Figure()

        # Beam
        fig.add_trace(
            go.Scatter(
                x=[0, span],
                y=[0, 0],
                mode="lines",
                line={"color": COLORS["primary"], "width": 10},
                name="Beam",
                hoverinfo="skip",
            )
        )
        # Supports (triangles) at the ends
        for sx in (0.0, span):
            fig.add_trace(
                go.Scatter(
                    x=[sx - 0.3, sx + 0.3, sx],
                    y=[-0.9, -0.9, 0],
                    mode="lines",
                    fill="toself",
                    fillcolor="rgba(160,160,160,0.5)",
                    line={"color": COLORS["text_secondary"], "width": 2},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        annotations = [
            # Load arrow (down)
            {
                "x": a,
                "y": 0.05,
                "ax": a,
                "ay": 1.2 + load * 0.06,
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "showarrow": True,
                "arrowhead": 2,
                "arrowsize": 1.3,
                "arrowwidth": 4,
                "arrowcolor": COLORS["gravity"],
            },
            {
                "x": a,
                "y": 1.35 + load * 0.06,
                "text": f"<b>Load = {load:.0f} kN</b>",
                "showarrow": False,
                "font": {"color": COLORS["gravity"], "size": 13},
            },
            # Left reaction (up)
            {
                "x": 0,
                "y": -0.05,
                "ax": 0,
                "ay": -0.05 - r_left * 0.08,
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "showarrow": True,
                "arrowhead": 2,
                "arrowsize": 1.3,
                "arrowwidth": 4,
                "arrowcolor": COLORS["wave"],
            },
            {
                "x": 0,
                "y": -0.25 - r_left * 0.08,
                "text": f"R_left = {r_left:.1f} kN",
                "showarrow": False,
                "font": {"color": COLORS["wave"], "size": 12},
            },
            # Right reaction (up)
            {
                "x": span,
                "y": -0.05,
                "ax": span,
                "ay": -0.05 - r_right * 0.08,
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "showarrow": True,
                "arrowhead": 2,
                "arrowsize": 1.3,
                "arrowwidth": 4,
                "arrowcolor": COLORS["wave"],
            },
            {
                "x": span,
                "y": -0.25 - r_right * 0.08,
                "text": f"R_right = {r_right:.1f} kN",
                "showarrow": False,
                "font": {"color": COLORS["wave"], "size": 12},
            },
        ]

        fig.update_layout(
            title={
                "text": "<b>A Simply Supported Beam</b><br>"
                "<sub>The two reactions always add up to the load: R_left + R_right = 10 kN</sub>"
            },
            xaxis={
                "range": [-1, span + 1],
                "showgrid": False,
                "zeroline": False,
                "title": "position along beam (m)",
            },
            yaxis={
                "range": [-1.6, 2.6],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            annotations=annotations,
            showlegend=False,
            height=480,
        )
        return fig

    beam_plot = mo.ui.plotly(beam_reactions_figure(load_pos.value), config=get_plotly_config())
    mo.output.replace(beam_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 5. Friction: the sideways force we couldn't live without

        Every force so far was tidy and obvious. Friction is the messy, indispensable one. It's the
        sideways grip between two touching surfaces, and it does two opposite-seeming jobs: it lets
        you *walk* (your shoe pushes back on the floor, the floor pushes you forward) and it *stops*
        boxes from sliding when you'd rather they didn't.

        The rule of thumb — good enough for almost everything — is that the friction force can grow
        only up to a limit set by how hard the surfaces are pressed together:

        $$f \le \mu\,N$$

        Here $N$ is the normal force squeezing the surfaces and $\mu$ (mu) is the **coefficient of
        friction**, a number that depends on the *pair* of materials. Two surprising facts, both of
        which Feynman highlights in his
        [chapter on force](https://www.feynmanlectures.caltech.edu/I_12.html#Ch12-S2):

        1. To a good approximation, friction **doesn't depend on the contact area**. A brick slides
           just as easily on its big face as on its small one, because spreading the weight over
           more area lowers the pressure in exactly the compensating amount.
        2. **Static friction** (before sliding starts) is usually a bit *stronger* than **kinetic
           friction** (once it's moving). That's why a heavy box lurches: it resists, then suddenly
           gives and slides.

        A block sits on a slope that you slowly tilt. Gravity's pull *along* the slope is
        $mg\sin\theta$, trying to slide it down. The most friction can offer back is
        $\mu\,mg\cos\theta$. The block breaks free the instant the first beats the second — and if
        you set them equal, the mass cancels completely:

        $$\tan\theta_{\text{slip}} = \mu$$

        So the angle at which things start to slide tells you $\mu$ directly, and it doesn't matter
        whether the block is heavy or light. *Pick a pair of materials, tilt the slope, and find the
        angle where it lets go.*
        """
    )
    return


@app.cell
def _(mo):
    material_pair = mo.ui.dropdown(
        options={
            "Rubber on dry concrete  (μ ≈ 1.0)": 1.0,
            "Steel on steel, dry  (μ ≈ 0.6)": 0.6,
            "Steel on ice  (μ ≈ 0.4)": 0.4,
            "Ice on ice  (μ ≈ 0.1)": 0.1,
            "PTFE (Teflon) on steel  (μ ≈ 0.04)": 0.04,
        },
        value="Steel on steel, dry  (μ ≈ 0.6)",
        label="Surface pair",
    )
    incline_angle = mo.ui.slider(
        start=0,
        stop=50,
        step=1,
        value=15,
        label="Slope angle θ (degrees)",
        show_value=True,
    )
    mo.vstack(
        [
            mo.hstack([mo.md("**Material pair:**"), material_pair], justify="start", gap=1),
            mo.hstack([mo.md("**Tilt the slope:**"), incline_angle], justify="start", gap=1),
        ]
    )
    return incline_angle, material_pair


@app.cell
def _(COLORS, get_plotly_config, go, incline_angle, material_pair, mo, np):
    def incline_figure(theta_deg, mu):
        theta = np.radians(theta_deg)
        base = 3.0
        height = base * np.tan(theta)

        slips = np.tan(theta) > mu
        block_color = COLORS["secondary"] if slips else COLORS["wave"]

        fig = go.Figure()

        # The wedge (incline)
        fig.add_trace(
            go.Scatter(
                x=[0, base, 0, 0],
                y=[0, 0, height, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(120,120,140,0.35)",
                line={"color": COLORS["text_secondary"], "width": 2},
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # Block sitting on the slope, partway up
        along = 1.6
        bx = base - along * np.cos(theta)
        by = height - along * np.sin(theta) if theta_deg > 0 else 0.0
        # offset the block slightly above the surface (perpendicular)
        nx, ny = -np.sin(theta), np.cos(theta)
        size = 0.35
        cx, cy = bx + nx * size, by + ny * size
        # corners of a small square aligned with the slope
        ux, uy = np.cos(theta), np.sin(theta)
        corners_x = [
            cx + s1 * ux * size + s2 * nx * size for s1, s2 in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        ]
        corners_y = [
            cy + s1 * uy * size + s2 * ny * size for s1, s2 in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        ]
        corners_x.append(corners_x[0])
        corners_y.append(corners_y[0])
        fig.add_trace(
            go.Scatter(
                x=corners_x,
                y=corners_y,
                mode="lines",
                fill="toself",
                fillcolor=block_color,
                line={"color": block_color, "width": 2},
                name="Block",
                hoverinfo="skip",
            )
        )

        pull = np.sin(theta)  # mg sinθ per unit mg
        grip = mu * np.cos(theta)  # μ mg cosθ per unit mg
        verdict = "SLIPS!" if slips else "holds"
        fig.update_layout(
            title={
                "text": f"<b>Block on a Slope</b><br>"
                f"<sub>tan θ = {np.tan(theta):.2f}   vs   μ = {mu:.2f}   →   the block {verdict}</sub>"
            },
            xaxis={
                "range": [-0.5, 3.5],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "range": [-0.5, 3.2],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 1.6,
                    "y": 2.9,
                    "text": f"pull down-slope ∝ sin θ = {pull:.2f}<br>max friction ∝ μ cos θ = {grip:.2f}",
                    "showarrow": False,
                    "font": {"color": COLORS["text"], "size": 12},
                    "align": "left",
                }
            ],
            showlegend=False,
            height=500,
        )
        return fig

    incline_plot = mo.ui.plotly(
        incline_figure(incline_angle.value, material_pair.value), config=get_plotly_config()
    )
    mo.output.replace(incline_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Real friction numbers

        The coefficient $\mu$ is not something you derive — it's *measured*, for each pair of
        surfaces, and it varies with roughness, cleanliness, temperature and moisture. Still, the
        typical values below (static friction, dry unless noted) are worth carrying in your head.
        Notice the enormous range: rubber grips concrete more than *twenty times* better than
        Teflon grips steel. That single fact is why tyres are rubber and why non-stick pans are
        coated with PTFE. Values compiled from
        [The Engineering ToolBox](https://www.engineeringtoolbox.com/friction-coefficients-d_778.html)
        and [RoyMech](https://www.roymech.co.uk/Useful_Tables/Tribology/co_of_frict.htm).
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo):
    def friction_bar_chart():
        pairs = [
            ("PTFE on steel", 0.04),
            ("Ice on ice", 0.10),
            ("Steel on ice", 0.40),
            ("Wood on wood", 0.45),
            ("Steel on steel (dry)", 0.60),
            ("Rubber on wet concrete", 0.70),
            ("Rubber on dry concrete", 1.00),
        ]
        names = [p[0] for p in pairs]
        values = [p[1] for p in pairs]

        fig = go.Figure(
            go.Bar(
                x=values,
                y=names,
                orientation="h",
                marker={"color": values, "colorscale": "Viridis", "showscale": False},
                text=[f"{v:.2f}" for v in values],
                textposition="outside",
            )
        )
        fig.update_layout(
            title={
                "text": "<b>Coefficient of Static Friction, μ</b><br><sub>slippery ↔ grippy (dry unless noted)</sub>"
            },
            xaxis={"title": "μ (dimensionless)", "range": [0, 1.15]},
            yaxis={"title": ""},
            height=460,
            font={"color": COLORS["text"]},
        )
        return fig

    friction_plot = mo.ui.plotly(friction_bar_chart(), config=get_plotly_config())
    mo.output.replace(friction_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 6. Stress and strain: what a force feels like *inside*

        Up to now we've drawn forces as arrows *on* objects. But to know whether a thing **breaks**,
        we have to go inside it and ask what each little piece of material is putting up with. Two
        ideas do all the work:

        - **Stress** is force spread over area: $\sigma = F/A$. It's really just *pressure inside a
          solid*, measured in pascals (Pa = N/m², usually megapascals, MPa). Pulling a thin wire and
          a thick rope with the same force, the thin wire is under far more stress — which is why it
          snaps first. Stress, not force, is what a material actually feels.
        - **Strain** is how much the material stretches, as a *fraction* of its length:
          $\varepsilon = \Delta L / L$. A 1-metre bar that stretches by 1 mm is at a strain of
          $0.001$. Strain has no units — it's a stretch compared to the original size.

        For most solids, over the everyday range, stress and strain are simply **proportional** —
        this is Hooke's law, written for materials:

        $$\sigma = E\,\varepsilon$$

        The constant $E$ is the **Young's modulus**, the material's *stiffness*: how much stress it
        takes to stretch it by a given fraction. A big $E$ means a stiff material that barely gives;
        a small $E$ means a floppy one. Steel's $E$ is about **200 GPa**; rubber's is a few
        *hundred-thousandths* of that, which is exactly why a rubber band stretches to twice its
        length while a steel wire of the same size barely moves. Feynman devotes a whole chapter to
        this, [Elasticity](https://www.feynmanlectures.caltech.edu/II_38.html).

        Push too far and the straight-line law ends. Past the **yield point** a metal deforms
        *permanently* (bend a paperclip and it stays bent); push further still and it reaches its
        **ultimate strength** and breaks. The plot shows the tell-tale opening slope for steel,
        aluminium and wood: **the steeper the line, the stiffer the material.** (Rubber's line would
        be almost flat along the floor of this chart — it's off the scale here.)
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo, np):
    def stress_strain_figure():
        # Elastic slopes use real Young's moduli (converted to MPa: 1 GPa = 1000 MPa)
        materials = [
            # name, E (GPa), yield stress (MPa), color
            ("Steel  (E ≈ 200 GPa)", 200, 250, COLORS["primary"]),
            ("Aluminium  (E ≈ 69 GPa)", 69, 275, COLORS["tertiary"]),
            ("Oak wood  (E ≈ 11 GPa)", 11, 40, COLORS["gravity"]),
        ]

        fig = go.Figure()
        for name, e_gpa, yield_mpa, color in materials:
            e_mpa = e_gpa * 1000.0
            strain_yield = yield_mpa / e_mpa
            strain = np.linspace(0, strain_yield, 40)
            stress = e_mpa * strain
            fig.add_trace(
                go.Scatter(
                    x=strain * 100,  # percent
                    y=stress,
                    mode="lines",
                    line={"color": color, "width": 4},
                    name=name,
                )
            )
            # Mark the yield point
            fig.add_trace(
                go.Scatter(
                    x=[strain_yield * 100],
                    y=[yield_mpa],
                    mode="markers",
                    marker={"color": color, "size": 11, "symbol": "x"},
                    showlegend=False,
                    hovertemplate=f"{name}<br>yield ≈ {yield_mpa} MPa<extra></extra>",
                )
            )

        fig.update_layout(
            title={
                "text": "<b>Stress–Strain: the Slope is Stiffness</b><br><sub>steeper line = stiffer material; × marks where it stops springing back</sub>"
            },
            xaxis={"title": "strain ε (%)", "range": [0, 0.45]},
            yaxis={"title": "stress σ (MPa)", "range": [0, 300]},
            height=520,
        )
        return fig

    stress_strain_plot = mo.ui.plotly(stress_strain_figure(), config=get_plotly_config())
    mo.output.replace(stress_strain_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 7. The everyday materials, compared honestly

        Now we can put the common building materials side by side and see *why* we reach for each
        one. Two numbers tell most of the story: **stiffness** ($E$, how much it resists stretching)
        and **density** ($\rho$, how heavy it is for its size). Their values below are standard
        reference figures from
        [The Engineering ToolBox](https://www.engineeringtoolbox.com/young-modulus-d_417.html)
        and matched material tables:

        | Material | Young's modulus $E$ (GPa) | Density $\rho$ (kg/m³) | Character |
        |---|---|---|---|
        | **Steel** | ~200 | 7850 | Very stiff and strong, but heavy |
        | **Aluminium** | ~69 | 2700 | A third as stiff as steel, a third the weight |
        | **Titanium** | ~116 | 4500 | Stiff *and* light — and expensive |
        | **Glass** | ~70 | 2500 | Stiff but brittle — no yielding, it just cracks |
        | **Concrete** | ~30 | 2400 | Great in *compression*, weak in *tension* |
        | **Oak wood** | ~11 | ~700 | Surprisingly good stiffness for its weight |
        | **Rubber** | ~0.01–0.1 | ~1100 | Barely stiff at all — it's for stretch and grip |

        Here's the subtlety that beginners miss: **steel and aluminium are almost equally good per
        kilogram.** Aluminium is one-third as stiff, but also one-third as heavy, so a chunk of
        aluminium and a chunk of steel of the *same weight* are about equally stiff. What you choose
        depends on whether you're short on *space* (use stiff, dense steel) or short on *weight*
        (use aluminium and make the part bigger). The chart below plots stiffness against density;
        the diagonal guide lines are lines of equal **stiffness-per-weight** ($E/\rho$).
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo, np):
    def material_chart():
        # name, E (GPa), density (kg/m3), color
        materials = [
            ("Steel", 200, 7850, COLORS["primary"]),
            ("Aluminium", 69, 2700, COLORS["tertiary"]),
            ("Titanium", 116, 4500, COLORS["accent1"]),
            ("Glass", 70, 2500, COLORS["quaternary"]),
            ("Concrete", 30, 2400, COLORS["text_secondary"]),
            ("Oak wood", 11, 700, COLORS["gravity"]),
            ("Rubber", 0.05, 1100, COLORS["particle"]),
        ]

        fig = go.Figure()

        # Guide lines of constant E/rho (specific stiffness)
        rho_line = np.array([500, 9000])
        for k in (0.01, 0.04):  # low and high specific stiffness
            fig.add_trace(
                go.Scatter(
                    x=rho_line,
                    y=k * rho_line / 1000.0,  # GPa
                    mode="lines",
                    line={"color": "rgba(160,160,160,0.35)", "width": 1, "dash": "dot"},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        for name, e_gpa, rho, color in materials:
            fig.add_trace(
                go.Scatter(
                    x=[rho],
                    y=[e_gpa],
                    mode="markers+text",
                    marker={"size": 18, "color": color, "line": {"color": "white", "width": 1}},
                    text=[name],
                    textposition="top center",
                    textfont={"size": 12, "color": COLORS["text"]},
                    name=name,
                    showlegend=False,
                    hovertemplate=f"<b>{name}</b><br>E = {e_gpa} GPa<br>ρ = {rho} kg/m³<extra></extra>",
                )
            )

        fig.update_layout(
            title={
                "text": "<b>Stiffness vs. Weight of Everyday Materials</b><br><sub>log–log; dotted lines = equal stiffness-per-weight</sub>"
            },
            xaxis={
                "title": "density ρ (kg/m³)",
                "type": "log",
                "range": [np.log10(400), np.log10(10000)],
            },
            yaxis={
                "title": "Young's modulus E (GPa)",
                "type": "log",
                "range": [np.log10(0.02), np.log10(400)],
            },
            height=560,
        )
        return fig

    material_plot = mo.ui.plotly(material_chart(), config=get_plotly_config())
    mo.output.replace(material_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 8. Beams: why *shape* beats *material*

        Here is the most useful single idea for anyone looking at a structure. When a beam carries a
        load across a gap, it **bends**, and bending does something clever: the top surface gets
        squeezed (**compression**) while the bottom surface gets stretched (**tension**). Somewhere
        in between is a layer that feels neither — the **neutral axis**. The material near the
        neutral axis is basically along for the ride; it's the material *far* from it, top and
        bottom, that does the real work of resisting the bend.

        That's why how much a beam resists bending is measured not by its area but by how its area
        is *distributed* away from the neutral axis — a quantity called the **second moment of area**,
        $I$. For a solid rectangle of width $b$ and depth $h$ (depth measured in the direction of the
        bending):

        $$I = \frac{b\,h^3}{12}$$

        Look hard at that $h^3$. **Depth matters cubed.** Make a beam twice as deep — keeping its
        width — and it becomes *eight times* stiffer against bending (that costs twice the material).
        But even for the *same amount of material*, re-shaping counts enormously: a wooden plank is
        floppy laid flat and rigid stood on its edge. Turning a plank of width $b$ and thickness $h$
        up onto its edge swaps the roles of $b$ and $h$, multiplying its stiffness by $(b/h)^2$ —
        for a typical 1-by-4 plank that's more than *ten times* stiffer, with not one extra gram of
        wood. It's the same material, simply moved away from the neutral axis. The actual sag under a
        central load follows

        $$\delta = \frac{F L^3}{48\,E\,I}$$

        so stiffness comes from three levers: the material ($E$), the shape ($I$), and — enormously
        — the span ($L^3$; a beam twice as long sags *eight times* as much). *Rotate the same
        cross-section from flat to upright and watch $I$, and the sag, transform.*
        """
    )
    return


@app.cell
def _(mo):
    beam_depth = mo.ui.slider(
        start=1.0,
        stop=6.0,
        step=0.25,
        value=1.5,
        label="Depth h of the cross-section (width b adjusts to keep area fixed)",
        show_value=True,
    )
    mo.hstack([mo.md("**Stand the plank on its edge:**"), beam_depth], justify="start", gap=1)
    return (beam_depth,)


@app.cell
def _(COLORS, get_plotly_config, go, mo, beam_depth):
    def beam_shape_figure(h):
        area = 6.0  # fixed cross-sectional area (same amount of material)
        b = area / h
        second_moment = b * h**3 / 12.0
        # deflection relative to a reference (h=1 case) — smaller I means more sag
        ref_i = area * 1.0**3 / 12.0
        rel_sag = ref_i / second_moment  # =1 at h=1, shrinks as h grows

        fig = go.Figure()

        # Cross-section rectangle centered at (1.5, 3), drawn to scale
        cx, cy = 1.5, 3.0
        scale = 0.5
        x0, x1 = cx - b * scale / 2, cx + b * scale / 2
        y0, y1 = cy - h * scale / 2, cy + h * scale / 2
        fig.add_trace(
            go.Scatter(
                x=[x0, x1, x1, x0, x0],
                y=[y0, y0, y1, y1, y0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 212, 255, 0.3)",
                line={"color": COLORS["primary"], "width": 2},
                name="cross-section",
                hoverinfo="skip",
            )
        )
        # Neutral axis
        fig.add_trace(
            go.Scatter(
                x=[x0 - 0.3, x1 + 0.3],
                y=[cy, cy],
                mode="lines",
                line={"color": COLORS["secondary"], "width": 2, "dash": "dash"},
                name="neutral axis",
                hoverinfo="skip",
            )
        )

        # A little sagging beam underneath, sag proportional to rel_sag
        beam_x = [4.0, 5.0, 6.0, 7.0, 8.0]
        sag = rel_sag
        beam_y = [3.5, 3.5 - 0.25 * sag, 3.5 - 0.4 * sag, 3.5 - 0.25 * sag, 3.5]
        fig.add_trace(
            go.Scatter(
                x=beam_x,
                y=beam_y,
                mode="lines",
                line={"color": COLORS["tertiary"], "width": 6},
                name="how much it sags",
                hoverinfo="skip",
            )
        )
        # supports for the little beam
        for sx in (4.0, 8.0):
            fig.add_trace(
                go.Scatter(
                    x=[sx - 0.2, sx + 0.2, sx],
                    y=[3.2, 3.2, 3.5],
                    mode="lines",
                    fill="toself",
                    fillcolor="rgba(160,160,160,0.5)",
                    line={"color": COLORS["text_secondary"], "width": 1},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        fig.update_layout(
            title={
                "text": f"<b>Same Material, Different Depth</b><br>"
                f"<sub>b = {b:.2f}, h = {h:.2f}  →  I = b·h³/12 = {second_moment:.2f}  "
                f"→  sag is {rel_sag:.2f}× the flat case</sub>"
            },
            xaxis={"range": [0, 9], "showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={
                "range": [1.5, 5],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 1.5,
                    "y": 4.6,
                    "text": "cross-section",
                    "showarrow": False,
                    "font": {"color": COLORS["primary"], "size": 12},
                },
                {
                    "x": 6.0,
                    "y": 4.6,
                    "text": "the beam's sag",
                    "showarrow": False,
                    "font": {"color": COLORS["tertiary"], "size": 12},
                },
            ],
            height=520,
        )
        return fig

    beam_shape_plot = mo.ui.plotly(beam_shape_figure(beam_depth.value), config=get_plotly_config())
    mo.output.replace(beam_shape_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The trick behind the I-beam

        If material near the neutral axis is barely working, why carry it at all? That's the whole
        idea of the **I-shaped beam**: put big slabs of material (the *flanges*) at the top and
        bottom where the stress is highest, and connect them with a thin *web* just strong enough to
        hold them apart. You get almost all the bending stiffness of a solid block for a small
        fraction of the material and weight.

        The figure compares an I-section with a solid square of the **same cross-sectional area** —
        the same amount of material. Because the I-section's area lives far from the neutral axis,
        its second moment of area $I$ is dramatically larger, and so is its resistance to bending.
        Shape, not more metal, is doing the work.
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo):
    def ibeam_comparison():
        fig = go.Figure()

        # --- I-beam geometry (drawn between y=1 and y=3, neutral axis at y=2) ---
        ox = 5.5
        flange_w, flange_t, web_w = 2.0, 0.35, 0.4
        web_h = 2.0 - 2 * flange_t  # keep the whole section exactly 2 units tall
        area_ibeam = 2 * (flange_w * flange_t) + web_w * web_h

        # --- Solid square (left), sized to the SAME area as the I-beam ---
        side = area_ibeam**0.5
        cx, cy = 1.5, 2.0
        half = side / 2
        sq = [
            (cx - half, cy - half),
            (cx + half, cy - half),
            (cx + half, cy + half),
            (cx - half, cy + half),
            (cx - half, cy - half),
        ]
        fig.add_trace(
            go.Scatter(
                x=[p[0] for p in sq],
                y=[p[1] for p in sq],
                mode="lines",
                fill="toself",
                fillcolor="rgba(160,160,160,0.4)",
                line={"color": COLORS["text_secondary"], "width": 2},
                name="Solid bar",
                hoverinfo="skip",
            )
        )
        i_square = side**4 / 12  # b·h³/12 for a square of this side

        fw, ww = flange_w / 2, web_w / 2
        top = [
            (ox - fw, 3.0),
            (ox + fw, 3.0),
            (ox + fw, 3.0 - flange_t),
            (ox + ww, 3.0 - flange_t),
            (ox + ww, 1.0 + flange_t),
            (ox + fw, 1.0 + flange_t),
            (ox + fw, 1.0),
            (ox - fw, 1.0),
            (ox - fw, 1.0 + flange_t),
            (ox - ww, 1.0 + flange_t),
            (ox - ww, 3.0 - flange_t),
            (ox - fw, 3.0 - flange_t),
            (ox - fw, 3.0),
        ]
        fig.add_trace(
            go.Scatter(
                x=[p[0] for p in top],
                y=[p[1] for p in top],
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 212, 255, 0.3)",
                line={"color": COLORS["primary"], "width": 2},
                name="I-beam",
                hoverinfo="skip",
            )
        )
        # Second moment of area about the neutral axis (parallel-axis theorem)
        d = web_h / 2 + flange_t / 2  # flange centroid to neutral axis
        i_beam = (
            2 * (flange_w * flange_t**3 / 12 + flange_w * flange_t * d**2) + web_w * web_h**3 / 12
        )

        # Neutral axes
        for cx in (1.5, ox):
            fig.add_trace(
                go.Scatter(
                    x=[cx - 1.9, cx + 1.9],
                    y=[2, 2],
                    mode="lines",
                    line={"color": COLORS["secondary"], "width": 1.5, "dash": "dash"},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        fig.update_layout(
            title={
                "text": "<b>Same Material, Smarter Shape</b><br><sub>put the metal where the stress is — far from the neutral axis</sub>"
            },
            xaxis={
                "range": [-0.5, 8],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "range": [0, 4],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 1.5,
                    "y": 0.6,
                    "text": f"solid bar<br>I ≈ {i_square:.1f}",
                    "showarrow": False,
                    "font": {"color": COLORS["text_secondary"], "size": 12},
                },
                {
                    "x": ox,
                    "y": 0.6,
                    "text": f"I-beam (same area)<br>I ≈ {i_beam:.1f}",
                    "showarrow": False,
                    "font": {"color": COLORS["primary"], "size": 12},
                },
            ],
            showlegend=False,
            height=460,
        )
        return fig

    ibeam_plot = mo.ui.plotly(ibeam_comparison(), config=get_plotly_config())
    mo.output.replace(ibeam_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 9. Stress concentration: where a shape secretly breaks first

        A structure rarely fails in the calm, average place. It fails at a **corner, a hole, a
        notch, a scratch** — anywhere the smooth flow of stress is forced to swerve. Picture the
        internal stress as flowing lines, like water streaming through the material. Where the
        material is uninterrupted the flow is even. Put a hole in the way and the flow lines have to
        crowd around it — and where they crowd, the stress spikes far above the average.

        For the cleanest case — a small round hole in a wide plate that's being pulled — the answer
        has been known since **Kirsch worked it out in 1898**: the stress right at the edge of the
        hole, on the sides square to the pull, is exactly **three times** the average stress far
        away. This "factor of three" is famous, and remarkably it doesn't depend on the material at
        all — steel, glass or plastic, the geometry alone triples the stress. (See
        [fracturemechanics.org](https://www.fracturemechanics.org/hole.html) for the full solution.)

        This is why holes get reinforced, why corners get rounded into fillets, and why a tiny
        scratch on glass or a nick on the edge of a phone screen is where the crack begins. A sharp
        corner is even worse than a round hole — the sharper the notch, the higher the spike. The
        heatmap shows the stress around a hole in a plate pulled left-and-right: cool where the flow
        is undisturbed, blazing at the top and bottom edges of the hole where it triples.
        """
    )
    return


@app.cell
def _(get_plotly_config, go, mo, np):
    def stress_concentration_figure():
        # Kirsch solution: uniaxial tension S along x, hole radius a at origin.
        # Hoop stress at the hole edge peaks at 3S on the sides (top/bottom, θ = ±90°).
        s = 1.0
        a = 1.0
        grid = np.linspace(-4, 4, 220)
        gx, gy = np.meshgrid(grid, grid)
        r = np.sqrt(gx**2 + gy**2)
        # Avoid r = 0 (and inside the hole) before dividing — no RuntimeWarnings
        r_safe = np.where(r < a, a, r)
        theta = np.arctan2(gy, gx)

        a2 = (a / r_safe) ** 2
        a4 = (a / r_safe) ** 4
        # Hoop (tangential) stress from the Kirsch solution
        sigma_tt = (s / 2) * (1 + a2) - (s / 2) * (1 + 3 * a4) * np.cos(2 * theta)
        # Blank out the hole itself
        sigma_tt = np.where(r < a, np.nan, sigma_tt)

        fig = go.Figure(
            go.Heatmap(
                x=grid,
                y=grid,
                z=sigma_tt,
                colorscale="Inferno",
                zmin=-1,
                zmax=3,
                colorbar={"title": "stress ÷ average"},
            )
        )
        # Outline the hole
        circle_t = np.linspace(0, 2 * np.pi, 100)
        fig.add_trace(
            go.Scatter(
                x=a * np.cos(circle_t),
                y=a * np.sin(circle_t),
                mode="lines",
                line={"color": "white", "width": 2},
                showlegend=False,
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            title={
                "text": "<b>Stress Around a Hole (pulled ← →)</b><br><sub>peaks at 3× the average at the top & bottom of the hole — Kirsch, 1898</sub>"
            },
            xaxis={"title": "", "showticklabels": False, "scaleanchor": "y"},
            yaxis={"title": "", "showticklabels": False},
            annotations=[
                {
                    "x": 0,
                    "y": 1.5,
                    "text": "3× here",
                    "showarrow": True,
                    "arrowhead": 2,
                    "arrowcolor": "white",
                    "font": {"color": "white", "size": 12},
                    "ax": 0,
                    "ay": 40,
                },
                {
                    "x": 0,
                    "y": -1.5,
                    "text": "3× here",
                    "showarrow": True,
                    "arrowhead": 2,
                    "arrowcolor": "white",
                    "font": {"color": "white", "size": 12},
                    "ax": 0,
                    "ay": -40,
                },
            ],
            height=560,
        )
        return fig

    stress_conc_plot = mo.ui.plotly(stress_concentration_figure(), config=get_plotly_config())
    mo.output.replace(stress_conc_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 10. Buckling: why long thin things fold instead of crush

        There's one last way to fail that has nothing to do with running out of strength. Take a
        strand of dry spaghetti, or a plastic ruler, and push on its ends. It doesn't crush — long
        before that, it suddenly bows sideways and snaps. This is **buckling**, and it's a
        *stability* failure: past a certain load the straight shape stops being the stable one, and
        the column leaps sideways into a bent shape.

        Euler found the load at which this happens, and it's a beautiful formula because of what's
        *in* it and what's *not*:

        $$P_{\text{crit}} = \frac{\pi^2 E I}{L^2}$$

        The critical load depends on the material stiffness $E$, the cross-section shape $I$ (that
        same second moment of area from the beam section), and — punishingly — the **square of the
        length**. It does *not* depend on how strong the material is. That's the whole surprise:
        a long slender column fails at a load far below what would crush it, and doubling its length
        quarters the load it can take. This is why tall thin things need to be either fat, braced
        partway up, or made of something stiff — and why you can't push a rope, or stand a long
        noodle on end. *The curve shows how the safe load collapses as a column gets longer; drag
        to see a column of a given length bow out once it's overloaded.*
        """
    )
    return


@app.cell
def _(mo):
    column_len = mo.ui.slider(
        start=1.0,
        stop=5.0,
        step=0.25,
        value=2.5,
        label="Column length L (m)",
        show_value=True,
    )
    mo.hstack([mo.md("**Lengthen the column:**"), column_len], justify="start", gap=1)
    return (column_len,)


@app.cell
def _(COLORS, create_play_pause_buttons, get_plotly_config, go, mo, np, column_len):
    def buckling_figure(length):
        # Fixed E*I; critical load falls as 1/L^2
        ei = 20.0
        lengths = np.linspace(1.0, 5.0, 100)
        p_crit_curve = np.pi**2 * ei / lengths**2
        this_pcrit = np.pi**2 * ei / length**2

        # Left panel data: the curve. Right panel: an animated buckling column.
        fig = go.Figure()

        # The P_crit vs L curve (plotted in x from 0..5, its own axis on left)
        fig.add_trace(
            go.Scatter(
                x=lengths,
                y=p_crit_curve,
                mode="lines",
                line={"color": COLORS["primary"], "width": 4},
                name="critical load",
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[length],
                y=[this_pcrit],
                mode="markers",
                marker={"color": COLORS["secondary"], "size": 16},
                name=f"L = {length:.2f} m",
                hovertemplate=f"L = {length:.2f} m<br>P_crit = {this_pcrit:.1f}<extra></extra>",
            )
        )

        # Animated buckling column drawn to the right (x shifted to 6..8 region)
        n_frames = 30
        base_x = 7.0
        y_col = np.linspace(0, this_pcrit, 60)  # height scaled to the load axis for shared view
        y_norm = np.linspace(0, 1, 60)
        frames = []
        for k in range(n_frames):
            amp = 0.9 * (k / (n_frames - 1))
            bow = amp * np.sin(np.pi * y_norm)
            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(x=lengths, y=p_crit_curve),
                        go.Scatter(x=[length], y=[this_pcrit]),
                        go.Scatter(
                            x=base_x + bow,
                            y=y_col,
                            mode="lines",
                            line={"color": COLORS["gravity"], "width": 8},
                        ),
                    ],
                    name=str(k),
                )
            )

        # initial straight column
        fig.add_trace(
            go.Scatter(
                x=base_x + np.zeros_like(y_col),
                y=y_col,
                mode="lines",
                line={"color": COLORS["gravity"], "width": 8},
                name="column",
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            title={
                "text": "<b>Buckling: Safe Load Falls as 1/L²</b><br><sub>left: critical load vs length  •  right: the column bows out when overloaded (press Play)</sub>"
            },
            xaxis={"title": "length L (m)  /  column (right)", "range": [0.5, 8.5]},
            yaxis={"title": "critical load  P_crit", "range": [0, 22]},
            updatemenus=[
                {
                    "type": "buttons",
                    "showactive": False,
                    "y": 1.15,
                    "x": 0.5,
                    "xanchor": "center",
                    "buttons": create_play_pause_buttons(),
                    "bgcolor": COLORS["paper"],
                    "font": {"color": COLORS["text"]},
                }
            ],
            height=540,
        )
        fig.frames = frames
        return fig

    buckling_plot = mo.ui.plotly(buckling_figure(column_len.value), config=get_plotly_config())
    mo.output.replace(buckling_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "A checklist: what to look at in any structure": mo.md(
                r"""
        When you look at a shelf, a bracket, a bench, or a bridge, run down this list — it's just
        the ten ideas above, in order:

        1. **Draw the forces.** What's pushing or pulling on the piece? Gravity, applied loads,
           the pushes from whatever it touches. Draw every arrow (§1).
        2. **Check equilibrium.** Do the up/down and left/right forces cancel? If not, it's
           accelerating — i.e. moving or failing (§2).
        3. **Check the moments.** Do the turning effects cancel about every pivot? A shelf bracket
           that balances forces can still rotate off the wall if the moments don't close (§3).
        4. **Identify the supports.** What does each connection actually provide — a normal push, a
           pin, a full built-in fixing? That tells you where the load flows (§4).
        5. **Follow the friction.** Is anything relying on grip — a ladder foot, a clamped joint,
           a bolt? Grip has a ceiling, $f \le \mu N$ (§5).
        6. **Find the stress.** Force over area. The thin, small-area places carry the highest
           stress and yield first (§6).
        7. **Know the material.** Stiff or floppy ($E$), strong or weak, ductile (bends first, like
           steel) or brittle (cracks with no warning, like glass or concrete in tension) (§7).
        8. **Look at the cross-section.** Depth matters *cubed*. Is the material placed far from the
           neutral axis, where it does the work? (§8).
        9. **Hunt the stress raisers.** Holes, sharp corners, notches, scratches — the real cracks
           start there, at up to 3× the average stress or more (§9).
        10. **Watch for slender parts.** Anything long and thin under a push can buckle far below
            its crushing strength (§10).

        None of this needs heavy mathematics. It needs the *habit of looking* — and now you have it.
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

        ## Where to read more

        Every claim here is standard, checkable physics. The best next steps:

        - **Feynman Lectures, Vol. I, Ch. 12 — [Characteristics of Force](https://www.feynmanlectures.caltech.edu/I_12.html)**
          (forces, and the surprising rules of friction)
        - **Feynman Lectures, Vol. II, Ch. 38 — [Elasticity](https://www.feynmanlectures.caltech.edu/II_38.html)**
          (stress, strain, Young's modulus, bending and buckling)
        - **Feynman Lectures, Vol. II, Ch. 39 — [Elastic Materials](https://www.feynmanlectures.caltech.edu/II_39.html)**
          (how real materials respond in every direction)
        - **Material stiffness data — [The Engineering ToolBox: Young's Modulus](https://www.engineeringtoolbox.com/young-modulus-d_417.html)**
        - **Friction data — [The Engineering ToolBox: Friction Coefficients](https://www.engineeringtoolbox.com/friction-coefficients-d_778.html)**
        - **Stress concentration — [Fracture Mechanics: Stress Concentrations at Holes](https://www.fracturemechanics.org/hole.html)**

        And if you want the friendliest book ever written on why structures hold together, look up
        J. E. Gordon's *Structures: Or Why Things Don't Fall Down* — same spirit as this notebook,
        no equations required.
        """
    )
    return


if __name__ == "__main__":
    app.run()
