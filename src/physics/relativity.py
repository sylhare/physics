import numpy as np

def lorentz_factor(v):
    """
    Calculate the Lorentz factor gamma.
    
    Args:
        v: Velocity as a fraction of light speed (v/c)
        
    Returns:
        gamma: 1 / sqrt(1 - v^2)
    """
    # Clip v to be just below 1.0 to avoid divide by zero
    v_abs = np.abs(v)
    v_clipped = np.minimum(v_abs, 0.999999)
    return 1.0 / np.sqrt(1.0 - v_clipped**2)

def lorentz_transform(t, x, v):
    """
    Apply Lorentz transformation to time and space coordinates.
    
    Args:
        t: Time coordinate(s)
        x: Space coordinate(s)
        v: Relative velocity (v/c)
        
    Returns:
        t_prime, x_prime
    """
    gamma = lorentz_factor(v)
    t_prime = gamma * (t - v * x)
    x_prime = gamma * (x - v * t)
    return t_prime, x_prime

def proper_time(dt, dx):
    """
    Calculate the proper time interval.
    
    Args:
        dt: Time interval
        dx: Space interval
        
    Returns:
        dtau: sqrt(dt^2 - dx^2)
    """
    interval_sq = dt**2 - dx**2
    return np.sqrt(np.maximum(0, interval_sq))

def doppler_shift(f, v, approaching=True):
    """
    Calculate relativistic Doppler shift.
    
    Args:
        f: Source frequency
        v: Relative velocity (v/c)
        approaching: True for blue shift, False for red shift
        
    Returns:
        f_observed
    """
    beta = np.abs(v)
    if approaching:
        return f * np.sqrt((1 + beta) / (1 - beta))
    else:
        return f * np.sqrt((1 - beta) / (1 + beta))

def relativistic_velocity_addition(u, v):
    """
    Relativistic velocity addition.
    
    Args:
        u: Velocity of object in frame S' (u/c)
        v: Velocity of frame S' relative to S (v/c)
        
    Returns:
        w: Velocity of object in frame S (w/c)
    """
    return (u + v) / (1 + u * v)
