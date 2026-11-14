"""Step 4 / D16: what-if scenarios -> how much cost and energy each lever could save, per persona.

LOCAL GOOD (outliers only: Engineering/Dev, Sandbox) - match what CMU's own best tenants already do:
  L1 cache     raise token-weighted cache share to the best baseline tenant's share
  L2 prompt    shrink prompts (per model) to the best baseline tenant's median prompt size
  L3 model mix move excess frontier-model calls (gpt-4o / gemini-1.5-pro) to the small model
               (gpt-4o-mini / gemini-1.5-flash) until the frontier share matches the best baseline tenant;
               the calls moved are the ones with the smallest output (proxy for routine tasks)
  L4 errors    cut the 400 rate to the best baseline tenant's rate (reported as failed calls avoided; failed
               calls cost $0 / 0 Wh in this model, see B0b X12)
  L_all        L1 + L2 + L3
GLOBAL GOOD (all tenants) - provider best practices, thresholds in config/scenario_params.csv (ASSUMPTIONS):
  G1 cache     token-weighted cache share -> global_cache_share_target
  G2 reasoning route global_reasoning_route_share of o1-preview calls to gpt-4o (hidden reasoning tokens dropped)
  G3 output cap  cap visible output at a percentile of the baseline's output for that model
  G_all        G1 + G2 + G3
LG_all         L_all then G_all (outliers); equals G_all for baseline tenants

Cost and energy use the same formulas and config files as 03_cost.py and 06_carbon.py.
Data is synthetic; energy is an ESTIMATE; some prices are unverified (B0b).
Run from repo root: py scripts/07_scenarios.py [config/pricing_X.csv]
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
pricing_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "config" / "pricing_list.csv"
if not pricing_path.is_absolute():
    pricing_path = ROOT / pricing_path
tag = pricing_path.stem

price = pd.read_csv(pricing_path).set_index("model")
bench = pd.read_csv(ROOT / "config" / "energy_benchmarks.csv")
cp = pd.read_csv(ROOT / "config" / "carbon_params.csv").set_index("param")["value"]
sp = pd.read_csv(ROOT / "config" / "scenario_params.csv").set_index("param")["value"]

BASE = ["org-prod-core", "org-marketing-ai", "prj-ai-enterprise-prod", "prj-ai-r-and-d"]
OUTLIERS = ["org-engineering-dev", "prj-ai-sandbox-testing"]
FRONTIER = {"openai": "gpt-4o", "gemini": "gemini-1.5-pro"}
SMALL = {"openai": "gpt-4o-mini", "gemini": "gemini-1.5-flash"}
REASONING, REASONING_TO = "o1-preview", "gpt-4o"

# ---- energy coefficients (same exact 3-point solve as 06_carbon.py) ----
SIZES = np.array([[1, 100, 300], [1, 1000, 1000], [1, 10000, 1500]], float)
coef = {r.benchmark_model: np.linalg.solve(SIZES, [r.short_wh, r.medium_wh, r.long_wh]) for _, r in bench.iterrows()}
model_map = {k.split(":", 1)[1]: v for k, v in cp.items() if k.startswith("model_map:")}
LOW_SCALE = float(cp["low_energy_scale"])
SH_LO, SH_HI = float(cp["cached_input_energy_share_low"]), float(cp["cached_input_energy_share_high"])
GRID_C = float(cp["grid_g_per_kwh_central"])

raw = pd.read_csv(ROOT / "data-clean" / "calls_unified.csv")
s0 = raw[raw.is_success].copy()
s0["reasoning_tokens"] = s0["reasoning_tokens"].fillna(0)
s0 = s0[["tenant_id", "persona_label", "provider", "model", "input_tokens", "cached_input_tokens",
         "output_tokens", "reasoning_tokens"]].reset_index(drop=True)


def totals(s):
    """Per-tenant cost and energy for a (possibly modified) frame of successful calls."""
    p = price.loc[s.model]
    unc = (s.input_tokens - s.cached_input_tokens).to_numpy()
    cac, out = s.cached_input_tokens.to_numpy(), s.output_tokens.to_numpy()
    cost = (unc * p.usd_per_1m_input.to_numpy() + cac * p.usd_per_1m_cached_input.to_numpy()
            + out * p.usd_per_1m_output.to_numpy()) / 1e6
    c = np.array([coef[model_map[m]] for m in s.model])
    a, bi, bo = c[:, 0], c[:, 1], c[:, 2]
    hi = a + bi * (unc + cac * SH_HI) + bo * out
    lo = LOW_SCALE * (a + bi * (unc + cac * SH_LO) + bo * out)
    t = pd.DataFrame({"tenant_id": s.tenant_id, "cost_usd": cost, "wh_low": lo, "wh_high": hi,
                      "wh_central": (lo + hi) / 2})
    g = t.groupby("tenant_id").sum()
    out_df = pd.DataFrame({"cost_usd": g.cost_usd,
                           "kwh_low": g.wh_low / 1000, "kwh_central": g.wh_central / 1000, "kwh_high": g.wh_high / 1000})
    out_df["kgco2e_central"] = out_df.kwh_central * GRID_C / 1000
    return out_df


# ---- local-good targets (best observed value among the 4 baseline tenants) ----
b = s0[s0.tenant_id.isin(BASE)]
cache_share = s0.groupby("tenant_id").apply(lambda d: d.cached_input_tokens.sum() / d.input_tokens.sum())
LOCAL_CACHE = cache_share[BASE].max()
best_median = (b.groupby(["provider", "model", "tenant_id"]).input_tokens.median()
                .groupby(["provider", "model"]).min())
frontier_share = s0.groupby(["provider", "tenant_id"]).apply(lambda d: (d.model == FRONTIER[d.name[0]]).mean())
LOCAL_FRONTIER = {pv: frontier_share[pv][[t for t in BASE if t in frontier_share[pv].index]].min() for pv in FRONTIER}
pct400 = raw.groupby("tenant_id").apply(lambda d: (d.status_code == 400).mean())
LOCAL_400 = pct400[BASE].min()
calls_all = raw.groupby("tenant_id").size()
visible = lambda d: d.output_tokens - d.reasoning_tokens
OUT_CAP = (b.assign(v=visible(b)).groupby("model").v.quantile(float(sp["global_output_cap_percentile"])))


# ---- scenario transforms (each returns a modified copy) ----
def raise_cache(s, tenants, target):
    s = s.copy()
    for t in tenants:
        m = s.tenant_id == t
        sh = s.loc[m, "cached_input_tokens"].sum() / s.loc[m, "input_tokens"].sum()
        if sh < target:
            f = (target - sh) / (1 - sh)  # same fraction of each call's uncached input becomes cached
            s.loc[m, "cached_input_tokens"] += (s.loc[m, "input_tokens"] - s.loc[m, "cached_input_tokens"]) * f
    return s


def trim_prompts(s, tenants):
    s = s.copy()
    for t in tenants:
        for (pv, mdl), target in best_median.items():
            m = (s.tenant_id == t) & (s.model == mdl)
            if not m.any():
                continue
            r = min(1.0, target / s.loc[m, "input_tokens"].median())
            s.loc[m, ["input_tokens", "cached_input_tokens"]] *= r
    return s


def move_calls(s, mask, n, new_model, drop_reasoning=False):
    idx = s[mask].assign(v=visible(s[mask])).sort_values("v").index[:max(0, int(round(n)))]
    s.loc[idx, "model"] = new_model
    if drop_reasoning:
        s.loc[idx, "output_tokens"] -= s.loc[idx, "reasoning_tokens"]
        s.loc[idx, "reasoning_tokens"] = 0
    return s


def fix_model_mix(s, tenants):
    s = s.copy()
    for t in tenants:
        tm = s.tenant_id == t
        pv = s.loc[tm, "provider"].iloc[0]
        excess = (s.loc[tm, "model"] == FRONTIER[pv]).mean() - LOCAL_FRONTIER[pv]
        s = move_calls(s, tm & (s.model == FRONTIER[pv]), excess * tm.sum(), SMALL[pv])
    return s


def route_reasoning(s, share):
    s = s.copy()
    for t in s.tenant_id.unique():
        m = (s.tenant_id == t) & (s.model == REASONING)
        s = move_calls(s, m, share * m.sum(), REASONING_TO, drop_reasoning=True)
    return s


def cap_output(s):
    s = s.copy()
    cap = s.model.map(OUT_CAP)
    s["output_tokens"] = s.reasoning_tokens + np.minimum(visible(s), cap)
    return s


ALL = list(s0.tenant_id.unique())
G_CACHE = float(sp["global_cache_share_target"])
G_ROUTE = float(sp["global_reasoning_route_share"])
L_all = lambda s: fix_model_mix(trim_prompts(raise_cache(s, OUTLIERS, LOCAL_CACHE), OUTLIERS), OUTLIERS)
G_all = lambda s: cap_output(route_reasoning(raise_cache(s, ALL, G_CACHE), G_ROUTE))

SCEN = [
    ("actual", "Actual (Oct 2026)", "actual", lambda s: s),
    ("L1_cache", f"Cache like CMU's best tenant ({LOCAL_CACHE:.1%})", "local good", lambda s: raise_cache(s, OUTLIERS, LOCAL_CACHE)),
    ("L2_prompt", "Prompt size like CMU's best tenant", "local good", lambda s: trim_prompts(s, OUTLIERS)),
    ("L3_model_mix", "Frontier-model share like CMU's best tenant", "local good", lambda s: fix_model_mix(s, OUTLIERS)),
    ("L_all", "All local-good levers", "local good", L_all),
    ("G1_cache", f"Cache share {G_CACHE:.0%} (global best practice)", "global good", lambda s: raise_cache(s, ALL, G_CACHE)),
    ("G2_route_reasoning", f"Route {G_ROUTE:.0%} of o1-preview calls to gpt-4o", "global good", lambda s: route_reasoning(s, G_ROUTE)),
    ("G3_output_cap", f"Cap visible output at baseline p{float(sp['global_output_cap_percentile'])*100:.0f}", "global good", cap_output),
    ("G_all", "All global-good levers", "global good", G_all),
    ("LG_all", "Local good + global good", "combined", lambda s: G_all(L_all(s))),
]

rows = []
for sid, label, grp, fn in SCEN:
    r = totals(fn(s0))
    r.loc["ALL_CAMPUS"] = r.sum()
    r["scenario"], r["scenario_label"], r["group"] = sid, label, grp
    rows.append(r)
res = pd.concat(rows).reset_index().rename(columns={"index": "tenant_id"})
act = res[res.scenario == "actual"].set_index("tenant_id")
for col in ("cost_usd", "kwh_central", "kgco2e_central"):
    base = res.tenant_id.map(act[col])
    res[f"delta_{col}"] = res[col] - base
    res[f"delta_{col}_pct"] = (res[col] - base) / base * 100
labels = s0.groupby("tenant_id").persona_label.first()
labels["ALL_CAMPUS"] = "All campus"
res.insert(1, "persona_label", res.tenant_id.map(labels))

# L4: failed (400) calls avoided - reported separately, no $ / Wh attached (B0b X12)
err = pd.DataFrame({"pct_400_actual": pct400 * 100, "pct_400_local_good": LOCAL_400 * 100, "calls": calls_all})
err["failed_400_calls_avoided_30d"] = ((pct400 - LOCAL_400).clip(lower=0) * calls_all).round().where(err.index.isin(OUTLIERS), 0)

out_dir = ROOT / "data-clean"
res.round(4).to_csv(out_dir / f"scenarios_by_tenant__{tag}.csv", index=False)
err.round(3).to_csv(out_dir / f"scenario_errors_avoided__{tag}.csv")

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 20)
print(f"Pricing: {pricing_path.name}")
print(f"Local-good targets: cache share {LOCAL_CACHE:.3%}; frontier share {LOCAL_FRONTIER}; 400 rate {LOCAL_400:.3%}")
print("Best-tenant median prompt per model:\n", best_median.to_string())
print("Output caps (visible tokens):\n", OUT_CAP.round(0).to_string())
view = res[["tenant_id", "scenario", "cost_usd", "delta_cost_usd_pct", "kwh_central", "delta_kwh_central_pct"]]
print("\n", view.pivot(index="scenario", columns="tenant_id", values="delta_cost_usd_pct").round(1).loc[[x[0] for x in SCEN]].to_string())
print("\nEnergy change % (central):\n", view.pivot(index="scenario", columns="tenant_id", values="delta_kwh_central_pct").round(1).loc[[x[0] for x in SCEN]].to_string())
camp = res[res.tenant_id == "ALL_CAMPUS"].set_index("scenario")[["cost_usd", "delta_cost_usd", "kwh_central", "delta_kwh_central", "delta_kgco2e_central"]]
print("\nCampus totals (30 days):\n", camp.round(1).to_string())
print("\n400s avoided:\n", err.to_string())
