"""Fast final assertions: logistic PD throughout Monte Carlo, EFC only, both engines."""
import json, sys, subprocess, math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
import config, data_loader, calculations, report, shocks

raw=data_loader.demo_portfolio()
en=calculations.compute_zem_components(data_loader.coerce_numeric(raw))
base=en.iloc[-1]
p=dict(config.DEFAULT_SHOCK_PARAMS, **config.DEFAULT_CASH_SETTINGS)
p.update(fuel_shock_pct=.5, fuel_cost_share=.35, waterfall_on=1.0, default_on_missed_debt=1.0,
        pd_method='rating', pd_on_default=1.0, pd_override_on_missed_service=True)
a=p['pd_logit_a'];b=p['pd_logit_b']

mc=shocks.run_monte_carlo(base,p,n_sims=8,fuel_std=.05,fx_std=.07,correlation=.2,horizon_years=3,lgd_pct=70)
assert not any(x in mc.columns for x in ['Default Year','Realised Cost','Realised Cost / GDP'])
for _,r in mc.iterrows():
    pd=1/(1+math.exp(-(a+b*float(r['Z_EM']))))
    assert abs(float(r['PD'])-pd)<1e-12
    assert abs(float(r['EFC'])-pd*float(r['EAD'])*float(r['LGD']))<1e-7*max(1,float(r['EFC']))

payload={'config':report.config_payload(),'base':json.loads(base.to_json()),'params':p,
  'engine':str(root/'templates/engine.js')}
js=r'''
const fs=require('fs');const i=JSON.parse(fs.readFileSync(0,'utf8'));
const E=require(i.engine).create(i.config); const ps=i.params;
const sims=E.monteCarlo(i.base,ps,{n:8,fuelSd:.05,fxSd:.07,rho:.2,H:3,lgd:70,seed:42});
let n=0, bad=[];
for(const sim of sims)for(const r of sim.path){
 const pd=1/(1+Math.exp(-(ps.pd_logit_a+ps.pd_logit_b*r.Z_EM)));
 if(Math.abs(r.PD-pd)>1e-12)bad.push(`PD ${r.Z_EM} ${r.PD} ${pd}`);
 if(Math.abs(r.EFC - pd*r.EAD*r.LGD)>1e-7*Math.max(1,Math.abs(r.EFC)))bad.push('EFC mismatch');
 if('Default Year' in r || 'Realised Cost' in r || 'Realised Cost' in sim)bad.push('Default draw present');
 n++;
}
console.log(JSON.stringify({n,bad}));
'''
proc=subprocess.run(['node','-e',js],input=json.dumps(payload),capture_output=True,text=True,check=True)
result=json.loads(proc.stdout)
assert not result['bad'], result['bad'][:3]
assert result['n']==8*4
print(f'PASS Python {len(mc)} records and JavaScript {result["n"]} records: full logistic, no override, EFC only.')
