import numpy as np

def velocity_verlet_step(pos, vel, mass, force_func, dt):
    """
    Perform a single Velocity Verlet integration step.
    
    Args:
        pos: Current position array [N, D]
        vel: Current velocity array [N, D]
        mass: Mass array [N]
        force_func: Function that returns acceleration for given positions
        dt: Time step
        
    Returns:
        next_pos, next_vel
    """
    # Half step for velocity
    acc = force_func(pos)
    vel_half = vel + 0.5 * acc * dt
    
    # Full step for position
    pos_next = pos + vel_half * dt
    
    # Half step for velocity with new acceleration
    acc_next = force_func(pos_next)
    vel_next = vel_half + 0.5 * acc_next * dt
    
    return pos_next, vel_next

def rk4_step(state, derivative_func, dt):
    """
    Perform a single 4th-order Runge-Kutta step.
    
    Args:
        state: Current state vector (pos and vel combined)
        derivative_func: Function that returns d(state)/dt
        dt: Time step
        
    Returns:
        next_state
    """
    k1 = derivative_func(state)
    k2 = derivative_func(state + 0.5 * dt * k1)
    k3 = derivative_func(state + 0.5 * dt * k2)
    k4 = derivative_func(state + dt * k3)
    
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def gravity_acceleration(pos, masses, G=1.0, softening=0.001):
    """
    Vectorized gravitational acceleration calculation.
    
    Args:
        pos: Positions [N, D]
        masses: Masses [N]
        G: Gravitational constant
        softening: Force softening to avoid singularities
        
    Returns:
        acc: Accelerations [N, D]
    """
    N = pos.shape[0]
    D = pos.shape[1]
    acc = np.zeros_like(pos)
    
    # Use broadcasting for distance calculation
    # Reshape to [N, 1, D] and [1, N, D] to get relative vectors [N, N, D]
    ri = pos.reshape(N, 1, D)
    rj = pos.reshape(1, N, D)
    r_vec = rj - ri  # r_vec[i, j] is vector from i to j
    
    # Square distances [N, N]
    r_sq = np.sum(r_vec**2, axis=2) + softening**2
    r_mag = np.sqrt(r_sq)
    
    # Force calculation: F = G * mi * mj * r_vec / r_mag^3
    # Acc: a_i = sum_j (G * mj * r_vec_ij / r_mag_ij^3)
    inv_r_cubed = 1.0 / (r_mag**3)
    
    # Masses mj [1, N]
    mj = masses.reshape(1, N)
    
    # Scalar part: G * mj / r_mag^3 [N, N]
    scalar = G * mj * inv_r_cubed
    
    # Acceleration [N, D] by summing over j
    # np.einsum('ij,ijd->id', scalar, r_vec)
    acc = np.sum(scalar[:, :, np.newaxis] * r_vec, axis=1)
    
    return acc
