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
        # Electric Circuits: Series, Parallel, and Everything In Between

        *A hands-on tour of how current, voltage, resistance, and power flow through a circuit —
        from a single resistor to a tangle of them — built in the spirit of the
        [Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/).*

        **Drawn from these Feynman lectures:**
        [Vol II, Ch 22 — AC Circuits](https://www.feynmanlectures.caltech.edu/II_22.html)
        (Kirchhoff's rules and how elements combine) ·
        [Vol II, Ch 25 — Circuit Elements](https://www.feynmanlectures.caltech.edu/II_25.html)
        (resistors and capacitors as idealised parts). Circuits weave several chapters together,
        so this one lives here under *Explorations*.

        ---

        ## Why bother with circuits?

        Flip a switch and a light comes on. Behind that everyday miracle is a loop of wire, a
        source pushing on the electric charge inside it, and a few parts that decide how hard the
        charge is pushed and how fast it flows. Learn to read that loop and you can look at almost
        any gadget — a torch, a phone charger, a string of fairy lights — and say, with reasons,
        *how much current flows here*, *what voltage sits across this part*, and *how much power it
        burns*.

        The wonderful thing is that the whole subject rests on **three quantities** and a small
        handful of rules for combining parts. We'll meet the quantities first, then build up circuits
        the way you'd actually build one: a single part, then two in a row, then two side by side,
        then the messy real thing that mixes both. Along the way we'll add the **capacitor** — a
        part that stores charge instead of burning it — and watch a circuit fill up and drain like
        a bucket.

        Every animation shows the **current actually flowing**: the little glowing dots *are* the
        moving charge. Where the dots crowd together and race, the current is large; where they
        thin out, it's small. And every rule comes with a **worked example** — real numbers, in a
        collapsible box you can open once you've seen the idea — so the theory always lands on
        something concrete.

        We'll build up in layers:

        1. **The three quantities** — voltage, current, resistance, and Ohm's law
        2. **Power** — how fast a circuit turns energy into heat and light
        3. **Series** — parts in a row: the current is shared, the voltage divides
        4. **Parallel** — parts side by side: the voltage is shared, the current divides
        5. **Mixed circuits** — reduce a tangle one clump at a time
        6. **Common setups & edge cases** — shortcuts, and the tricks that catch people out
        7. **Kirchhoff's rules** — the two laws underneath everything, and the divider shortcuts
        8. **Bridge circuits & the diamond** — the *losange*, and how to solve what won't reduce
        9. **Capacitors** — storing charge, and why they combine backwards from resistors
        10. **The RC circuit** — charging and draining, and the time constant τ
        11. **A full worked example** — one circuit, every tool, all the numbers

        Nothing here needs more than school algebra. Let's go and look.
        """
    )
    return


@app.cell
def _(COLORS, create_play_pause_buttons, go, np):
    # ------------------------------------------------------------------
    # Shared circuit-drawing helpers, reused by every schematic below.
    # A circuit is just wires (lines), components (labelled boxes), and
    # charge (glowing dots that drift along the wires). Only the dots move
    # between animation frames; everything else is drawn once.
    # ------------------------------------------------------------------

    def wire(path, color=None, width=3):
        """A length of wire through the given list of (x, y) corner points."""
        pts = np.asarray(path, dtype=float)
        return go.Scatter(
            x=pts[:, 0],
            y=pts[:, 1],
            mode="lines",
            line={"color": color or COLORS["text_secondary"], "width": width},
            showlegend=False,
            hoverinfo="skip",
        )

    def component(cx, cy, label, color, width=1.1, height=0.66, fill=None):
        """A labelled box (resistor, battery, capacitor) centred on (cx, cy).

        `fill` overrides the box fill colour; pass a transparent colour to let an
        animated glow behind the box show through (used by the power section).
        """
        hw, hh = width / 2, height / 2
        box = go.Scatter(
            x=[cx - hw, cx + hw, cx + hw, cx - hw, cx - hw],
            y=[cy - hh, cy - hh, cy + hh, cy + hh, cy - hh],
            mode="lines",
            line={"color": color, "width": 3},
            fill="toself",
            fillcolor=fill or COLORS["paper"],
            showlegend=False,
            hoverinfo="skip",
        )
        text = go.Scatter(
            x=[cx],
            y=[cy],
            mode="text",
            text=[f"<b>{label}</b>"],
            textfont={"color": color, "size": 14},
            showlegend=False,
            hoverinfo="skip",
        )
        return [box, text]

    def label(cx, cy, text, color, size=14):
        """A free-floating text label (for currents, voltages, notes)."""
        return go.Scatter(
            x=[cx],
            y=[cy],
            mode="text",
            text=[text],
            textfont={"color": color, "size": size},
            showlegend=False,
            hoverinfo="skip",
        )

    def charge_dots(path, n_dots, phase, color=None, size=9):
        """`n_dots` glowing charges spread evenly along `path`, shifted by `phase`.

        `phase` is measured in gaps: advancing it by 1 slides every dot forward
        into its neighbour's place, so any whole-number phase looks identical and
        the flow loops seamlessly. More dots on a wire means more current: at a
        fixed drift speed, packing charges closer *is* more charge per second
        passing any point.
        """
        pts = np.asarray(path, dtype=float)
        seg = np.diff(pts, axis=0)
        seg_len = np.hypot(seg[:, 0], seg[:, 1])
        total = float(seg_len.sum())
        cum = np.concatenate([[0.0], np.cumsum(seg_len)])
        gap = total / max(n_dots, 1)
        dists = (np.arange(n_dots) * gap + phase * gap) % total
        xs, ys = [], []
        for d in dists:
            k = int(np.searchsorted(cum, d, side="right") - 1)
            k = min(max(k, 0), len(seg_len) - 1)
            frac = (d - cum[k]) / seg_len[k] if seg_len[k] else 0.0
            xs.append(pts[k, 0] + frac * seg[k, 0])
            ys.append(pts[k, 1] + frac * seg[k, 1])
        return go.Scatter(
            x=xs,
            y=ys,
            mode="markers",
            marker={
                "size": size,
                "color": color or COLORS["electric"],
                "line": {"color": COLORS["text"], "width": 0.5},
            },
            showlegend=False,
            hoverinfo="skip",
        )

    def play_pause_menu():
        """The standard top-right Play/Pause control, shared by every animation."""
        return [
            {
                "type": "buttons",
                "x": 1.0,
                "y": 1.12,
                "xanchor": "right",
                "yanchor": "bottom",
                "direction": "left",
                "showactive": False,
                "buttons": create_play_pause_buttons(),
                "bgcolor": COLORS["paper"],
                "font": {"color": COLORS["text"]},
            }
        ]

    ANIM_FRAMES = 90  # ~4.5 s per play at the shared 50 ms/frame — long and smooth
    ANIM_CYCLES = 3  # dots drift three whole gaps across a play, so the flow reads

    def flow(specs, n_frames=ANIM_FRAMES, cycles=ANIM_CYCLES):
        """Turn a list of `(path, n_dots, color)` specs into a `dot_fn` for
        `circuit_animation`: each frame drifts every stream on by a shared phase,
        so wires with more dots simply carry more current. The dots advance
        `cycles` gaps over the whole play, ending where they began (seamless loop).
        """

        def dot_fn(i):
            phase = cycles * i / n_frames
            return [charge_dots(path, n, phase, color=color) for path, n, color in specs]

        return dot_fn

    def legend_swatches(items):
        """Dummy (invisible) markers that put a colour key in the Plotly legend.

        `items` = list of (colour, text); each becomes one legend row so readers
        know what the yellow / blue / red dots mean without cluttering the figure.
        """
        return [
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"size": 11, "color": color},
                name=text,
                showlegend=True,
                hoverinfo="skip",
            )
            for color, text in items
        ]

    def circuit_animation(
        wire_traces,
        dot_fn,
        overlay_traces,
        title,
        xrange,
        yrange,
        legend=None,
        n_frames=ANIM_FRAMES,
        height=460,
    ):
        """Assemble a schematic with an animated charge flow drawn *behind* the parts.

        Draw order (back to front): wires → charge dots → component boxes and
        labels. Because the dots sit under the boxes and labels, the moving charge
        slides behind each component and never hides its text. `dot_fn(i)` returns
        the moving traces for frame `i`; it must return the same count every frame.
        `legend` = optional list of (colour, text) rows explaining the dot colours.
        """
        first_dots = dot_fn(0)
        n_wire = len(wire_traces)
        dot_indices = list(range(n_wire, n_wire + len(first_dots)))
        frames = [
            go.Frame(data=first_dots if i == 0 else dot_fn(i), traces=dot_indices, name=str(i))
            for i in range(n_frames)
        ]
        swatches = legend_swatches(legend) if legend else []
        fig = go.Figure(data=[*wire_traces, *first_dots, *overlay_traces, *swatches], frames=frames)
        fig.update_layout(
            title={"text": title},
            xaxis={"range": xrange, "showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={
                "range": yrange,
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "scaleanchor": "x",
            },
            showlegend=bool(legend),
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": -0.02,
                "xanchor": "center",
                "x": 0.5,
                "bgcolor": "rgba(22, 33, 62, 0.6)",
                "font": {"color": COLORS["text"], "size": 12},
            },
            margin={"l": 30, "r": 30, "t": 70, "b": 60},
            height=height,
            updatemenus=play_pause_menu(),
        )
        return fig

    def series_parallel_scene(labels, currents, note, title, height=460):
        """The shared schematic for a resistor in series feeding a parallel pair,
        reused by the mixed-circuit (§5) and full-example (§9) animations.

        `labels` = (V, R₁, R₂, R₃) strings; `currents` = (I_main, I₂, I₃) in amps.
        Dot density tracks those currents, so the same drawing serves any values.
        """
        left_x, split_x, join_x = 0.7, 4.6, 8.2
        y_top, y_bot, y_mid = 3.4, 1.2, 2.3
        series_seg = [(left_x, y_mid), (left_x, y_top), (split_x, y_top)]
        left_rail = [(split_x, y_top), (split_x, y_bot)]
        branch_top = [(split_x, y_top), (join_x, y_top)]
        branch_bot = [(split_x, y_bot), (join_x, y_bot)]
        right_rail = [(join_x, y_top), (join_x, y_bot)]
        return_seg = [(join_x, y_bot), (left_x, y_bot), (left_x, y_mid)]
        v_lbl, r1_lbl, r2_lbl, r3_lbl = labels
        i_main, i2, i3 = currents

        wires = [
            wire(series_seg),
            wire(left_rail),
            wire(branch_top),
            wire(branch_bot),
            wire(right_rail),
            wire(return_seg),
        ]
        overlays = [
            *component(left_x, y_mid, v_lbl, COLORS["quaternary"], width=1.0, height=1.2),
            *component(2.6, y_top, r1_lbl, COLORS["tertiary"]),
            *component(6.4, y_top, r2_lbl, COLORS["primary"]),
            *component(6.4, y_bot, r3_lbl, COLORS["secondary"]),
            label(2.6, y_top + 0.5, f"I = {i_main:g} A (all of it)", COLORS["electric"], size=12),
            label(6.4, y_top + 0.5, f"I₂ = {i2:g} A", COLORS["primary"], size=12),
            label(6.4, y_bot - 0.5, f"I₃ = {i3:g} A", COLORS["secondary"], size=12),
            label(9.2, y_mid, note, COLORS["text_secondary"], size=11),
        ]
        specs = [
            (series_seg, max(2, round(i_main * 2.0)), COLORS["electric"]),
            (branch_top, max(2, round(i2 * 1.5)), COLORS["primary"]),
            (branch_bot, max(2, round(i3 * 1.5)), COLORS["secondary"]),
            (return_seg, max(2, round(i_main * 3.4)), COLORS["electric"]),
        ]
        return circuit_animation(
            wires,
            flow(specs),
            overlays,
            title=title,
            xrange=[-0.2, 10.6],
            yrange=[0.4, 4.2],
            legend=[
                (COLORS["electric"], f"yellow — main current ({i_main:g} A)"),
                (COLORS["primary"], f"blue — through R₂ ({i2:g} A)"),
                (COLORS["secondary"], f"red — through R₃ ({i3:g} A)"),
            ],
            height=height,
        )

    return (
        charge_dots,
        circuit_animation,
        component,
        flow,
        label,
        play_pause_menu,
        series_parallel_scene,
        wire,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The three quantities, and the one law that ties them

        A circuit runs on three numbers. The trick to never getting confused is a picture: think
        of **water in pipes**.

        - **Voltage $V$** (volts, V) is the *push* — the electrical "pressure" a battery or socket
          puts across the circuit. Like water pressure, it's a difference *between two points*: it
          only makes sense to ask "the voltage *across* this part," never "the voltage *at* one
          wire" on its own.
        - **Current $I$** (amperes, A) is the *flow* — how much charge streams past a point each
          second, like litres of water per second through a pipe. One amp is a coulomb of charge
          every second.
        - **Resistance $R$** (ohms, Ω) is the *narrowness* — how much the part fights the flow. A
          thin, restrictive pipe has high resistance; a fat open one has low resistance.

        These three are locked together by **Ohm's law**, the single most useful equation in all
        of electronics:

        $$V = I \, R \qquad\Longleftrightarrow\qquad I = \frac{V}{R} \qquad\Longleftrightarrow\qquad R = \frac{V}{I}$$

        Read it in words: *push equals flow times narrowness*. Turn up the push (voltage) and more
        current flows. Make the pipe narrower (more resistance) and less current flows for the same
        push. That's the whole of it — every calculation below is this law, applied cleverly.

        The slider below is Ohm's law you can feel. A **9 V** battery sits across one resistor; drag
        the resistance and watch the current $I = V/R$ respond.
        """
    )
    return


@app.cell
def _(mo):
    ohm_resistance = mo.ui.slider(
        start=3,
        stop=90,
        step=1,
        value=18,
        label="Resistance R (ohms), across a fixed 9 V battery",
        show_value=True,
    )
    mo.hstack([mo.md("**Turn the resistance:**"), ohm_resistance], justify="start", gap=1)
    return (ohm_resistance,)


@app.cell
def _(COLORS, get_plotly_config, go, mo, np, ohm_resistance):
    def ohm_figure(resistance):
        voltage = 9.0
        current = voltage / resistance  # amps, from Ohm's law
        power = voltage * current  # watts

        r_axis = np.linspace(3, 90, 200)
        i_axis = voltage / r_axis
        curve = go.Scatter(
            x=r_axis,
            y=i_axis * 1000,  # milliamps for a friendlier axis
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name="I = V / R",
            hoverinfo="skip",
        )
        marker = go.Scatter(
            x=[resistance],
            y=[current * 1000],
            mode="markers",
            marker={"size": 16, "color": COLORS["electric"]},
            name="operating point",
            hoverinfo="skip",
        )
        fig = go.Figure(data=[curve, marker])
        fig.update_layout(
            title={
                "text": f"<b>Ohm's Law: one resistor across 9 V</b><br>"
                f"<sub>R = {resistance:.0f} Ω  →  I = 9 / {resistance:.0f} = "
                f"{current * 1000:.0f} mA,  power P = V·I = {power:.2f} W</sub>"
            },
            xaxis={"title": "Resistance R (Ω)"},
            yaxis={"title": "Current I (mA)"},
            height=430,
            showlegend=False,
        )
        return fig

    ohm_plot = mo.ui.plotly(ohm_figure(ohm_resistance.value), config=get_plotly_config())
    mo.output.replace(ohm_plot)
    return


@app.cell
def _(
    COLORS, circuit_animation, component, flow, get_plotly_config, label, mo, ohm_resistance, wire
):
    def ohm_flow_figure(resistance):
        current = 9.0 / resistance  # amps
        # The same one-resistor loop, but now you can *see* the current: raise R
        # with the slider above and the stream of charge thins out.
        loop = [(0.6, 1.0), (0.6, 3.0), (4.5, 3.0), (8.4, 3.0), (8.4, 1.0), (0.6, 1.0)]
        n_dots = min(30, max(1, round(current * 8)))
        wires = [wire(loop, width=3)]
        overlays = [
            *component(0.6, 2.0, "9 V", COLORS["quaternary"], width=1.0, height=1.1),
            *component(4.5, 3.0, f"R = {resistance:.0f} Ω", COLORS["primary"], width=1.7),
            label(4.5, 2.2, f"I = {current * 1000:.0f} mA", COLORS["electric"], size=14),
        ]
        return circuit_animation(
            wires,
            flow([(loop, n_dots, COLORS["electric"])]),
            overlays,
            title="<b>Ohm's law, live — bigger R throttles the flow of charge</b>",
            xrange=[-0.2, 9.2],
            yrange=[0.2, 4.0],
            legend=[(COLORS["electric"], "yellow — current")],
            height=380,
        )

    ohm_flow_plot = mo.ui.plotly(ohm_flow_figure(ohm_resistance.value), config=get_plotly_config())
    mo.output.replace(ohm_flow_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Power: how fast the circuit spends energy

        Voltage and current together tell you the **power** — the rate at which the circuit turns
        electrical energy into something else (heat in a resistor, light in a bulb, motion in a
        motor). Power is measured in **watts (W)**, and one watt is one joule every second.

        $$P = V \, I$$

        Because Ohm's law links $V$ and $I$, you can rewrite power using whichever two quantities
        you happen to know:

        $$P = V\,I = I^2 R = \frac{V^2}{R}$$

        All three say the same thing. Use $P = I^2 R$ when you know the current through a part
        (handy for parts in a row, which share a current), and $P = V^2/R$ when you know the
        voltage across it (handy for parts side by side, which share a voltage).

        One more distinction that trips people up: **power is not energy.** Power (watts) is the
        *rate*; **energy** is power multiplied by time,

        $$E = P \, t,$$

        measured in joules, or — on your electricity bill — in **kilowatt-hours** (1 kWh is running
        1000 W for one hour). A 60 W bulb doesn't "use 60 W per hour"; it *is* 60 W, and left on
        for an hour it uses 60 watt-hours of energy.

        In the animation, the charge flows through a resistor and the resistor glows: every charge
        that squeezes through gives up a little energy as heat, and the glow pulses with the power
        $P = I^2R$ being dissipated.
        """
    )
    return


@app.cell
def _(
    COLORS, charge_dots, circuit_animation, component, get_plotly_config, go, label, mo, np, wire
):
    def power_figure():
        loop = [(0.6, 1.0), (0.6, 3.0), (4.5, 3.0), (8.4, 3.0), (8.4, 1.0), (0.6, 1.0)]
        cx, cy = 4.5, 3.0
        wires = [wire(loop, width=3)]
        overlays = [
            *component(0.6, 2.0, "12 V", COLORS["quaternary"], width=1.0, height=1.1),
            # Transparent fill so the pulsing heat-glow behind it shows through.
            *component(cx, cy, "R", COLORS["secondary"], width=1.4, fill="rgba(0,0,0,0)"),
            label(cx, 2.1, "P = I²R burned as heat", COLORS["gravity"], size=13),
        ]

        def dot_fn(i):
            phase = 3 * i / 90
            pulse = 0.5 + 0.5 * float(np.sin(2 * np.pi * i / 30))
            glow = go.Scatter(
                x=[cx],
                y=[cy],
                mode="markers",
                marker={
                    "size": 60 + 45 * pulse,
                    "color": COLORS["gravity"],
                    "opacity": 0.10 + 0.16 * pulse,
                    "line": {"width": 0},
                },
                showlegend=False,
                hoverinfo="skip",
            )
            return [glow, charge_dots(loop, 14, phase)]

        return circuit_animation(
            wires,
            dot_fn,
            overlays,
            title="<b>Power: current forced through a resistor comes out as heat</b>",
            xrange=[-0.2, 9.2],
            yrange=[0.2, 4.0],
            legend=[(COLORS["electric"], "yellow — current (spends energy as heat)")],
            height=400,
        )

    power_plot = mo.ui.plotly(power_figure(), config=get_plotly_config())
    mo.output.replace(power_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: the numbers behind a 60 W light bulb": mo.md(
                r"""
        A household bulb is rated **60 W at 120 V**. What is going on inside it?

        **Current it draws.** From $P = V I$,

        $$I = \frac{P}{V} = \frac{60}{120} = 0.5\ \text{A}.$$

        **Its resistance (when hot).** From $R = V / I$,

        $$R = \frac{120}{0.5} = 240\ \Omega,$$

        and as a check, $P = V^2/R = 120^2 / 240 = 14400/240 = 60$ W. ✓

        **Energy used in an evening.** Left on for 5 hours,

        $$E = P\,t = 60\ \text{W} \times 5\ \text{h} = 300\ \text{Wh} = 0.30\ \text{kWh}.$$

        At about \$0.15 per kWh that's roughly **4.5 cents** for the evening — the whole reason
        the world switched to LED bulbs, which get the same light for a fifth of the watts.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Series: parts in a row share the current

        The simplest way to wire two parts is **in a row**, one after the other, so the same loop
        of wire runs through both. This is a **series** circuit, and it has one defining feature:

        > There is only one path, so **the current is the same everywhere.** Every charge that
        > leaves the battery must pass through *every* part in turn.

        In the water picture, it's a single pipe with two narrow sections back to back. The same
        litres-per-second flow through both — and the two restrictions *add up*, so the total
        resistance is just the sum:

        $$R_\text{series} = R_1 + R_2 + R_3 + \cdots$$

        The current pushed through that total is $I = V / R_\text{series}$, the same in every part.
        And because each resistor drops some of the voltage as the current fights through it, the
        **voltages add back up to the source** (that's Kirchhoff's voltage law, coming in §7):

        $$V = V_1 + V_2 + \cdots, \qquad V_k = I\,R_k.$$

        In the animation, notice the dots are **evenly spaced all the way round** and move at one
        speed — that's "the current is the same everywhere" made visible. The bigger resistor
        simply steals a bigger share of the 12 V push.
        """
    )
    return


@app.cell
def _(COLORS, circuit_animation, component, flow, label, mo, get_plotly_config, wire):
    def series_figure():
        # A single rectangular loop: battery on the left, two resistors along the top.
        loop = [
            (0.6, 1.0),  # battery top terminal
            (0.6, 3.0),
            (3.0, 3.0),  # R1 sits around here
            (6.4, 3.0),  # R2 sits around here
            (8.6, 3.0),
            (8.6, 1.0),
            (0.6, 1.0),  # back to the battery
        ]
        wires = [wire(loop, width=3)]
        overlays = [
            *component(0.6, 2.0, "12 V", COLORS["quaternary"], width=1.0, height=1.1),
            *component(3.0, 3.0, "R₁ = 4 Ω", COLORS["primary"]),
            *component(6.4, 3.0, "R₂ = 8 Ω", COLORS["secondary"]),
            label(4.7, 3.7, "same current everywhere: I = 1 A", COLORS["electric"], size=13),
            label(3.0, 2.2, "V₁ = 4 V", COLORS["primary"], size=13),
            label(6.4, 2.2, "V₂ = 8 V", COLORS["secondary"], size=13),
            label(1.5, 0.6, "+", COLORS["quaternary"], size=18),
            label(1.5, 3.4, "−", COLORS["text_secondary"], size=18),
        ]

        # One current everywhere → one evenly-spaced stream of charge.
        return circuit_animation(
            wires,
            flow([(loop, 22, COLORS["electric"])]),
            overlays,
            title="<b>Series circuit — one path, one current</b>",
            xrange=[-0.2, 9.4],
            yrange=[0.0, 4.2],
            legend=[(COLORS["electric"], "yellow — current (same everywhere)")],
            height=440,
        )

    series_plot = mo.ui.plotly(series_figure(), config=get_plotly_config())
    mo.output.replace(series_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: two resistors in series across 12 V": mo.md(
                r"""
        Take $V = 12$ V, $R_1 = 4\ \Omega$, $R_2 = 8\ \Omega$, wired in a row.

        **Step 1 — total resistance.** Series resistances add:

        $$R_\text{series} = R_1 + R_2 = 4 + 8 = 12\ \Omega.$$

        **Step 2 — the current (same everywhere).** Ohm's law on the whole loop:

        $$I = \frac{V}{R_\text{series}} = \frac{12}{12} = 1\ \text{A}.$$

        **Step 3 — the voltage each resistor drops.** Ohm's law on each part, using that one
        current:

        $$V_1 = I R_1 = 1 \times 4 = 4\ \text{V}, \qquad V_2 = I R_2 = 1 \times 8 = 8\ \text{V}.$$

        Check: $V_1 + V_2 = 4 + 8 = 12$ V — they add back to the source. ✓ The bigger resistor
        takes the bigger share of the voltage.

        **Step 4 — the power in each part.** With the shared current, $P = I^2 R$ is easiest:

        $$P_1 = I^2 R_1 = 1^2 \times 4 = 4\ \text{W}, \qquad P_2 = 1^2 \times 8 = 8\ \text{W}.$$

        Total $P = 4 + 8 = 12$ W, and as a check $P = V I = 12 \times 1 = 12$ W. ✓
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Parallel: parts side by side share the voltage

        Now wire the two parts **side by side**, both ends joined, so each has its own path back to
        the battery. This is a **parallel** circuit, and it's the mirror image of series:

        > Both parts are connected straight across the source, so **the voltage is the same across
        > each one.** But the current now has a choice of routes, so it *splits*.

        In the water picture, it's one pipe branching into two before rejoining — the same pressure
        drives both branches, but more water takes the wider (lower-resistance) branch. The branch
        currents add up to the total (that's Kirchhoff's current law, §7):

        $$I = I_1 + I_2 + \cdots, \qquad I_k = \frac{V}{R_k}.$$

        Because you've *added a second path*, the combination is **easier** for current than either
        resistor alone — so the total resistance comes out *smaller than the smallest branch*. The
        rule adds the reciprocals:

        $$\frac{1}{R_\text{parallel}} = \frac{1}{R_1} + \frac{1}{R_2} + \cdots$$

        For exactly two resistors that rearranges into the handy **product-over-sum** form:

        $$R_\text{parallel} = \frac{R_1 R_2}{R_1 + R_2}.$$

        In the animation, both branches feel the same 12 V, but the **4 Ω branch runs three times
        denser** than the 12 Ω branch — three times the current — and the trunk wire carries the
        sum of the two. Watch the dots split at the junction and merge again on the way back.
        """
    )
    return


@app.cell
def _(COLORS, circuit_animation, component, flow, label, mo, get_plotly_config, wire):
    def parallel_figure():
        # Battery on the left; the loop splits into a top branch (R1) and a
        # bottom branch (R2) between the two vertical rails, then rejoins.
        left_rail_x, right_rail_x = 2.4, 8.0
        y_top, y_bot = 3.4, 1.0
        y_mid = 2.2

        trunk_in = [(0.7, y_mid), (0.7, y_top), (left_rail_x, y_top)]
        trunk_left_rail = [(left_rail_x, y_top), (left_rail_x, y_bot)]
        branch_top = [(left_rail_x, y_top), (right_rail_x, y_top)]
        branch_bot = [(left_rail_x, y_bot), (right_rail_x, y_bot)]
        right_rail = [(right_rail_x, y_top), (right_rail_x, y_bot)]
        trunk_out = [(right_rail_x, y_bot), (0.7, y_bot), (0.7, y_mid)]

        wires = [
            wire(trunk_in),
            wire(trunk_left_rail),
            wire(branch_top),
            wire(branch_bot),
            wire(right_rail),
            wire(trunk_out),
        ]
        overlays = [
            *component(0.7, y_mid, "12 V", COLORS["quaternary"], width=1.0, height=1.2),
            *component(5.2, y_top, "R₁ = 4 Ω", COLORS["primary"]),
            *component(5.2, y_bot, "R₂ = 12 Ω", COLORS["secondary"]),
            label(5.2, y_top + 0.5, "I₁ = 3 A", COLORS["primary"], size=13),
            label(5.2, y_bot - 0.5, "I₂ = 1 A", COLORS["secondary"], size=13),
            label(1.35, y_top + 0.35, "I = 4 A", COLORS["electric"], size=13),
            label(9.0, y_mid, "same 12 V<br>across both", COLORS["text_secondary"], size=12),
        ]

        # Dot counts scale with current × wire length, so the *spacing* (dots
        # per unit length) tracks the current: trunk 4 A, top branch 3 A, bottom
        # branch 1 A — the 4 Ω branch runs three times denser.
        return circuit_animation(
            wires,
            flow(
                [
                    (trunk_in, 4, COLORS["electric"]),
                    (branch_top, 6, COLORS["primary"]),
                    (branch_bot, 2, COLORS["secondary"]),
                    (trunk_out, 12, COLORS["electric"]),
                ]
            ),
            overlays,
            title="<b>Parallel circuit — one voltage, the current splits</b>",
            xrange=[-0.2, 10.4],
            yrange=[0.2, 4.4],
            legend=[
                (COLORS["electric"], "yellow — total current (4 A)"),
                (COLORS["primary"], "blue — through R₁ (3 A)"),
                (COLORS["secondary"], "red — through R₂ (1 A)"),
            ],
            height=460,
        )

    parallel_plot = mo.ui.plotly(parallel_figure(), config=get_plotly_config())
    mo.output.replace(parallel_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: two resistors in parallel across 12 V": mo.md(
                r"""
        Take $V = 12$ V, $R_1 = 4\ \Omega$, $R_2 = 12\ \Omega$, wired side by side.

        **Step 1 — total resistance (product over sum).**

        $$R_\text{parallel} = \frac{R_1 R_2}{R_1 + R_2} = \frac{4 \times 12}{4 + 12}
          = \frac{48}{16} = 3\ \Omega.$$

        Notice it's **smaller than either branch** (smaller than the 4 Ω) — adding a second path
        always makes it easier for current.

        **Step 2 — the branch currents (same voltage on each).** Ohm's law per branch:

        $$I_1 = \frac{V}{R_1} = \frac{12}{4} = 3\ \text{A}, \qquad
          I_2 = \frac{V}{R_2} = \frac{12}{12} = 1\ \text{A}.$$

        **Step 3 — the total current.** The branches rejoin, so their currents add:

        $$I = I_1 + I_2 = 3 + 1 = 4\ \text{A}.$$

        Check against the total resistance: $I = V / R_\text{parallel} = 12 / 3 = 4$ A. ✓ The
        low-resistance branch hogs three-quarters of the current.

        **Step 4 — the power (same voltage, so $P = V^2/R$ is easiest).**

        $$P_1 = \frac{V^2}{R_1} = \frac{144}{4} = 36\ \text{W}, \qquad
          P_2 = \frac{144}{12} = 12\ \text{W},$$

        total $48$ W, matching $P = V I = 12 \times 4 = 48$ W. ✓
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Mixed circuits: reduce the tangle one clump at a time

        Real circuits are rarely all-series or all-parallel — they're a mix. The good news is that
        you never need a new idea, only the two rules you already have, applied **from the inside
        out**:

        1. Find a clump that is *purely* series or *purely* parallel.
        2. Replace it with its single equivalent resistance.
        3. Redraw. The circuit is now simpler. Repeat until one resistor remains.
        4. Now walk *back outwards*: the total current splits and voltages divide, branch by branch.

        The circuit below is the classic first example: a resistor **in series** with a **parallel
        pair**. We collapse the parallel pair into one resistor, add it to the series resistor to
        get the total, find the main current — then expand back out to see how that current divides
        between the two parallel branches. The animation shows the full current flowing through
        $R_1$, then splitting evenly through the two equal branches, then merging on the way home.
        """
    )
    return


@app.cell
def _(get_plotly_config, mo, series_parallel_scene):
    # R₁ = 3 Ω in series feeds R₂ ∥ R₃ = 6 Ω ∥ 6 Ω; 3 A splits evenly into 1.5 A each.
    mixed_plot = mo.ui.plotly(
        series_parallel_scene(
            labels=("18 V", "R₁ = 3 Ω", "R₂ = 6 Ω", "R₃ = 6 Ω"),
            currents=(3, 1.5, 1.5),
            note="R₂ ∥ R₃ = 3 Ω",
            title="<b>Mixed circuit — a resistor in series with a parallel pair</b>",
        ),
        config=get_plotly_config(),
    )
    mo.output.replace(mixed_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: series resistor feeding a parallel pair": mo.md(
                r"""
        The circuit above: $V = 18$ V, with $R_1 = 3\ \Omega$ in series, feeding $R_2 = 6\ \Omega$
        in parallel with $R_3 = 6\ \Omega$.

        **Step 1 — collapse the parallel pair.** Two equal resistors in parallel give half:

        $$R_{23} = \frac{R_2 R_3}{R_2 + R_3} = \frac{6 \times 6}{6 + 6} = \frac{36}{12}
          = 3\ \Omega.$$

        The circuit is now just $R_1 = 3\ \Omega$ in series with $R_{23} = 3\ \Omega$.

        **Step 2 — total resistance and main current.**

        $$R_\text{total} = R_1 + R_{23} = 3 + 3 = 6\ \Omega, \qquad
          I = \frac{V}{R_\text{total}} = \frac{18}{6} = 3\ \text{A}.$$

        This full 3 A flows through $R_1$.

        **Step 3 — voltage splits between the series resistor and the pair (KVL).**

        $$V_1 = I R_1 = 3 \times 3 = 9\ \text{V}, \qquad
          V_{23} = I R_{23} = 3 \times 3 = 9\ \text{V},$$

        and $V_1 + V_{23} = 9 + 9 = 18$ V back to the source. ✓

        **Step 4 — the pair's 9 V drives each branch (Ohm's law per branch).**

        $$I_2 = \frac{V_{23}}{R_2} = \frac{9}{6} = 1.5\ \text{A}, \qquad
          I_3 = \frac{9}{6} = 1.5\ \text{A},$$

        and $I_2 + I_3 = 3$ A = the main current (KCL). ✓

        **Step 5 — power.** Total $P = V I = 18 \times 3 = 54$ W, of which $R_1$ burns
        $I^2 R_1 = 9 \times 3 = 27$ W and the pair burns the remaining $27$ W (13.5 W each).
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. Common setups, shortcuts, and edge cases

        You now have the two moves — **series adds, parallel takes reciprocals** — and the recipe to
        reduce any tangle. Here are the shortcuts worth memorising, and the edge cases that catch
        people out.

        **Two shortcuts that cover most real circuits:**

        - **$n$ identical resistors in series:** $R_\text{eq} = nR$. Three 100 Ω in a row → 300 Ω.
        - **$n$ identical resistors in parallel:** $R_\text{eq} = R/n$. Three 100 Ω side by side → 33.3 Ω.

        **Two sanity checks you can always apply:**

        - **Series** is always *larger than the largest* resistor — you keep adding restriction.
        - **Parallel** is always *smaller than the smallest* resistor — you keep adding paths.

        If a result ever breaks one of those, you've slipped a digit somewhere.

        The animation makes the point with the very same parts: take two 4 Ω resistors and wire them
        both ways. In **series** they make 8 Ω and sip 1.5 A; in **parallel** they make 2 Ω and gulp
        6 A — four times the current, from identical components.
        """
    )
    return


@app.cell
def _(COLORS, charge_dots, circuit_animation, component, get_plotly_config, label, mo, np, wire):
    def compare_figure():
        def plen(path):
            pts = np.asarray(path, dtype=float)
            return float(np.hypot(*np.diff(pts, axis=0).T).sum())

        def n_for(path, current):
            return max(2, round(0.5 * current * plen(path)))

        # SERIES (top): the two 4 Ω resistors in a row.
        loop_s = [
            (0.6, 5.4),
            (0.6, 7.4),
            (3.4, 7.4),
            (6.2, 7.4),
            (8.6, 7.4),
            (8.6, 5.4),
            (0.6, 5.4),
        ]
        # PARALLEL (bottom): the same two resistors side by side.
        lrx, rrx = 2.6, 8.0
        trunk_in = [(0.6, 2.0), (0.6, 3.4), (lrx, 3.4)]
        left_rail = [(lrx, 3.4), (lrx, 0.6)]
        branch_top = [(lrx, 3.4), (rrx, 3.4)]
        branch_bot = [(lrx, 0.6), (rrx, 0.6)]
        right_rail = [(rrx, 3.4), (rrx, 0.6)]
        trunk_out = [(rrx, 0.6), (0.6, 0.6), (0.6, 2.0)]

        wires = [
            wire(loop_s),
            wire(trunk_in),
            wire(left_rail),
            wire(branch_top),
            wire(branch_bot),
            wire(right_rail),
            wire(trunk_out),
        ]
        overlays = [
            *component(0.6, 6.4, "12 V", COLORS["quaternary"], width=1.0, height=1.1),
            *component(3.4, 7.4, "4 Ω", COLORS["primary"]),
            *component(6.2, 7.4, "4 Ω", COLORS["secondary"]),
            label(4.8, 8.0, "SERIES:  4 + 4 = 8 Ω  →  I = 1.5 A", COLORS["electric"], size=13),
            *component(0.6, 2.0, "12 V", COLORS["quaternary"], width=1.0, height=1.1),
            *component(5.3, 3.4, "4 Ω", COLORS["primary"]),
            *component(5.3, 0.6, "4 Ω", COLORS["secondary"]),
            label(4.8, 4.0, "PARALLEL:  4 ∥ 4 = 2 Ω  →  I = 6 A", COLORS["electric"], size=13),
        ]

        def dot_fn(i):
            phase = 3 * i / 90
            return [
                charge_dots(loop_s, n_for(loop_s, 1.5), phase, color=COLORS["electric"]),
                charge_dots(trunk_in, n_for(trunk_in, 6), phase, color=COLORS["electric"]),
                charge_dots(branch_top, n_for(branch_top, 3), phase, color=COLORS["primary"]),
                charge_dots(branch_bot, n_for(branch_bot, 3), phase, color=COLORS["secondary"]),
                charge_dots(trunk_out, n_for(trunk_out, 6), phase, color=COLORS["electric"]),
            ]

        return circuit_animation(
            wires,
            dot_fn,
            overlays,
            title="<b>Same two resistors, two montages — parallel pulls 4× the current</b>",
            xrange=[-0.2, 9.4],
            yrange=[0.2, 8.4],
            legend=[
                (COLORS["electric"], "yellow — total current"),
                (COLORS["primary"], "blue — through one 4 Ω"),
                (COLORS["secondary"], "red — through the other 4 Ω"),
            ],
            height=620,
        )

    compare_plot = mo.ui.plotly(compare_figure(), config=get_plotly_config())
    mo.output.replace(compare_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ The mirror table: series vs parallel at a glance": mo.md(
                r"""
        | | **Series** (one path) | **Parallel** (many paths) |
        |---|---|---|
        | Current | **same** through every part | **splits** between parts |
        | Voltage | **splits** across parts | **same** across every part |
        | Resistance | adds: $R_1 + R_2 + \cdots$ | reciprocals add (always smaller) |
        | Total vs parts | bigger than the **biggest** | smaller than the **smallest** |
        | $n$ equal parts | $nR$ | $R/n$ |
        | Capacitors | reciprocals add (smaller) | add (bigger) |

        Series and parallel are mirror images: flip a circuit from one to the other and every row of
        this table flips with it.
        """
            ),
            "▸ Edge cases that trip people up": mo.md(
                r"""
        **A short circuit (0 Ω) in parallel wins everything.** A bare wire has essentially no
        resistance, so put one across a resistor and product-over-sum gives
        $R_\text{eq} = R\cdot 0/(R+0) = 0$: all the current pours through the wire and the resistor
        beside it carries almost none. That's why a stray wire across a battery is dangerous — the
        current is then limited only by the battery itself.

        **An open circuit (∞ Ω) stops a series path dead.** A broken wire or unplugged part is
        infinite resistance. In *series* that makes the whole loop infinite and the current zero —
        one gap and nothing flows (why old fairy-light strings all went dark when a single bulb
        blew). In *parallel* an open branch just carries no current; the rest of the circuit doesn't
        notice.

        **The bottleneck is the biggest in series, the smallest in parallel.** A 1 kΩ in series with
        a 10 Ω behaves like ~1 kΩ — the big one dominates. But a 1 kΩ in *parallel* with a 10 Ω
        behaves like ~10 Ω — the *small* one dominates, because current takes the easy path. When one
        resistor is far larger or smaller than its neighbour, you can often ignore the other.
        """
            ),
            "▸ Worked example: three resistors in parallel (a shared power rail)": mo.md(
                r"""
        A 12 V rail feeds three loads at once: $R_1 = 6\ \Omega$, $R_2 = 3\ \Omega$, $R_3 = 2\ \Omega$.

        **Total resistance — add the reciprocals** (product-over-sum is for two only):

        $$\frac{1}{R_\text{eq}} = \frac16 + \frac13 + \frac12 = \frac{1}{6} + \frac{2}{6} + \frac{3}{6}
          = \frac{6}{6} = 1 \;\Rightarrow\; R_\text{eq} = 1\ \Omega,$$

        smaller than the smallest branch (2 Ω), as it must be.

        **Each branch sees the full 12 V:**

        $$I_1 = \frac{12}{6} = 2\ \text{A}, \qquad I_2 = \frac{12}{3} = 4\ \text{A}, \qquad
          I_3 = \frac{12}{2} = 6\ \text{A}.$$

        **Total current:** $I = 2 + 4 + 6 = 12\ \text{A}$, matching $I = V/R_\text{eq} = 12/1 = 12$ A. ✓
        The smallest resistor hogs the most current — the current divider at work.
        """
            ),
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Kirchhoff's rules, and the divider shortcuts

        Everything above is really two bookkeeping laws in disguise — **Kirchhoff's rules**, the
        foundation the whole subject stands on. They're just statements that charge and energy are
        conserved:

        - **Current law (KCL):** at any junction, current in = current out. Charge doesn't pile up
          anywhere, so *what flows in must flow out*. (This is why parallel branch currents add.)
        - **Voltage law (KVL):** around any closed loop, the voltage rises and drops sum to zero.
          The energy a charge gains at the battery it gives back, exactly, to the parts. (This is
          why series voltages add up to the source.)

        Two everyday shortcuts fall straight out of them.

        **The voltage divider.** Two resistors in series split the source voltage in proportion to
        their resistance. The voltage across the *lower* resistor $R_2$ is

        $$V_\text{out} = V \, \frac{R_2}{R_1 + R_2}.$$

        This is how a volume knob, a sensor, or a microcontroller input gets a smaller, tapped-off
        voltage from a bigger one. (It assumes almost no current is drawn from the tap — hang a
        heavy load on $V_\text{out}$ and it sags, because the load sits in parallel with $R_2$.)
        Drag the slider to tap off any fraction you like.

        **The current divider.** Two resistors in parallel split the incoming current in *inverse*
        proportion — more goes through the *smaller* resistor:

        $$I_1 = I \, \frac{R_2}{R_1 + R_2}.$$

        (Note the other resistor's value on top — the branch you're solving for gets the *opposite*
        branch's resistance in the numerator.)

        The animation shows Kirchhoff's current law in the flesh: **5 A flow into the junction, and
        exactly 5 A flow out** — 3 A up one branch, 2 A down the other. Charge never piles up at a
        node, so what arrives must leave.
        """
    )
    return


@app.cell
def _(COLORS, circuit_animation, flow, get_plotly_config, go, label, mo, wire):
    def kcl_figure():
        node = (4.2, 2.0)
        wire_in = [(0.4, 2.0), node]
        wire_top = [node, (8.4, 3.3)]
        wire_bot = [node, (8.4, 0.7)]
        wires = [wire(wire_in), wire(wire_top), wire(wire_bot)]
        node_dot = go.Scatter(
            x=[node[0]],
            y=[node[1]],
            mode="markers",
            marker={"size": 13, "color": COLORS["text"]},
            showlegend=False,
            hoverinfo="skip",
        )
        overlays = [
            node_dot,
            label(1.9, 2.35, "I = 5 A in", COLORS["electric"], size=14),
            label(6.9, 3.5, "3 A out", COLORS["primary"], size=13),
            label(6.9, 0.5, "2 A out", COLORS["secondary"], size=13),
            label(4.2, 1.2, "KCL: 5 = 3 + 2", COLORS["text_secondary"], size=13),
        ]
        # Dot counts track current (in = top + bottom), so the two outgoing
        # streams together carry exactly what the incoming wire delivers.
        return circuit_animation(
            wires,
            flow(
                [
                    (wire_in, 8, COLORS["electric"]),
                    (wire_top, 6, COLORS["primary"]),
                    (wire_bot, 4, COLORS["secondary"]),
                ]
            ),
            overlays,
            title="<b>Kirchhoff's current law — what flows in flows out</b>",
            xrange=[0.0, 9.4],
            yrange=[0.0, 4.0],
            legend=[
                (COLORS["electric"], "yellow — 5 A in"),
                (COLORS["primary"], "blue — 3 A out"),
                (COLORS["secondary"], "red — 2 A out"),
            ],
            height=400,
        )

    kcl_plot = mo.ui.plotly(kcl_figure(), config=get_plotly_config())
    mo.output.replace(kcl_plot)
    return


@app.cell
def _(mo):
    divider_ratio = mo.ui.slider(
        start=0.5,
        stop=9.0,
        step=0.5,
        value=2.0,
        label="Bottom resistor R₂ (kΩ), with R₁ fixed at 2 kΩ across 9 V",
        show_value=True,
    )
    mo.hstack([mo.md("**Tap off a voltage:**"), divider_ratio], justify="start", gap=1)
    return (divider_ratio,)


@app.cell
def _(COLORS, divider_ratio, get_plotly_config, go, mo, np):
    def divider_figure(r2_k):
        source, r1_k = 9.0, 2.0
        r2_axis = np.linspace(0.5, 9.0, 200)
        v_out_axis = source * r2_axis / (r1_k + r2_axis)
        v_out = source * r2_k / (r1_k + r2_k)

        curve = go.Scatter(
            x=r2_axis,
            y=v_out_axis,
            mode="lines",
            line={"color": COLORS["tertiary"], "width": 3},
            hoverinfo="skip",
        )
        marker = go.Scatter(
            x=[r2_k],
            y=[v_out],
            mode="markers",
            marker={"size": 16, "color": COLORS["electric"]},
            hoverinfo="skip",
        )
        fig = go.Figure(data=[curve, marker])
        fig.update_layout(
            title={
                "text": f"<b>Voltage divider</b><br><sub>V_out = 9 · R₂/(R₁+R₂) = "
                f"9 · {r2_k:.1f}/(2 + {r2_k:.1f}) = {v_out:.2f} V</sub>"
            },
            xaxis={"title": "Bottom resistor R₂ (kΩ)"},
            yaxis={"title": "Tapped voltage V_out (V)", "range": [0, 9]},
            height=430,
            showlegend=False,
        )
        return fig

    divider_plot = mo.ui.plotly(divider_figure(divider_ratio.value), config=get_plotly_config())
    mo.output.replace(divider_plot)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. Bridge circuits and the diamond — when series-parallel isn't enough

        Wire four resistors into a **diamond** (a *losange*): two arms climbing to a top node, two
        dropping to a bottom node, driven across the left–right diagonal. That one is still easy —
        it's just two series pairs sitting in parallel, and everything from §5 handles it.

        The trouble starts when you drop a **fifth resistor across the middle**, bridging the top and
        bottom nodes. This is the famous **Wheatstone bridge**, and it breaks the whole
        series-parallel game: look as hard as you like and there is no pair of resistors that is
        *purely* in series or *purely* in parallel. Reduction stalls on the first step.

        When that happens, you reach for one of three tools:

        1. **The balance shortcut.** If the arms are in proportion,

           $$\frac{R_1}{R_2} = \frac{R_3}{R_4} \quad\Longleftrightarrow\quad R_1 R_4 = R_2 R_3,$$

           the two middle nodes sit at exactly the same voltage, so **no current flows through the
           bridge at all.** Delete the bridge resistor and reduce the rest normally. This is how a
           Wheatstone bridge *measures* an unknown resistor: adjust a known one until the bridge
           current reads zero, then read the answer off the ratio — precise, and independent of the
           source voltage.

        2. **Kirchhoff's laws (the method that always works).** Label a current in every branch,
           write KCL at each node and KVL around enough loops to match the unknowns, and solve the
           simultaneous equations. It never fails; it's just more algebra. The interactive below does
           exactly this — solving the bridge by **nodal analysis**, computing every branch current
           live as you drag the slider.

        3. **The delta–wye (Δ–Y) transform.** Any triangle of three resistors ("delta", Δ) can be
           swapped for an equivalent three-spoke star ("wye", Y) that the rest of the circuit can't
           tell apart. One such swap turns the bridge back into something series-parallel. Each Y
           spoke is the product of its two neighbouring Δ resistors over the sum of all three:

           $$R_A = \frac{R_{AB}\,R_{AC}}{R_{AB}+R_{BC}+R_{CA}} \quad(\text{and likewise for } R_B, R_C).$$

        Drag the slider and watch the bridge solve itself. Away from balance the teal bridge current
        flows; hit **R₄ = 10 Ω** and it drops to zero — only then does the diamond collapse back into
        two simple parallel branches.
        """
    )
    return


@app.cell
def _(mo):
    r4_slider = mo.ui.slider(
        start=4,
        stop=24,
        step=1,
        value=6,
        label="Bridge arm R₄ (Ω) — the bridge balances at R₄ = 10 Ω",
        show_value=True,
    )
    mo.hstack(
        [mo.md("**Adjust R₄ (watch the bridge current):**"), r4_slider], justify="start", gap=1
    )
    return (r4_slider,)


@app.cell
def _(
    COLORS,
    charge_dots,
    circuit_animation,
    component,
    get_plotly_config,
    go,
    label,
    mo,
    np,
    r4_slider,
    wire,
):
    def bridge_figure(r4):
        source = 20.0
        r1 = r2 = r3 = r5 = 10.0
        r4 = float(r4)
        g1, g2, g3, g4, g5 = 1 / r1, 1 / r2, 1 / r3, 1 / r4, 1 / r5
        # Nodal analysis: fix V_A = 20 V (source +) and V_C = 0 (reference), then
        # solve KCL at the two middle nodes B and D for their voltages.
        coeff = np.array([[g1 + g2 + g5, -g5], [-g5, g3 + g4 + g5]])
        rhs = np.array([g1 * source, g3 * source])
        v_b, v_d = (float(v) for v in np.linalg.solve(coeff, rhs))
        i1 = g1 * (source - v_b)  # A → B
        i2 = g2 * v_b  # B → C
        i3 = g3 * (source - v_d)  # A → D
        i4 = g4 * v_d  # D → C
        i5 = g5 * (v_b - v_d)  # bridge B → D
        i_tot = i1 + i3
        balanced = abs(i5) < 0.02

        ax, ay = 2.2, 2.2
        bx, by = 5.0, 3.9
        dx, dy = 5.0, 0.5
        cx, cy = 8.2, 2.2
        trunk_in = [(1.2, 2.2), (ax, ay)]
        arm_ab = [(ax, ay), (bx, by)]
        arm_ad = [(ax, ay), (dx, dy)]
        arm_bc = [(bx, by), (cx, cy)]
        arm_dc = [(dx, dy), (cx, cy)]
        bridge = [(bx, by), (dx, dy)]
        ret = [(cx, cy), (9.0, 2.2), (9.0, -0.6), (0.7, -0.6), (0.7, 1.5)]
        wires = [wire(w) for w in (trunk_in, arm_ab, arm_ad, arm_bc, arm_dc, bridge, ret)]

        def node_dot(x, y):
            return go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker={"size": 9, "color": COLORS["text"]},
                showlegend=False,
                hoverinfo="skip",
            )

        overlays = [
            *component(0.7, 2.2, "20 V", COLORS["quaternary"], width=1.0, height=1.3),
            *component(
                (ax + bx) / 2, (ay + by) / 2, "R₁", COLORS["primary"], width=0.9, height=0.5
            ),
            *component(
                (bx + cx) / 2, (by + cy) / 2, "R₂", COLORS["primary"], width=0.9, height=0.5
            ),
            *component(
                (ax + dx) / 2, (ay + dy) / 2, "R₃", COLORS["secondary"], width=0.9, height=0.5
            ),
            *component(
                (dx + cx) / 2, (dy + cy) / 2, "R₄", COLORS["secondary"], width=0.9, height=0.5
            ),
            *component(
                (bx + dx) / 2, (by + dy) / 2, "R₅", COLORS["tertiary"], width=0.9, height=0.5
            ),
            node_dot(ax, ay),
            node_dot(bx, by),
            node_dot(dx, dy),
            node_dot(cx, cy),
            label(ax - 0.32, ay + 0.36, "A", COLORS["text"], 13),
            label(bx, by + 0.32, "B", COLORS["text"], 13),
            label(dx, dy - 0.32, "D", COLORS["text"], 13),
            label(cx + 0.3, cy + 0.35, "C", COLORS["text"], 13),
            label(4.5, -0.32, f"total current I = {i_tot:.2f} A", COLORS["electric"], 12),
            label(
                6.45,
                2.2,
                f"I₅ = {i5:.2f} A" + ("  (balanced!)" if balanced else ""),
                COLORS["tertiary"],
                13,
            ),
        ]

        def branch_dots(path, current, phase, color):
            n = max(0, round(3.0 * abs(current)))
            directed = path if current >= 0 else path[::-1]
            return charge_dots(directed, n, phase, color=color)

        def dot_fn(i):
            phase = 3 * i / 90
            return [
                branch_dots(trunk_in, i_tot, phase, COLORS["electric"]),
                branch_dots(arm_ab, i1, phase, COLORS["primary"]),
                branch_dots(arm_ad, i3, phase, COLORS["secondary"]),
                branch_dots(arm_bc, i2, phase, COLORS["primary"]),
                branch_dots(arm_dc, i4, phase, COLORS["secondary"]),
                branch_dots(bridge, i5, phase, COLORS["tertiary"]),
                branch_dots(ret, i_tot, phase, COLORS["electric"]),
            ]

        state = "balanced — bridge carries nothing" if balanced else "unbalanced — bridge conducts"
        return circuit_animation(
            wires,
            dot_fn,
            overlays,
            title=f"<b>Wheatstone bridge — R₁=R₂=R₃=R₅=10 Ω, R₄={r4:.0f} Ω</b><br>"
            f"<sub>solved live by nodal analysis: bridge current I₅ = {i5:.2f} A ({state})</sub>",
            xrange=[-0.2, 9.6],
            yrange=[-0.9, 4.4],
            legend=[
                (COLORS["electric"], "yellow — total current"),
                (COLORS["primary"], "blue — top path (R₁, R₂)"),
                (COLORS["secondary"], "red — bottom path (R₃, R₄)"),
                (COLORS["tertiary"], "teal — bridge (R₅)"),
            ],
            height=540,
        )

    bridge_plot = mo.ui.plotly(bridge_figure(r4_slider.value), config=get_plotly_config())
    mo.output.replace(bridge_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: the balanced bridge that measures a resistor": mo.md(
                r"""
        The bridge's fame comes from measurement. Wire two known "ratio" arms $R_1 = 10\ \Omega$ and
        $R_2 = 20\ \Omega$, a known adjustable $R_3$, and the unknown $R_4$ you want to measure.
        Turn $R_3$ until a meter in the bridge reads **exactly zero current**. At that balance point

        $$\frac{R_1}{R_2} = \frac{R_3}{R_4} \;\Rightarrow\; R_4 = R_3\,\frac{R_2}{R_1}.$$

        Say balance is reached at $R_3 = 15\ \Omega$. Then

        $$R_4 = 15 \times \frac{20}{10} = 30\ \Omega,$$

        read off from three *known* resistances — with no dependence on the source voltage or the
        meter's calibration, only on the null. That's why a bridge can measure to a fraction of a
        percent.

        With the bridge balanced it carries no current, so the network is simply two series branches
        in parallel:

        $$(R_1 + R_3) \parallel (R_2 + R_4) = 25 \parallel 50 = \frac{25 \times 50}{75}
          = 16.7\ \Omega.$$
        """
            ),
            "▸ Worked example: cracking an unbalanced bridge with Δ–Y": mo.md(
                r"""
        Take an *unbalanced* bridge across A–C, all values in ohms: $R_{AB}=30$, $R_{AD}=30$,
        $R_{BD}=30$ (the bridge), $R_{BC}=20$, $R_{DC}=5$. Since $R_{AB}/R_{BC}=1.5$ but
        $R_{AD}/R_{DC}=6$, it is **not** balanced — the bridge carries current, and no two resistors
        are cleanly in series or parallel.

        **Step 1 — turn the triangle A–B–D into a Y.** The delta
        $R_{AB}=R_{AD}=R_{BD}=30\ \Omega$ becomes a star with centre $N$; each spoke is

        $$R = \frac{30 \times 30}{30 + 30 + 30} = \frac{900}{90} = 10\ \Omega,$$

        so $R_{NA}=R_{NB}=R_{ND}=10\ \Omega$.

        **Step 2 — now it's series-parallel.** From $N$, the path through $B$ is
        $R_{NB}+R_{BC} = 10+20 = 30\ \Omega$; the path through $D$ is $R_{ND}+R_{DC} = 10+5 =
        15\ \Omega$. Those two run in parallel:

        $$30 \parallel 15 = \frac{30 \times 15}{45} = 10\ \Omega.$$

        **Step 3 — add the last spoke in series:**

        $$R_{AC} = R_{NA} + 10 = 10 + 10 = 20\ \Omega.$$

        A tangled five-resistor bridge collapses to a clean **20 Ω** — no simultaneous equations, just
        one Δ→Y swap.
        """
            ),
            "▸ The method that never fails: Kirchhoff, step by step": mo.md(
                r"""
        When there's no shortcut, Kirchhoff's laws always solve it — and the interactive above uses
        exactly this recipe:

        1. **Pick a reference node** (voltage 0) and label the unknown node voltages. For the bridge,
           ground $C$ and fix $A$ at the source $V$; the unknowns are $V_B$ and $V_D$.
        2. **Write KCL at each unknown node** as "currents leaving sum to zero", each current written
           as (voltage difference) × (conductance $g = 1/R$). At $B$:

           $$g_1(V_B - V_A) + g_2(V_B - V_C) + g_5(V_B - V_D) = 0,$$

           and similarly at $D$.
        3. **Collect into a linear system** — here two equations in $V_B, V_D$ — and solve it (by
           hand, or with `numpy.linalg.solve`):

           $$\begin{aligned}
           (g_1 + g_2 + g_5)\,V_B - g_5\,V_D &= g_1 V, \\
           -g_5\,V_B + (g_3 + g_4 + g_5)\,V_D &= g_3 V.
           \end{aligned}$$
        4. **Back-substitute** for every branch current, e.g. $I_5 = g_5(V_B - V_D)$ through the
           bridge. When $V_B = V_D$ the bridge current is zero — the balance condition falls out
           automatically.

        This **nodal analysis** scales to any network: $n$ unknown nodes give $n$ equations. It's more
        work than a clever reduction, but it never gets stuck.
        """
            ),
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 9. Capacitors: storing charge instead of burning it

        Every part so far has *resisted* current and turned energy into heat. A **capacitor**
        (French *condensateur*) does something completely different: it **stores** charge, like a
        tiny rechargeable bucket. Two metal plates sit close together but not touching; pile
        electrons onto one plate and an equal number are pushed off the other, and the plates hold
        that charge until you give it somewhere to go.

        How much charge it holds depends on the voltage across it and on its **capacitance $C$**
        (measured in **farads, F** — in practice microfarads, µF):

        $$Q = C \, V.$$

        A bigger capacitor, or a bigger voltage, stores more charge. And unlike a resistor, a
        charged capacitor holds **energy** you can get back out again:

        $$E = \tfrac{1}{2} C V^2.$$

        Here's the twist that catches everyone out: **capacitors combine the *opposite* way to
        resistors.**

        - **In parallel**, the plate areas effectively add, so capacitances simply add:
          $$C_\text{parallel} = C_1 + C_2 + \cdots$$
        - **In series**, the *reciprocals* add (the same product-over-sum trick as parallel
          resistors), giving a *smaller* total:
          $$\frac{1}{C_\text{series}} = \frac{1}{C_1} + \frac{1}{C_2} + \cdots$$

        A clean way to remember it: **capacitors are the mirror of resistors.** Wherever resistors
        add, capacitors take reciprocals, and vice-versa.

        The animation runs a full cycle. First it **charges**: charge streams onto the plates and
        the gap fills, but as it fills the capacitor pushes back harder, so the current fades to
        nothing once it's full. Then it **discharges**: the stored charge drains back out and the
        current runs the *other* way, fading again as the plates empty. That fade-and-flow is the
        whole story of the next section.
        """
    )
    return


