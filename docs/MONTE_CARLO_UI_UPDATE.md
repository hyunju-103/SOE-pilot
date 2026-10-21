# Monte Carlo UI update

- Monte Carlo settings are an accessible, collapsed-by-default disclosure in the standalone HTML: click **Monte Carlo settings** to reveal simulations, shock standard deviations, correlations and shock-centre note.
- The PD model selector is shown separately and stays visible, as do all simulation results and model comparison tables.
- Scope badges are given explicit spacing below the selector; duplicate 'Full logistic · default' badge removed.
- Invalid correlations automatically expand the settings panel and display the validation message in the visible page.
- Streamlit uses a collapsed-by-default `st.expander` for the matching Monte Carlo settings. The PD model selector and outputs remain outside the expander.
- No numeric parameters, PD formulas, Monte Carlo paths, seeds, or waterfall functionality changed.
