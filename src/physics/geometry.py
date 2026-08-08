"""Small geometry helpers shared across the physics visualizations.

These are pure-numpy utilities (no plotting dependencies) for the geometric
patterns that recur throughout the notebooks: rotating points in 2D, tracing
circle outlines, and building radial surfaces for 3D embedding diagrams.
"""

from collections.abc import Sequence

import numpy as np


def rotation_matrix(angle: float) -> np.ndarray:
    """Return the 2x2 counter-clockwise rotation matrix for ``angle`` radians."""
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([[cos_a, -sin_a], [sin_a, cos_a]])


def rotate2d(x, y, angle: float):
    """Rotate 2D point(s) counter-clockwise about the origin.

    Args:
        x: X coordinate(s) - scalar or array, broadcast with ``y``.
        y: Y coordinate(s) - scalar or array, broadcast with ``x``.
        angle: Rotation angle in radians.

    Returns:
        Tuple ``(x_rotated, y_rotated)`` matching the input shape.
    """
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a


def circle(
    radius: float = 1.0,
    n: int = 100,
    center: Sequence[float] = (0.0, 0.0),
):
    """Return ``(x, y)`` arrays tracing a circle outline.

    Args:
        radius: Circle radius.
        n: Number of points around the circle.
        center: ``(cx, cy)`` centre of the circle.

    Returns:
        Tuple ``(x, y)`` of coordinate arrays of length ``n``.
    """
    theta = np.linspace(0, 2 * np.pi, n)
    cx, cy = center
    return cx + radius * np.cos(theta), cy + radius * np.sin(theta)


def polar_mesh(r, theta):
    """Build a radial mesh and convert it to Cartesian coordinates.

    Useful for 3D embedding diagrams (wormhole throats, Flamm's paraboloid,
    ...) where a surface ``Z = f(R, Theta)`` is drawn over a polar grid.

    Args:
        r: 1D array of radial coordinates.
        theta: 1D array of angular coordinates (radians).

    Returns:
        Tuple ``(X, Y, R, Theta)`` of 2D meshgrid arrays. ``R``/``Theta`` are
        provided so the caller can compute the surface height ``Z``.
    """
    R, Theta = np.meshgrid(r, theta)
    return R * np.cos(Theta), R * np.sin(Theta), R, Theta
