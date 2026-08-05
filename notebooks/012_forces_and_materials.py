import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    from physics.geometry import rotate2d
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
        make_subplots,
        mo,
        np,
        rotate2d,
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
        8. **Heat and thermal stress** — why a trapped material pushes back when it's warmed
        9. **Inside a beam** — reading the shear and bending along its length
        10. **Beams** — why *shape* beats *material*, and why a plank is stiff on its edge
        11. **Torsion** — twisting instead of bending, and why shafts are hollow
        12. **Stress concentration** — where a shape secretly breaks first
        13. **Fatigue** — how repeated loads snap things far below their strength
        14. **Buckling** — why a long thin thing folds instead of crushing
        15. **Factor of safety** — how much margin to leave, and why

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
def _(COLORS, get_plotly_config, go, mo, np, rotate2d, seesaw_pos):
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
            return rotate2d(x, 0.0, phi)

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

        It helps to sort supports by *what they can push back with*:

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

        ## 8. Heat and thermal stress: the force a trapped material makes

        There's one more property of a material that quietly causes an enormous amount of trouble:
        it changes size with temperature. Warm almost anything and it swells; cool it and it
        shrinks. The amount is set by the **coefficient of thermal expansion** $\alpha$ — the
        fractional stretch per degree:

        $$\frac{\Delta L}{L} = \alpha\,\Delta T$$

        The numbers are tiny (a few parts in a hundred-thousand per degree) but the *material
        matters*: aluminium expands about **twice as much as steel** for the same warming, and a
        special alloy called Invar barely expands at all. If the object is free to move, this is
        harmless — it just quietly gets a little bigger.

        The trouble starts when the material is **not free** — when it's clamped between two things
        that won't budge (a callback to the constraints of §4). Now it *wants* to expand but can't,
        and the constraint pushes back exactly hard enough to squash it back to size. That squeezing
        builds a real internal stress, and here's the startling part — it doesn't depend on the
        length at all:

        $$\sigma_{\text{thermal}} = E\,\alpha\,\Delta T$$

        A steel bar warmed by just $50°C$ and prevented from expanding develops about **120 MPa** of
        stress — roughly *half its yield strength* — from a temperature change you'd barely feel.
        This is why bridges sit on sliding **expansion joints** and why railway rails can buckle
        sideways in a heatwave. (One subtlety worth its own note: *heating* a trapped bar **squeezes**
        it — the stress is compression. To crack a brittle thing like glass you need *tension*, which
        is why it's a sudden *temperature difference* that does the damage: pour boiling water into a
        cold thick glass and the inner face expands while the cold outer face holds it back, putting
        that outer skin in tension until it splits.) *Pick a metal, turn up the temperature, and watch
        the compressive stress climb toward the yield point when the bar is held fast.*
        """
    )
    return


@app.cell
def _(mo):
    thermal_material = mo.ui.dropdown(
        options={
            "Aluminium  (α ≈ 23 ×10⁻⁶/°C)": "Aluminium",
            "Steel  (α ≈ 12 ×10⁻⁶/°C)": "Steel",
        },
        value="Steel  (α ≈ 12 ×10⁻⁶/°C)",
        label="Material",
    )
    delta_t = mo.ui.slider(
        start=0,
        stop=120,
        step=5,
        value=50,
        label="Temperature rise ΔT (°C)",
        show_value=True,
    )
    mo.vstack(
        [
            mo.hstack([mo.md("**Material:**"), thermal_material], justify="start", gap=1),
            mo.hstack([mo.md("**Warm it up:**"), delta_t], justify="start", gap=1),
        ]
    )
    return delta_t, thermal_material


@app.cell
def _(COLORS, delta_t, get_plotly_config, go, mo, thermal_material):
    def thermal_figure(name, dt):
        # (alpha ×10⁻⁶/°C, E in GPa, danger stress in MPa, what "danger" means)
        props = {
            "Aluminium": (23.0, 69.0, 275.0, "yield"),
            "Steel": (12.0, 200.0, 250.0, "yield"),
        }
        alpha, e_gpa, danger, danger_label = props[name]
        free_strain_pct = alpha * 1e-6 * dt * 100
        stress = e_gpa * alpha * dt / 1000.0  # MPa, = E·α·ΔT
        over = stress >= danger
        bar_color = COLORS["secondary"] if over else COLORS["wave"]

        fig = go.Figure()

        # Two rigid walls
        for wx in (0.0, 6.0):
            fig.add_trace(
                go.Scatter(
                    x=[wx, wx],
                    y=[-1, 1],
                    mode="lines",
                    line={"color": COLORS["text_secondary"], "width": 10},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
        # The clamped bar
        fig.add_trace(
            go.Scatter(
                x=[0.1, 5.9, 5.9, 0.1, 0.1],
                y=[-0.4, -0.4, 0.4, 0.4, -0.4],
                mode="lines",
                fill="toself",
                fillcolor=bar_color,
                line={"color": bar_color, "width": 2},
                name=name,
                hoverinfo="skip",
            )
        )

        verdict = (
            f"σ ≥ {danger_label} strength ({danger:.0f} MPa) → it would {danger_label}!"
            if over
            else f"still safe (below {danger_label} ≈ {danger:.0f} MPa)"
        )
        fig.update_layout(
            title={
                "text": f"<b>A Bar Clamped Between Two Walls, Warmed by {dt}°C</b><br>"
                f"<sub>if free it would grow {free_strain_pct:.3f}%  ·  held fast it builds "
                f"σ = E·α·ΔT = {stress:.0f} MPa</sub>"
            },
            xaxis={
                "range": [-0.6, 6.6],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "range": [-1.6, 1.6],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": 3,
                    "y": 1.25,
                    "text": f"<b>{verdict}</b>",
                    "showarrow": False,
                    "font": {"color": bar_color, "size": 14},
                },
            ],
            showlegend=False,
            height=420,
        )
        return fig

    thermal_plot = mo.ui.plotly(
        thermal_figure(thermal_material.value, delta_t.value), config=get_plotly_config()
    )
    mo.output.replace(thermal_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 9. Inside a beam: shear and bending, section by section

        In §4 we found the forces the supports push back with. But those are at the *ends* — to know
        where a beam is actually working hardest, and where it will crack, we have to walk along its
        length and ask, at each cross-section: *what is the material here having to carry?*

        The trick is to imagine slicing the beam at some point and looking at one of the two pieces.
        That piece must still be in equilibrium all by itself, so whatever the missing half used to
        provide, the material at the cut must now supply. It comes in two parts:

        - the **shear force** $V$ — the up-and-down force transmitted across the cut (what would make
          one half slide past the other), and
        - the **bending moment** $M$ — the turning effort carried through the cut (what actually
          bends the beam).

        Both change as you move along the beam, and we draw them as two curves beneath the beam: the
        **shear diagram** and the **bending-moment diagram**. Together they are a kind of X-ray of
        the beam. The bending moment is the one that matters most, because — as we'll see in §10 — the
        bending stress is $\sigma = M y / I$, so **the cross-section carrying the largest bending
        moment is the one most likely to fail.** For a simply supported beam with a single load at
        position $a$, the moment peaks *right under the load* at

        $$M_{\max} = \frac{P\,a\,(L-a)}{L},$$

        which is largest when the load sits at mid-span. *Slide the load and watch both diagrams
        breathe — notice the sharp kink in the moment right where the load sits.*
        """
    )
    return


