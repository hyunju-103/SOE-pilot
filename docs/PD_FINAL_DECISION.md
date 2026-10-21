# SOE Monte Carlo PD: final modeling decision (20 October 2026)

## Two defensible, explicitly different specifications

**Primary model specification**: full two-parameter logistic `PD = sigmoid(a + b * Z-EM)` across all simulated years and draws; coefficients `a = -2.18031828`, `b = -1.10613960`. This is a constrained approximation of 20 **illustrative** rating PDs. It cannot fit all 20 exactly and has not been validated against observed SOE defaults. At representative scores, its mean absolute error is ~1.378 percentage points (previous ~1.815), maximum ~8.173 pp (previous ~8.327). The AAA and BBB anchor PDs remain above original values; CCC+ is underestimated (~8.10% vs 16.27%). **Do not claim this is a fully credible empirical PD model.**

**Rating-preserving sensitivity**: monotone piecewise cubic Hermite interpolation (PCHIP) **of logit(PD)**. Anchors are the finite-band midpoints, AAA=4.90 and D=-1.50. It passes exactly through every one of the 20 anchor PDs. One-sided monotone derivatives make it C1-continuous, with straight logit-space tails: PD approaches 1 in sufficiently severe distress, and approaches 0 for high Z-EM. Equal PD anchors in CCC/CCC+ may create a flat segment. This is not a single logistic function and thus cannot replace the primary mode if the two-parameter logistic specification is required.

## Consistent comparison

The Monte Carlo UI now supports selecting either model. The **default remains full logistic**. Its comparison table uses **exactly the same random shock paths, balance sheet, EAD and LGD**, varying only the PD curve. Both Python and JavaScript engines are updated. Exports include `PD_Full_Logistic`, `PD_Rating_Anchored`, `EFC_Full_Logistic`, and `EFC_Rating_Anchored`.

`Debt Default` is a **missed-debt-service flag**, not an observed realised default event. It is never used to override the Monte Carlo PD. The simulation estimates `EFC = PD × EAD × LGD` only, **without Bernoulli default draws or realised government payouts**. The P95 is the 95th percentile across paths **of expected costs**, not of realised fiscal payments. Debt-service flags can still affect the underlying Z-EM and cash-flow outcomes. The deterministic PD selector and standalone EFC tab have not been changed to force the Monte Carlo PD method.

## Operational limitations

- These two curves are judgmental mapping rules, not estimates from matched 1-year historical default observations. External validations and horizon consistency are needed before policy/public use.
- Neither the 20 rating PDs nor those reference Z-EM midpoints are observed cohort-frequency samples. Anchor error of 0 by construction is **not** proof of better out-of-sample prediction.
- Never add `EFC_Full_Logistic` and `EFC_Rating_Anchored`; these are alternative model assumptions on identical exposures, not additive risk channels.
- Source code and static HTML must be regenerated together. Use `python report.py --demo --out SOE-Fiscal-Risk-Final.html` after a change.
- The original Waterfall financial and default-service flag mechanics remain unchanged; regression tests should be run after every modification.
