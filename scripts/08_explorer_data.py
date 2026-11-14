"""Viz explorer data: aggregate the costed+carbon call table into a small cube for explorer/index.html.

Output: explorer/data.js  (window.EXPLORER_DATA = {...})
  cube   - one row per tenant x model: sums of calls, outcomes, tokens, cost, energy (low/central/high), carbon
  dist   - token quantiles (p10/p25/p50/p75/p90) of successful calls for each grouping dimension value
  meta   - date range, row count, sources
Data is synthetic; energy/carbon are ESTIMATES (see process-log.md B3, B0b).
Run from repo root: py scripts/08_explorer_data.py
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data-clean" / "calls_costed_carbon__pricing_list.csv"
OUT = ROOT / "explorer" / "data.js"

PURPOSE = {  # D17: data's model names + purpose label
    "o1-preview": "Reasoning",
    "gpt-4o": "Frontier", "gemini-1.5-pro": "Frontier",
    "gpt-4o-mini": "Small/fast", "gemini-1.5-flash": "Small/fast",
}

cols = ["model", "tenant_id", "provider", "status_code", "is_success", "input_tokens", "output_tokens",
        "cached_input_tokens", "reasoning_tokens", "persona_label", "environment", "merge_candidate",
        "cost_usd", "cost_usd_no_cache", "wh_low", "wh_central", "wh_high",
        "gco2e_low", "gco2e_central", "gco2e_high", "date"]
df = pd.read_csv(SRC, usecols=cols)
df["purpose"] = df["model"].map(PURPOSE)
df["is_400"] = df.status_code.eq(400)
df["is_429"] = df.status_code.eq(429)
for c in ["input_tokens", "output_tokens", "cached_input_tokens", "reasoning_tokens"]:
    df[c] = df[c].fillna(0)

keys = ["tenant_id", "persona_label", "provider", "environment", "merge_candidate", "model", "purpose"]
cube = (df.groupby(keys).agg(
    calls=("is_success", "size"), success=("is_success", "sum"), e400=("is_400", "sum"), e429=("is_429", "sum"),
    input_tokens=("input_tokens", "sum"), output_tokens=("output_tokens", "sum"),
    cached_tokens=("cached_input_tokens", "sum"), reasoning_tokens=("reasoning_tokens", "sum"),
    cost=("cost_usd", "sum"), cost_nocache=("cost_usd_no_cache", "sum"),
    wh_low=("wh_low", "sum"), wh_central=("wh_central", "sum"), wh_high=("wh_high", "sum"),
    g_low=("gco2e_low", "sum"), g_central=("gco2e_central", "sum"), g_high=("gco2e_high", "sum"),
).reset_index())
for c in ["success", "e400", "e429"]:
    cube[c] = cube[c].astype(int)

dims = {"persona": "persona_label", "model": "model", "purpose": "purpose",
        "environment": "environment", "provider": "provider", "merge": "merge_candidate"}
ok = df[df.is_success]
dist = {}
for dim, col in dims.items():
    dist[dim] = {}
    for tok in ["input_tokens", "output_tokens"]:
        q = ok.groupby(col)[tok].quantile([.1, .25, .5, .75, .9]).unstack()
        dist[dim][tok] = {k: [round(float(v)) for v in row] for k, row in q.iterrows()}

meta = {
    "rows": int(len(df)), "date_min": str(df.date.min()), "date_max": str(df.date.max()),
    "note": "Synthetic telemetry (CMU IronViz Fall 2026). Cost = list prices (some unverified). "
            "Energy/carbon = estimates from Jegham et al. 2025 + Google 2025 benchmarks x CodeCarbon grid factors.",
}
OUT.parent.mkdir(exist_ok=True)
payload = {"meta": meta, "cube": cube.round(6).to_dict(orient="records"), "dist": dist}
OUT.write_text("window.EXPLORER_DATA = " + json.dumps(payload) + ";\n", encoding="utf-8")
print(f"wrote {OUT} ({len(cube)} cube rows, {OUT.stat().st_size/1024:.1f} KB)")
