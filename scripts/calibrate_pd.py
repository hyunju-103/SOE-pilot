"""Reproduce the documented full-logistic fitting procedure without rewriting config.py."""
from pathlib import Path
import csv, sys
import numpy as np
from scipy.optimize import least_squares
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from config import Z_RATING_TABLE
rows=[]
for lo,hi,n,pd in Z_RATING_TABLE:
    z=lo if np.isfinite(lo) and not np.isfinite(hi) else hi if not np.isfinite(lo) else (lo+hi)/2
    rows.append((n,z,pd))
weights={'D':5,'CCC-':4,'CCC':4,'CCC+':5,'B-':3}
x=np.array([r[1] for r in rows]);y=np.array([r[2] for r in rows]);w=np.array([weights.get(r[0],1) for r in rows]);
f=lambda ab: np.sqrt(w)*(1/(1+np.exp(-(ab[0]+ab[1]*x)))-y)
a,b=least_squares(f,[-2,-1],bounds=([-12,-5],[2,-0.01])).x
print(f"Calibrated a={a:.8f}, b={b:.8f}")
print(f"Mean absolute PD difference = {100*np.mean(abs(f([a,b])/np.sqrt(w))):.2f} percentage points")
