"""Dashboard data (D26): every number the one-page dashboard shows, computed from data-clean outputs.

Only LOCAL-GOOD scenario results are used (D26: the global-good / combined totals are kept out of visuals).
Output: dashboard/data.js  (window.DASH = {...})
Run from repo root (after 03, 06, 05, 07): py scripts/09_dashboard_data.py
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DC = ROOT / "data-clean"
OUT = ROOT / "dashboard" / "data.js"
PURPOSE = {"o1-preview": "Reasoning", "gpt-4o": "Frontier", "gemini-1.5-pro": "Frontier",
           "gpt-4o-mini": "Small/fast", "gemini-1.5-flash": "Small/fast"}
OUTLIERS = ["org-engineering-dev", "prj-ai-sandbox-testing"]

calls = pd.read_csv(DC / "calls_costed_carbon__pricing_list.csv",
                    usecols=["tenant_id", "provider", "model", "is_success", "cost_usd", "wh_central"])
pm = pd.read_csv(DC / "persona_metrics.csv")
carbon = pd.read_csv(DC / "carbon_by_tenant__pricing_list.csv")
scen = pd.read_csv(DC / "scenarios_by_tenant__pricing_list.csv")
err = pd.read_csv(DC / "scenario_errors_avoided__pricing_list.csv")

# 1. headline (30 days)
camp = scen[(scen.tenant_id == "ALL_CAMPUS") & (scen.scenario == "actual")].iloc[0]
headline = {
    "requests": int(len(calls)), "success": int(calls.is_success.sum()),
    "cost": float(camp.cost_usd),
    "kwh": [float(camp.kwh_low), float(camp.kwh_central), float(camp.kwh_high)],
    "kgco2e": [float(carbon.kgco2e_30d_low.sum()), float(carbon.kgco2e_30d_central.sum()), float(carbon.kgco2e_30d_high.sum())],
}

# 2. persona cards
cards = []
for _, r in pm.iterrows():
    c = carbon[carbon.tenant_id == r.tenant_id].iloc[0]
    cards.append({
        "tenant": r.tenant_id, "persona": r.persona_label, "provider": r.provider,
        "outlier": r.tenant_id in OUTLIERS,
        "requests": int(c.calls),
        "prompt_median": float(r.median_input_tokens), "cache_pct": float(r.cache_share_pct),
        "r400_pct": float(r.pct_400), "premium_pct": float(r.pct_calls_premium_model),
        "cost_per": float(r.cost_per_success_usd), "wh_per": float(r.wh_per_success_central),
    })
eff = pm[~pm.tenant_id.isin(OUTLIERS)]
majority = {  # range across the 4 efficient groups (statistically indistinguishable, script 04)
    "cache_pct": [float(eff.cache_share_pct.min()), float(eff.cache_share_pct.max())],
    "r400_pct": [float(eff.pct_400.min()), float(eff.pct_400.max())],
    "prompt_median_openai": float(eff[eff.provider == "openai"].median_input_tokens.median()),
    "prompt_median_gemini": float(eff[eff.provider == "gemini"].median_input_tokens.median()),
}

# 3. reasoning share (OpenAI, successful requests)
oa = calls[(calls.provider == "openai") & calls.is_success].assign(purpose=lambda d: d.model.map(PURPOSE))
g = oa.groupby("purpose").agg(req=("model", "size"), cost=("cost_usd", "sum"), wh=("wh_central", "sum"))
share = (100 * g / g.sum()).round(2)
purpose_share = {p: {"requests": float(share.loc[p, "req"]), "cost": float(share.loc[p, "cost"]),
                     "energy": float(share.loc[p, "wh"])} for p in ["Reasoning", "Frontier", "Small/fast"]}
per_req = (g.cost / g.req)
cost_ratio_reasoning_vs_frontier = float(per_req["Reasoning"] / per_req["Frontier"])

# 4. local-good opportunity (Dev & Sandbox only)
levers = {"L1_cache": "Reuse stable prompt text (cache)", "L2_prompt": "Trim prompts",
          "L3_model_mix": "Use the small model for routine work", "L_all": "All three together"}
opp = {}
for t in OUTLIERS:
    s = scen[scen.tenant_id == t].set_index("scenario")
    a = s.loc["actual"]
    opp[t] = {"actual_cost": float(a.cost_usd), "actual_kwh": float(a.kwh_central),
              "levers": [{"key": k, "label": v, "d_cost": float(s.loc[k].delta_cost_usd),
                          "d_cost_pct": float(s.loc[k].delta_cost_usd_pct),
                          "d_kwh": float(s.loc[k].delta_kwh_central),
                          "d_kwh_pct": float(s.loc[k].delta_kwh_central_pct)} for k, v in levers.items()],
              "failed_avoided": int(err[err.tenant_id == t].failed_400_calls_avoided_30d.iloc[0])}
cl = scen[(scen.tenant_id == "ALL_CAMPUS")].set_index("scenario")
campus_local = {"d_cost": float(cl.loc["L_all"].delta_cost_usd), "d_cost_pct": float(cl.loc["L_all"].delta_cost_usd_pct),
                "d_kwh": float(cl.loc["L_all"].delta_kwh_central), "d_kwh_pct": float(cl.loc["L_all"].delta_kwh_central_pct),
                "d_kwh_low": float(cl.loc["L_all"].kwh_low - cl.loc["actual"].kwh_low),
                "d_kwh_high": float(cl.loc["L_all"].kwh_high - cl.loc["actual"].kwh_high),
                "failed_avoided": int(err.failed_400_calls_avoided_30d.sum())}

# 5. (P14 prototypes) per-request averages by purpose (OpenAI), and a "request builder" model kit
per_purpose = {p: {"cost": float(g.loc[p, "cost"] / g.loc[p, "req"]), "wh": float(g.loc[p, "wh"] / g.loc[p, "req"])}
               for p in ["Reasoning", "Frontier", "Small/fast"]}
import numpy as np
full = pd.read_csv(DC / "calls_costed_carbon__pricing_list.csv",
                   usecols=["tenant_id", "model", "is_success", "input_tokens", "output_tokens",
                            "cached_input_tokens", "reasoning_tokens"])
ok = full[full.is_success & ~full.tenant_id.isin(OUTLIERS)]
price = pd.read_csv(ROOT / "config" / "pricing_list.csv").set_index("model")
bench = pd.read_csv(ROOT / "config" / "energy_benchmarks.csv").set_index("benchmark_model")
cp = pd.read_csv(ROOT / "config" / "carbon_params.csv").set_index("param")["value"]
coef = {}
for bm, r in bench.iterrows():  # exact 3-point fit, same as 06_carbon.py
    A = np.array([[1, 100, 300], [1, 1000, 1000], [1, 10000, 1500]], float)
    a, bi, bo = np.linalg.solve(A, np.array([r.short_wh, r.medium_wh, r.long_wh]))
    coef[bm] = {"a": a, "b_in": bi, "b_out": bo}
kit = {}
for m in PURPOSE:
    o = ok[ok.model == m]
    bm = cp[f"model_map:{m}"]
    hidden = (o.reasoning_tokens / o.output_tokens).median() if m == "o1-preview" else 0.0
    kit[m] = {"purpose": PURPOSE[m],
              "price_in": float(price.loc[m, "usd_per_1m_input"]), "price_cached": float(price.loc[m, "usd_per_1m_cached_input"]),
              "price_out": float(price.loc[m, "usd_per_1m_output"]), "price_status": price.loc[m, "status"],
              "energy": {k: float(v) for k, v in coef[bm].items()}, "energy_proxy": bm != m,
              "baseline": {"prompt": float(o.input_tokens.median()), "output": float(o.output_tokens.median()),
                           "cache_share": float(o.cached_input_tokens.sum() / o.input_tokens.sum()),
                           "hidden_share": float(hidden)}}
    od = full[full.is_success & full.tenant_id.isin(OUTLIERS) & (full.model == m)]
    if len(od):
        kit[m]["outlier"] = {"prompt": float(od.input_tokens.median()), "output": float(od.output_tokens.median()),
                             "cache_share": float(od.cached_input_tokens.sum() / od.input_tokens.sum())}
energy_params = {"low_scale": float(cp["low_energy_scale"]), "cached_low": float(cp["cached_input_energy_share_low"]),
                 "cached_high": float(cp["cached_input_energy_share_high"])}
equivalents = {"phone_charge_kwh": 0.019, "phone_source": "US EPA Greenhouse Gas Equivalencies Calculator, calculations and references (smartphone charged = 0.019 kWh; DOE/Dommu 2024)",
               "led_bulb_w": 10, "led_note": "ASSUMPTION: a typical 10 W LED bulb"}

OUT.parent.mkdir(exist_ok=True)
payload = {"headline": headline, "cards": cards, "majority": majority, "purpose_share": purpose_share,
           "cost_ratio_reasoning_vs_frontier": cost_ratio_reasoning_vs_frontier,
           "opportunity": opp, "campus_local": campus_local,
           "per_purpose": per_purpose, "kit": kit, "energy_params": energy_params, "equivalents": equivalents}
OUT.write_text("window.DASH = " + json.dumps(payload, indent=1) + ";\n", encoding="utf-8")
print(json.dumps({k: payload[k] for k in ["headline", "purpose_share", "campus_local", "majority"]}, indent=1),
      "\nratio", round(cost_ratio_reasoning_vs_frontier, 2))
