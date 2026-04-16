# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "pyarrow>=22.0.0",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AF1204 Individual Portfolio  |  Vanesh Kumar
    BSc Accounting and Finance  |  City St George's, University of London
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import micropip
    return micropip, mo, pd


@app.cell
def _(pd):
    # S&P 500 dataset loaded from lecturer gist — WASM-safe remote URL (Week 4)
    _URL = (
        "https://gist.githubusercontent.com/DrAYim/"
        "80393243abdbb4bfe3b45fef58e8d3c8/raw/"
        "ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/"
        "sp500_ZScore_AvgCostofDebt.csv"
    )
    vk_df = pd.read_csv(_URL)

    # Drop rows with missing values in key columns (Week 2 — exception handling)
    vk_df = vk_df.dropna(subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key",
                                   "Market_Cap", "Name", "Ticker"])

    # Winsorise — remove extreme outliers (Week 6 — data cleaning)
    vk_df = vk_df[vk_df["AvgCost_of_Debt"] < 5]
    vk_df = vk_df[vk_df["Z_Score_lag"].between(-10, 40)]

    # Feature engineering (Week 4)
    vk_df = vk_df.copy()
    vk_df["cost_pct"] = vk_df["AvgCost_of_Debt"] * 100
    vk_df["mcap_bn"]  = vk_df["Market_Cap"] / 1e9

    # Pre-aggregate sector statistics — used by multiple tabs
    sec_stats = (
        vk_df.groupby("Sector_Key")
        .agg(
            avg_cost_pct=("cost_pct", "mean"),
            avg_zscore=("Z_Score_lag", "mean"),
            avg_mcap_bn=("mcap_bn", "mean"),
            n_companies=("Name", "nunique"),
            n_obs=("Name", "count"),
        )
        .round(3)
        .reset_index()
        .rename(columns={"Sector_Key": "Sector"})
    )

    # Top 5 companies per sector by average market cap — for sunburst chart
    _tc = (
        vk_df.groupby(["Sector_Key", "Name"])["mcap_bn"]
        .mean()
        .reset_index()
    )
    _tc = _tc[_tc["mcap_bn"] > 0]
    _tc = _tc.sort_values("mcap_bn", ascending=False)
    _tc = (
        _tc.groupby("Sector_Key", group_keys=False)
        .apply(lambda g: g.head(5))
        .reset_index(drop=True)
    )
    top_companies = _tc.rename(columns={
        "Sector_Key": "Sector",
        "Name": "Company",
        "mcap_bn": "Avg_MCap_Bn",
    })

    return sec_stats, top_companies, vk_df


@app.cell
def _(mo):
    tab_profile = mo.md("""
## Vanesh Kumar

Email: Vanesh.kumar@bayes.city.ac.uk | Mobile: +44 7365353362

---

**Profile**

Motivated Accounting and Finance student at City St Georges, University of London,
with internship experience in ledger management, invoice checking, and financial
documentation. Strong analytical skills, attention to detail, and growing technical
ability in Excel and Python.

---

**Education**

BSc Accounting and Finance | City St Georges, University of London | 2025 to 2028

International Foundation Year (Computer Science) | Durham University | Completed 2025

A-Levels: Computer Science (D), Mathematics (C), Physics (D)
Foundation Public School, Hyderabad | 2022 to 2024

---

**Experience**

Accounting Intern, United Agro Chemicals | Oct 2024 to Nov 2024
- Organised financial documents, checked invoices, updated records using Excel

Finance Accounting Intern, SGM Sugar Mills Ltd | Jun 2024 to Jul 2024
- Assisted in maintaining ledgers and reviewing expenses for accuracy

---

**Skills:** Python, pandas, Plotly, Marimo, Excel | Languages: English, Urdu
    """)
    return (tab_profile,)


@app.cell
def _(mo, tab_profile):
    app_tabs = mo.ui.tabs({"Profile": tab_profile})
    mo.md(f"""
# Vanesh Kumar
AF1204 Individual Portfolio | BSc Accounting and Finance | City St Georges, University of London

---

{app_tabs}
    """)
    return


if __name__ == "__main__":
    app.run()
