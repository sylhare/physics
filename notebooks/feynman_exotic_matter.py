import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    return go, make_subplots, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # Exotic Matter: The Key to Spacetime Engineering

        *A researcher's guide to negative energy and its possibilities*

        ---

        ## What is Exotic Matter?

        In general relativity, the curvature of spacetime is determined by the distribution
        of matter and energy through Einstein's field equations:

        $$G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

        Normal matter curves spacetime in "normal" ways—it attracts. But the equations
        don't forbid matter that curves spacetime the other way—matter that **repels**
        gravitationally. This is **exotic matter**.

        **Key property:** Exotic matter has **negative energy density** as measured by
        at least some observers. This isn't antimatter (which has positive energy) or
        dark matter (which also has positive energy). It's something far stranger.

        **Why it matters:**

        | Application | Requires |
        |-------------|----------|
        | Traversable wormholes | Negative energy to hold throat open |
        | Alcubierre warp drive | Negative energy at bubble walls |
        | Time machines | Negative energy to create closed timelike curves |
        | Warp drive optimization | Less negative energy = more feasible |

        > *"The question isn't whether exotic matter is possible—quantum mechanics says it is.
        > The question is whether enough of it can exist in the right configuration."*
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Historical Development: How We Got Here

        The story of exotic matter spans nearly a century of theoretical physics.

        **1935 — Einstein-Rosen Bridges**

        Einstein and Rosen discovered that the Schwarzschild black hole solution
        could be extended to connect two separate regions of spacetime. These
        "bridges" were the first mathematical wormholes—but they pinched off
        too quickly to traverse.

        **1948 — Casimir's Prediction**

        Hendrik Casimir predicted that two uncharged metal plates in a vacuum
        would experience an attractive force. More importantly, the energy density
        between the plates would be **negative** relative to the vacuum outside.
        This was the first concrete example of negative energy in physics.

        **1957 — Wheeler's Spacetime Foam**

        John Wheeler proposed that at the Planck scale ($10^{-35}$ m), spacetime
        itself might be a "foam" of tiny wormholes constantly forming and
        disappearing. Quantum fluctuations could briefly create exotic matter.

        **1988 — Morris & Thorne's Traversable Wormholes**

        Michael Morris and Kip Thorne asked: what would a wormhole need to be
        traversable by humans? Their answer: exotic matter at the throat, violating
        the "null energy condition." This paper launched modern wormhole physics.

        **1994 — Alcubierre's Warp Drive**

        Miguel Alcubierre showed that general relativity allows a "warp bubble"
        that could travel faster than light. The catch: it requires a shell of
        exotic matter with total negative energy equal to the mass of Jupiter
        (later optimized down, but still enormous).

        **1996 — Ford & Roman's Quantum Inequalities**

        Larry Ford and Tom Roman proved that quantum mechanics places strict
        limits on how much negative energy can exist and for how long. Nature
        seems to protect itself from unlimited exotic matter.
        """
    )
    return


@app.cell
def _(go, np):
    def create_historical_timeline():
        """Create a visual timeline of exotic matter research."""
        events = [
            (1935, "Einstein-Rosen\nBridges", "Wormholes discovered mathematically"),
            (1948, "Casimir\nEffect", "First negative energy prediction"),
            (1957, "Wheeler's\nFoam", "Quantum spacetime fluctuations"),
            (1958, "Casimir\nVerified", "Sparnaay's experiment"),
            (1988, "Morris-Thorne\nWormholes", "Traversable wormholes need exotic matter"),
            (1994, "Alcubierre\nWarp Drive", "FTL requires negative energy"),
            (1996, "Quantum\nInequalities", "Limits on negative energy"),
            (1997, "Precision\nCasimir", "Lamoreaux confirms to 5%"),
            (2011, "Casimir\nRepulsion", "Repulsive Casimir force measured"),
        ]

        years = [e[0] for e in events]
        labels = [e[1] for e in events]
        descriptions = [e[2] for e in events]

        fig = go.Figure()

        # Timeline
        fig.add_trace(go.Scatter(
            x=[1930, 2020], y=[0, 0],
            mode="lines",
            line=dict(color="white", width=2),
            showlegend=False,
        ))

        # Events
        colors = ["cyan", "yellow", "magenta", "green", "orange", "red", "purple", "cyan", "yellow"]
        for i, (year, label, desc) in enumerate(events):
            y_offset = 0.5 if i % 2 == 0 else -0.5

            # Vertical line
            fig.add_trace(go.Scatter(
                x=[year, year], y=[0, y_offset * 0.8],
                mode="lines",
                line=dict(color=colors[i], width=2),
                showlegend=False,
            ))

            # Event marker
            fig.add_trace(go.Scatter(
                x=[year], y=[0],
                mode="markers",
                marker=dict(size=12, color=colors[i]),
                showlegend=False,
            ))

            # Label
            fig.add_annotation(
                x=year, y=y_offset,
                text=f"<b>{label}</b><br><sub>{year}</sub>",
                showarrow=False,
                font=dict(size=10, color=colors[i]),
                align="center",
            )

        fig.update_layout(
            title=dict(
                text="<b>Timeline of Exotic Matter Research</b><br><sub>From mathematical curiosity to experimental physics</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Year", range=[1930, 2020], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)", dtick=10),
            yaxis=dict(range=[-1, 1], showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor="rgba(0,0,30,0.95)",
            height=400,
        )

        return fig

    timeline_fig = create_historical_timeline()
    timeline_fig
    return create_historical_timeline, timeline_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Energy Conditions: Rules That Exotic Matter Breaks

        General relativity doesn't specify what matter can exist—it just describes
        how matter curves spacetime. Einstein's equations work equally well whether
        you put in positive or negative energy. So physicists invented **energy conditions**
        as reasonable assumptions about what "physically realistic" matter should satisfy.

        Think of these as guardrails—not laws of physics themselves, but expectations
        based on all the matter we've observed. Breaking them isn't mathematically
        forbidden; it's just unusual.

        ---

        **The Weak Energy Condition (WEC):**

        $$T_{\mu\nu} u^\mu u^\nu \geq 0$$

        **What the math says:** The stress-energy tensor $T_{\mu\nu}$ describes how
        matter and energy are distributed. The 4-velocity $u^\mu$ represents an
        observer's motion through spacetime. This condition says: contract (multiply)
        these together, and you should get something non-negative.

        **What it means in plain English:** Any observer, moving at any speed in any
        direction, should measure positive energy density. No one should see negative
        energy.

        $$\rho \geq 0 \quad \text{(energy density is positive)}$$

        **Why it seems reasonable:** Everything we see—rocks, stars, light, even
        antimatter—has positive energy. A rock has positive mass-energy. A photon
        has positive energy $E = h\nu$. Even the vacuum was thought to have zero
        energy (the lowest possible).

        ---

        **The Null Energy Condition (NEC):**

        $$T_{\mu\nu} k^\mu k^\nu \geq 0$$

        **What the math says:** Now $k^\mu$ is a null vector—the 4-velocity of a
        light ray. We're asking: what does a photon "see" as it passes through?

        **What it means in plain English:** Along any light ray, the combination
        of energy density and pressure must be non-negative:

        $$\rho + p \geq 0 \quad \text{(energy density + pressure is positive)}$$

        **Why this matters:** This is the *weakest* of the classical energy conditions.
        If you violate this, you're really in exotic territory. The NEC is what
        wormholes and warp drives need to break.

        **The key insight:** Pressure contributes to gravity in general relativity!
        This seems strange—in Newtonian physics, only mass gravitates. But Einstein
        showed that pressure also curves spacetime. So even with $\rho > 0$, if
        $p < -\rho$ (extreme negative pressure), you get NEC violation.

        ---

        **The Strong Energy Condition (SEC):**

        $$\left(T_{\mu\nu} - \frac{1}{2}T g_{\mu\nu}\right) u^\mu u^\nu \geq 0$$

        **What the math says:** This is more complex—we subtract half the trace
        (total) of the stress-energy tensor. The trace $T = g^{\mu\nu}T_{\mu\nu}$
        captures the "total" content.

        **What it means in plain English:** Gravity should always be attractive.
        Matter should always pull other matter together, never push it apart.

        **The cosmic surprise:** Dark energy violates this! The accelerating
        expansion of the universe means something is pushing galaxies apart.
        Whatever dark energy is, it has $\rho + 3p < 0$ (since $p \approx -\rho$
        for a cosmological constant). So the SEC is **already violated in nature**
        on cosmic scales.

        ---

        **The Dominant Energy Condition (DEC):**

        $$T_{\mu\nu} u^\mu \text{ is future-directed and non-spacelike}$$

        **What it means:** Energy cannot flow faster than light. If you measure
        energy density and momentum density, the momentum shouldn't exceed what
        light could carry.

        This combines the WEC with causality—energy should be positive AND should
        respect the speed limit.

        *The visualization shows how different types of matter sit in the ρ-p diagram,
        and where exotic matter must live to enable spacetime engineering.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_energy_conditions_visualization():
        """Visualize the energy conditions in ρ-p space."""

        # Create ρ-p diagram
        rho = np.linspace(-2, 3, 100)
        p = np.linspace(-2, 3, 100)
        Rho, P = np.meshgrid(rho, p)

        fig = go.Figure()

        # WEC region: ρ ≥ 0
        fig.add_trace(go.Scatter(
            x=[0, 0, 3, 3, 0], y=[-2, 3, 3, -2, -2],
            fill="toself",
            fillcolor="rgba(0, 255, 255, 0.15)",
            line=dict(color="cyan", width=2),
            name="WEC satisfied (ρ ≥ 0)",
        ))

        # NEC region: ρ + p ≥ 0 (line is ρ = -p)
        fig.add_trace(go.Scatter(
            x=[-2, 3], y=[2, -3],
            mode="lines",
            line=dict(color="yellow", width=3),
            name="NEC boundary (ρ + p = 0)",
        ))

        # NEC satisfied region
        nec_x = [3, -2, 3]
        nec_y = [-3, 2, 3]
        fig.add_trace(go.Scatter(
            x=nec_x, y=nec_y,
            fill="toself",
            fillcolor="rgba(255, 255, 0, 0.1)",
            line=dict(width=0),
            name="NEC satisfied region",
        ))

        # SEC region: ρ + 3p ≥ 0 (line is ρ = -3p)
        fig.add_trace(go.Scatter(
            x=[-2, 3], y=[2/3, -1],
            mode="lines",
            line=dict(color="magenta", width=2, dash="dash"),
            name="SEC boundary (ρ + 3p = 0)",
        ))

        # Example points
        examples = [
            (1, 0, "Normal matter", "green"),
            (1, 1/3, "Radiation", "yellow"),
            (0.5, -0.5, "Dark energy (w=-1)", "orange"),
            (-0.5, 0.5, "Wormhole throat", "red"),
            (-1, -0.3, "Warp bubble wall", "red"),
        ]

        for rho_val, p_val, label, color in examples:
            fig.add_trace(go.Scatter(
                x=[rho_val], y=[p_val],
                mode="markers+text",
                marker=dict(size=12, color=color),
                text=[label],
                textposition="top right",
                textfont=dict(size=10, color=color),
                showlegend=False,
            ))

        # Axes
        fig.add_hline(y=0, line_color="white", line_width=1, opacity=0.5)
        fig.add_vline(x=0, line_color="white", line_width=1, opacity=0.5)

        # Exotic matter region label
        fig.add_annotation(
            x=-1, y=-1,
            text="<b>EXOTIC MATTER</b><br>Violates WEC & NEC",
            font=dict(size=12, color="red"),
            showarrow=False,
            bgcolor="rgba(255,0,0,0.2)",
        )

        fig.update_layout(
            title=dict(
                text="<b>Energy Conditions:</b> What 'Normal' Matter Satisfies<br><sub>Exotic matter lives in the forbidden regions</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title="Energy density ρ", range=[-2.5, 3.5], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)", zeroline=False),
            yaxis=dict(title="Pressure p", range=[-2.5, 3.5], showgrid=True,
                      gridcolor="rgba(255,255,255,0.1)", zeroline=False),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, font=dict(size=10)),
            plot_bgcolor="rgba(0,0,30,0.95)",
        )

        return fig

    energy_conditions_fig = create_energy_conditions_visualization()
    energy_conditions_fig
    return create_energy_conditions_visualization, energy_conditions_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Casimir Effect: Negative Energy is Real

        The Casimir effect is our best evidence that negative energy density exists.

        **The Setup:**

        Place two uncharged, perfectly conducting parallel plates in a vacuum,
        separated by distance $a$. The space between them is empty... or is it?

        **Quantum Vacuum:**

        Even "empty" space teems with quantum fluctuations—virtual particle-antiparticle
        pairs constantly appearing and disappearing. These fluctuations have energy,
        and they exist at all wavelengths.

        **The Key Insight:**

        Between the plates, only fluctuations with wavelengths that "fit" can exist
        (standing waves). Outside the plates, all wavelengths are allowed.

        Fewer modes inside → less vacuum energy inside → **negative energy density**
        relative to outside!

        **The Math:**

        The energy density between the plates:

        $$u = -\frac{\pi^2 \hbar c}{720 a^4}$$

        The force per unit area (Casimir pressure):

        $$F/A = -\frac{\pi^2 \hbar c}{240 a^4}$$

        For plates 100 nm apart: $F/A \approx 1$ atmosphere!

        **Experimental Verification:**

        - 1958: Sparnaay (qualitative confirmation)
        - 1997: Lamoreaux (5% precision)
        - 2001: Bressi et al. (15% using parallel plates)
        - Modern: Better than 1% precision achieved

        *The animation shows how the Casimir effect creates negative energy.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_casimir_animation():
        """Animate the Casimir effect and vacuum fluctuations."""
        n_frames = 80

        frames = []

        for i in range(n_frames):
            t = 2 * np.pi * i / n_frames

            frame_data = []

            # Plates
            plate_height = 2
            frame_data.append(go.Scatter(
                x=[-1, -1], y=[-plate_height/2, plate_height/2],
                mode="lines",
                line=dict(color="silver", width=8),
                name="Conducting plates",
            ))
            frame_data.append(go.Scatter(
                x=[1, 1], y=[-plate_height/2, plate_height/2],
                mode="lines",
                line=dict(color="silver", width=8),
                showlegend=False,
            ))

            # Vacuum fluctuations outside (all wavelengths)
            for j in range(6):
                # Left side - multiple wavelengths
                x_left = np.linspace(-4, -1.2, 100)
                wavelength = 0.3 + j * 0.2
                phase = t + j * 0.5
                y_wave = 0.15 * np.sin(2 * np.pi * x_left / wavelength + phase)
                y_offset = (j - 2.5) * 0.35
                alpha = 0.3 + 0.1 * np.sin(phase)

                frame_data.append(go.Scatter(
                    x=x_left, y=y_wave + y_offset,
                    mode="lines",
                    line=dict(color=f"rgba(100, 200, 255, {alpha})", width=1),
                    showlegend=False,
                ))

                # Right side
                x_right = np.linspace(1.2, 4, 100)
                y_wave_r = 0.15 * np.sin(2 * np.pi * x_right / wavelength + phase)
                frame_data.append(go.Scatter(
                    x=x_right, y=y_wave_r + y_offset,
                    mode="lines",
                    line=dict(color=f"rgba(100, 200, 255, {alpha})", width=1),
                    showlegend=False,
                ))

            # Inside - only modes that fit (fewer!)
            for j in range(2):  # Only 2 modes fit
                x_inside = np.linspace(-0.9, 0.9, 100)
                n_mode = j + 1
                wavelength_inside = 2 * 1.8 / n_mode  # Standing wave condition
                phase = t
                y_wave = 0.2 * np.sin(n_mode * np.pi * (x_inside + 0.9) / 1.8) * np.cos(phase)
                y_offset = (j - 0.5) * 0.6

                frame_data.append(go.Scatter(
                    x=x_inside, y=y_wave + y_offset,
                    mode="lines",
                    line=dict(color="rgba(255, 200, 100, 0.6)", width=2),
                    showlegend=False,
                ))

            # Energy density indicators
            # Outside: higher (normal vacuum)
            frame_data.append(go.Scatter(
                x=[-3], y=[1.3],
                mode="text",
                text=["ρ = 0<br>(vacuum reference)"],
                textfont=dict(size=11, color="cyan"),
                showlegend=False,
            ))

            # Inside: lower (negative!)
            frame_data.append(go.Scatter(
                x=[0], y=[1.3],
                mode="text",
                text=["<b>ρ < 0</b><br>(negative energy!)"],
                textfont=dict(size=11, color="orange"),
                showlegend=False,
            ))

            # Arrows showing attraction
            arrow_phase = 0.1 * np.sin(2 * t)
            frame_data.append(go.Scatter(
                x=[-1.5 + arrow_phase, -1.1], y=[0, 0],
                mode="lines",
                line=dict(color="red", width=3),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[1.5 - arrow_phase, 1.1], y=[0, 0],
                mode="lines",
                line=dict(color="red", width=3),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[-1.5 + arrow_phase], y=[0],
                mode="markers",
                marker=dict(size=10, color="red", symbol="triangle-right"),
                name="Casimir force",
            ))
            frame_data.append(go.Scatter(
                x=[1.5 - arrow_phase], y=[0],
                mode="markers",
                marker=dict(size=10, color="red", symbol="triangle-left"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Casimir Effect:</b> Fewer Modes Inside = Negative Energy<br><sub>Virtual fluctuations create real, measurable forces</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-4.5, 4.5], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1.5, 1.8], showgrid=False, zeroline=False, showticklabels=False),
                showlegend=True,
                legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01),
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

    casimir_fig = create_casimir_animation()
    casimir_fig
    return create_casimir_animation, casimir_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Quantum Inequalities: Nature's Limits

        If negative energy exists, why can't we just make lots of it? Nature has
        built-in limits—**quantum inequalities**.

        **Ford-Roman Inequality (1996):**

        The magnitude of negative energy $|\rho_{neg}|$ and its duration $\tau$ are
        constrained:

        $$|\rho_{neg}| \cdot \tau^4 \lesssim \frac{\hbar}{c}$$

        **What this means:**

        - Large negative energy → must be very brief
        - Long-lasting negative energy → must be very small
        - You can "borrow" negative energy, but must "pay it back" quickly

        **The Quantum Interest Conjecture:**

        When negative energy is followed by positive energy (as required), the positive
        energy must exceed the negative energy by an amount that grows with the delay.
        Like a loan with interest!

        $$E_{positive} \geq |E_{negative}| + \text{"interest"}$$

        **Numerical example:**

        To maintain $\rho = -1 \text{ kg/m}^3$ (modest by wormhole standards):

        - Allowed duration: $\tau \sim 10^{-29}$ seconds
        - That's a billion times shorter than the Planck time!

        For a wormhole requiring $\sim 10^{30}$ kg of negative mass:

        - Either concentrate it in a Planck-scale region (unmeasurable)
        - Or spread it out and violate quantum inequalities

        *This is why exotic matter is so difficult—nature guards against it.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_quantum_inequality_animation():
        """Visualize the quantum inequality constraint."""
        n_frames = 100

        frames = []

        for i in range(n_frames):
            progress = i / n_frames

            t = np.linspace(-2, 4, 500)

            frame_data = []

            # Different pulse shapes satisfying quantum inequality
            # ρ(t) * τ^4 ~ constant

            # Case 1: Brief, large negative pulse
            if progress < 0.33:
                p = progress / 0.33
                tau1 = 0.2 + 0.3 * (1 - p)  # Width decreases
                amplitude1 = 1.0 / (tau1**2)  # Amplitude increases to compensate
                rho1_neg = -amplitude1 * np.exp(-t**2 / (2 * tau1**2))
                # Must be followed by positive (interest!)
                rho1_pos = amplitude1 * 1.2 * np.exp(-(t - 1.5)**2 / (2 * (tau1 * 1.5)**2))
                rho1 = rho1_neg + rho1_pos
                title_extra = "Brief & intense (must repay quickly)"
                color = "magenta"
            elif progress < 0.66:
                # Case 2: Extended, small negative region
                p = (progress - 0.33) / 0.33
                tau2 = 0.5 + 0.5 * p
                amplitude2 = 0.3 / (tau2**2)
                rho2_neg = -amplitude2 * np.exp(-t**2 / (2 * tau2**2))
                rho2_pos = amplitude2 * 1.1 * np.exp(-(t - 2)**2 / (2 * tau2**2))
                rho1 = rho2_neg + rho2_pos
                title_extra = "Extended & weak (less interest needed)"
                color = "cyan"
            else:
                # Case 3: Show constraint curve
                p = (progress - 0.66) / 0.34
                tau3 = 0.3
                amplitude3 = 0.5 + 0.5 * np.sin(4 * np.pi * p)
                rho1 = -amplitude3 * np.exp(-t**2 / (2 * tau3**2))
                rho1 += amplitude3 * 1.3 * np.exp(-(t - 1.5)**2 / (2 * (tau3 * 1.2)**2))
                title_extra = "Constraint: |ρ| × τ⁴ ≤ ℏ/c"
                color = "yellow"

            # Energy density plot
            frame_data.append(go.Scatter(
                x=t, y=rho1,
                mode="lines",
                fill="tozeroy",
                line=dict(color=color, width=2),
                fillcolor=f"rgba(255, 255, 0, 0.2)" if color == "yellow"
                         else ("rgba(255, 0, 255, 0.2)" if color == "magenta"
                               else "rgba(0, 255, 255, 0.2)"),
                name="Energy density ρ(t)",
            ))

            # Zero line
            frame_data.append(go.Scatter(
                x=[-2, 4], y=[0, 0],
                mode="lines",
                line=dict(color="white", width=1),
                showlegend=False,
            ))

            # Negative region label
            frame_data.append(go.Scatter(
                x=[0], y=[min(rho1) * 0.5],
                mode="text",
                text=["BORROW"],
                textfont=dict(size=12, color="red"),
                showlegend=False,
            ))

            # Positive region label
            frame_data.append(go.Scatter(
                x=[1.5], y=[max(rho1) * 0.7],
                mode="text",
                text=["REPAY\n(with interest)"],
                textfont=dict(size=10, color="green"),
                showlegend=False,
            ))

            # Title with current state
            frame_data.append(go.Scatter(
                x=[1], y=[2],
                mode="text",
                text=[f"<b>{title_extra}</b>"],
                textfont=dict(size=12, color=color),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Quantum Inequalities:</b> Borrow Negative Energy, Pay It Back<br><sub>Nature enforces energy conservation with 'interest'</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Time", range=[-2.5, 4.5], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(title="Energy density ρ", range=[-3, 3], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)"),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
                plot_bgcolor="rgba(0,0,30,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
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
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    quantum_inequality_fig = create_quantum_inequality_animation()
    quantum_inequality_fig
    return create_quantum_inequality_animation, quantum_inequality_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Squeezed Vacuum States: Engineering Negative Energy

        Beyond the static Casimir effect, quantum optics offers another source of
        negative energy: **squeezed vacuum states**.

        **The Quantum Vacuum:**

        In quantum mechanics, even empty space has fluctuations. For the electromagnetic
        field, this means the electric field $E$ fluctuates randomly around zero:

        $$\langle E \rangle = 0, \quad \langle E^2 \rangle = \frac{\hbar \omega}{2\epsilon_0 V} \neq 0$$

        These fluctuations are symmetric—equally likely positive or negative.

        **Squeezing the Vacuum:**

        Using nonlinear optical crystals, we can "squeeze" the vacuum—reduce fluctuations
        in one property (say, $E$) at the cost of increasing them in another (say, $B$).

        $$\Delta E_{squeezed} < \Delta E_{vacuum}$$

        During part of each cycle, the squeezed vacuum has **less energy than normal
        vacuum**—that's negative energy density!

        **Mathematical Description:**

        A squeezed state has uncertainty relations:

        $$\Delta X_1 = e^{-r} \Delta X_{vac}, \quad \Delta X_2 = e^{+r} \Delta X_{vac}$$

        where $r$ is the squeezing parameter. The energy density oscillates:

        $$\rho(t) = \rho_{vac} \left[\cosh(2r) - \sinh(2r)\cos(2\omega t)\right]$$

        For part of each cycle, $\rho < \rho_{vac} = 0$ (negative!).

        **Experimental Status:**

        - Squeezed light is routinely produced in labs
        - Used in LIGO to improve gravitational wave detection
        - Squeezing factors of $r > 1$ achieved
        - But total integrated energy is still positive (quantum inequalities!)

        *The animation shows how squeezing creates periodic negative energy.*
        """
    )
    return


