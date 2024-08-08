"""
@author: Vivian
ds3500
Prof. John Rachlin
3/10/2024
"""

# import libraries
from drv import DRV  

# formula N = R* * fp * ne * f1 * fi * fc * L

# R*
R = DRV(type='normal', mean=2.25, stdev=0.43, bins=100)
print("R:", R.ev())

# fp
fp = DRV(dist={.85: 0.25, 0.90: 0.25, 0.95: 0.50}, type='discrete', bins=100)
print("fp:", fp.ev())

# ne
ne = DRV(type='uniform', min=1, max=5, bins=20)
print("ne:", ne.ev())

# f1
f1 = DRV(type='uniform', min=0, max=1, bins=20)
print("f1:", f1.ev())

# fi 
fi = DRV(type='uniform', min=0, max=1, bins=20)
print("fi:", fi.ev())

# fc 
fc = DRV(type='uniform', min=0, max=1, bins=20)
print("fc:", fc.ev())

# L
L = DRV(type='normal', mean=10000, stdev=2000, bins=100)
print("L:", L.ev())

N = R * fp * ne * f1 * fi * fc * L
N_ev = N.ev()
print("N ev:", N_ev)
print("N. std:", N.stdev())

N.plot(cumulative=False, log_scale=True, trials=0, bins=100)

