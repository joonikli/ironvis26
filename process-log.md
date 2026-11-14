# process-log.md — IronViz Process Log

> Filled in by the agent as work happens. Instructions live in `process.md`.

## B0. Decision Register (human decisions)
> Every decision the human makes is recorded here, in order, with what the AI proposed and where the decision is applied. B6 has the fuller collaboration narrative. Status: ✅ decided · ⏳ pending · 🔁 revisited.

| ID | Date | Decision area | AI proposed | **Human decision** | Why / note | Applied in | Status |
|---|---|---|---|---|---|---|---|
| D1 | 2026-11-14 | Working style | n/a | Ask the human on major decisions, and **ask before making any visuals** | Human-in-the-loop control over story and visuals | All work | ✅ |
| D2 | 2026-11-14 | Persona mapping | Merge the 6 tenants into 4 personas | **Keep all 6 tenants separate**, and label what each could combine with. Use the data dictionary crosswalk to merge across OpenAI and Gemini | Stay faithful to the data and keep options open | B2; `merge_candidate` column in `scripts/01_clean_harmonize.py` | ✅ |
| D3 | 2026-11-14 | Audience | Offered CIO, provost/deans, or a mixed audience | **Mixed campus audience** (a dean, a student, and an IT admin) | Each persona should leave knowing which of their own AI habits to change | B1; plain language throughout | ✅ |
| D4 | 2026-11-14 | Tooling | Install pandas | **Accepted:** install pandas | | `scripts/*` | ✅ |
| D5 | 2026-11-14 | Source of truth for synthetic-data questions | Claude was reasoning from the files alone | **Use the competition info-session deck** to answer questions about the synthetic data | It's the organizers' authoritative description | B3 (deck vs. data check) | ✅ |
| D6 | 2026-11-14 | Deck/data mismatch | Report the mismatch openly | **Ignore the deck's anomaly claims** and analyze only what's in the data | | B3 | ✅ |
| D7 | 2026-11-14 | Student persona | Map students by workload (recommended) | **Accepted:** sandbox-testing and R&D are the student proxies, **labeled as an assumption** | Timestamps can't separate students from staff | B2, B3 methods | ✅ |
| D8 | 2026-11-14 | Story focus for the 4 look-alike tenants | Dev/sandbox vs. "efficient baseline" | **Dig for small differences first**, then decide | Make sure the 4 are truly alike before merging them in the story | `scripts/04_small_differences.py`; B4 (result: no meaningful differences) | 🔁 to be re-decided with the evidence (see P1) |
| D9 | 2026-11-14 | Pricing source | Published list prices | **Use list prices for now, swappable for CMU AI Gateway rates later** | CMU's own rates may differ | `config/pricing_list.csv`, `config/README.md`, `scripts/03_cost.py` | ✅ |
| D10 | 2026-11-14 | Documentation | n/a | **Document every human decision in `process-log.md`** | Rubric criterion 7 (human-in-the-loop documentation) | This section (B0) | ✅ |
| D11 | 2026-11-14 | Story focus (resolves P1, revisits D8) | Three threads: dev/sandbox outlier, o1-preview cost, caching | **Dev and sandbox are the outliers. Find the best of the other 4 as "local good" (what good looks like at CMU). Find "global good" from external data and token-efficiency best practices** | Two benchmarks: local (best CMU tenant) and global (outside best practice). Personas are measured against both | Story structure; `scripts/05_local_best.py` (planned) | ✅ |
| D12 | 2026-11-14 | Carbon method (resolves P2) | Energy per 1K tokens from Hugging Face carbon logs × CodeCarbon grid factors, shown as a low-to-high range | **Accepted as proposed** | | `scripts/06_carbon.py` (planned) | ✅ |
| D13 | 2026-11-14 | Price verification (P3) | Human checks archived pricing pages | **Hold off for now.** Unverified prices stay flagged | | `config/pricing_list.csv` status column | ⏸ deferred |
| D14 | 2026-11-14 | Carbon baseline (revises D12) | The HF dataset turned out to be 10 laptop-CPU runs of plain Python (no LLM, no tokens), so it can't give energy per token. Claude proposed a published LLM range instead | **Accepted the published LLM range.** Low end: Google's measured median Gemini prompt (0.24 Wh; arXiv:2508.15734). High end: the "How Hungry is AI?" GPT-4o estimate (about 0.42 Wh short query; arXiv:2505.09598). Scale by tokens, × CodeCarbon grid factors. HF dataset cited only as context | Use LLM-specific evidence, shown as a range rather than one false-precision number | `scripts/06_carbon.py` (planned), B7 citations | ✅ |
| D15 | 2026-11-14 | Persona labels (resolves P4) | The 6 labels in B2 | **Keep as proposed** | | B2, `persona_label` column | ✅ |
| D16 | 2026-11-14 | "Global good" method (resolves P5) | Offered: what-if scenarios on our data (recommended), fixed external targets, or local good only | **What-if scenarios.** Provider best practices (prompt caching, routing simple tasks to smaller models, output-length caps) are applied to our calls to estimate Δ$ and ΔkWh | Shows how big each lever is for each persona | `scripts/07_scenarios.py`, `config/scenario_params.csv`, B4, B8 | ✅ |
| D17 | 2026-11-14 | Model naming (resolves P6) | Offered: tier names with today's models in footnotes (recommended), the data's model names, or current model names | **Use the data's model names, each with a label for what that model is for**, e.g. "o1-preview (reasoning model, for multi-step problems)", "gpt-4o / gemini-1.5-pro (frontier model, for general high-quality work)", "gpt-4o-mini / gemini-1.5-flash (small/fast model, for routine tasks)" | Stays faithful to the data and still tells readers what each model does | All visuals and B8; the retirement status stays in the limitations (B0b notice) | ✅ |
| D18 | 2026-11-14 | Model drift as a lens on the main question | Claude offered 7 angles: (1) lasting habits vs expiring details, (2) a purpose → current-model table, (3) ratios + swappable re-runs, (4) retiring-model risk + migration playbook, (5) persona roles, (6) dated ranges / benchmark drift, (7) model-independent monitoring | **User note:** the models are outdated on purpose, to teach working past outdated data and model drift. **Adopted angles 1, 2, 5 and 6.** Not adopted: 3, 4 and 7. Note added to `instructionsprocess.md` §1 as drafted | Recommendations must stay useful after the models change | `instructionsprocess.md` §1 "Lens"; B8 shelf-life tags; date stamps on charts | ✅ |
| D19 | 2026-11-14 | Build tool (resolves P7) | Tableau Public if required; otherwise code-generated charts exported to PDF/PNG | **HTML/Python**: Python prepares the chart data, and an HTML page draws the charts and is exported to PDF/PNG | Data and scripts are already in Python | Viz build | ✅ |
| D20 | 2026-11-14 | Dashboard story and scope (resolves P8) | 4–5 charts on one page: problem → persona breakdown → hidden driver → opportunity → recommendations | **Accepted with edits:** (a) the **persona breakdown must be filterable** by persona; (b) the **"hidden driver" (o1-preview) chart is open for rethinking**: Claude to suggest other widgets or visualizations that fit the model-drift lens (D18) → P12. The rest of the order is accepted | Interactivity lets each persona find themselves. The hidden-driver chart should not depend on a retired model's name alone | B5 | ✅ (P12 open) |
| D21 | 2026-11-14 | How to show personas (resolves P9) | All 6 in one color system, with Dev and Sandbox highlighted and the other 4 muted | **Show all 6** | Consistent with D2 | All visuals, palette | ✅ |
| D23 | 2026-11-14 | Scenario inputs (resolves P11 and P13) | Replace the invented targets (50% cache, 50% reasoning reroute) with inputs from our data only | **Yes: inputs must come only from our data.** Headline = local good (CMU's best tenant). Outside practices are sized per unit (+10 points of cache share; per reasoning request moved). The 75% figure is shown only as a ceiling. The global (−32%) and combined (−41%) totals are dropped | User: "the 50% isn't based on anything. That's bad." | `config/scenario_params.csv`, `scripts/07_scenarios.py` (to update), B0a #9 | ✅ |
| D24 | 2026-11-14 | Focus and viz exploration | Claude summarized open items and suggested applying D23 to the scenarios first | **Rejected: do not apply D23 to the code for now.** Focus on data visualization and visual aesthetics. User asked for a simple HTML + JavaScript program to explore different arrangements of the data | Explore chart forms before committing to a dashboard | `scripts/08_explorer_data.py` → `explorer/data.js`; `explorer/index.html` | ✅ |
| D25 | 2026-11-14 | Viz explorer (revisits D24) | Claude built and opened `explorer/index.html` | **Rejected: "not very good, scratch the idea for now."** Files left in place (not deleted) in case it's revisited. User asked Claude to review past decisions and suggest next steps | | `explorer/` (shelved) | ✅ |
| D26 | 2026-11-14 | Apply the decision-review suggestions; local good only | Claude reviewed D1–D25 and made 10 suggestions: static persona cards instead of a filter; experimental work as the student role; "efficient majority" instead of naming Core Production; keep the global/combined totals out; show o1-preview as a ratio and flag its price; show 400s as wasted requests; lead with energy and give carbon only as a range; close P12 with E5 + F5; a 4-part story; a sentence on the slides' anomalies | **Accepted all. "Keep those numbers out, only use local good result."** The −32% (global) and −41% (combined) totals appear in no visual. P12 resolved as E5 (share of requests vs cost and energy) + F5 (persona cards). D23 code changes are still not applied (D24) | `scripts/09_dashboard_data.py` → `dashboard/data.js`; `dashboard/index.html` | ✅ |
| D27 | 2026-11-14 | Creative prototypes (P14) | Claude proposed A–E and recommended A + B as a static poster | **"Build all of them to prototype."** Built `prototypes/index.html`: (A) isometric server rooms (1 block = 5 kWh, 1 sheet = 500 prompt tokens, blue = cached, 1 red light = 1 broken request in 100); (B) a 100-square unit chart that morphs between requests, cost and energy, plus coin stacks; (C) a request-builder toy with sliders and presets (efficient group, Dev habit, Sandbox habit, reasoning for a routine question) that uses the same price and energy formulas as scripts 03 and 06; (D) scrollytelling of one prompt's journey; (E) everyday comparisons (phone charges at 0.019 kWh from the US EPA; LED minutes with an assumed 10 W bulb). Local-good results only. No 3D/three.js | User to pick which to keep | `scripts/09_dashboard_data.py` (adds per_purpose, kit, equivalents) → `dashboard/data.js`; `prototypes/index.html` | ⏳ awaiting pick |
| D22 | 2026-11-14 | Recommendations draft (P10) | Draft levers per persona | **Keep the draft as a section in this file for now** (B8, marked DRAFT). Not final | Revisit once the charts exist | B8 | ✅ (draft) |

**Pending decisions (waiting on the human):**
| ID | Question | AI recommendation | Status |
|---|---|---|---|
| P3 | Verify unverified prices (o1-preview, gemini-1.5-pro, flash cached) | Human checks the archived late-2024 official pricing pages in a browser | ⏸ deferred (D13) |
| P4 | Confirm the 6 proposed persona labels in B2 | Keep the labels as proposed | ✅ resolved by D15 |
| P5 | "Global good": which outside best practices to benchmark against (plan step 4) | Use provider docs on prompt caching, model routing, and output-length limits, plus the Jegham and Google efficiency figures. Express each as a "what-if" scenario on our data | ✅ resolved by D16 |
| P6 | How to frame recommendations now that every model in the data is retired or being retired (see the model-availability notice below) | Use **tier-based** wording: "reasoning tier," "frontier tier," "small/fast tier," with today's equivalents named in a footnote. Treat o1-preview usage as a synthetic-data artifact | ✅ resolved by D17 (edited: data's model names + purpose label) |
| P7 | Build tool for the final visual (Tableau Public vs. code such as Python/Plotly or HTML/D3) | Tableau Public, if the competition expects it; otherwise code-generated charts exported to PDF/PNG | ✅ resolved by D19 (HTML/Python) |
| P8 | Dashboard story and scope: how many charts, and in what order | 4–5 charts in the order problem → persona breakdown → opportunity → recommendations, all on one page | ✅ resolved by D20 (edited) |
| P9 | How to show personas: all 6 tenants, or 3 groups (Dev & Sandbox, the 4-tenant baseline, and o1-preview as a cross-cutting issue) | Show all 6 tenants in one color system, with Dev and Sandbox highlighted and the other 4 muted as the baseline | ✅ resolved by D21 (all 6) |
| P10 | Recommendations per persona: which levers become recommendations | Dev & Sandbox: trim prompts, validate requests (fewer 400s), enable caching. Production and Marketing: cap answer length, route reasoning calls to a frontier model. Campus/IT: a routing policy plus a per-tenant scorecard | 🟡 kept as a DRAFT in B8 (D22) |
| P11 | Scenario settings (50% cache, 50% of reasoning calls rerouted, p75 output cap): keep, or change | Keep them, labeled as illustrative | ⏳ **User objected (2026-11-14): "the 50% isn't based on anything. That's bad."** Claude proposed data-grounded replacements (see the B6 row). Awaiting a choice |
| P12 | Replacement for the "hidden driver" (o1-preview) chart under the model-drift lens (D18) | Options: (A) purpose → model "living table" with call share vs cost share and retirement status; (B) interactive routing slider (what if X% of reasoning calls used a frontier model?); (C) model-lifecycle timeline with the data window marked. Recommended: A, with B's slider if time allows | 🔁 **User rejected A–C (2026-11-14): "not helpful for thinking about what to do moving forward."** New forward-looking options proposed: D (a "which model for this task?" guide), E (per-request price tags as dated ratios), F (each persona's role when models change). Mockups of D, E and F: https://claude.ai/artifact/NKvAmpnJFGxD43v7WEhs3K (A–C: https://claude.ai/artifact/M824FjjqQst3GEJbbH1Myb). User asked for 2 more versions each of E and F with clearer insights: E2 receipt, E3 relative cost vs energy, F2 habit scorecard, F3 distance to CMU best (https://claude.ai/artifact/Y1JKxp3qQSZAh4XZtaCnpA). All 10 options on one page: https://claude.ai/artifact/ViimKfpnvMrvvaT7N19VBt. Claude recommends E2 + F3. **User asked for easier-to-read visuals:** 3 more versions each, E4 (cost of one request), E5 (share of requests vs share of the bill), E6 (what $10 buys), F4 (bars per habit), F5 (persona cards), F6 (today vs CMU best). All versions of E and F are in a local file: `mockups/p12-E-F-all-versions.html`. Awaiting a choice |
| P14 | More creative visual form (user, 2026-11-14: "the data looks boring and there is too much clustered, too hard to understand"; asked about simple pictures or three.js computers; pointed to pudding.cool) | Claude looked at Pudding examples (onions: sliders and an "explode" toggle that make standard deviation visible; love story: one icon per person, clay illustrations, one idea per scroll step). Options: (A) isometric 2D "server room" illustration per persona; (B) pictograms / unit charts (coins, lightbulbs, error lights); (C) "build a request" toy with sliders; (D) one request's journey as scrollytelling; (E) everyday equivalents. Recommended **A + B as a static poster** (exports to PDF), with 3D (three.js) at most as a hero image, because 3D distorts size comparisons and doesn't export to PDF | ⏳ asked 2026-11-14 |
| P13 | P11 follow-up: scenario inputs based only on what we already know | (1) Local good per metric (already computed: −15% cost, −7% energy). (2) Per-unit sizes: +10 points of cache share at every tenant = −$187/month and about −8 to −9 kWh; each o1-preview call moved to gpt-4o saves about $0.25 and about 4.8 Wh (central). (3) Data ceiling: 75.5% of o1-preview calls give answers no longer than the same tenant's median gpt-4o answer (a ceiling, not a target; answer length ≠ task difficulty). (4) Null finding: o1-preview share is 9.6–10.4% in every OpenAI tenant, so CMU has no internal example of lower reasoning use. Recommended: headline = local good; outside practices = per-unit sizes; drop the global and combined totals | ⏳ asked 2026-11-14 |