@app.cell
def _(go, np):
    def create_squeezed_vacuum_animation():
        """Visualize squeezed vacuum states and negative energy density."""
        n_frames = 80

        frames = []

        for i in range(n_frames):
            t = 2 * np.pi * i / 40  # Two full cycles
            time_array = np.linspace(0, 4 * np.pi, 200)

            # Squeezing parameter
            r = 1.0

            # Normal vacuum fluctuations (unit circle in phase space)
            theta_circle = np.linspace(0, 2 * np.pi, 100)
            x_vac = 0.8 * np.cos(theta_circle)
            y_vac = 0.8 * np.sin(theta_circle)

            # Squeezed vacuum (ellipse)
            x_squeeze = 0.8 * np.exp(-r) * np.cos(theta_circle)
            y_squeeze = 0.8 * np.exp(r) * np.sin(theta_circle)

            # Rotate ellipse with time
            angle = t / 2
            x_sq_rot = x_squeeze * np.cos(angle) - y_squeeze * np.sin(angle)
            y_sq_rot = x_squeeze * np.sin(angle) + y_squeeze * np.cos(angle)

            # Energy density over time
            rho = np.cosh(2 * r) - np.sinh(2 * r) * np.cos(2 * time_array)
            # Normalize so vacuum = 0
            rho_normalized = rho - 1

            # Current time marker
            current_rho = np.cosh(2 * r) - np.sinh(2 * r) * np.cos(2 * t) - 1

            frame_data = []

            # Phase space plot (left side concept)
            # Normal vacuum circle
            frame_data.append(go.Scatter(
                x=x_vac - 5, y=y_vac,
                mode="lines",
                line=dict(color="cyan", width=2, dash="dash"),
                name="Normal vacuum",
            ))

            # Squeezed ellipse
            frame_data.append(go.Scatter(
                x=x_sq_rot - 5, y=y_sq_rot,
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 200, 0, 0.3)",
                line=dict(color="yellow", width=2),
                name="Squeezed vacuum",
            ))

            # Current field value (point on ellipse)
            phase_angle = t
            x_point = 0.8 * np.exp(-r) * np.cos(phase_angle)
            y_point = 0.8 * np.exp(r) * np.sin(phase_angle)
            x_point_rot = x_point * np.cos(angle) - y_point * np.sin(angle)
            y_point_rot = x_point * np.sin(angle) + y_point * np.cos(angle)

            frame_data.append(go.Scatter(
                x=[x_point_rot - 5], y=[y_point_rot],
                mode="markers",
                marker=dict(size=10, color="white"),
                name="Field state",
            ))

            # Energy density plot (right side)
            frame_data.append(go.Scatter(
                x=time_array, y=rho_normalized,
                mode="lines",
                line=dict(color="magenta", width=2),
                fill="tozeroy",
                fillcolor="rgba(255, 0, 255, 0.2)",
                name="Energy density ρ(t)",
            ))

            # Zero line
            frame_data.append(go.Scatter(
                x=[0, 4 * np.pi], y=[0, 0],
                mode="lines",
                line=dict(color="white", width=1),
                showlegend=False,
            ))

            # Current time marker
            frame_data.append(go.Scatter(
                x=[t], y=[current_rho],
                mode="markers",
                marker=dict(size=12, color="white", symbol="star"),
                name=f"ρ = {current_rho:.2f}",
            ))

            # Negative region shading
            neg_times = time_array[rho_normalized < 0]
            if len(neg_times) > 0:
                frame_data.append(go.Scatter(
                    x=[neg_times[0], neg_times[-1]],
                    y=[-0.1, -0.1],
                    mode="text",
                    text=["← NEGATIVE →", ""],
                    textfont=dict(size=10, color="red"),
                    showlegend=False,
                ))

            # Labels
            frame_data.append(go.Scatter(
                x=[-5], y=[1.5],
                mode="text",
                text=["<b>Phase Space</b>"],
                textfont=dict(size=11, color="white"),
                showlegend=False,
            ))

            frame_data.append(go.Scatter(
                x=[6], y=[3],
                mode="text",
                text=["<b>Energy Density</b>"],
                textfont=dict(size=11, color="white"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Squeezed Vacuum:</b> Engineering Negative Energy<br><sub>Squeeze fluctuations in one direction, expand in another</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-7, 14], showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(range=[-2, 4], showgrid=False, showticklabels=False, zeroline=False),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, font=dict(size=10)),
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

    squeezed_vacuum_fig = create_squeezed_vacuum_animation()
    squeezed_vacuum_fig
    return create_squeezed_vacuum_animation, squeezed_vacuum_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## What Would It Take? Research Directions

        As a researcher, how might you approach making exotic matter practical?

        ### Direction 1: Scale Up the Casimir Effect

        **Current status:** Casimir energy is tiny—about $10^{-3}$ J/m³ at 100 nm separation.

        **Potential approaches:**

        - **Nanostructured metamaterials:** Engineer surfaces to enhance Casimir effect
        - **Dynamic Casimir effect:** Moving mirrors can convert vacuum fluctuations to
          real photons—could this work in reverse?
        - **Casimir cavities with special geometry:** Certain shapes might concentrate
          negative energy

        **The challenge:** Even optimistic estimates give energy densities far below
        what's needed. You'd need $10^{40}$ enhancement to reach wormhole scales.

        ### Direction 2: Topological Effects

        **The idea:** Some quantum field configurations have topologically protected
        negative energy regions.

        - **Cosmic strings:** Theoretical line-like defects in spacetime
        - **Domain walls:** Boundaries between different vacuum states
        - **Quantum vortices:** In superconductors and superfluids

        **Current status:** Mostly theoretical. No way to create or control these at
        useful scales.

        ### Direction 3: Quantum Gravity Loopholes

        **The hope:** Quantum inequalities were derived in flat spacetime. Perhaps
        curved spacetime or full quantum gravity allows exceptions?

        - **Near black hole horizons:** Extreme curvature might enable exotic matter
        - **Planck scale effects:** At $10^{-35}$ m, our theories break down
        - **String theory compactifications:** Extra dimensions might help

        **Current status:** We don't have a theory of quantum gravity, so this is
        speculative.
        """
    )
    return


@app.cell
def _(go, np):
    def create_research_directions_visualization():
        """Visualize the gap between what we have and what we need."""

        # Energy density scale (log scale)
        categories = [
            "Casimir (100nm)",
            "Casimir (1nm)",
            "Best squeezed\nlight",
            "Optimized\nwarp drive",
            "Original\nwarp drive",
            "Wormhole\nthroat",
        ]

        # Energy densities in J/m³ (approximate)
        values = [
            1e-3,      # Casimir at 100nm
            1e9,       # Casimir at 1nm (scales as 1/a^4)
            1e2,       # Squeezed vacuum (lab scale)
            1e47,      # Optimized Alcubierre
            1e65,      # Original Alcubierre
            1e55,      # Wormhole
        ]

        colors = ["cyan", "cyan", "yellow", "red", "red", "red"]

        fig = go.Figure()

        # Bar chart
        fig.add_trace(go.Bar(
            x=categories,
            y=np.log10(values),
            marker_color=colors,
            text=[f"10^{int(np.log10(v))}" for v in values],
            textposition="outside",
            textfont=dict(size=12),
        ))

        # Achievable line
        fig.add_hline(y=10, line_dash="dash", line_color="green",
                     annotation_text="Current achievable")

        # Need line
        fig.add_hline(y=50, line_dash="dash", line_color="red",
                     annotation_text="Minimum for spacetime engineering")

        # Gap annotation
        fig.add_annotation(
            x=2.5, y=30,
            text="<b>THE GAP</b><br>~40 orders of magnitude",
            font=dict(size=14, color="orange"),
            showarrow=False,
            bgcolor="rgba(255,165,0,0.2)",
        )

        fig.update_layout(
            title=dict(
                text="<b>The Exotic Matter Challenge:</b> What We Have vs What We Need<br><sub>Negative energy density (log scale, J/m³)</sub>",
                font=dict(size=16),
            ),
            xaxis=dict(title=""),
            yaxis=dict(title="log₁₀(|ρ|) in J/m³", range=[0, 70]),
            plot_bgcolor="rgba(0,0,30,0.95)",
            showlegend=False,
        )

        return fig

    research_fig = create_research_directions_visualization()
    research_fig
    return create_research_directions_visualization, research_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Experimental Validation: How to Test

        Even without building a wormhole, we can test exotic matter physics:

        ### Test 1: Precision Casimir Measurements

        **Goal:** Verify quantum field theory predictions to extreme precision.

        **Current:** ~1% agreement between theory and experiment.

        **Future directions:**
        - Different geometries (spheres, cylinders, corrugated plates)
        - Different materials (conductors, dielectrics, metamaterials)
        - Dynamic Casimir effect (moving mirrors creating photons)
        - Thermal corrections at different temperatures

        ### Test 2: Gravitational Effects of Negative Energy

        **The idea:** If negative energy exists, it should produce *repulsive* gravity.

        **Challenges:**
        - Casimir energy is far too weak to measure gravitationally
        - Would need $\sim 10^{20}$ enhancement to detect with current technology

        **Future:** Space-based experiments with better isolation from noise.

        ### Test 3: Analog Gravity Systems

        **The idea:** Simulate curved spacetime using other physical systems.

        **Examples:**
        - Sound waves in moving fluids → "acoustic black holes"
        - Light in nonlinear media → "optical event horizons"
        - BECs (Bose-Einstein Condensates) → quantum vacuum analogues

        **What we can learn:**
        - Hawking radiation analogues (confirmed in 2019!)
        - Behavior of quantum fields in curved space
        - Possibly negative energy dynamics

        ### Test 4: Quantum Information Approaches

        **Recent insight:** Negative energy is related to quantum entanglement.

        The **Quantum Null Energy Condition (QNEC):**

        $$\langle T_{kk} \rangle \geq \frac{\hbar}{2\pi} S''$$

        Energy density bounded by the second derivative of entanglement entropy!

        **Implication:** Creating negative energy might require creating specific
        entanglement patterns. Quantum computers might help explore this.
        """
    )
    return


