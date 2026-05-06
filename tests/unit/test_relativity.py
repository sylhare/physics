import numpy as np
import pytest
from physics.relativity import (
    lorentz_factor,
    lorentz_transform,
    proper_time,
    doppler_shift,
    relativistic_velocity_addition
)

def test_lorentz_factor():
    assert lorentz_factor(0.0) == 1.0
    assert lorentz_factor(0.6) == pytest.approx(1.25)
    assert lorentz_factor(0.8) == pytest.approx(1.666666, rel=1e-5)
    # Test clipping
    assert lorentz_factor(1.0) == lorentz_factor(0.999999)

def test_lorentz_transform():
    # v = 0.6c, gamma = 1.25
    # S frame: t=1, x=0
    # S' frame: t' = gamma(t - vx) = 1.25(1 - 0) = 1.25
    #           x' = gamma(x - vt) = 1.25(0 - 0.6) = -0.75
    t_prime, x_prime = lorentz_transform(1.0, 0.0, 0.6)
    assert t_prime == pytest.approx(1.25)
    assert x_prime == pytest.approx(-0.75)

def test_proper_time():
    # dt=5, dx=3 -> dtau = sqrt(25 - 9) = 4
    assert proper_time(5.0, 3.0) == 4.0
    # Spacelike interval should return 0 (due to np.maximum(0, ...))
    assert proper_time(3.0, 5.0) == 0.0

def test_doppler_shift():
    f = 100.0
    v = 0.6
    # blue shift: f' = f * sqrt((1+beta)/(1-beta)) = 100 * sqrt(1.6/0.4) = 100 * 2 = 200
    assert doppler_shift(f, v, approaching=True) == pytest.approx(200.0)
    # red shift: f' = f * sqrt((1-beta)/(1+beta)) = 100 * sqrt(0.4/1.6) = 100 * 0.5 = 50
    assert doppler_shift(f, v, approaching=False) == pytest.approx(50.0)

def test_relativistic_velocity_addition():
    # u = 0.5c, v = 0.5c -> w = (0.5 + 0.5) / (1 + 0.25) = 1.0 / 1.25 = 0.8
    assert relativistic_velocity_addition(0.5, 0.5) == pytest.approx(0.8)
    # u = 0.9c, v = 0.9c -> w = 1.8 / 1.81 approx 0.994
    assert relativistic_velocity_addition(0.9, 0.9) == pytest.approx(1.8/1.81)
