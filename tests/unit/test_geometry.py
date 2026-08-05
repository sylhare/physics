import numpy as np
import pytest

from physics.geometry import circle, polar_mesh, rotate2d, rotation_matrix


def test_rotation_matrix_quarter_turn():
    R = rotation_matrix(np.pi / 2)
    # Rotating the unit x vector by 90 deg gives the unit y vector.
    v = R @ np.array([1.0, 0.0])
    assert v == pytest.approx([0.0, 1.0], abs=1e-12)


def test_rotate2d_scalar_quarter_turn():
    x, y = rotate2d(1.0, 0.0, np.pi / 2)
    assert x == pytest.approx(0.0, abs=1e-12)
    assert y == pytest.approx(1.0, abs=1e-12)


def test_rotate2d_identity():
    x, y = rotate2d(2.0, -3.0, 0.0)
    assert (x, y) == pytest.approx((2.0, -3.0))


def test_rotate2d_matches_matrix_on_arrays():
    xs = np.array([1.0, 0.0, -1.0, 0.5])
    ys = np.array([0.0, 1.0, 0.0, 0.5])
    angle = 0.7
    xr, yr = rotate2d(xs, ys, angle)
    expected = np.column_stack([xs, ys]) @ rotation_matrix(angle).T
    assert xr == pytest.approx(expected[:, 0])
    assert yr == pytest.approx(expected[:, 1])


def test_rotate2d_preserves_length():
    xr, yr = rotate2d(3.0, 4.0, 1.234)
    assert np.hypot(xr, yr) == pytest.approx(5.0)


def test_circle_radius_and_shape():
    x, y = circle(radius=2.0, n=50)
    assert len(x) == 50
    assert len(y) == 50
    assert np.hypot(x, y) == pytest.approx(np.full(50, 2.0))


def test_circle_center_offset():
    x, y = circle(radius=1.0, n=10, center=(3.0, -1.0))
    assert np.hypot(x - 3.0, y + 1.0) == pytest.approx(np.ones(10))


def test_polar_mesh_shapes_and_cartesian():
    r = np.linspace(1.0, 3.0, 4)
    theta = np.linspace(0, 2 * np.pi, 5)
    X, Y, R, Theta = polar_mesh(r, theta)
    assert X.shape == Y.shape == R.shape == Theta.shape == (5, 4)
    # Cartesian coordinates must lie on their radius.
    assert np.hypot(X, Y) == pytest.approx(R)