@app.cell
def _(
    COLORS, charge_dots, circuit_animation, component, get_plotly_config, go, label, mo, np, wire
):
    def capacitor_figure():
        battery_seg = [(0.6, 1.0), (0.6, 3.0)]
        top_path = [(0.6, 3.0), (6.0, 3.0), (6.0, 2.3)]  # battery + → top plate
        bot_path = [(6.0, 1.7), (6.0, 1.0), (0.6, 1.0)]  # bottom plate → battery −
        top_plate = [(5.3, 2.3), (6.7, 2.3)]
        bot_plate = [(5.3, 1.7), (6.7, 1.7)]

        wires = [wire(battery_seg), wire(top_path), wire(bot_path)]
        overlays = [
            wire(top_plate, color=COLORS["secondary"], width=6),
            wire(bot_plate, color=COLORS["primary"], width=6),
            *component(0.6, 2.0, "5 V", COLORS["quaternary"], width=1.0, height=1.1),
            label(7.5, 2.3, "+Q", COLORS["secondary"], size=15),
            label(7.5, 1.7, "−Q", COLORS["primary"], size=15),
            label(3.0, 0.5, "one full cycle: charge, then discharge", COLORS["text_secondary"], 12),
        ]

        def dot_fn(i):
            # First half charges the capacitor; second half discharges it. On
            # discharge the current reverses (phase runs backwards) and the
            # stored charge drains back out.
            if i < 45:
                f = i / 44.0
                level = 1.0 - float(np.exp(-f * 5.0))  # gap fills 0 → 1
                cur = float(np.exp(-f * 5.0))  # charging current e^(−t/τ) → 0
                phase = 3 * i / 90
                status, status_color = "charging ▲", COLORS["wave"]
            else:
                f = (i - 45) / 44.0
                level = float(np.exp(-f * 5.0))  # gap drains 1 → 0
                cur = float(np.exp(-f * 5.0))  # discharge current, same envelope
                phase = -3 * i / 90  # current runs the other way
                status, status_color = "discharging ▼", COLORS["secondary"]
            n_dots = round(9 * cur)
            y_fill = 1.74 + level * 0.52
            fill = go.Scatter(
                x=[5.45, 6.55, 6.55, 5.45, 5.45],
                y=[1.74, 1.74, y_fill, y_fill, 1.74],
                mode="lines",
                line={"width": 0},
                fill="toself",
                fillcolor="rgba(167, 139, 250, 0.40)",  # stored charge on the plates
                showlegend=False,
                hoverinfo="skip",
            )
            status_text = go.Scatter(
                x=[3.0],
                y=[3.6],
                mode="text",
                text=[status],
                textfont={"color": status_color, "size": 14},
                showlegend=False,
                hoverinfo="skip",
            )
            return [
                charge_dots(top_path, n_dots, phase, color=COLORS["electric"]),
                charge_dots(bot_path, n_dots, phase, color=COLORS["electric"]),
                fill,
                status_text,
            ]

        return circuit_animation(
            wires,
            dot_fn,
            overlays,
            title="<b>Charging then discharging — it fills up, then drains back out</b>",
            xrange=[-0.2, 8.6],
            yrange=[0.2, 4.0],
            legend=[
                (COLORS["electric"], "yellow — current (charge/discharge)"),
                (COLORS["spacetime"], "purple — stored charge"),
                (COLORS["secondary"], "red — +Q plate"),
                (COLORS["primary"], "blue — −Q plate"),
            ],
            height=440,
        )

    capacitor_plot = mo.ui.plotly(capacitor_figure(), config=get_plotly_config())
    mo.output.replace(capacitor_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: combining and charging a capacitor": mo.md(
                r"""
        Take $C_1 = 2\ \mu\text{F}$ and $C_2 = 4\ \mu\text{F}$.

        **In parallel** (capacitances add):

        $$C_\text{parallel} = C_1 + C_2 = 2 + 4 = 6\ \mu\text{F}.$$

        **In series** (reciprocals add — product over sum, like parallel resistors):

        $$C_\text{series} = \frac{C_1 C_2}{C_1 + C_2} = \frac{2 \times 4}{2 + 4}
          = \frac{8}{6} \approx 1.33\ \mu\text{F},$$

        smaller than either one — the mirror image of resistors.

        **Charge and energy stored.** Put the 6 µF parallel combination across $V = 10$ V:

        $$Q = C V = (6 \times 10^{-6})(10) = 6 \times 10^{-5}\ \text{C} = 60\ \mu\text{C},$$

        $$E = \tfrac{1}{2} C V^2 = \tfrac{1}{2}(6 \times 10^{-6})(10^2)
          = 3 \times 10^{-4}\ \text{J} = 0.30\ \text{mJ}.$$

        That's the energy that flashes back out when it discharges — exactly the trick a camera
        flash uses to dump a big pulse of light in a fraction of a second.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 10. The RC circuit: charging, draining, and the time constant

        Put a resistor and a capacitor in series with a battery and you get the most useful little
        circuit in electronics — the **RC circuit**. Close the switch and the capacitor doesn't
        charge instantly; the resistor throttles the flow, so the voltage climbs along a smooth
        curve and eases into the source voltage:

        $$V_C(t) = V\left(1 - e^{-t / RC}\right).$$

        The current starts high (an empty capacitor looks like a plain wire) and dies away as the
        capacitor fills up and pushes back:

        $$I(t) = \frac{V}{R}\, e^{-t / RC}.$$

        The whole speed of the process is set by one number, the **time constant**

        $$\tau = R\,C,$$

        measured in seconds. After one $\tau$ the capacitor has reached **63%** of the way; after
        about **5 τ** it's essentially full (over 99%). Draining is the mirror image — the same
        curve upside-down, $V_C(t) = V_0\,e^{-t/RC}$ — with the same $\tau$.

        In the animation, watch two things at once: the **curve** climbing toward the source voltage,
        and the **charge flow slowing down** as the capacitor fills. The dots crowd through fast at
        first, then thin out to a trickle — that's the current dying away. Drag the slider to change
        the resistance, and watch a bigger $R$ stretch the whole process out in time.
        """
    )
    return


