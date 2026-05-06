import numpy as np
import pytest
from physics.integrators import velocity_verlet_step, rk4_step, gravity_acceleration

def test_velocity_verlet_harmonic_oscillator():
    # Simple harmonic oscillator: a = -k/m * x
    k = 1.0
    m = 1.0
    def force_func(pos):
        return -k/m * pos
    
    pos = np.array([[1.0, 0.0]])
    vel = np.array([[0.0, 0.0]])
    dt = 0.1
    
    next_pos, next_vel = velocity_verlet_step(pos, vel, m, force_func, dt)
    
    # Expected: x_next approx x0 + v0*dt + 0.5*a0*dt^2 = 1.0 + 0 - 0.5*1.0*0.01 = 0.995
    assert next_pos[0, 0] == pytest.approx(0.995)
    # v_half = 0 + 0.5*(-1.0)*0.1 = -0.05
    # a_next = -0.995
    # v_next = -0.05 + 0.5*(-0.995)*0.1 = -0.05 - 0.04975 = -0.09975
    assert next_vel[0, 0] == pytest.approx(-0.09975)

def test_rk4_step_linear():
    # dy/dt = y
    def derivative_func(y):
        return y
    
    state = np.array([1.0])
    dt = 0.1
    
    next_state = rk4_step(state, derivative_func, dt)
    
    # Analytical solution: y(t) = e^t -> y(0.1) = e^0.1 approx 1.10517
    assert next_state[0] == pytest.approx(np.exp(0.1), rel=1e-5)

def test_gravity_acceleration_two_bodies():
    # Two bodies on X axis at -1 and 1
    pos = np.array([[-1.0, 0.0], [1.0, 0.0]])
    masses = np.array([1.0, 1.0])
    G = 1.0
    # Use default softening to avoid division by zero for i=j
    acc = gravity_acceleration(pos, masses, G=G)
    
    # Distance is 2.0. Force F = G*m1*m2/r^2 = 1*1*1/4 = 0.25
    # Acceleration a1 = F/m1 = 0.25 (towards body 2, so +X)
    # Acceleration a2 = -0.25 (towards body 1, so -X)
    assert acc[0, 0] == pytest.approx(0.25, rel=1e-3)
    assert acc[1, 0] == pytest.approx(-0.25, rel=1e-3)
    assert acc[0, 1] == 0.0
    assert acc[1, 1] == 0.0
