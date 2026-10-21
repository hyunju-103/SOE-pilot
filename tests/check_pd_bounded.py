"""Bounded rating-anchored PD (the Monte Carlo default): anchors, monotone, clamped tails, continuity,
Python/JS parity on Z in [-8, 12] step 1e-3, and the Monte Carlo default method in both engines."""
import json, math, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
import config, report, data_loader, calculations, shocks
from pd_curves import anchored_pd

fails = []
def check(name, ok, detail=""):
    print(("OK   " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok: fails.append(name)

# anchors and bounds, derived from the rating table
anch = []
for lo, hi, r, p in config.Z_RATING_TABLE:
    z = lo if math.isfinite(lo) and not math.isfinite(hi) else hi if not math.isfinite(lo) else (lo + hi) / 2
    anch.append((z, p, r))
z_lo, z_hi = min(a[0] for a in anch), max(a[0] for a in anch)
pd_lo = [p for z, p, r in anch if z == z_lo][0]; pd_hi = [p for z, p, r in anch if z == z_hi][0]
check("20 rating anchors", len(anch) == 20)
check("bounds are the D and AAA anchors", (z_lo, z_hi, pd_lo, pd_hi) == (-1.5, 4.9, 0.40, 0.0002), f"{z_lo} {z_hi} {pd_lo} {pd_hi}")

grid = [-8 + i * 1e-3 for i in range(20001)]            # -8 .. 12
py = [anchored_pd(z) for z in grid]
eps = 1e-12
check("Python exact at all 20 anchors", max(abs(anchored_pd(z) - p) for z, p, _ in anch) < eps)
check("Python monotone non-increasing", all(py[i + 1] <= py[i] + 1e-15 for i in range(len(py) - 1)))
check("Python PD == 40% for Z <= -1.5", all(abs(v - 0.40) < eps for z, v in zip(grid, py) if z <= z_lo))
check("Python PD == 0.02% for Z >= 4.9", all(abs(v - 0.0002) < eps for z, v in zip(grid, py) if z >= z_hi))
mx = max(abs(py[i + 1] - py[i]) for i in range(len(py) - 1))
check("Python continuous: max |dPD| between grid points < 2e-3", mx < 2e-3, f"max {mx:.3e}")
check("NaN in -> NaN out (Python)", math.isnan(anchored_pd(float('nan'))))

payload = {'config': report.config_payload(), 'zs': grid, 'anchors': [a[0] for a in anch], 'engine': str(R / 'templates/engine.js')}
runner = r'''const fs=require('fs');const p=JSON.parse(fs.readFileSync(0,'utf8'));const e=require(p.engine).create(p.config);
const f=z=>e.pdValue(z,e.zRating(z),false,{pd_method:'rating_smooth'});
console.log(JSON.stringify({grid:p.zs.map(f),anch:p.anchors.map(f),nan:Number.isNaN(f(NaN))}));'''
out = json.loads(subprocess.run(['node', '-e', runner], capture_output=True, text=True, input=json.dumps(payload), check=True).stdout)
js = out['grid']
check("JS exact at all 20 anchors", max(abs(v - p) for v, (z, p, _) in zip(out['anch'], anch)) < eps)
check("JS monotone non-increasing", all(js[i + 1] <= js[i] + 1e-15 for i in range(len(js) - 1)))
check("JS PD == 40% for Z <= -1.5", all(abs(v - 0.40) < eps for z, v in zip(grid, js) if z <= z_lo))
check("JS PD == 0.02% for Z >= 4.9", all(abs(v - 0.0002) < eps for z, v in zip(grid, js) if z >= z_hi))
mxj = max(abs(js[i + 1] - js[i]) for i in range(len(js) - 1))
check("JS continuous: max |dPD| between grid points < 2e-3", mxj < 2e-3, f"max {mxj:.3e}")
check("NaN in -> NaN out (JS)", out['nan'])
par = max(abs(a - b) for a, b in zip(py, js))
check("Py/JS parity < 1e-12 on the whole grid", par < eps, f"max {par:.3e}")

# Monte Carlo default method and EFC column, both engines
raw = data_loader.demo_portfolio(); en = calculations.compute_zem_components(data_loader.coerce_numeric(raw)); base = en.iloc[-1]
p = dict(config.DEFAULT_SHOCK_PARAMS, **config.DEFAULT_CASH_SETTINGS); p.update(fuel_shock_pct=.5, fuel_cost_share=.35)
mc = shocks.run_monte_carlo(base, p, n_sims=10, fuel_std=.05, fx_std=.07, correlation=.2, horizon_years=2, lgd_pct=70, seed=42)
check("Python MC default method is rating_smooth", set(mc['MC_PD_Model']) == {'rating_smooth'})
check("Python MC default EFC == EFC_Rating_Anchored", bool((abs(mc['EFC'] - mc['EFC_Rating_Anchored']) < 1e-9).all()))
payload = {'config': report.config_payload(), 'base': json.loads(base.to_json()), 'params': p, 'engine': str(R / 'templates/engine.js')}
runner = r'''const fs=require('fs');const i=JSON.parse(fs.readFileSync(0,'utf8'));const E=require(i.engine).create(i.config);
const s=E.monteCarlo(i.base,i.params,{n:10,fuelSd:.05,fxSd:.07,rho:.2,H:2,lgd:70,seed:42});
const rows=s.flatMap(x=>x.path);
console.log(JSON.stringify({m:[...new Set(rows.map(r=>r.MC_PD_Model))],e:Math.max(...rows.map(r=>Math.abs(r.EFC-r.EFC_Rating_Anchored)))}));'''
o = json.loads(subprocess.run(['node', '-e', runner], capture_output=True, text=True, input=json.dumps(payload), check=True).stdout)
check("JS MC default method is rating_smooth", o['m'] == ['rating_smooth'], str(o['m']))
check("JS MC default EFC == EFC_Rating_Anchored", o['e'] < 1e-9, f"max diff {o['e']:.1e}")
if fails:
    print("FAILED:", ", ".join(fails)); sys.exit(1)
print("PASS bounded rating-anchored PD")
