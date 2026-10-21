# Two-parameter full-logistic PD calibration · 20 October 2026

**Primary model specification:** `PD(Z)=sigmoid(a+bZ)`, **a = -2.18031828**, **b = -1.10613960**. This is an illustrative constrained *minimax* fitting rule for the 20 reference rating PDs, not an empirically validated default model. Refit with `python scripts/calibrate_pd.py --refit` (`scipy` required).

## Reproducible objective

Take each rating's finite Z-EM band midpoint; AAA=4.90, D=-1.50. Find parameters a,b,t minimizing **t**, such that `abs(sigmoid(a+b*z_i)-PD_i) <= t` for every one of the 20 ratings, `b <= -0.01`, and `sigmoid(a+b*z_AAA) <= 2.5 * PD_AAA`, `sigmoid(a+b*z_BBB) <= 2.5 * PD_BBB`. These extra caps constrain extreme relative overestimation for low reference PD anchors; 2.5 is an illustrative judgment call, not statistically validated. Solve with SLSQP bounded optimization and check the constraints.

| Metric at the 20 reference points | Previous | Updated full logistic |
|---|---:|---:|
| Mean absolute difference | 1.815 percentage points | **1.378 pp** |
| Maximum absolute difference | 8.327 pp | **8.173 pp** |
| AAA reference = 0.020% | 0.188% | **0.050%** |
| BBB reference = 0.250% | 1.199% | **0.508%** |
| CCC+ reference = 16.270% | 10.657% | **8.097%** |
| D reference = 40.000% | 35.537% | **37.259%** |

**Interpretation:** even the improved two-parameter curve materially underestimates CCC+ and overestimates CCC−. No two-parameter sigmoid can interpolate all 20 reference levels. Changing the fitting loss or anchor constraints would change the coefficients. 

## Rating-anchored sensitivity

`pd_curves.py` and `templates/engine.js` implement monotone cubic Hermite interpolation of logit(PD), with tails linear in logit space. It matches every reference PD **at the defined representative score** (zero in-sample interpolation error) and is C1-continuous in Z, with PD within (0,1). At rating boundaries the PD is smooth rather than identical to the old piecewise-constant PD. This is not a two-parameter full logistic and is labeled as an alternative, not the primary logistic model.

Both models calculate `EFC = PD*EAD*LGD` on **the same simulated financial paths**; no Bernoulli default or realised loss draw. A missed debt service marker does not override MC PD. The final-year P95 is a percentile of expected costs across shock paths; it is not an actual budget payment tail-risk measure. Neither model has validation against SOE default observations, and observed outcomes are needed before making predictions for fiscal policy.

See `docs/PD_FINAL_DECISION.md` for usage and methods.