---

## B0a. Headline Findings (living summary; details and evidence in B4)
> All numbers come from **synthetic** telemetry (Oct 1–30, 2026; 202,650 calls). Cost uses list prices (some unverified). Energy and carbon are **estimates** from published benchmarks, not measurements.

1. **Dev and Sandbox are the outliers; the other 4 tenants are one "efficient baseline."** Among the 4, 0 of 42 comparisons were meaningful (Bonferroni plus a ≥10% effect). Core Production Services is the tie-break "local good."
2. **Dev and Sandbox gaps vs local good** (best tenant on the same provider):

   | Measure | Engineering / Dev | Sandbox |
   |---|---|---|
   | Cost per call | 1.5× | 2.0× |
   | Energy per call | 1.2× | 1.5× |
   | Prompt size | 1.9× | 3.8× |
   | Premium-model share | 1.3× | 1.4× |
   | Cache share | 2.4–2.7% | 2.4–2.7% |
   | Bad-request (400) rate | 6.0–6.1% | 6.0–6.1% |

   The baseline targets are a cache share of 22.6% and a 400 rate of 1.1%.
3. **Reasoning model (o1-preview) concentration:** it's about 10% of OpenAI calls, but **60–69% of OpenAI cost** and **about 30–35% of OpenAI energy**. About 60% of its output is hidden reasoning tokens.
4. **Total 30-day footprint (estimate):**
   - Cost is **$5,711** (caching already saved $235).
   - Energy is **277 / 387 / 496 kWh** (low / central / high).
   - Carbon is **26 / 135 / 292 kg CO₂e**. Grid cleanliness alone swings carbon about 6×.
