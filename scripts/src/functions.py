
import numpy as np

def constant (t):
    t = np.full(len(t), 1)
    return t

def linear (t, t0):
    return (t / t0)

def invlinear (t, t0):
    value = 1 - (t/ t0)
    return np.clip (value, 0, 1)

def sin (t, a, f):
    return 1 + a * np.sin(f * t)

def exp (t, t0):
    exponent = 5 * (t - t0) / t0
    return np.e ** exponent

def invexp (t , t0):
    exponent = (-5) * t / t0
    return np.e ** exponent

def quartcos (t, t0):
    return np.cos(np.pi * t / (2 * t0))

def quartsin (t, t0):
    return np.sin(np.pi * t / (2 * t0))

def halfcos (t, t0):
    a = 1 + np.cos (np.pi * t / t0)
    return a / 2

def halfsin (t, t0):
    val = t / t0
    a = 1 + np.cos(np.pi * (val + (1/2)))
    return a / 2

def log (t, t0):
    result = np.where(t > t0, t, t0)
    np.log10(result, out=result, where=result > 0)
    return result
    '''
    val = (-9) * t / t0
    return np.log10(val + 1)
    '''
    
def invlog (t, t0):
    t [t < t0] = np.log10(((-9) * t [t< t0] / t0) + 10)
    t [t >= t0] = 0
    
    return t

def tri (t, t0, t1, a1):
    t [t < t1] = t[t < t1] * a1 / t1
    t [t > t1] = ((t [t > t1] - t1) / (t1 - t0)) + a1

    return t

def pulses (t, t0, t1, a1):
    val = t/t0 - abs (t/t0)