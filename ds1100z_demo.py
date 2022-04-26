# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 18:23:22 2022

@author: HIROKI-TAKAHASHI
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import ds1100z as rigol

ch = 1
tscale = 1e-3
toffset = 2e-3
vscale = 1
voffset = 0.3
trig_ch = 1
trig_lvl = 1

scope = rigol.open_first_device()
scope.set_time_scale(tscale)
scope.set_time_offset(toffset)
scope.set_ch_scale(ch, vscale)
scope.set_ch_offset(ch, voffset)
scope.set_trig_source(trig_ch)
scope.set_trig_level(trig_lvl)

scope.single()
start_time = time.time()
while True:
    time_elapsed = time.time()-start_time
    if time_elapsed > 12*tscale and scope.get_trig_status() == 'STOP':
        break
    if  time_elapsed > 10:
        print("Time expired!")
        break

t, y = scope.get_waveform(ch)
N = len(y)
dt = t[1]-t[0]
Y = np.fft.fft(y)
f = np.fft.fftfreq(N, dt)
# Extract only positive frequency part
if N % 2 == 0:
    Np = int(N/2)
else:
    Np = int((N-1)/2)+1
Ypos = Y[0:Np]
fpos = f[0:Np]
#plt.plot(t, y)
#plt.figure()
plt.plot(fpos, abs(2*Ypos)**2)
plt.xlim(0, 10e3)
scope.close()