@app.cell
def _(mo):
    sfbm_pos = mo.ui.slider(
        start=0.5,
        stop=5.5,
        step=0.1,
        value=3.0,
        label="Load position a (m from left support)",
        show_value=True,
    )
    mo.hstack([mo.md("**Move the load:**"), sfbm_pos], justify="start", gap=1)
    return (sfbm_pos,)


@app.cell
def _(COLORS, get_plotly_config, make_subplots, mo, sfbm_pos):
    def shear_moment_figure(a):
        span = 6.0
        load = 10.0  # kN
        r_left = load * (span - a) / span
        m_max = load * a * (span - a) / span

        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            row_heights=[0.36, 0.32, 0.32],
            vertical_spacing=0.07,
            subplot_titles=(
                "the beam and its load",
                "shear force  V (kN)",
                "bending moment  M (kN·m)",
            ),
        )

        # Row 1: beam + supports + load marker
        fig.add_scatter(
            x=[0, span],
            y=[0, 0],
            mode="lines",
            line={"color": COLORS["primary"], "width": 8},
            showlegend=False,
            hoverinfo="skip",
            row=1,
            col=1,
        )
        for sx in (0.0, span):
            fig.add_scatter(
                x=[sx - 0.25, sx + 0.25, sx, sx - 0.25],
                y=[-0.6, -0.6, 0, -0.6],
                mode="lines",
                fill="toself",
                fillcolor="rgba(160,160,160,0.5)",
                line={"color": COLORS["text_secondary"], "width": 1},
                showlegend=False,
                hoverinfo="skip",
                row=1,
                col=1,
            )
        fig.add_scatter(
            x=[a],
            y=[0.2],
            mode="markers",
            marker={"size": 16, "color": COLORS["gravity"], "symbol": "triangle-down"},
            showlegend=False,
            hovertemplate=f"load {load:.0f} kN at a={a:.1f} m<extra></extra>",
            row=1,
            col=1,
        )

        # Row 2: shear force (step)
        fig.add_scatter(
            x=[0, a, a, span],
            y=[r_left, r_left, r_left - load, r_left - load],
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(78, 205, 196, 0.3)",
            line={"color": COLORS["tertiary"], "width": 3},
            showlegend=False,
            hovertemplate="V = %{y:.1f} kN<extra></extra>",
            row=2,
            col=1,
        )

        # Row 3: bending moment (triangle, peak under the load)
        fig.add_scatter(
            x=[0, a, span],
            y=[0, m_max, 0],
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.3)",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
            hovertemplate="M = %{y:.1f} kN·m<extra></extra>",
            row=3,
            col=1,
        )
        fig.add_scatter(
            x=[a],
            y=[m_max],
            mode="markers+text",
            marker={"size": 10, "color": COLORS["secondary"]},
            text=[f" M_max = {m_max:.1f}"],
            textposition="top center",
            textfont={"color": COLORS["secondary"], "size": 12},
            showlegend=False,
            hoverinfo="skip",
            row=3,
            col=1,
        )

        fig.update_xaxes(
            range=[-0.5, span + 0.5], row=3, col=1, title_text="position along beam (m)"
        )
        fig.update_yaxes(showticklabels=False, row=1, col=1, range=[-0.9, 0.7])
        fig.update_layout(
            title={"text": "<b>Shear & Bending-Moment Diagrams</b>"},
            height=640,
            showlegend=False,
        )
        return fig

    sfbm_plot = mo.ui.plotly(shear_moment_figure(sfbm_pos.value), config=get_plotly_config())
    mo.output.replace(sfbm_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 10. Beams: why *shape* beats *material*

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

        ## 11. Torsion: twisting instead of bending

        Bending isn't the only way to load a bar. You can also **twist** it — that's what happens to
        the shaft turning a wheel, the spindle behind a doorknob, the bit of a screwdriver, or a
        wrench handle. Twisting is called **torsion**, and it rhymes beautifully with everything we
        just learned about beams.

        When you twist a round shaft, the outer skin is sheared the most and the material right on
        the central axis isn't worked at all — the axis is the torsional twin of a beam's *neutral
        axis*. So, exactly as with bending, what resists the twist is how far the material sits from
        the centre, captured this time by the **polar second moment of area** $J$. The angle the
        shaft twists through is

        $$\theta = \frac{T\,L}{G\,J},$$

        where $T$ is the applied torque and $G$ is the **shear modulus** — the material's stiffness
        against shearing, a cousin of Young's modulus (steel $\approx 79$ GPa, aluminium
        $\approx 26$ GPa, each roughly $0.4\times$ its $E$). For a solid round shaft
        $J = \pi d^4/32$.

        And now the same punchline as the I-beam, because it's the same physics: since the core does
        almost nothing, you can **hollow it out** and lose almost no stiffness while shedding a lot
        of weight. A **tube** of the same weight as a solid rod is far stiffer in twist — which is
        exactly why bicycle frames, scaffolding poles, and drive shafts are hollow tubes, not solid
        bars. The figure compares a solid shaft with a tube of the *same cross-sectional area*.
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo, np):
    def torsion_figure():
        theta = np.linspace(0, 2 * np.pi, 100)

        # Solid shaft: radius r, area = π r²  (take r = 1)
        r = 1.0
        area = np.pi * r**2
        j_solid = np.pi * r**4 / 2

        # Tube of the SAME area: choose inner radius, solve outer from equal area
        r_in = 1.0
        r_out = (r_in**2 + area / np.pi) ** 0.5  # π(r_out² − r_in²) = area
        j_tube = np.pi * (r_out**4 - r_in**4) / 2

        fig = go.Figure()

        # --- Solid shaft (left), centred at x = -2.2 ---
        cxs = -2.2
        fig.add_trace(
            go.Scatter(
                x=cxs + r * np.cos(theta),
                y=r * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor="rgba(160,160,160,0.5)",
                line={"color": COLORS["text_secondary"], "width": 2},
                name="Solid shaft",
                hoverinfo="skip",
            )
        )

        # --- Tube (right), centred at x = +2.2: outer disk with a punched hole ---
        cxt = 2.2
        fig.add_trace(
            go.Scatter(
                x=cxt + r_out * np.cos(theta),
                y=r_out * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 212, 255, 0.35)",
                line={"color": COLORS["primary"], "width": 2},
                name="Tube",
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=cxt + r_in * np.cos(theta),
                y=r_in * np.sin(theta),
                mode="lines",
                fill="toself",
                fillcolor=COLORS["background"],
                line={"color": COLORS["primary"], "width": 2},
                showlegend=False,
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            title={
                "text": "<b>Same Material, Solid vs. Hollow — in Twist</b><br>"
                "<sub>equal cross-sectional area; the tube's material sits farther from the axis</sub>"
            },
            xaxis={
                "range": [-4, 4.5],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "range": [-2, 2.4],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            annotations=[
                {
                    "x": cxs,
                    "y": -1.7,
                    "text": f"solid<br>J ≈ {j_solid:.1f}",
                    "showarrow": False,
                    "font": {"color": COLORS["text_secondary"], "size": 13},
                },
                {
                    "x": cxt,
                    "y": -1.7,
                    "text": f"tube (same area)<br>J ≈ {j_tube:.1f}",
                    "showarrow": False,
                    "font": {"color": COLORS["primary"], "size": 13},
                },
                {
                    "x": 0,
                    "y": 2.05,
                    "text": f"the tube is {j_tube / j_solid:.1f}× stiffer in twist, for the same metal",
                    "showarrow": False,
                    "font": {"color": COLORS["text"], "size": 13},
                },
            ],
            showlegend=False,
            height=460,
        )
        return fig

    torsion_plot = mo.ui.plotly(torsion_figure(), config=get_plotly_config())
    mo.output.replace(torsion_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 12. Stress concentration: where a shape secretly breaks first

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

        ## 13. Fatigue: how repeated loads snap things far below their strength

        Section 12 found the *hotspots* — the corners, holes and scratches where stress spikes. Now
        add the one ingredient that turns a hotspot into a disaster: **repetition**. Bend a paperclip
        once and it's fine; bend it back and forth a dozen times and it snaps. Nothing about the
        single bend was dangerous — it was the *cycling* that did it. This is **fatigue**, and it is
        behind a huge share of all real-world mechanical failures precisely because it strikes at
        stresses *well below* the one a material could survive if you loaded it only once.

        What happens physically: at a stress raiser, a microscopic crack forms, then creeps forward a
        tiny bit on every cycle. For a long time you'd never know — until the crack has eaten enough
        of the cross-section that the remainder can't carry even the ordinary load, and the part
        breaks suddenly, with no bending or warning. The map of this behaviour is the **S–N curve**:
        the stress amplitude $S$ against the number of cycles $N$ a specimen survives. It was first
        charted by August Wöhler in the 1860s, trying to understand why railway axles kept breaking.

        The plot below shows the single most important difference between two everyday metals:

        - **Steel has an *endurance limit*** — a stress (very roughly *half* its ultimate strength)
          **below which it survives essentially forever.** Keep the cycling gentler than that line
          and a steel part has, for practical purposes, infinite life.
        - **Aluminium has no such floor.** Its curve keeps sliding downward — cycle it long enough,
          however gently, and it *will* eventually fail. So aluminium parts must be designed for a
          finite life and retired on schedule, never assumed to last forever.

        (These are polished-laboratory numbers. Real notches, welds and rough surfaces — the very
        stress raisers of §12 — pull the usable limit *lower*, which is why fatigue and stress
        concentration are two halves of the same safety story.)
        """
    )
    return


@app.cell
def _(COLORS, get_plotly_config, go, mo, np):
    def fatigue_figure():
        log_n = np.linspace(3, 9, 200)  # 10³ … 10⁹ cycles

        # Steel: slopes down, then flattens at an endurance limit (~half UTS)
        steel_endurance = 225.0
        steel = np.where(
            log_n < 6,
            450 - (450 - steel_endurance) * (log_n - 3) / 3,
            steel_endurance,
        )
        # Aluminium: keeps declining, no endurance limit
        aluminium = 300 - 35 * (log_n - 3)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=10**log_n,
                y=steel,
                mode="lines",
                line={"color": COLORS["primary"], "width": 4},
                name="Steel — has an endurance limit",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=10**log_n,
                y=aluminium,
                mode="lines",
                line={"color": COLORS["tertiary"], "width": 4},
                name="Aluminium — no endurance limit",
            )
        )
        # Endurance-limit guide line for steel
        fig.add_trace(
            go.Scatter(
                x=[10**3, 10**9],
                y=[steel_endurance, steel_endurance],
                mode="lines",
                line={"color": COLORS["primary"], "width": 1, "dash": "dot"},
                showlegend=False,
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            title={
                "text": "<b>The S–N Curve: Strength Fades with Repetition</b><br><sub>lower stress → more cycles survived; steel finds a floor, aluminium never does</sub>"
            },
            xaxis={"title": "cycles to failure  N  (log scale)", "type": "log"},
            yaxis={"title": "repeated stress amplitude  S (MPa)", "range": [0, 470]},
            annotations=[
                {
                    "x": 7,
                    "y": 250,
                    "text": "steel's endurance limit — safe below here forever",
                    "showarrow": False,
                    "font": {"color": COLORS["primary"], "size": 11},
                    "xref": "x",
                    "xanchor": "center",
                },
                {
                    "x": 8.3,
                    "y": 100,
                    "text": "aluminium keeps falling",
                    "showarrow": False,
                    "font": {"color": COLORS["tertiary"], "size": 11},
                    "xref": "x",
                },
            ],
            height=520,
        )
        return fig

    fatigue_plot = mo.ui.plotly(fatigue_figure(), config=get_plotly_config())
    mo.output.replace(fatigue_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 14. Buckling: why long thin things fold instead of crushing

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
    mo.md(
        r"""
        ---

        ## 15. Factor of safety: how much margin to leave

        We can now find the stress inside a part (§6, §9–§11) and the stress a material can take
        (§7, §13). The last idea is the humblest and quietly the most important of all: **never run
        a part right up to its limit.**

        Why not? Because every number you used is a little bit wrong in the dangerous direction. The
        real load is heavier than you guessed — someone stands on the shelf, the wind gusts, a
        pothole doubles the force for an instant. The real material is a little weaker than the
        handbook — a flaw, a bad batch, a cold day. So you take the strength the material can bear,
        divide it by a **factor of safety**, and only ever allow the part to be stressed up to that
        lower "allowable" level:

        $$\text{factor of safety} = \frac{\text{strength the material can take}}{\text{stress it actually sees}}$$

        A factor of $1$ means it fails exactly at the expected load — no margin at all, one surprise
        from disaster. Ordinary, well-understood, non-critical things live around **1.5–2**. When
        the loads are uncertain, the material is brittle (it cracks with no warning — §7), the part
        will be cycled for years (§13), or a failure would hurt someone, the margin climbs to **3, 4,
        or more.** Too small and it breaks; too large and it's needlessly heavy, bulky and expensive.
        Choosing the number is a genuine act of judgement, and it draws on *every* idea in this
        notebook. *Push the load up and watch the margin shrink from comfortable, to nervous, to
        gone.*
        """
    )
    return


@app.cell
def _(mo):
    applied_stress = mo.ui.slider(
        start=20,
        stop=280,
        step=10,
        value=90,
        label="Working stress the part actually sees (MPa)",
        show_value=True,
    )
    mo.hstack([mo.md("**Load it harder:**"), applied_stress], justify="start", gap=1)
    return (applied_stress,)


@app.cell
def _(COLORS, applied_stress, get_plotly_config, go, mo):
    def safety_figure(working):
        yield_stress = 250.0  # mild steel
        ultimate = 400.0
        fos = yield_stress / working

        if fos >= 2:
            color, mood = COLORS["wave"], "comfortable margin"
        elif fos >= 1.5:
            color, mood = COLORS["quaternary"], "getting tight"
        elif fos > 1:
            color, mood = COLORS["gravity"], "dangerously little margin"
        else:
            color, mood = COLORS["secondary"], "past yield — it fails!"

        fig = go.Figure()

        # Coloured strength zones along a horizontal stress axis
        fig.add_trace(
            go.Scatter(
                x=[0, yield_stress, yield_stress, 0, 0],
                y=[0, 0, 1, 1, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(52, 211, 153, 0.18)",
                line={"width": 0},
                showlegend=False,
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[yield_stress, ultimate, ultimate, yield_stress, yield_stress],
                y=[0, 0, 1, 1, 0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(249, 115, 22, 0.20)",
                line={"width": 0},
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Yield & ultimate markers
        for xval, lbl, col in [
            (yield_stress, f"yield {yield_stress:.0f}", COLORS["quaternary"]),
            (ultimate, f"ultimate {ultimate:.0f}", COLORS["secondary"]),
        ]:
            fig.add_trace(
                go.Scatter(
                    x=[xval, xval],
                    y=[0, 1.15],
                    mode="lines",
                    line={"color": col, "width": 2, "dash": "dash"},
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
            fig.add_annotation(
                x=xval, y=1.28, text=lbl, showarrow=False, font={"color": col, "size": 12}
            )

        # The working-stress marker
        fig.add_trace(
            go.Scatter(
                x=[working],
                y=[0.5],
                mode="markers",
                marker={"size": 26, "color": color, "symbol": "triangle-up"},
                name="working stress",
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            title={
                "text": f"<b>Factor of Safety = strength ÷ working stress = {fos:.2f}</b><br>"
                f"<sub>working stress {working:.0f} MPa vs. yield {yield_stress:.0f} MPa  →  {mood}</sub>"
            },
            xaxis={
                "title": "stress (MPa)",
                "range": [0, 440],
                "showgrid": False,
                "zeroline": False,
            },
            yaxis={
                "range": [0, 1.5],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            annotations=[
                {
                    "x": working,
                    "y": 0.15,
                    "text": f"<b>FoS = {fos:.2f}</b>",
                    "showarrow": False,
                    "font": {"color": color, "size": 15},
                },
            ],
            showlegend=False,
            height=380,
        )
        return fig

    safety_plot = mo.ui.plotly(safety_figure(applied_stress.value), config=get_plotly_config())
    mo.output.replace(safety_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "A checklist: what to look at in any structure": mo.md(
                r"""
        When you look at a shelf, a bracket, a bench, or a bridge, run down this list — it's just
        the fifteen ideas above, in order:

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
        8. **Ask about temperature.** Will it be warmed or cooled while held fast? A trapped material
           builds real stress, $\sigma = E\alpha\Delta T$, from a change you'd barely feel (§8).
        9. **Walk along the beam.** Where is the bending moment largest? That cross-section — often
           mid-span or right under a load — is the one most likely to fail (§9).
        10. **Look at the cross-section.** Depth matters *cubed*. Is the material placed far from the
            neutral axis, where it does the work? (§10).
        11. **Check for twist.** Is anything being turned rather than bent? Shafts carry torque, and
            a hollow tube does it far more efficiently than a solid rod (§11).
        12. **Hunt the stress raisers.** Holes, sharp corners, notches, scratches — the real cracks
            start there, at up to 3× the average stress or more (§12).
        13. **Count the cycles.** Will the load repeat? If so, fatigue can snap it far below its
            one-time strength — and aluminium never gets a safe floor the way steel does (§13).
        14. **Watch for slender parts.** Anything long and thin under a push can buckle far below
            its crushing strength (§14).
        15. **Leave a margin.** Never run to the limit — divide the strength by a factor of safety,
            larger when the loads, the material, or the stakes are uncertain (§15).

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
        - **Thermal expansion data — [The Engineering ToolBox: Coefficients of Linear Thermal Expansion](https://www.engineeringtoolbox.com/linear-expansion-coefficients-d_95.html)**
        - **Stress concentration — [Fracture Mechanics: Stress Concentrations at Holes](https://www.fracturemechanics.org/hole.html)**
        - **Fatigue and the endurance limit — [Wikipedia: Fatigue limit](https://en.wikipedia.org/wiki/Fatigue_limit)**

        And if you want the friendliest book ever written on why structures hold together, look up
        J. E. Gordon's *Structures: Or Why Things Don't Fall Down* — same spirit as this notebook,
        no equations required.
        """
    )
    return


if __name__ == "__main__":
    app.run()
