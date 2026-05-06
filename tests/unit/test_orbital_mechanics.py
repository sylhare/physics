import numpy as np
import pytest
from physics.orbital_mechanics import (
    solve_kepler_equation,
    true_anomaly_from_eccentric,
    ellipse_from_eccentricity
)

def test_solve_kepler_equation_circular():
    # e = 0 -> M = E
    assert solve_kepler_equation(1.0, 0.0) == 1.0

def test_solve_kepler_equation_elliptical():
    # M = E - e*sin(E)
    # If E = pi/2, e = 0.5, then M = pi/2 - 0.5*1 = pi/2 - 0.5
    M = np.pi/2 - 0.5
    e = 0.5
    E = solve_kepler_equation(M, e)
    assert E == pytest.approx(np.pi/2)

def test_true_anomaly_from_eccentric():
    # E = 0 -> theta = 0
    assert true_anomaly_from_eccentric(0.0, 0.5) == 0.0
    # E = pi -> theta = pi
    assert true_anomaly_from_eccentric(np.pi, 0.5) == pytest.approx(np.pi)

def test_ellipse_coordinates():
    e = 0.0 # Circle
    a = 1.0
    x, y = ellipse_from_eccentricity(e, a, n_points=100)
    
    # Check radius is 1 for all points
    r = np.sqrt(x**2 + y**2)
    assert np.allclose(r, 1.0)
    
    # Check start point
    assert x[0] == pytest.approx(1.0)
    assert y[0] == pytest.approx(0.0)