@app.cell
def _(mo):
    rc_resistance = mo.ui.slider(
        start=5,
        stop=40,
        step=5,
        value=10,
        label="Resistance R (kΩ), charging a 100 µF capacitor from 5 V",
        show_value=True,
    )
    mo.hstack(
        [mo.md("**Change the time constant τ = RC:**"), rc_resistance], justify="start", gap=1
    )
    return (rc_resistance,)


@app.cell
def _(
    COLORS,
    charge_dots,
    get_plotly_config,
    go,
    label,
    mo,
    np,
    play_pause_menu,
    rc_resistance,
    wire,
):
    def rc_figure(r_kohm):
        source = 5.0
        cap = 100e-6  # farads
        res = r_kohm * 1000.0
        tau = res * cap  # seconds
        t_max = 5 * tau
        t = np.linspace(0, t_max, 60)
        v_c = source * (1 - np.exp(-t / tau))

        # A little charging loop drawn beneath the curve; dot density tracks I(t).
        loop = [(0.0, -1.7), (0.0, -0.8), (3.0, -0.8), (3.0, -1.7), (0.0, -1.7)]

        curve = go.Scatter(
            x=t,
            y=v_c,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name="blue line — capacitor voltage V_C(t)",
            showlegend=True,
            hoverinfo="skip",
        )
        target = go.Scatter(
            x=[0, t_max],
            y=[source, source],
            mode="lines",
            line={"color": COLORS["text_secondary"], "width": 1, "dash": "dash"},
            showlegend=False,
            hoverinfo="skip",
        )
        tau_mark = go.Scatter(
            x=[tau],
            y=[source * (1 - np.exp(-1))],
            mode="markers+text",
            marker={"size": 11, "color": COLORS["quaternary"]},
            text=["  63% at t = τ"],
            textposition="middle right",
            textfont={"color": COLORS["quaternary"], "size": 12},
            showlegend=False,
            hoverinfo="skip",
        )
        head = go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker={"size": 15, "color": COLORS["electric"]},
            showlegend=False,
            hoverinfo="skip",
        )
        legend_dot = go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={"size": 11, "color": COLORS["electric"]},
            name="yellow dots — charging current I(t)",
            showlegend=True,
            hoverinfo="skip",
        )
        wire_trace = wire(loop, width=2)
        dots0 = charge_dots(loop, 10, 0.0)
        # Draw order keeps the moving charge (dots0) *under* the note and the
        # marker, so the flowing dots never sit on top of the text.
        static = [
            curve,
            target,
            tau_mark,
            wire_trace,
            dots0,
            label(1.5, -0.4, "charging current I(t) — watch it fade", COLORS["text_secondary"], 11),
            head,
            legend_dot,
        ]

        n_frames = 90

        def frame_data(i):
            frac = i / (n_frames - 1)
            ti = frac * t_max
            vi = source * (1 - np.exp(-ti / tau))
            # Fewer dots as the current dies away: n ∝ I(t) = (V/R)·e^(−t/τ).
            n_dots = max(1, round(10 * float(np.exp(-ti / tau))))
            return [
                charge_dots(loop, n_dots, frac * 6.0),
                go.Scatter(
                    x=[ti],
                    y=[vi],
                    mode="markers",
                    marker={"size": 15, "color": COLORS["electric"]},
                    hoverinfo="skip",
                ),
            ]

        frames = [go.Frame(data=frame_data(i), traces=[4, 6], name=str(i)) for i in range(n_frames)]
        fig = go.Figure(data=static, frames=frames)
        fig.update_layout(
            title={
                "text": f"<b>RC charging — R = {r_kohm:.0f} kΩ, C = 100 µF, "
                f"τ = RC = {tau:.1f} s</b><br><sub>reaches 63% at one τ, "
                f"over 99% by 5τ = {t_max:.0f} s</sub>"
            },
            xaxis={"title": "time t (s)", "range": [-t_max * 0.02, t_max * 1.05]},
            yaxis={
                "title": "capacitor voltage V_C (V)",
                "range": [-2.0, source * 1.15],
                "showticklabels": True,
            },
            height=520,
            showlegend=True,
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "left",
                "x": 0.0,
                "bgcolor": "rgba(22, 33, 62, 0.6)",
                "font": {"color": COLORS["text"], "size": 12},
            },
            updatemenus=play_pause_menu(),
        )
        return fig

    rc_plot = mo.ui.plotly(rc_figure(rc_resistance.value), config=get_plotly_config())
    mo.output.replace(rc_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Worked example: how long does an RC circuit take to charge?": mo.md(
                r"""
        Charge a $C = 100\ \mu\text{F}$ capacitor through $R = 10\ \text{k}\Omega$ from a
        $V = 5$ V source.

        **The time constant.**

        $$\tau = R C = (10\,000\ \Omega)(100 \times 10^{-6}\ \text{F}) = 1.0\ \text{s}.$$

        **The starting current** (empty capacitor, so all the voltage is across the resistor):

        $$I_0 = \frac{V}{R} = \frac{5}{10\,000} = 0.5\ \text{mA}.$$

        **Voltage after one time constant** ($t = \tau = 1$ s):

        $$V_C = 5\left(1 - e^{-1}\right) = 5(1 - 0.368) = 5(0.632) = 3.16\ \text{V}.$$

        **Practically full** after about $5\tau = 5$ s:

        $$V_C = 5\left(1 - e^{-5}\right) = 5(1 - 0.0067) = 4.97\ \text{V} \;(99.3\%).$$

        Double the resistor to 20 kΩ and $\tau$ doubles to 2 s — everything happens half as fast.
        This simple "charge to 63% per τ" is the timing behind blinking LEDs, camera-flash
        recharge, debounced buttons, and the smoothing capacitor in every power supply.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 11. Putting it all together

        Here is one circuit that uses every tool at once: a source, a resistor in series, and a
        parallel pair — the kind of thing you'd actually meet on a breadboard. The recipe never
        changes: **collapse inward to find the total current, then expand outward to split it.**
        Watch the 2 A leave the source, cross $R_1$, split into 1 A + 1 A through the equal pair,
        and merge again on the way home. Open the box for the full walkthrough, with every number.
        """
    )
    return