5. **Output tokens drive energy, so caching is mainly a cost lever.** Output tokens use about 7–60× more energy per token than input. Caching avoids up to about 9% of cost but at most about 4.5% of energy. For energy, the levers are **model tier and output length**.
6. **Sandbox (student proxy) leans on gemini-1.5-pro:** 65% of its calls but 86% of its energy, with 3.8× larger prompts than the baseline.
7. **Rate limiting (429) is uniform and low** (1.8–2.3%), and there are no retry storms. Time-of-day patterns are flat. **Not a story.**
8. **Every model in the data is retired or being retired as of 2026-11-14** (see below). Per D17, visuals use the data's model names, each with a purpose label (reasoning / frontier / small-fast).
9. **What-if scenarios (D16, `scripts/07_scenarios.py`; 30 days, central energy):**

   | Scenario | Campus Δ cost | Campus Δ energy | Dev | Sandbox |
   |---|---|---|---|---|
   | Local good, all levers (Dev and Sandbox only) | −$865 (−15%) | −27 kWh (−7%) | −31% $ / −13% kWh | −48% $ / −23% kWh |
   | Global good, all levers (every tenant) | −$1,856 (−32%) | −66 kWh (−17%) | −37% / −22% | −27% / −19% |
   | Local + global | **−$2,360 (−41%)** | **−83 kWh (−21%)**, −29 kg CO₂e | −54% / −29% | −56% / −35% |

   - Biggest single **cost** lever: routing half of the o1-preview calls to gpt-4o (−$1,161, −20%).
   - Biggest single **energy** lever: 50% caching (−33 kWh, −8.5%).
   - For Dev and Sandbox, **trimming prompts** is the best local lever (−21% / −26% cost; −11% / −18% energy).
   - Fixing 400s to the local-good rate avoids about **3,355 failed calls** a month (1,814 Dev + 1,541 Sandbox). They cost $0 in this model.

---

## B0b. Proxies, Assumptions & Swappable Inputs (what could be replaced later)
> Anything here is a stand-in. When better data arrives, swap the file or parameter and re-run the listed script. Nothing else needs to change.

| # | What | Current proxy / assumption | Why | How to replace later | Re-run |
|---|---|---|---|---|---|
| X1 | **Prices: o1-preview** | $15 / $7.50 / $60 per 1M (third-party; cached = 50% assumed) | Model is retired and not on the official page; Wayback Machine is blocked for Claude | Edit `config/pricing_list.csv` (or a new `pricing_cmu.csv`) | `03_cost.py` → `06_carbon.py` → `05_local_best.py` |
| X2 | **Prices: gemini-1.5-pro** | $1.25 / $0.3125 / $5.00 (third-party; Google gives only % cuts) | Same | Same | Same |
| X3 | **Price: gemini-1.5-flash cached input** | $0.01875 (third-party). Input and output are official | Same | Same | Same |
| X4 | **All prices vs CMU's real rates** | Public list prices | D9: swappable for CMU AI Gateway rates | Copy to `config/pricing_cmu.csv` and run `py scripts/03_cost.py config/pricing_cmu.csv` | Same |
| X5 | **Energy for o1-preview** | Uses the **o1** benchmark | o1-preview was never benchmarked | `config/carbon_params.csv` → `model_map:o1-preview` | `06_carbon.py` → `05` |
| X6 | **Energy for gemini-1.5-pro** | Uses the **gpt-4o** benchmark (frontier tier) | Jegham et al. has no Gemini rows | `model_map:gemini-1.5-pro`, or add a Gemini row to `config/energy_benchmarks.csv` | Same |
| X7 | **Energy for gemini-1.5-flash** | Uses the **gpt-4o-mini** benchmark (small tier) | Same | `model_map:gemini-1.5-flash` | Same |
| X8 | **gpt-4o-mini energy** | Jegham et al. assume A100 hardware, so mini comes out *more* energy per output token than gpt-4o | Authors' assumption | Replace its row in `config/energy_benchmarks.csv` with a better benchmark | Same |
| X9 | **Low-energy bound** | Scale = 0.24 Wh (Google median, no token length) ÷ 0.423 Wh (Jegham GPT-4o short) = 0.567 | Google gives no per-token rate | `low_energy_scale` in `config/carbon_params.csv` | Same |
| X10 | **Energy of cached tokens** | 0% (low) to 50% (high) of normal input energy | No public measurement | `cached_input_energy_share_low/high` | Same |
| X11 | **Grid carbon intensity** | 94 / 350 / 588 g CO₂e per kWh (CodeCarbon GCP us-west1 / Jegham Azure / CodeCarbon GCP us-west3) | The data center region isn't in the logs | `grid_g_per_kwh_*`. A natural swap is Pittsburgh's PJM grid or the provider's actual region | `06_carbon.py` → `05` |
| X12 | **Failed calls (400/429)** | $0 cost and 0 Wh, because there are no token counts | Providers don't bill failures, but compute and staff time are still wasted | Add a per-failure energy assumption in `06_carbon.py` if needed | `06` |
| X13 | **Student persona** | Sandbox Testers and Researchers (R&D) are student proxies (D7) | No user IDs or department tags; timestamps are flat | Re-map in `TENANTS` in `scripts/01_clean_harmonize.py` | All scripts |
| X14 | **Persona = tenant** | Each org or project ID is treated as one persona (D2, D15) | The only grouping field in the logs | Same as X13 | All scripts |
| X16 | **Global cache target** | 50% token-weighted cache share for every tenant | No published campus benchmark. Illustrative best practice | `global_cache_share_target` in `config/scenario_params.csv` | `07_scenarios.py` |
| X17 | **Share of reasoning calls that are "routine"** | 50% of o1-preview calls (smallest visible output) move to gpt-4o, and their hidden reasoning tokens are dropped | We can't see task content. Small output is used as a stand-in for routine | `global_reasoning_route_share` | `07` |
| X18 | **Output cap** | Visible output capped at the baseline p75 for the same model. Moved calls keep the same tokens on their new model | No quality data, so we assume the shorter answers are still good enough | `global_output_cap_percentile` | `07` |
| X19 | **Model-mix energy (L3)** | Moving gpt-4o calls to gpt-4o-mini saves little energy, because of the A100 assumption (X8) | Inherited from the benchmark | Fix X8 | `06` → `07` |
| X15 | **Not modeled** | Gemini cache-storage fees, batch/flex discounts, >128K-token pricing tier, water use | Not in the logs, or out of scope | Extend `03_cost.py` / `06_carbon.py` | |

