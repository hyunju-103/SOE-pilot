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

## Monte Carlo, GDP lookup and compact controls (2026-10-20)

- Monte Carlo results use a six-card, two-column arrangement (percentile path and zones; EFC and Z-EM distributions; PD comparison and percentile summary).
- Cash waterfall and missed-debt-service switches now give conditional effect explanations. The latter is a single-scenario sensitivity and does not override Monte Carlo logistic PD.
- Compact On/Off controls no longer stretch to the entire column; the Monte Carlo disclosure is also slimmer.
- GDP reference lookup: user chooses country and base year, and the browser queries World Bank WDI `NY.GDP.MKTP.CN` (GDP, current local currency, source=2) live. It never invents missing years or an FX conversion.
- GDP unit selector supports financial-statement units, full LCU, thousands, millions and billions. Results are divided by the uploaded statement unit multiplier before entering the shared GDP state, retaining consistent EFC/GDP ratios.
- Apply GDP is an explicit action. Country currency mismatches and reference-year mismatches prevent auto-apply; unknown currency matches require explicit confirmation; the manually entered GDP field remains available.
- The browser needs internet access for the optional World Bank reference lookup. Offline / API failures show an explanation and leave manual GDP entry accessible.
- Tested in Chromium with mocked World Bank responses: country and year lookup, billions display, apply conversion, incompatible-currency rejection, compact switches and six Monte Carlo result panels; no page JavaScript exceptions.


## Compact framework layout and percentile-path axis (2026-10-20)

- Model Framework blue heading now uses a one-line title grouping with compact 8px vertical padding (approximately 40px total at desktop width).
- All six framework cards use content-driven heights instead of fixed min-height. Both six-column Home and three-column/two-row Monte Carlo layouts are compact; tablet and mobile breakpoints also remove excessive min-height.
- Monte Carlo EFC percentile path uses an automatically scaled Y axis rather than forcing zero, avoiding a nearly-flat line around high EFC values; the chart subtitle explicitly states the axis need not begin at zero.
- Histogram Y axes continue showing counts, not monetary values, and are unchanged.
- Tested in isolated Chromium layout at 1460px: Home 148px, compact Monte Carlo 212px, title band 40px in both. Inline JavaScript passed Node syntax checks. Full runtime Monte Carlo E2E test was inconclusive due browser timeout.

