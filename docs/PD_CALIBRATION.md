# Monte Carlo full-logistic PD calibration (October 2026)

## Decision implemented

- **Monte Carlo:** full logistic PD for **every** simulated Z-EM, not rating jumps and not a rating-plus-tail hybrid. Both the Python Streamlit and the JavaScript/HTML Monte Carlo paths enforce this, regardless of the deterministic scenario PD selector.
- **Single scenarios:** original choices and original default rating method are preserved. The Expected Fiscal Cost tab is unchanged.
- **Materialisation:** existing first-default draw and EAD × LGD loss logic is retained, not rewritten.

## Formula and calibration

`PD(Z) = 1 / (1 + exp(-(a + b * Z)))`, `a = -1.92665108`, `b = -0.88741214`.

This is an **illustrative calibration**, not an empirically validated default model. Optimisation uses weighted nonlinear least squares on **PD levels** (not log-odds) versus the `Z_RATING_TABLE` entries in `config.py`. For finite Z bands the representative score is the midpoint; AAA uses its finite lower boundary (4.90) and D uses its finite upper boundary (-1.50). High-distress observations receive larger weights (D=5, CCC-=4, CCC=4, CCC+=5, B-=3, all others=1). A negative slope is constrained. See the CSV for all 20 comparisons.

Average absolute difference from reference PD levels: 1.81 percentage points; maximum: 8.33 percentage points. **The full logistic cannot exactly preserve the 20 step-level values with just two coefficients**, and the ratings table itself is an indicative proxy (not default-frequency observations tied to Z-EM). John should review whether deviations are acceptable before citing point estimates as validated risk measures.

Key anchors:

| Rating | Representative Z | Existing PD | Calibrated logistic PD |
|---|---:|---:|---:|
| D | -1.500 | 40.00% | 35.54% |
| CCC- | -1.125 | 20.00% | 28.33% |
| CCC | -0.400 | 16.27% | 17.20% |
| CCC+ | 0.225 | 16.27% | 10.66% |
| B- | 0.700 | 7.10% | 7.26% |
| BBB | 2.800 | 0.25% | 1.20% |

## Important implementation limits

1. The Monte Carlo PD curve is endogenous to each drawn financial path **via its year-specific Z-EM**. This is a structural score-to-PD mapping, not a causal/default-data-estimated model.
2. If the cash waterfall records a missed debt payment, `pd_on_default` (default 100%) overrides logistic PD. The materialised loss is model-defined, not a confirmed government obligation.
3. Multi-year default draws use the first year that an independent uniform random draw falls below that year's conditional PD. Interpret subsequent years accordingly; defaulted paths are not repeatedly counted as new defaults.
4. Strong calibration requires externally sourced historical default frequency estimates, a rating cohort horizon, and country/SOE validation. The current rating-to-Z proxies cannot uniquely establish a credible statistical relationship.
5. Changing calibration coefficients in `config.py` updates the JavaScript engine through its injected CFG, but the CSV must be regenerated using `scripts/calibrate_pd.py` for consistent documentation.
6. PD/EFC charts in existing slide decks and deterministic EFC pages are **not** automatically updated by this Monte Carlo-only change.
