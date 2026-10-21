# Final PD model + interface · 20 October 2026

- **Full logistic is the MC default** under the default model specification. The full-logistic calibration was updated (a=-2.18031828, b=-1.10613960) to reduce rating anchor error under explicit bounded minimax constraints.
- **Smooth rating-anchored** option provides a separately labeled, C1 monotone PCHIP curve of logit PD that exactly matches 20 rating PD reference anchors; it is not a single logistic formula. This is a *model-risk sensitivity*.
- Both engines' MC pages include a selector and display a **same-draw comparison** of median and P95 final-year expected fiscal cost. Exports include both alternative costs, not cumulative/additive costs.
- Single-scenario PD controls, static EFC tab and cash Waterfall mechanics are retained; MC does not override PD to 100% on a missed debt-service flag; actual default/loss simulation is outside scope.
- The MC results display P95 *expected fiscal cost*, not P95 actual government outlays, and no claims are made of out-of-sample or historical validation.
- All core pages, shock controls, waterfall options, SENELEC presets, and original tabs are retained.
- Calibration specification: `docs/PD_CALIBRATION.md`; tests: `tests/check_pd_model_final.py`.