@app.cell
def _(get_plotly_config, mo, series_parallel_scene):
    # V = 18 V, R₁ = 3 Ω in series with R₂ ∥ R₃ = 12 Ω ∥ 12 Ω → 2 A splitting into 1 A + 1 A.
    full_plot = mo.ui.plotly(
        series_parallel_scene(
            labels=("18 V", "R₁ = 3 Ω", "R₂ = 12 Ω", "R₃ = 12 Ω"),
            currents=(2, 1, 1),
            note="V₁ = 6 V<br>pair = 12 V",
            title="<b>The whole circuit at once — 2 A in, 1 A + 1 A through the pair</b>",
        ),
        config=get_plotly_config(),
    )
    mo.output.replace(full_plot)
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "▸ Full worked example: solve the whole circuit, step by step": mo.md(
                r"""
        **The circuit.** A $V = 18$ V source drives $R_1 = 3\ \Omega$ in series with a parallel
        pair, $R_2 = 12\ \Omega$ alongside $R_3 = 12\ \Omega$. Find every current, every voltage,
        and every power.

        **Step 1 — reduce the parallel pair.** Two equal resistors in parallel give half:

        $$R_{23} = \frac{R_2 R_3}{R_2 + R_3} = \frac{12 \times 12}{12 + 12} = \frac{144}{24}
          = 6\ \Omega.$$

        **Step 2 — total resistance (now a simple series).**

        $$R_\text{total} = R_1 + R_{23} = 3 + 6 = 9\ \Omega.$$

        **Step 3 — the main current (Ohm's law on the whole loop).**

        $$I = \frac{V}{R_\text{total}} = \frac{18}{9} = 2\ \text{A}.$$

        This full 2 A flows through $R_1$.

        **Step 4 — voltage divides between $R_1$ and the pair (KVL).**

        $$V_1 = I R_1 = 2 \times 3 = 6\ \text{V}, \qquad V_{23} = I R_{23} = 2 \times 6 = 12\ \text{V}.$$

        Check: $6 + 12 = 18$ V back to the source. ✓

        **Step 5 — the pair's 12 V drives each branch (Ohm's law per branch).**

        $$I_2 = \frac{V_{23}}{R_2} = \frac{12}{12} = 1\ \text{A}, \qquad
          I_3 = \frac{V_{23}}{R_3} = \frac{12}{12} = 1\ \text{A}.$$

        Check (KCL): $I_2 + I_3 = 1 + 1 = 2$ A = the main current. ✓

        **Step 6 — power everywhere.**

        $$P_1 = I^2 R_1 = 2^2 \times 3 = 12\ \text{W}, \qquad
          P_2 = P_3 = \frac{V_{23}^2}{R} = \frac{144}{12} = 12\ \text{W each}.$$

        Total $P = 12 + 12 + 12 = 36$ W, matching the source $P = V I = 18 \times 2 = 36$ W. ✓

        **That's the entire method.** Reduce inward, solve the simplest loop, then expand back out —
        splitting current at every junction and dividing voltage across every series step. Any DC
        resistor network, however tangled, falls to exactly these moves.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "The one-page cheat sheet: every formula in this notebook": mo.md(
                r"""
        | Quantity | Formula | In words |
        |---|---|---|
        | Ohm's law | $V = IR$ | push = flow × narrowness |
        | Power | $P = VI = I^2R = V^2/R$ | rate of energy use (watts) |
        | Energy | $E = Pt$ | watts × time (joules, or kWh) |
        | **Resistors in series** | $R = R_1 + R_2 + \cdots$ | same current; voltages add |
        | **Resistors in parallel** | $\dfrac{1}{R} = \dfrac{1}{R_1} + \dfrac{1}{R_2} + \cdots$ | same voltage; currents add |
        | Two in parallel | $R = \dfrac{R_1 R_2}{R_1 + R_2}$ | product over sum |
        | Voltage divider | $V_\text{out} = V\dfrac{R_2}{R_1+R_2}$ | series taps a fraction |
        | Current divider | $I_1 = I\dfrac{R_2}{R_1+R_2}$ | parallel splits inversely |
        | Kirchhoff current (KCL) | $\sum I_\text{in} = \sum I_\text{out}$ | charge is conserved at a node |
        | Kirchhoff voltage (KVL) | $\sum V = 0$ around a loop | energy is conserved round a loop |
        | Bridge balance | $R_1 R_4 = R_2 R_3$ | bridge current = 0 (removable) |
        | Delta → Wye | $R_A = \dfrac{R_{AB}R_{AC}}{R_{AB}+R_{BC}+R_{CA}}$ | unlocks a non-reducible network |
        | Capacitor charge | $Q = CV$ | stored charge |
        | Capacitor energy | $E = \tfrac{1}{2}CV^2$ | stored energy |
        | **Capacitors in parallel** | $C = C_1 + C_2 + \cdots$ | add (mirror of resistors) |
        | **Capacitors in series** | $\dfrac{1}{C} = \dfrac{1}{C_1} + \dfrac{1}{C_2} + \cdots$ | reciprocals add |
        | RC charging | $V_C = V\left(1 - e^{-t/RC}\right)$ | 63% per time constant |
        | Time constant | $\tau = RC$ | seconds; full by ~5τ |

        **The whole method for any resistor network:** reduce series/parallel clumps inward to one
        resistance → find the main current with Ohm's law → expand back outward, dividing voltage
        across series steps and current across parallel branches. **If it won't reduce** (a bridge or
        worse), fall back to a Δ–Y swap, or to Kirchhoff/nodal analysis, which always works.
        """
            )
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where to read more

        Every rule here is standard, checkable physics. Good next steps, for validation and depth:

        - **Feynman Lectures, Vol. II, Ch. 22 — [AC Circuits](https://www.feynmanlectures.caltech.edu/II_22.html)**
          (Kirchhoff's rules and how impedances — the AC generalisation of resistance — combine)
        - **Feynman Lectures, Vol. II, Ch. 25 — [Circuit Elements](https://www.feynmanlectures.caltech.edu/II_25.html)**
          (resistors, capacitors, and inductors as idealised parts)
        - **HyperPhysics — [Ohm's Law and DC circuits](https://hyperphysics.gsu.edu/hbase/electric/ohmlaw.html)**
          (series/parallel combinations, with interactive calculators)
        - **Wikipedia — [Wheatstone bridge](https://en.wikipedia.org/wiki/Wheatstone_bridge)** and
          **[Y-Δ transform](https://en.wikipedia.org/wiki/Y-%CE%94_transform)**
          (the diamond, its balance condition, and delta–wye conversion)
        - **HyperPhysics — [Capacitor combinations](https://hyperphysics.gsu.edu/hbase/electric/capac.html)**,
          **[charging an RC circuit](https://hyperphysics.gsu.edu/hbase/electric/capchg.html)**, and
          **[discharging](https://hyperphysics.gsu.edu/hbase/electric/capdis.html)**
        - **Wikipedia — [Series and parallel circuits](https://en.wikipedia.org/wiki/Series_and_parallel_circuits)**,
          **[Voltage divider](https://en.wikipedia.org/wiki/Voltage_divider)**,
          **[RC circuit](https://en.wikipedia.org/wiki/RC_circuit)**, and
          **[Kirchhoff's circuit laws](https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws)**
        - **All About Circuits — [free online textbook](https://www.allaboutcircuits.com/textbook/direct-current/)**
          (the friendliest full course on DC circuits, with more worked examples)

        The beauty of circuits is how far these few rules reach: from a single resistor to the power
        grid, it's Ohm, Kirchhoff, and the habit of reducing a tangle one clump at a time.
        """
    )
    return


if __name__ == "__main__":
    app.run()
