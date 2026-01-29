"""Orbital mechanics calculations for Kepler's laws."""

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq


def solve_kepler_equation(M: float, e: float, tol: float = 1e-10) -> float:
    """
    Solve Kepler's equation: M = E - e*sin(E) for E.

    Args:
        M: Mean anomaly (radians)
        e: Eccentricity (0 <= e < 1)
        tol: Convergence tolerance

    Returns:
        E: Eccentric anomaly (radians)
    """
    if e == 0:
        return M

    # Use Brent's method for robust solution
    def kepler_eq(E: float) -> float:
        return E - e * np.sin(E) - M

    # E is bounded by M - e <= E <= M + e for e < 1
    E = brentq(kepler_eq, M - np.pi, M + np.pi)
    return E


def true_anomaly_from_eccentric(E: float, e: float) -> float:
    """
    Convert eccentric anomaly to true anomaly.

    Args:
        E: Eccentric anomaly (radians)
        e: Eccentricity

    Returns:
        theta: True anomaly (radians)
    """
    return 2 * np.arctan2(
        np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)
    )


def ellipse_from_eccentricity(
    e: float, a: float = 1.0, n_points: int = 200
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Generate ellipse coordinates with sun at one focus.

    Args:
        e: Eccentricity (0 <= e < 1)
        a: Semi-major axis (default 1.0)
        n_points: Number of points

    Returns:
        (x, y): Arrays of coordinates
    """
    theta = np.linspace(0, 2 * np.pi, n_points)
    # Polar equation of ellipse with focus at origin
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def kepler_orbit(
    e: float, a: float = 1.0, n_frames: int = 100
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Generate orbital trajectory with correct timing (Kepler's 2nd law).

    Args:
        e: Eccentricity
        a: Semi-major axis
        n_frames: Number of time steps

    Returns:
        (x, y, t): Position arrays and normalized time (0 to 1)
    """
    # Mean anomaly progresses linearly with time
    M_values = np.linspace(0, 2 * np.pi, n_frames, endpoint=False)

    x = np.zeros(n_frames)
    y = np.zeros(n_frames)

    for i, M in enumerate(M_values):
        E = solve_kepler_equation(M, e)
        theta = true_anomaly_from_eccentric(E, e)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x[i] = r * np.cos(theta)
        y[i] = r * np.sin(theta)

    t = M_values / (2 * np.pi)  # Normalized time [0, 1)
    return x, y, t


def swept_area_points(
    e: float, a: float, theta_start: float, theta_end: float, n_points: int = 50
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Generate points for a swept area wedge (for visualizing Kepler's 2nd law).

    Returns polygon vertices: origin -> arc -> origin

    Args:
        e: Eccentricity
        a: Semi-major axis
        theta_start: Starting true anomaly (radians)
        theta_end: Ending true anomaly (radians)
        n_points: Points along the arc

    Returns:
        (x, y): Arrays forming closed polygon
    """
    theta = np.linspace(theta_start, theta_end, n_points)
    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    x_arc = r * np.cos(theta)
    y_arc = r * np.sin(theta)

    # Create closed polygon: origin -> arc -> origin
    x = np.concatenate([[0], x_arc, [0]])
    y = np.concatenate([[0], y_arc, [0]])

    return x, y


def projectile_trajectory(
    v0: float, g: float = 9.8, R: float = 6.371e6, n_points: int = 500
) -> tuple[NDArray[np.floating], NDArray[np.floating], bool]:
    """
    Calculate projectile trajectory for Newton's cannon thought experiment.

    Uses simplified 2D orbital mechanics.

    Args:
        v0: Initial horizontal velocity (m/s)
        g: Surface gravity (m/s²)
        R: Planet radius (m)
        n_points: Number of trajectory points

    Returns:
        (x, y, is_orbit): Trajectory coordinates and whether it achieves orbit
    """
    # For visualization, we work in units where R=1
    # Circular orbit velocity: v_circ = sqrt(g*R)
    v_circ = np.sqrt(g * R)

    # Normalize velocity
    v_norm = v0 / v_circ

    if v_norm < 1:
        # Suborbital: simple parabolic approximation for visualization
        # Time of flight for quarter orbit approximation
        t_max = 2 * v0 / g * (1 + v_norm)
        t = np.linspace(0, t_max, n_points)

        # Initial position at surface
        x0, y0 = 0, R

        # Simplified trajectory (parabolic)
        x = v0 * t
        y = y0 - 0.5 * g * t**2

        # Clip to surface
        below_surface = x**2 + y**2 < R**2
        if np.any(below_surface):
            idx = np.argmax(below_surface)
            x = x[:idx]
            y = y[:idx]

        return x / R, y / R, False

    else:
        # Orbital trajectory
        # Energy determines orbit type
        specific_energy = 0.5 * v0**2 - g * R

        if specific_energy >= 0:
            # Escape trajectory - cap at some distance
            e = 1.0 + 2 * specific_energy * R / (g * R**2)
            e = min(e, 0.95)  # Cap for visualization
        else:
            # Bound orbit
            a = -g * R**2 / (2 * specific_energy)  # Semi-major axis
            # Eccentricity from energy and angular momentum
            L = v0 * R  # Angular momentum per unit mass
            e = np.sqrt(1 + 2 * specific_energy * L**2 / (g * R) ** 2)
            e = min(max(e, 0), 0.95)  # Bound for visualization

        # Generate orbital points
        theta = np.linspace(0, 2 * np.pi, n_points)
        p = R * v_norm**2  # Semi-latus rectum
        r = p / (1 + e * np.cos(theta))

        # Position (starting from top of planet, moving right)
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        return x / R, y / R, True
