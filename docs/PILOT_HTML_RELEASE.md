# SOE Fiscal Risk Dashboard — Pilot HTML Release

Published interactive snapshot: `SOE-Fiscal-Risk-Final.html` (header restored to original navy `#002244`).

## What is published

- Six-stage model journey and redesigned Monte Carlo cards / output layout.
- Full logistic PD as the default Monte Carlo expected-fiscal-cost calculation.
- Smooth rating-anchored PD provided as a comparison / sensitivity analysis.
- Cash-flow waterfall, correlated fuel / FX and optional interest / revenue shocks.
- EFC = PD × EAD × LGD. No Bernoulli default events or realised loss draws.
- Collapsible Monte Carlo controls and extended calibration information.
- Revised illustrative logistic calibration (prioritises lower maximum reference-rating PD error).
- Existing navigation, upload functionality, KPI, Z-EM, EFC and reporting views retained in the standalone UI.
- No person-specific names in page copy.

## Streamlit deployment

`Home.py` reads the tracked standalone HTML snapshot if present, and passes it to `components.html`.
It retains `report.build_app_data()/render_html()` as a fallback if that file is absent.
The deployed pilot UI therefore uses this exact reviewed HTML snapshot rather than
silently rebuilding an older version from the Python templates.

**Maintenance note:** `templates/` and `config.py` have not been synchronized with
this reviewed HTML snapshot. Rebuilding via `report.py` alone may yield a different
UI / calibration. Until sources are synchronized, update and review
`SOE-Fiscal-Risk-Final.html` for the published pilot interface.

## Checks

- HTML file content checksum (git blob SHA): `7a5ef140b36c1725b54be1372771fbc16e217a70`.
- Inline executable JavaScript passed `node --check`; JSON data scripts excluded from JS syntax checking.
- The navy title/header and expected-fiscal-cost-only simulation controls were inspected.
- Actual Streamlit Cloud deployment status and numerical model validation are separate checks.

## Interpretation

The logistic calibration is illustrative and tied to reference rating PDs, **not** estimated
from observed SOE defaults. The displayed P95 EFC is the 95th percentile across simulated
*expected* costs, **not** an observed government payout or a quantile of realised losses.
