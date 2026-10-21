"""Illustrative, monotone C1 logit-cubic curve passing through ALL rating PD anchors.

C1 PCHIP slopes (Fritsch–Butland), operating on log-odds. The outer tails
continue with the endpoint logit slopes, so the PD stays between 0 and 1.
This is a rating-preserving *sensitivity*, not a single two-parameter logistic
or an empirically calibrated default frequency model.
"""
from functools import lru_cache
import math
from config import Z_RATING_TABLE


def _sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def _end(h0, h1, d0, d1):
    m = ((2*h0+h1)*d0-h0*d1)/(h0+h1)
    if m*d0 <= 0: return 0.0
    if d0*d1 < 0 and abs(m) > 3*abs(d0): return 3*d0
    return m


@lru_cache(maxsize=1)
def anchors():
    rows=[]
    for lo,hi,r,p in Z_RATING_TABLE:
        z = lo if math.isfinite(lo) and not math.isfinite(hi) else hi if not math.isfinite(lo) else (lo+hi)/2
        rows.append((float(z), math.log(p/(1-p)),r,float(p)))
    rows.sort()
    x=tuple(r[0] for r in rows)
    y=tuple(r[1] for r in rows)
    h=[x[i+1]-x[i] for i in range(len(x)-1)]
    delta=[(y[i+1]-y[i])/h[i] for i in range(len(h))]
    d=[0.0]*len(x)
    d[0]=_end(h[0],h[1],delta[0],delta[1])
    d[-1]=_end(h[-1],h[-2],delta[-1],delta[-2])
    for i in range(1,len(x)-1):
        if delta[i-1]*delta[i]<=0:
            d[i]=0.0
        else:
            w1=2*h[i]+h[i-1];w2=h[i]+2*h[i-1]
            d[i]=(w1+w2)/(w1/delta[i-1]+w2/delta[i])
    return x,y,tuple(d)


def anchored_pd(z):
    try:
        z=float(z)
    except (TypeError, ValueError, OverflowError):
        return float('nan')
    if not math.isfinite(z):
        return float('nan')
    x,y,d=anchors()
    if z<=x[0]:
        return _sigmoid(y[0]+d[0]*(z-x[0]))
    if z>=x[-1]:
        return _sigmoid(y[-1]+d[-1]*(z-x[-1]))
    import bisect
    i=bisect.bisect_right(x,z)-1
    h=x[i+1]-x[i]
    t=(z-x[i])/h
    v=(2*t**3-3*t*t+1)*y[i]+(t**3-2*t*t+t)*h*d[i]+(-2*t**3+3*t*t)*y[i+1]+(t**3-t*t)*h*d[i+1]
    return _sigmoid(v)