**Model availability notice (checked 2026-11-14, OpenAI deprecations page, https://developers.openai.com/api/docs/deprecations):**
- **o1-preview:** shut down **Jul 28, 2025**, replaced by o3. This row came from a summarized part of the page, so it isn't verbatim.
- **o1:** shut down **Oct 23, 2026**, replaced by gpt-5.6-sol. Notice was given Apr 22, 2026, and the model page says "Shut down."
- **gpt-4o** (2024-08-06, 2024-11-20) and **gpt-4o-mini** (2024-07-18): deprecated, with shutdown on **Jan 14, 2027**, replaced by gpt-6-luna. Notice was given Oct 14, 2026.
- **Gemini 1.5 Pro and Flash:** no longer listed on Google's current Gemini API pricing page.

**Implication:** the synthetic logs show o1-preview in use in Oct 2026, more than a year after its real shutdown. That's a **synthetic-data artifact**. It doesn't invalidate the behavioral findings (reasoning-tier concentration, prompt bloat, low caching), but recommendations should name **tiers** and behaviors, with current equivalents in footnotes (P6).


## B1. Purpose & Question (Doc Section 1)
- **Final question:** (working) *What specific AI recommendations should Carnegie Mellon University implement to benefit different personas on campus, addressing gaps in understanding effective AI use for lower cost and resource consumption?*
- **Audience / decision-maker:** Mixed campus audience: deans, students, and IT admins. Each persona should leave knowing which of their own AI habits to change (decided 2026-11-14).
- **Changes & reasons:**

## B2. Personas
**Decision (user, 2026-11-14):** Keep all 6 tenants as separate personas for now, and label which ones could be combined (D2). **Labels confirmed by the user (D15).** Sandbox Testers and Researchers (R&D) are the student proxies (D7, an assumption).

| Persona (proposed label) | How identified in data | Environment | Could combine with | Notes |
|---|---|---|---|---|
| Engineering / Developers | `organization_id = org-engineering-dev` (OpenAI) | dev | Sandbox Testers → "Dev & Sandbox" | Both are high-token, low-cache, high-400 tenants |
| Sandbox Testers | `gcp_project_id = prj-ai-sandbox-testing` (Gemini) | sandbox | Engineering / Developers → "Dev & Sandbox" | |
| Core Production Services | `organization_id = org-prod-core` (OpenAI) | prod | Enterprise Production → "Production Services" | Could stand in for campus admin/staff tools |
| Enterprise Production | `gcp_project_id = prj-ai-enterprise-prod` (Gemini) | prod | Core Production Services → "Production Services" | |
| Marketing / Communications | `organization_id = org-marketing-ai` (OpenAI) | business | No Gemini twin | Statistically almost identical to org-prod-core |
| Researchers (R&D) | `gcp_project_id = prj-ai-r-and-d` (Gemini) | research | No OpenAI twin | Statistically almost identical to prj-ai-enterprise-prod |

Students aren't directly identifiable. No tenant is student-specific, and time of day is flat.

## B3. Data & Methods
| Source | One row = | Key fields | Prep steps | Assumptions / limits |
|---|---|---|---|---|
| `data-uncleaned/openai_pipeline_telemetry_raw.csv` | One OpenAI API call | `id`, `created_at` (UTC), `model` (gpt-4o, gpt-4o-mini, o1-preview), `organization_id` (3 orgs), `status_code` (200/400/429), `error` (JSON), `usage` (JSON: prompt, completion, cached, reasoning tokens) | Profiled 2026-11-14: 108,450 rows, 2026-10-01 → 2026-10-30, 0 duplicate IDs, 0 malformed JSON. `usage` is blank on all 5,239 failed calls (400 + 429) | Synthetic. Failed calls have no token counts, so their cost/carbon can't be measured directly |
| `data-uncleaned/gemini_pipeline_telemetry_raw.csv` | One Gemini API call | `response_id`, `timestamp` (UTC), `model_version` (1.5-pro, 1.5-flash), `gcp_project_id` (3 projects), `http_response_code`, `error_details` (JSON), `usageMetadata` (JSON: prompt, candidates, cachedContent tokens) | Profiled 2026-11-14: 94,200 rows, same 30-day window, 0 duplicate IDs, 0 malformed JSON. `usageMetadata` is blank on all 4,557 failed calls | Synthetic. Same NULL-token limitation |
| Data dictionary (`data-uncleaned/Fall 2026 - CMU Student IronViz_ Data Dictionary & Quality Guide.docx`) | n/a | Field definitions, cross-provider crosswalk, NULL rules, "cached is a subset of input" rule | Used as the harmonization spec | Provided by the competition organizers |
| `data-clean/calls_unified.csv` (built by `scripts/01_clean_harmonize.py`) | One API call, either provider | Harmonized fields from the crosswalk, plus `outcome`, `uncached_input_tokens`, `cache_hit_share`, `date`, `hour_utc`, `weekday`, `persona_label`, `environment`, `merge_candidate` | Defensive JSON parsing, ISO-8601 to UTC datetime, type casting. **0 rows dropped**: failed calls are kept and flagged so failure rates stay correct | Gemini has no reasoning-token field (left NULL) |
| `data-clean/tenant_summary.csv` (built by `scripts/02_tenant_summary.py`) | One tenant | Calls, % 400, % 429, median and p90 input tokens, median output tokens, token-weighted cache share, % of calls with zero cache, total tokens | Successful calls only for the token stats; all calls for the error rates | |
| `config/pricing_list.csv` | One model's price | Input, cached-input and output USD per 1M tokens; verification status; source; date accessed | Swappable (D9) | 3 of 5 models are partly or fully unverified (P3) |
| `data-clean/calls_costed__pricing_list.csv`, `cost_by_tenant__pricing_list.csv` (built by `scripts/03_cost.py`) | One call / one tenant | `cost_usd`, `cost_usd_no_cache`, `cache_savings_usd` | Failed calls cost $0 (not billed) | Depends on the pricing file |
| `config/energy_benchmarks.csv` + `config/carbon_params.csv` | One benchmark model / one parameter | Jegham et al. Table 4 energy (Wh) at 3 prompt sizes; model→benchmark map (PROXY flags); low-energy scale; cached-token energy share; grid factors | Swappable, like pricing | Gemini and o1-preview are proxies. The gpt-4o-mini row assumes A100 hardware (authors' choice) |
| `data-clean/calls_costed_carbon__pricing_list.csv`, `carbon_by_tenant__*.csv`, `carbon_by_tenant_model__*.csv` (built by `scripts/06_carbon.py`) | One call / tenant / tenant × model | `wh_low/central/high`, `gco2e_low/central/high`, no-cache counterfactuals, `energy_is_proxy` | Failed calls = 0 Wh (no token data) | **Estimates, not measurements** |
| `data-clean/persona_metrics.csv`, `local_best_ranking.csv`, `outliers_vs_local_good.csv` (built by `scripts/05_local_best.py`) | One tenant | Normalized behavior, cost and energy metrics; best-of-4 ranking; outlier multiples vs local good | | Ranking is a tie-break (see 04) |
| `data-clean/scenarios_by_tenant__*.csv`, `scenario_errors_avoided__*.csv` (built by `scripts/07_scenarios.py`, D16) | One tenant × scenario (plus an ALL_CAMPUS row) | Cost, kWh (low/central/high), kg CO₂e, and Δ vs actual (absolute and %). Local-good levers L1–L4, global-good levers G1–G3, plus combinations | Re-prices and re-estimates energy on modified copies of the successful calls, using the same formulas and configs as 03 and 06 | Thresholds are assumptions (B0b X16–X19). Calls are moved uniformly, not by task |
| `data-clean/small_differences.csv` (built by `scripts/04_small_differences.py`) | One metric comparison between two tenants | Values, relative difference, 95% CI, p-value, statistical and practical flags | | See the methods below |

**Profiling observations (raw, not findings yet):**
- Calls are spread almost evenly across all 24 UTC hours for every org/project, so the time-of-day split is flat and **time of day can't be used to identify personas**.
- Two groups stand out. *Dev/sandbox* (`org-engineering-dev`, `prj-ai-sandbox-testing`) has about 2–4× larger prompts, a cache-hit share of about 2.5% versus about 19–23% elsewhere, and a 400-error rate about 5× higher (6.1% / 6.0% vs about 1.1–1.2%).
- The other four groups (`org-prod-core`, `org-marketing-ai`, `prj-ai-r-and-d`, `prj-ai-enterprise-prod`) look nearly the same on every metric profiled so far.
- 429 (rate limit) rates are similar across groups (about 1.8–2.3%).

**QA results (`data-clean/qa_report.txt`):** 202,650 rows (108,450 OpenAI + 94,200 Gemini, matching the dictionary). 0 duplicate IDs, 0 unparseable usage, 0 failed calls with usage present, 0 cases of cached > input, 0 rows where total ≠ input + output, 0 negative values. Each provider has exactly one error message per status code.

**Synthetic-data artifacts (threats to interpretation):**
- Every day has **exactly 6,755 calls**, so daily volume is fixed by the generator. Day-to-day and weekday volume trends are meaningless; only rates and mixes vary.
- Hour of day is flat for every tenant.
- 429s are never clustered (at most 2 per tenant per minute), so there's **no evidence of retry storms**. The daily 429 rate only ranges from 1.7% to 3.0%.

**Competition deck vs. the released data (checked 2026-11-14):** The info-session deck (`../../Fall 2026 Student Iron Viz Competition and Data Set Information Session.pptx.pdf`) confirms the data is **synthetic** (slides 3 and 7), has **no user IDs or department tags** (slide 7), and expects personas to be "reverse-engineered from timestamps and token counts" (slide 7). Slide 9 says about 5.5% of rows contain injected anomalies. A targeted check (`anomaly_check.py`, scratch) found **none of them in this release**:

| Deck claim (slide 9) | In our files? |
|---|---|
| 429s during late-night student peaks | **No.** The 429 rate is 1.6–2.3% in every US-Eastern hour, and volume is about 8,430 calls in every hour |
| 500 / 503 server faults | **No.** Only 200, 400 and 429 appear |
| Truncated JSON, string-typed numbers, 200s with NULL payloads | **No.** 0 / 0 / 0. The data dictionary agrees: "All usage values on 200 records are valid JSON in this release" |
| Runaway loops (>16k output tokens, >45s latency) | **No.** Max output is 5,631 tokens, and there is no latency field |
| Prompt spikes (>120k tokens) | **No.** Max input is 52,188 |

The files in `../../Fall 2026 Data/` are byte-identical to `data-uncleaned/` (MD5 match), so this is the only release. **Interpretation:** this release is cleaner than the deck describes. **Per D6, the deck's anomaly claims are ignored** and the analysis covers only what's in the data. Defensive parsing stays in the pipeline as good practice, and no anomalies are invented.

**Timestamps carry no persona signal:** calls arrive about every 12.9 seconds (max gap 24.9 s), hour by hour, with flat token sizes, cache share and model mix across hours. **Token counts within each tenant × model are single-peaked** (log-normal-looking), so there are no hidden subgroups. The persona signal comes from **tenant + model choice + cache behavior + prompt size + 400 rate**.

**Pricing (2026-11-14):** `config/pricing_list.csv` is swappable. To use CMU rates, run `py scripts/03_cost.py config/pricing_cmu.csv` (see `config/README.md`). The `status` column records how far each price is verified:
- **gpt-4o** ($2.50 input / $1.25 cached / $10.00 output per 1M) and **gpt-4o-mini** ($0.15 / $0.075 / $0.60): verified on the official OpenAI pricing page, Standard tier.
- **gemini-1.5-flash**: input $0.075 and output $0.30 are official (Google blog, Aug 8 2024). The cached price ($0.01875) is unverified.
- **gemini-1.5-pro** ($1.25 / $0.3125 / $5.00) and **o1-preview** ($15 / $7.50 / $60) are **UNVERIFIED**. Both models are retired and missing from current official pages. Google's blog gives only percentage cuts, and the Wayback Machine is blocked for Claude's fetch tool. **The user should confirm these manually in a browser from archived late-2024 pricing pages.**

Cost per call = uncached input × input price + cached × cached price + output × output price. Failed calls cost $0 because providers don't bill them. The counterfactual "no cache" cost gives the cache savings. Not modeled: Gemini cache-storage fees, batch discounts, and the >128K tier (max prompt is 52K).

**Energy and carbon method (D14, `scripts/06_carbon.py`):**
1. For each benchmark model, solve E = a + b_in·input + b_out·output exactly from Jegham et al.'s 3 prompt sizes (100/300, 1,000/1,000, 10,000/1,500 tokens). This gives per-token coefficients:

   | Benchmark model | a (Wh per call) | b_in (Wh per 1K input tokens) | b_out (Wh per 1K output tokens) |
   |---|---|---|---|
   | gpt-4o | 0.121 | 0.131 | 0.963 |
   | gpt-4o-mini | 0.020 | 0.031 | 1.846 |
   | o1 | 1.535 | 0.103 | 2.409 |

2. Map telemetry models to benchmarks: o1-preview → o1, gemini-1.5-pro → gpt-4o, gemini-1.5-flash → gpt-4o-mini. **All three are proxies.**
3. **High** = the benchmark energy, with cached tokens at 50% of input energy. **Low** = high × 0.567 (Google's measured 0.24 Wh ÷ Jegham's 0.423 Wh), with cached tokens at 0%. **Central** = the midpoint.
4. Carbon = energy × grid factor. Low uses 94 g/kWh (CodeCarbon, GCP us-west1). Central uses 350 g/kWh (Jegham, Azure). High uses 588 g/kWh (CodeCarbon, GCP us-west3).
5. Caching "avoided energy" = energy if the cached tokens had been processed as normal input, minus the actual estimate.

**Why:** the HF dataset isn't LLM inference (D14), and these are the most specific public, per-model, per-token-size LLM figures. A range is honest about the uncertainty.
**Caveats:** Gemini has no benchmark (proxy). Google's 0.24 Wh comes with no prompt length, so it's used as a scale factor, not a token rate. The gpt-4o-mini benchmark assumes A100 hardware, so it comes out *more* energy per output token than gpt-4o. Treat model-level energy comparisons involving mini with care.

**Local-good method (D11, `scripts/05_local_best.py`):**
- Rank the 4 baseline tenants on 8 normalized metrics.
- Error and cache metrics are ranked across all 4.
- Prompt size, premium-model share, cost per call and Wh per call are ranked within each provider (rescaled to a 1–4 scale).
- "Local good" = the **best observed value per metric** among the 4: a realistic, already-achieved CMU target.

**Methods chosen & why (so far):**
- Normalize everything per call or per 1K tokens, because tenants have different call counts (31K–36K).
- Use **medians and p90** for tokens, because the distributions are right-skewed (p90 is about 2–4× the median).
- Use a **token-weighted cache share**, plus the share of calls with zero cache, to separate "caches a little" from "never caches."
- Compare within a provider wherever possible (OpenAI tenants with each other, Gemini tenants with each other), because the model families differ.
- **Small-difference testing:** two-proportion z-tests for rates, and bootstrap 95% CIs (2,000 resamples, seed 42) for medians and p90s. Use a **Bonferroni** correction across the 42 metrics, plus a practical threshold of ≥10% relative difference. Large samples make almost any gap "significant," so effect size decides.
- **Student proxy (assumption, user decision):** sandbox-testing and R&D are treated as the closest proxies for student workloads (coursework experiments and research). This is not observable in the data and must be labeled as an assumption in the final viz.

## B4. Findings & Interpretation
_Preliminary findings. Cost uses `config/pricing_list.csv` (some prices unverified, P3). Energy and carbon are **estimated** ranges (D14). The data is synthetic._

| Finding | Persona | Goal (cost / sustainability) | Evidence | Threats / edge cases |
|---|---|---|---|---|
| Dev/sandbox almost never uses prompt caching | Engineering/Dev, Sandbox | Both | Token-weighted cache share is 2.7% / 2.4%, vs 19–23% for the other 4 tenants. About 95% of their calls have zero cached tokens, vs 56–63% elsewhere | Synthetic data. Dev prompts may legitimately vary more and be harder to cache |
| Dev/sandbox sends much larger prompts | Engineering/Dev, Sandbox | Both | Median input is 8,038 (eng-dev) vs about 4,300 for the other OpenAI tenants, and 13,986 (sandbox) vs about 3,690 for the other Gemini tenants. The gap holds **within each model** (e.g., gemini-1.5-pro is 18,764 vs about 12,000) | Is it bigger tasks or unpruned context? We can't tell from the data |
| Dev/sandbox has about 5× more malformed requests (400) | Engineering/Dev, Sandbox | Both (wasted calls and engineering time) | 400 rate is 6.1% / 6.0% vs 1.1–1.2% | Failed calls have no token counts, so their wasted compute can't be measured directly |
| Sandbox leans on the bigger model | Sandbox | Both | 65% gemini-1.5-pro vs about 47% in the other Gemini tenants. Eng-dev is 59% gpt-4o vs about 43% | Model choice could depend on the task |
| o1-preview reasoning tokens are hidden output | All OpenAI tenants | Both | Median 60% of o1 output tokens are reasoning tokens, and o1 is about 10% of calls in every OpenAI tenant | Billed as output tokens |
| Rate limiting (429) is uniform and low | All | Cost (minor) | 1.8–2.3% for every tenant, with no clustering or retry storms | Probably not a headline story |
| 4 non-dev tenants are nearly indistinguishable, **now tested formally** | Prod, Marketing, R&D, Enterprise | n/a | `scripts/04_small_differences.py` ran 42 comparisons within each provider (error rates, model mix, and per model: median and p90 input, output, cache-hit %, cache depth, cost, o1 reasoning share). Results are in `data-clean/small_differences.csv`. **0 of 42 are both statistically clear (Bonferroni α = 0.0012) and ≥10% relative difference.** The only Bonferroni-significant gap is o1-preview share (prod-core 9.6% vs marketing 10.4%, p = 0.0011, −7% relative), which is too small to matter. The 429 gap (2.14% vs 1.84%, p = 0.004) doesn't survive the correction | With about 30K calls per tenant, tiny gaps reach significance, so practical relevance is judged on effect size. **Conclusion: these 4 behave as one "efficient baseline" profile in this synthetic release** |
| **o1-preview drives most OpenAI cost** | All OpenAI tenants | Cost | o1-preview is about 10% of calls but **60% (eng-dev), 69% (marketing) and 67% (prod-core) of each tenant's cost**. Mean is $0.25–0.34 per call vs $0.027–0.037 for gpt-4o and $0.001 for gpt-4o-mini | ⚠️ o1-preview price is **UNVERIFIED** (third-party $15/$60 per 1M). It's also a reasoning model, so about 60% of its output is hidden reasoning tokens |
| Dev/sandbox costs more per call | Engineering/Dev, Sandbox | Cost | Mean cost per successful call: eng-dev $0.055 vs about $0.037 for the other OpenAI tenants (+50%); sandbox $0.021 vs $0.011 for the other Gemini tenants (+100%) | All Gemini prices are partly or fully unverified |
| Caching already saves about 5–9% where it's used, and almost nothing in dev/sandbox | All | Cost (and energy, TBD) | Cache savings as % of no-cache cost: eng-dev 0.9%, sandbox 1.3%, vs 5.4% (OpenAI baseline) and 8.5–8.8% (Gemini baseline). Total savings are $234.72 of $5,711.25 over 30 days | Excludes Gemini cache-storage fees. Synthetic volumes |
| **Total 30-day footprint (estimate)** | All | Sustainability | Energy is 277 / 387 / 496 kWh (low / central / high). Carbon is 26 / 135 / 292 kg CO₂e | The grid choice swings carbon about 6×. Proxies cover all Gemini usage and o1-preview |
| **Output tokens drive energy; caching saves money more than energy** | All | Both | Output energy is about 7–60× input energy per token (b_out vs b_in). Caching avoids only 0.6–0.9% of energy for dev/sandbox and 2.6–4.5% for the baseline, vs 0.9–8.8% of cost | Benchmark-derived. The real energy cost of cached tokens is unknown, so a 0–50% range is used |
| **o1-preview is about 10% of calls but about 30–35% of OpenAI energy** | All OpenAI tenants | Sustainability | Central estimate 6.4–6.9 Wh per o1 call vs 1.6–2.0 for gpt-4o and 1.2–1.3 for gpt-4o-mini | o1 used as a proxy for o1-preview |
| **Sandbox's lean toward gemini-1.5-pro = 86% of its energy** | Sandbox Testers (student proxy) | Both | Pro is 65% of calls but 86% of energy. It averages 3.4 Wh per call in sandbox vs 2.5 in the baseline, because of bigger prompts | Gemini energy is a proxy (gpt-4o coefficients) |
| **Outliers vs local good** | Engineering/Dev, Sandbox | Both | Eng-dev vs best OpenAI baseline: 1.52× cost per call, 1.21× energy per call, 1.89× prompt size, 1.31× premium-model share. Sandbox vs best Gemini baseline: 2.01× cost, 1.50× energy, 3.79× prompt size, 1.37× premium share. 400 rate is 6.0–6.1% vs a 1.11% local good. Cache share is 2.4–2.7% vs 22.6% | Local good comes from the same synthetic generator |
| **Local good = Core Production Services (tie-break)** | Prod (best of 4) | Both | Mean rank 1.62 vs 2.75–2.88. It wins cache share (22.6%), prompt size, cost and energy within OpenAI. Local-good targets: 400 ≤ 1.11%, 429 ≤ 1.84%, cache share ≥ 22.6%, any-cache calls ≥ 44.5% | **Not a meaningful lead** (script 04). OpenAI tenants rank higher on cache partly because of provider caching mechanics |

## B5. Visualization Decisions (Doc Section 4)
| Chart # | Insight (one sentence) | Options considered | Chosen & why | Accessibility notes |
|---|---|---|---|---|
| KPIs | 30 days: 202,650 requests, $5,711, 386 kWh (277–496), carbon only as a 26–292 kg range | KPI tiles; BANs | KPI tiles. Energy leads; carbon is shown only as a range because the grid assumption swings it about 6× (D26) | Text, no color encoding |
| 1 | Dev and Sandbox are worse on prompt size, cache reuse and 400 rate; the other 4 are within one narrow band | Filterable bar (D20), small multiples, persona cards (F5) | Persona cards (F5), because a filter is lost in a PDF/PNG export. Each habit shows a bar plus the efficient-majority band, with ✓/✕ | Orange = Dev/Sandbox, gray = the others (D21); ✓/✕ symbols so meaning isn't carried by color alone; tooltips |
| 2 | Reasoning = 10% of OpenAI requests, 65% of cost, 32% of energy | E–E6 options (P12) | E5 with energy added as a third bar. Footnote: price unverified, model names expire | Gray / blue / green with text labels on every bar |
| 3 | Local good only: Dev −31% cost / −13% energy, Sandbox −48% / −23%; campus −$865 (−15%), −27 kWh (−7%, range 21–34); 3,355 fewer 400s | Dumbbell, waterfall, lever bars | Lever bars per persona plus a tile. **Global/combined totals excluded (D26)** | Cost and energy each have their own labeled bar |
| 4 | Recommendations by persona with shelf-life tags | Persona cards, priority matrix, highlight table | Table with Habit / Expiring-detail tags, plus a living purpose → model table (D18) | Tags are text, not color only |

## B6. AI Collaboration / HITL (Doc Sections 2 & 3)
| Date | Task | AI contribution | Human decision (accept / edit / reject + why) | Key prompt / pivot |
|---|---|---|---|---|
| 2026-11-14 | Data profiling (plan steps 1–2 kickoff) | Claude profiled both raw CSVs with a stdlib Python script (row counts, date range, models, orgs, status codes, NULL usage, token medians, cache share, hour-of-day) | Asked about persona mapping, audience, and tooling (see the next 3 rows) | "get started on instructionsprocess… ask me for major decisions and before making any visuals" |
| 2026-11-14 | Persona mapping | Claude offered 3 options and recommended merging to 4 personas | **Edited.** Keep all 6 tenants separate, but label what each could be combined with. User pointed to the data dictionary for how to merge across providers | Pivot: a 6-tenant base with a `merge_candidate` column |
| 2026-11-14 | Audience | Claude offered CIO, provost/deans, or a mixed audience | **Chose mixed campus audience** (a dean, a student, and an IT admin must all understand it, and each persona changes their own habits) | Plain language is required throughout |
| 2026-11-14 | Tooling | Claude asked to install pandas | **Accepted.** pandas installed with `pip install --user` | |
| 2026-11-14 | Cleaning, harmonizing, QA, and first tenant summary | Claude wrote `scripts/01_clean_harmonize.py` (following the dictionary crosswalk) and `scripts/02_tenant_summary.py`, ran the QA checks, and found the synthetic artifacts (fixed 6,755 calls/day, flat hours, no retry storms) | Pending user review of the proposed persona labels and next steps | Finding: the dev/sandbox vs. everyone-else split is the strongest signal in the data |
| 2026-11-14 | Synthetic-data questions | User pointed Claude to the competition info-session deck. Claude read it and checked each anomaly it describes against the data. Result: none are present, timestamps are uniform, and the files match the "Fall 2026 Data" copy | User redirected Claude to the authoritative source instead of guessing | Pivot: the deck's "staff vs. student by time of day" framing can't be supported by this release |
| 2026-11-14 | Deck/data mismatch | Claude recommended reporting the mismatch openly | **Rejected. Ignore the deck's anomaly claims** and analyze only what's in the data | |
| 2026-11-14 | Student persona | Claude offered 3 options | **Accepted the recommendation:** map students by workload. Sandbox-testing and R&D are the student proxies, and this is labeled as an assumption | |
| 2026-11-14 | Story focus for the 4 look-alike tenants | Claude recommended "dev/sandbox vs. baseline" | **Rejected for now. Dig for small differences first** (with significance checks), then decide | |
| 2026-11-14 | Pricing | Claude recommended published list prices | **Edited.** Use list prices for now, but make them **swappable** for CMU's AI Gateway rates later (a config file, not hard-coded) | |
| 2026-11-14 | Price lookup | Claude searched the web, then used fetch subagents on the official OpenAI and Google pages. 2 of 5 models were fully verified. The Wayback Machine was blocked. Claude flagged the unverified prices instead of presenting them as fact | Pending: user to verify o1-preview and gemini-1.5-pro prices | Guardrail: "don't fabricate numbers" |
| 2026-11-14 | Cost and small-difference analysis | Claude wrote `scripts/03_cost.py` (swappable pricing) and `scripts/04_small_differences.py` (bootstrap, z-tests, Bonferroni). Found that o1-preview drives 60–69% of OpenAI cost, and that the 4 look-alike tenants show no meaningful differences | Pending: user to re-decide the story focus with this evidence | Pivot candidate: an "o1-preview cost concentration" story |
| 2026-11-14 | Decision documentation | Claude added the B0 Decision Register (D1–D10, pending P1–P4), fixed a broken B3 table, and updated stale notes to match D6 | **User asked** that every human decision be documented in this file | "document decisions i make in process-log.md" |
| 2026-11-14 | Story focus, carbon, labels | Claude logged D11–D13 and D15. While starting the carbon work, it inspected the HF dataset and found it was 10 laptop-CPU Python runs. It flagged this instead of using it, and proposed published LLM benchmarks | **D14: accepted the published LLM range** | Pivot: the HF dataset was demoted to context only |
| 2026-11-14 | Benchmark retrieval and carbon model | Fetch subagent read Jegham et al. v5 (Table 4, Table 1) and Google's arXiv:2508.15734. Claude wrote `scripts/06_carbon.py` (exact 3-point per-token fit, low/central/high, configurable) | Pending user review | Finding: output tokens drive energy, so caching is mainly a cost lever |
| 2026-11-14 | Local-good benchmark | Claude wrote `scripts/05_local_best.py` (best-of-4 ranking and outlier multiples) | Pending user review | Core Production Services is the tie-break winner |
| 2026-11-14 | Proxy register, headline findings, model availability | User asked for the proxies and the major findings to be clearly written down, and asked whether o1 is still accessible. Claude added B0a (headline findings) and B0b (proxies and swappable inputs, X1–X15). A fetch subagent checked OpenAI's deprecations page: o1 shut down Oct 23 2026, o1-preview Jul 28 2025, gpt-4o and mini shut down Jan 14 2027 | User-directed | Pivot candidate (P6): tier-based recommendations, because every model in the data is retired or being retired |
| 2026-11-14 | Global good and model naming (P5, P6) | Claude offered 3 options for each and recommended what-if scenarios and tier-only wording | **P5 accepted (D16): what-if scenarios. P6 edited (D17):** keep the data's model names, but add a label for what each model is for | Pivot: model names stay; a purpose label replaces the tier-only wording |
| 2026-11-14 | Scenario model | Claude wrote `config/scenario_params.csv` and `scripts/07_scenarios.py`. Local-good levers use targets computed from the best baseline tenant. Global-good thresholds are flagged assumptions (X16–X19). The actual row reproduces $5,711 / 386.5 kWh | Pending user review of the scenario thresholds | Finding: local + global could cut campus cost about 41% and energy about 21%. Routing reasoning calls is the biggest cost lever, and caching is the biggest energy lever |
| 2026-11-14 | Model-drift lens | User explained that the models are outdated on purpose (a lesson in outdated data and model drift) and asked Claude to explore how recommendations can accommodate change. Claude proposed 7 angles and drafted a note | **Edited:** kept angles 1, 2, 5 and 6 (habits vs details, purpose table, persona roles, dated ranges). Approved the note as drafted (D18) | "how can we accommodate change in our recommendations?" Pivot: every recommendation gets a shelf-life tag |
| 2026-11-14 | Next-step decisions (P7–P11) | Claude listed 5 open decisions, each with a recommendation | **P7 → HTML/Python (D19). P8 edited (D20):** the persona breakdown is filterable, and Claude is asked for model-drift alternatives to the hidden-driver chart (P12). **P9 → all 6 (D21). P10 → kept as a draft in B8 (D22). P11 →** the user asked for a plain-language explanation before deciding | Pivot: the o1-preview chart is reframed through the model-drift lens |
| 2026-11-14 | P12 mockups and the 50% target (P11) | Claude built a mockup page of options A, B and C using real pipeline numbers (https://claude.ai/artifact/M824FjjqQst3GEJbbH1Myb). The user asked "how do you know" about the 50% cache target, and Claude admitted it was an invented target. Claude proposed: (1) use CMU's own best tenant (22.6%) as the cache target; (2) report savings per 10 percentage points of cache share instead of picking one target; (3) treat the 50% reasoning reroute the same way, as a range or slider | **User: "the 50% isn't based on anything. That's bad."** Choice pending | Guardrail: no invented targets. Every scenario number must trace back to the data or a citation |
| 2026-11-14 | Viz arrangement explorer (D24) | Claude wrote `scripts/08_explorer_data.py` (aggregates the costed + carbon call table into a 15-row tenant × model cube plus token quantiles) and `explorer/index.html` (plain JS/SVG, no libraries). It offers 10 chart types (sorted bar, dot, lollipop, grouped, stacked, 100% stacked, heatmap, small multiples, share-of-requests vs share-of-measure dumbbell, token box plot) × 17 measures × 6 group/split dimensions, plus persona filters, highlight Dev & Sandbox, low–high estimate ranges, log scale, data table, light/dark, an editable insight title, "copy setup" for logging, and SVG download. Colors use a validated colorblind-aware categorical palette with a fixed color per entity | **User asked for it.** User has not yet picked any arrangements | "create a simple html program with javascript that lets me explore the different arrangements of data" |

## B7. Glossary & Citations
- **Terms:**
- **Sources:**
  - Carnegie Mellon University (2026). *Student IronViz Challenge, Fall 2026 Information Session* [slides]. Sponsored by the Vice Provost for Teaching & Learning Innovation and CMU Core Competencies. Used for the data provenance (synthetic), the theme, and the deliverables (visual export as PDF/PNG, source code, AI-use documentation).
  - Carnegie Mellon University (2026). *Fall 2026 CMU Student IronViz: Data Dictionary & Quality Guide* [docx]. Used for field definitions and the cross-provider crosswalk.
  - Jegham, N., et al. (2025). *How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference.* arXiv:2505.09598v5 (11 Nov 2025). https://arxiv.org/abs/2505.09598. Used for per-model energy at 3 prompt sizes (Table 4) and the Azure carbon intensity of 0.35 kg/kWh (Table 1).
  - Elsworth, C., et al. (2025). *Measuring the environmental impact of delivering AI at Google Scale.* arXiv:2508.15734 (21 Aug 2025). https://arxiv.org/abs/2508.15734. Used for the measured median Gemini Apps text prompt (0.24 Wh, 0.03 g CO₂e, 0.26 mL water), which sets the low-energy scale. Google notes it is not third-party verified.
  - CodeCarbon (mlco2). *cloud/impact.csv* grid carbon intensity by cloud region. https://github.com/mlco2/codecarbon/blob/master/codecarbon/data/cloud/impact.csv (accessed 2026-11-14). Used for the low (94, us-west1) and high (588, us-west3) grid factors.
  - Rehman, M. (2026). *ai-carbon-footprint-experiment-logs* [Hugging Face dataset]. https://huggingface.co/datasets/MotebaRehman/ai-carbon-footprint-experiment-logs. **Context only.** It has 10 CodeCarbon runs of simple Python programs on a laptop CPU, with no LLM inference, so it was not used for estimates (D14).
  - OpenAI API pricing: https://developers.openai.com/api/docs/pricing (accessed 2026-11-14). Google Developers Blog, Gemini 1.5 Flash price update (Aug 8 2024) and 1.5 Pro price reduction (Sept 24 2024). Third-party price aggregators are listed in `config/pricing_list.csv`.

## B8. Recommendations by Persona
> **DRAFT (D22, 2026-11-14).** Kept here for later review, not final. Impacts come from `scripts/07_scenarios.py` (B0a #9). Shelf life follows D18: a *habit* lasts across model changes, and a *detail* expires with a model or price.

| Persona | Recommendation (draft) | Expected cost impact | Expected sustainability impact | Shelf life | Supporting chart |
|---|---|---|---|---|---|
| Engineering / Developers, Sandbox Testers (student proxies) | Trim prompts to only the context needed | Dev −21%, Sandbox −26% | Dev −11%, Sandbox −18% energy | Habit | TBD |
| Engineering / Developers, Sandbox Testers | Validate requests before sending to cut malformed (400) calls from about 6% to about 1% | About 3,355 failed calls avoided per month ($0 billed in this model) | Wasted compute and staff time (not measured) | Habit | TBD |
| Engineering / Developers, Sandbox Testers | Put stable instructions first so prompt caching applies | Included in the local-good totals | Included in the local-good totals | Habit | TBD |
| Core Production, Enterprise Production, Marketing, Researchers | Cap answer length | Campus −2% | Campus −3% energy | Habit | TBD |
| All OpenAI tenants | Use the reasoning model only for multi-step problems; send routine work to a frontier model | Campus −20% | Campus −6% energy | Habit (the model names are details) | TBD |
| Campus IT / leadership | Keep a living purpose → current-model table, plus a monthly per-tenant scorecard (cache share, 400 rate, prompt size) | Enables all of the above | Enables all of the above | Habit | TBD |

## B9. Final Review Checklist
- [ ] Every chart answers part of the main question
- [ ] Each rubric criterion self-scored (1–4) with notes
- [ ] Limitations stated; synthetic/estimated data flagged
- [ ] Citations complete
- [ ] Visual, analytical, and written pieces tell one story
