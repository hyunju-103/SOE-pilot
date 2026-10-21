"""Report/optionally refit the constrained minimax full-logistic reference PD curve.

`python scripts/calibrate_pd.py`: report accuracy using installed config.
`python scripts/calibrate_pd.py --refit`: requires scipy, fit two parameters and print; does not silently overwrite config.py.
"""
from pathlib import Path
import sys, math, argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import config
ap=argparse.ArgumentParser();ap.add_argument('--refit',action='store_true');arg=ap.parse_args()
rows=[]
for lo,hi,r,p in config.Z_RATING_TABLE:
 z=lo if math.isfinite(lo) and not math.isfinite(hi) else hi if not math.isfinite(lo) else (lo+hi)/2
 rows.append((r,z,p))
z=np.array([r[1] for r in rows]); y=np.array([r[2] for r in rows]); names=[r[0] for r in rows]
prob=lambda ab: 1/(1+np.exp(-np.clip(ab[0]+ab[1]*z,-700,700)))
a=config.DEFAULT_CASH_SETTINGS['pd_logit_a'];b=config.DEFAULT_CASH_SETTINGS['pd_logit_b']
if arg.refit:
 from scipy.optimize import minimize
 c=[{'type':'ineq','fun':lambda x:x[2]-abs(prob(x)-y)}, {'type':'ineq','fun':lambda x:-.01-x[1]}]
 for r in ['AAA','BBB']:
  j=names.index(r)
  c.append({'type':'ineq','fun':lambda x,j=j:2.5*y[j]-prob(x)[j]})
 res=minimize(lambda x:x[2], [a,b,.1], method='SLSQP', bounds=[(-12,2),(-5,-.01),(0,1)], constraints=c,options={'ftol':1e-14,'maxiter':3000})
 if not res.success: raise RuntimeError(res.message)
 a,b,_=res.x
 print('Refitted (not written into config.py):',a,b)
diff=prob((a,b))-y
print(f'a={a:.8f} b={b:.8f}; MAE={np.mean(abs(diff))*100:.6f}pp; max={max(abs(diff))*100:.6f}pp')
print('AAA factor',prob((a,b))[names.index('AAA')]/y[names.index('AAA')]);print('BBB factor',prob((a,b))[names.index('BBB')]/y[names.index('BBB')])
for (r,z0,p0),q in zip(rows,prob((a,b))):print(f'{r:5} z={z0:7.3f} reference={p0*100:9.4f}% logistic={q*100:9.4f}% error={(q-p0)*100:+8.4f}pp')
