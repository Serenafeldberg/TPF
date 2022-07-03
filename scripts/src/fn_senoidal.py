

import numpy as np
import matplotlib.pyplot as plt

def fn_senoidal (tsart, tend , a, fs, tstep = 0.1):
    t = np.arange(tsart, tend, tstep)

    y = a * np.sin(2 * np.pi * fs * t)

    return t , y
#fid, ax = plt.subplots()
#ax.plot (t, y)
'''
fn = fn_senoidal(0, 15, 4, 0.2)
plt.plot(fn[0], fn[1])
plt.show()
fn_sinusoidales = fn_senoidal(0,15, 3, 0.4)
plt.plot(fn_sinusoidales[0], fn_sinusoidales[1])
plt.plot(fn[0]+fn_sinusoidales[0], fn[1] + fn_sinusoidales[1])
plt.show()
'''

def synthesize (a, ff, tstart, tend, tstep = 0.01):
    k = 1
    t = np.arange(tstart, tend, tstep)
    yy = 0
    for i in range (len(a)):
        y = a[i] * np.sin(2* np.pi * k *ff * t)
        yy+= y
        k += 1

    plt.plot(t,yy)
'''
A=[0.63, -0.31, 0.21, -0.16, 0.13, -0.1, 0.09, -0.08]
fn = synthesize(A, 0.2, 0, 10.1)
plt.show()
'''
def gen_arrays (fc = 4, a = 4):
    t = np.arange(0, 15, 0.01)
    y = a * np.sin(2 * np.pi*fc*t)
    w1 = np.sin(2*np.pi*0.2*t) + 5
    z1 = w1 * y 
    plt.plot(t,z1)
    plt.show()
    w2 = np.exp(-t)
    z2 = w2 * y
    plt.plot(t,z2)
    plt.show()
    w3 = 0.5 - 0.5*np.cos(2*np.pi*t/0.01/(len(t)-1))
    z3 = w3 * y
    plt.plot(t,z3)
    plt.show()

def sinusoidal (fs, a, tstart, tend, duration, tstep = 0.005):
    t_prov = np.arange(tstart, tend, tstep)
    start = tstart
    for i in range (len(t_prov)-1):
        if 0 <= t_prov[i] <= duration:
            t = np.arange(start, (start + tstep), tstep)
            y = a * np.sin(2 * np.pi * fs * t)
            plt.plot(t,y)
        else:
            t = np.arange(start, (start + tstep), tstep)
            print(t)
            y = 0
            plt.plot(t,y)
        start += tstep
        
    plt.show()

#sinusoidal(440, 4, -0.01, 0.031, 0.027)

def sinu (fs, a, tstart, tend, fm, phi, tstep = 0.005):
    ts = 1/ fm
    n = tend / ts
    t = np.arange(tstart, n, tstep)
    y = a * np.sin(2 * np.pi * fs * n * ts + phi * (np.pi / 180))
    plt.plot(t,y)
    plt.show()

sinu(440, 1, 0, 0.027, 0.023, 1000, 0.001)