@app.cell
def _(go, np):
    def create_analog_gravity_animation():
        """Visualize analog gravity in a flowing fluid."""
        n_frames = 60

        frames = []

        for i in range(n_frames):
            t = i / n_frames

            frame_data = []

            # Flowing fluid (varying velocity)
            x = np.linspace(-5, 5, 50)
            y = np.linspace(-2, 2, 20)
            X, Y = np.meshgrid(x, y)

            # Fluid velocity profile (faster in center, simulating drain)
            # Creates acoustic horizon where flow speed = sound speed
            v_flow = 1.5 / (1 + 0.3 * X**2)  # Peaks at center

            # Sound speed (constant)
            c_sound = 1.0

            # Horizon is where v_flow = c_sound
            horizon_x = np.sqrt((1.5 / c_sound - 1) / 0.3) if 1.5 > c_sound else 0

            # Sound waves trying to propagate upstream
            wave_positions = []
            for wave_start in [-4, -3, -2, -1, 0, 1, 2, 3]:
                # Wave position depends on local flow velocity
                local_v = 1.5 / (1 + 0.3 * wave_start**2)
                wave_x = wave_start + (c_sound - local_v) * t * 3

                # Waves inside horizon get swept in
                if abs(wave_start) < horizon_x:
                    wave_x = wave_start - local_v * t * 2  # Swept inward
                wave_positions.append((wave_x, wave_start))

            # Draw flow field
            for j in range(0, len(x), 3):
                for k in range(0, len(y), 2):
                    vx = v_flow[k, j]
                    frame_data.append(go.Scatter(
                        x=[X[k, j], X[k, j] - vx * 0.3],
                        y=[Y[k, j], Y[k, j]],
                        mode="lines",
                        line=dict(color=f"rgba(100, 150, 255, {min(vx/1.5, 1) * 0.5})", width=1),
                        showlegend=False,
                    ))

            # Acoustic horizon
            frame_data.append(go.Scatter(
                x=[horizon_x, horizon_x], y=[-2, 2],
                mode="lines",
                line=dict(color="red", width=3, dash="dash"),
                name="Acoustic horizon (v = c_sound)",
            ))
            frame_data.append(go.Scatter(
                x=[-horizon_x, -horizon_x], y=[-2, 2],
                mode="lines",
                line=dict(color="red", width=3, dash="dash"),
                showlegend=False,
            ))

            # Sound waves
            for wave_x, start_x in wave_positions:
                if abs(start_x) < horizon_x:
                    color = "red"  # Trapped
                else:
                    color = "cyan"  # Can escape

                frame_data.append(go.Scatter(
                    x=[wave_x], y=[0],
                    mode="markers",
                    marker=dict(size=8, color=color, symbol="circle"),
                    showlegend=False,
                ))

            # Central "drain" (analogous to black hole)
            frame_data.append(go.Scatter(
                x=[0], y=[0],
                mode="markers",
                marker=dict(size=20, color="black", line=dict(color="white", width=2)),
                name="Drain (analog black hole)",
            ))

            # Labels
            frame_data.append(go.Scatter(
                x=[3], y=[1.5],
                mode="text",
                text=["Sound escapes ↗"],
                textfont=dict(size=10, color="cyan"),
                showlegend=False,
            ))
            frame_data.append(go.Scatter(
                x=[0], y=[1.5],
                mode="text",
                text=["Sound trapped ↓"],
                textfont=dict(size=10, color="red"),
                showlegend=False,
            ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>Analog Gravity:</b> Acoustic Black Hole in Flowing Fluid<br><sub>Sound waves behave like light near a black hole horizon</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(title="Position", range=[-5.5, 5.5], showgrid=True,
                          gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(title="", range=[-2.5, 2.5], showgrid=False, showticklabels=False),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, font=dict(size=10)),
                plot_bgcolor="rgba(0,0,50,0.95)",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        y=-0.15,
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
                margin=dict(b=80),
            ),
            frames=frames,
        )

        return fig

    analog_gravity_fig = create_analog_gravity_animation()
    analog_gravity_fig
    return create_analog_gravity_animation, analog_gravity_fig


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## The Path Forward: A Research Roadmap

        If you wanted to make exotic matter practical, here's a possible roadmap:

        ### Phase 1: Foundations (Now - 2030)

        **Goals:**
        - Complete precision tests of quantum vacuum effects
        - Develop better theoretical understanding of quantum inequalities
        - Explore connections between entanglement and negative energy
        - Create high-fidelity analog gravity experiments

        **Key questions:**
        - Are quantum inequalities fundamental or approximate?
        - Can topological effects concentrate negative energy?
        - What does quantum gravity say about energy conditions?

        ### Phase 2: Enhancement (2030 - 2050)

        **Goals:**
        - Engineer metamaterials that enhance Casimir effect by 10-100×
        - Develop dynamic Casimir systems for controllable negative energy
        - Test gravitational effects of Casimir cavities (if detectable)
        - Advance quantum computing to simulate exotic matter configurations

        **Key questions:**
        - Can we beat classical limits using quantum effects?
        - Do curved spacetime regions allow more negative energy?
        - Can we create macroscopic squeezed vacuum states?

        ### Phase 3: Spacetime Engineering (2050+)

        **Goals:**
        - If fundamental barriers can be overcome, develop applications
        - Microscale wormhole experiments (if possible)
        - Warp field interferometry (detecting spacetime distortion)

        **Key questions:**
        - Is nature's protection of chronology absolute?
        - Can quantum gravity enable what classical GR forbids?
        - Are there completely new approaches we haven't thought of?

        ---

        > *"The important thing is not to stop questioning. Curiosity has its own
        > reason for existing."* — Albert Einstein
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Making the Mathematics Work: Theoretical Approaches

        Let's be bold. If we were researchers trying to make exotic matter viable,
        what theoretical frameworks might we explore? Here are the most promising
        approaches, with the mathematics that might make them work.

        ---

        ### Approach 1: Exploiting Quantum Inequality Loopholes

        The Ford-Roman quantum inequalities were derived with specific assumptions:
        - Flat (Minkowski) spacetime
        - Free (non-interacting) quantum fields
        - Standard vacuum state

        **What if we relax these assumptions?**

        **Curved Spacetime Loophole:**

        In curved spacetime, the inequalities become:

        $$\bar{\rho} \geq -\frac{C(\text{curvature}) \cdot \hbar}{\tau_0^4}$$

        The constant $C$ depends on the local spacetime curvature. Near a black hole
        or in a highly curved region, $C$ might be larger, allowing more negative energy!

        **The research question:** Can we find a self-consistent solution where
        the exotic matter creates just enough curvature to allow its own existence?

        This is like asking: can the wormhole hold itself open?

        **Mathematical condition for self-consistency:**

        $$G_{\mu\nu}[\rho_{exotic}] = 8\pi T_{\mu\nu}[\rho_{exotic}]$$

        where the geometry $G$ created by the exotic matter $\rho$ must be exactly
        the geometry needed for that matter to exist within quantum inequality bounds.

        ---

        ### Approach 2: Interacting Field Enhancement

        Free fields have strict quantum inequalities. But real fields interact—
        photons scatter off photons (via virtual electron loops), quarks exchange
        gluons, etc.

        **The key insight:** Interactions can create correlations that modify
        vacuum fluctuations in ways that might evade the standard inequalities.

        **Example: Nonlinear QED**

        In strong electromagnetic fields, QED becomes nonlinear. The effective
        Lagrangian includes terms like:

        $$\mathcal{L}_{eff} = \frac{1}{2}(E^2 - B^2) + \frac{\alpha^2}{90 m_e^4}
        \left[(E^2 - B^2)^2 + 7(E \cdot B)^2\right] + ...$$

        These nonlinear corrections modify vacuum energy. In principle, clever
        field configurations might produce larger negative energy densities.

        **The research question:** Can nonlinear field interactions create
        "vacuum engineering" that amplifies negative energy?

        ---

        ### Approach 3: Topological Negative Energy

        Some quantum field configurations have negative energy that's **topologically
        protected**—it can't be smoothly deformed away.

        **Example: The Kink Solution**

        In a scalar field theory with potential $V(\phi) = \lambda(\phi^2 - v^2)^2$,
        there's a solution called a "kink" that interpolates between vacua:

        $$\phi(x) = v \tanh\left(\frac{x}{\delta}\right)$$

        The energy density of the kink has both positive and negative regions!

        **Why this matters:** The negative energy region is stable—it's protected
        by the topology of the field configuration. You can't remove it without
        destroying the entire structure.

        **The research question:** Can we create stable topological defects in
        3+1 dimensions that have macroscopic negative energy regions?

        ---

        ### Approach 4: Extra Dimensions (String Theory)

        String theory requires extra spatial dimensions, typically compactified
        (curled up) at small scales. This changes everything about energy conditions.

        **Kaluza-Klein reduction:**

        When you "dimensionally reduce" from higher dimensions, what looks like
        the energy-momentum tensor in 4D is actually a projection of a higher-
        dimensional object:

        $$T_{\mu\nu}^{(4D)} = T_{\mu\nu}^{(10D)} + \text{(terms from extra dimensions)}$$

        **The opportunity:** The extra terms can contribute negative energy density
        in our 4D world, even if the full 10D theory satisfies energy conditions!

        **Mathematical setup:**

        In 10D string theory, the metric is:

        $$ds^2 = g_{\mu\nu}dx^\mu dx^\nu + g_{mn}dy^m dy^n$$

        where $y^m$ are the compact extra dimensions. Warping these dimensions
        (making them vary over 4D space) creates effective 4D stress-energy:

        $$T_{\mu\nu}^{eff} = -\frac{1}{8\pi G} G_{\mu\nu}^{(extra)}$$

        This can be negative!

        ---

        ### Approach 5: Modified Gravity

        What if gravity itself works differently than Einstein thought?

        **f(R) gravity:**

        Replace the Einstein-Hilbert action with a more general function:

        $$S = \int d^4x \sqrt{-g} \left[\frac{f(R)}{16\pi G} + \mathcal{L}_m\right]$$

        where $f(R)$ is some function of the Ricci scalar $R$.

        **What this does:** The modified field equations have extra terms that
        can mimic the effects of exotic matter without requiring actual negative
        energy:

        $$G_{\mu\nu} + E_{\mu\nu}[f(R)] = 8\pi G T_{\mu\nu}$$

        where $E_{\mu\nu}$ is an "effective stress-energy" from the modified gravity.

        **The opportunity:** Perhaps wormholes and warp drives don't need exotic
        matter—they just need the right modified gravity theory!

        **Current status:** Some f(R) theories allow wormholes without exotic matter.
        But these theories must also match observations (solar system tests,
        gravitational waves, etc.), which constrains them heavily.

        ---

        ### The Grand Challenge: A Self-Consistent Framework

        What we really need is a theoretical framework where:

        1. **Quantum field theory** is consistent (no infinities, sensible vacuum)
        2. **General relativity** is satisfied (Einstein's equations hold)
        3. **Energy conditions can be violated** in controlled ways
        4. **Causality is protected** (no grandfather paradoxes)
        5. **The math all fits together** self-consistently

        This might require:
        - A complete theory of quantum gravity
        - New understanding of the vacuum state
        - Novel topological configurations
        - Or physics we haven't imagined yet

        **The optimist's view:** We've been surprised before. Quantum mechanics,
        relativity, and dark energy all violated previous assumptions about
        how nature "should" work.

        **The realist's view:** The 40 orders of magnitude gap is enormous. Even
        if loopholes exist, exploiting them may be forever beyond technology.

        **The researcher's view:** The only way to know is to keep investigating.
        """
    )
    return


@app.cell
def _(go, np):
    def create_self_consistency_visualization():
        """Visualize the self-consistency challenge for exotic matter."""
        n_frames = 80

        frames = []

        for i in range(n_frames):
            progress = i / n_frames

            # Show the feedback loop: exotic matter -> curvature -> allows exotic matter

            # Circle representing the self-consistency condition
            theta = np.linspace(0, 2 * np.pi, 100)
            circle_x = 2 * np.cos(theta)
            circle_y = 2 * np.sin(theta)

            # Arrows showing the feedback loop
            arrow_angle = 2 * np.pi * progress

            # Three stages of the loop
            stages = [
                (0, "Exotic Matter\n(negative ρ)"),
                (2*np.pi/3, "Spacetime\nCurvature"),
                (4*np.pi/3, "Modified\nQuantum Bounds"),
            ]

            frame_data = []

            # Central label
            frame_data.append(go.Scatter(
                x=[0], y=[0],
                mode="text",
                text=["<b>Self-Consistency</b><br>Challenge"],
                textfont=dict(size=14, color="white"),
                showlegend=False,
            ))

            # Draw stages
            for angle, label in stages:
                x = 3 * np.cos(angle)
                y = 3 * np.sin(angle)

                # Stage marker
                frame_data.append(go.Scatter(
                    x=[x], y=[y],
                    mode="markers+text",
                    marker=dict(size=40, color="rgba(100,100,255,0.5)",
                               line=dict(color="cyan", width=2)),
                    text=[label],
                    textposition="middle center",
                    textfont=dict(size=10, color="white"),
                    showlegend=False,
                ))

            # Animated arrows between stages
            for j, (angle, _) in enumerate(stages):
                next_angle = stages[(j + 1) % 3][0]

                # Arrow from this stage to next
                mid_angle = (angle + next_angle) / 2
                if j == 2:  # Handle wrap-around
                    mid_angle = angle + np.pi/3

                # Arrow position based on animation
                arrow_progress = (progress * 3 - j) % 1

                if j == int(progress * 3) % 3:
                    # This arrow is active
                    start_x = 3 * np.cos(angle) + 0.5 * np.cos(angle + np.pi/2)
                    start_y = 3 * np.sin(angle) + 0.5 * np.sin(angle + np.pi/2)
                    end_x = 3 * np.cos(next_angle) - 0.5 * np.cos(next_angle + np.pi/2)
                    end_y = 3 * np.sin(next_angle) - 0.5 * np.sin(next_angle + np.pi/2)

                    # Interpolate
                    arrow_x = start_x + arrow_progress * (end_x - start_x)
                    arrow_y = start_y + arrow_progress * (end_y - start_y)

                    frame_data.append(go.Scatter(
                        x=[arrow_x], y=[arrow_y],
                        mode="markers",
                        marker=dict(size=15, color="yellow", symbol="circle"),
                        name="Energy flow",
                    ))

            # Curved arrows (static)
            for j in range(3):
                angle_start = stages[j][0] + 0.3
                angle_end = stages[(j+1) % 3][0] - 0.3

                if j == 2:
                    angles = np.linspace(angle_start, angle_end + 2*np.pi, 30)
                else:
                    angles = np.linspace(angle_start, angle_end, 30)

                arc_x = 3 * np.cos(angles)
                arc_y = 3 * np.sin(angles)

                frame_data.append(go.Scatter(
                    x=arc_x, y=arc_y,
                    mode="lines",
                    line=dict(color="rgba(255,255,0,0.5)", width=2),
                    showlegend=False,
                ))

            # Equations
            equations = [
                (4, 2.5, "G<sub>μν</sub> = 8πT<sub>μν</sub>"),
                (4, -2.5, "ρ<sub>neg</sub> · τ<sup>4</sup> ≤ ℏ/c"),
            ]

            for x, y, eq in equations:
                frame_data.append(go.Scatter(
                    x=[x], y=[y],
                    mode="text",
                    text=[eq],
                    textfont=dict(size=11, color="cyan"),
                    showlegend=False,
                ))

            frames.append(go.Frame(data=frame_data, name=str(i)))

        fig = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(
                    text="<b>The Self-Consistency Challenge:</b><br><sub>Can exotic matter create the conditions needed for its own existence?</sub>",
                    font=dict(size=16),
                ),
                xaxis=dict(range=[-5, 6], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-4, 4], showgrid=False, zeroline=False, showticklabels=False,
                          scaleanchor="x"),
                showlegend=False,
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

    self_consistency_fig = create_self_consistency_visualization()
    self_consistency_fig
    return create_self_consistency_visualization, self_consistency_fig


@app.cell
def _(mo):
    mo.accordion(
        {
            "Mathematical Deep Dive: Deriving Quantum Inequalities": mo.md(
                r"""
        **The Ford-Roman Derivation (simplified):**

        Start with the stress-energy tensor for a quantum field:

        $$\langle T_{\mu\nu} \rangle = \langle 0 | T_{\mu\nu} | 0 \rangle + \text{(state-dependent part)}$$

        For a free scalar field in the vacuum state, average energy density is zero
        (after renormalization). But for excited states, it can fluctuate.

        **Key insight:** Sample the energy density along an observer's worldline with
        a sampling function $f(t)$:

        $$\bar{\rho} = \int_{-\infty}^{\infty} \langle \rho(t) \rangle f(t)^2 \, dt$$

        **Result:** For any physically realizable quantum state:

        $$\bar{\rho} \geq -\frac{C \hbar}{\tau_0^4}$$

        where $\tau_0$ is the characteristic time scale of the sampling function and
        $C$ is a numerical constant (depends on field type, dimensions, etc.).

        **Physical meaning:** You cannot make $\bar{\rho}$ arbitrarily negative. The
        more you try to localize the negative energy (smaller $\tau_0$), the less
        negative it can be (inequality gets tighter).

        **For 4D Minkowski space, massless scalar field:**

        $$\bar{\rho} \geq -\frac{3}{32\pi^2} \frac{\hbar c}{\tau_0^4}$$

        **Numerical example:**
        For $\tau_0 = 10^{-15}$ s (femtosecond laser pulse):

        $$|\bar{\rho}_{max}| \sim 10^{24} \text{ J/m}^3$$

        Still 20+ orders of magnitude short of warp drive requirements!
        """
            ),
            "Mathematical Deep Dive: The Casimir Effect": mo.md(
                r"""
        **Setup:** Two parallel perfectly conducting plates separated by distance $a$.

        **Vacuum energy between plates:**

        The electromagnetic field must satisfy boundary conditions (E parallel = 0 at
        plates). Only discrete modes are allowed:

        $$k_n = \frac{n\pi}{a}, \quad n = 1, 2, 3, ...$$

        Each mode has zero-point energy $\frac{1}{2}\hbar\omega_n$. Sum over all modes:

        $$E_{between} = \frac{\hbar c}{2} \sum_{n=1}^{\infty} \int \frac{d^2k_\perp}{(2\pi)^2}
        \sqrt{k_\perp^2 + \frac{n^2\pi^2}{a^2}}$$

        This sum diverges! But the energy *outside* the plates also diverges. The
        *difference* is finite.

        **Regularization (zeta function method):**

        $$E = \frac{\hbar c \pi^2}{720 a^3} A$$

        where $A$ is the plate area.

        **Energy density:**

        $$u = -\frac{\pi^2 \hbar c}{720 a^4} < 0$$

        **The minus sign is crucial:** Less vacuum energy inside than outside means
        negative energy density relative to the vacuum.

        **Casimir force:**

        $$F = -\frac{dE}{da} = -\frac{\pi^2 \hbar c}{240 a^4} A$$

        Negative force = attraction.

        **Numerical values at $a = 100$ nm:**
        - Force: $F/A \approx 1.3 \times 10^{-3}$ N/m² ≈ 1 mPa
        - Energy density: $u \approx -10^{-3}$ J/m³
        """
            ),
            "Open Questions in Exotic Matter Research": mo.md(
                r"""
        **Fundamental Questions:**

        1. **Are quantum inequalities exact or approximate?**
           - Derived in flat spacetime—do they hold in curved spacetime?
           - Derived for free fields—what about interacting fields?
           - Do non-perturbative effects allow violations?

        2. **What happens at the Planck scale?**
           - Quantum gravity might change energy conditions
           - Spacetime foam could provide natural negative energy
           - String theory suggests extra dimensions—do they help?

        3. **Is the chronology protection conjecture true?**
           - Hawking proposed that physics prevents time machines
           - Is this a fundamental principle or emergent behavior?
           - What mechanism enforces it?

        **Practical Questions:**

        4. **Can metamaterials enhance Casimir effects significantly?**
           - Some designs show 10-100× enhancement
           - Is there a fundamental limit?
           - Can we achieve "Casimir batteries"?

        5. **Can quantum computers simulate exotic matter?**
           - Quantum simulation of curved spacetime
           - Entanglement as a source of negative energy
           - Tensor networks and energy conditions

        6. **What's the smallest testable wormhole?**
           - Planck-scale wormholes are unobservable
           - Is there a "minimum viable wormhole"?
           - What signatures would we look for?

        **Speculative Questions:**

        7. **Could advanced civilizations have solved this?**
           - The "Fermi paradox" angle
           - Signs of spacetime engineering in cosmological data
           - SETI for warp signatures

        8. **Is our universe already exotic?**
           - Dark energy violates the strong energy condition
           - Inflation required brief violation of energy conditions
           - Is exotic matter more natural than we think?
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

        ## Summary: The State of Exotic Matter

        | Aspect | Current Status |
        |--------|----------------|
        | **Existence** | Proven (Casimir effect, squeezed states) |
        | **Magnitude** | ~40 orders of magnitude below needs |
        | **Duration** | Quantum inequalities limit time × magnitude |
        | **Control** | Limited (static Casimir, optical squeezing) |
        | **Theory** | Well-understood in QFT; gaps at quantum gravity |

        **What we know:**

        1. Negative energy density **exists**—the Casimir effect is real and measured
        2. Quantum mechanics places **strict limits** on how much can exist
        3. Current technology produces negative energy **far too weak** for spacetime engineering
        4. **Fundamental barriers** may exist, but we don't fully understand them yet

        **What we don't know:**

        1. Whether quantum inequalities are **exact** or have loopholes
        2. What **quantum gravity** says about energy conditions
        3. Whether **new physics** could enable macroscopic exotic matter
        4. If nature has an **absolute prohibition** on time machines

        ---

        > *"We are at the very beginning of time for the human race. It is not
        > unreasonable that we grapple with problems. But there are tens of thousands
        > of years in the future. Our responsibility is to do what we can, learn what
        > we can, improve the solutions, and pass them on."*
        > — Richard Feynman

        The quest for exotic matter isn't just about warp drives and wormholes—it's
        about understanding the deepest structure of reality. Whether or not we ever
        engineer spacetime, the journey teaches us about quantum fields, gravity, and
        the nature of the vacuum itself.
        """
    )
    return


if __name__ == "__main__":
    app.run()
