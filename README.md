# RAVEN-Match — Research Sandbox
**Team Jarvis** · GokulJayandan R S · Keerthana Janakiraman · Mridula B · Boomika L

An **independent experimental sandbox** for the central RAVEN-Match research hypotheses: budgeted member-level clarification, complementary endpoint questions, persistent information value, reciprocal hard-constraint enforcement, and repeated matching across a finite decision horizon.

> **Scope:** This project is **NOT** the official Vouchsafe/IITM simulator; its generated profiles, acceptance probabilities, occupancy, and scoring are deliberately simplified. Reported `proxy-MSMI` is a synthetic proxy, **not** an official score. Do not use this project's measurements as evidence of leaderboard improvement.

## What's implemented

- Synthetic generator with age, geography, gender, relationship-goal/style proxies, arrival/departure dates, and missing/declined mandatory data.
- Reciprocal hard-feasibility checks separated from predicted pair utility.
- Daily 12-unit clarification cap, modelled as at most four hard-bundle requests.
- Six policies: no questions, FIFO, top pair endpoints, singleton value heuristic, complementary portfolio planning, and a simple persistent-value variant.
- Exact small-graph maximum-weight matching and scalable greedy allocation fallback.
- Approximate 60-day synthetic decision cycles with member occupancy and probabilistic positive-outcome proxies.
- Seed-paired evaluation and three scenario families (standard, sparse, cold-start).
- Automated tests and a Colab-readable notebook entry point.

## Quick start

```bash
python -m unittest discover -s tests -v
python run_experiments.py --seeds 12 --members 24
python make_figures.py --input results/episodes.csv
```

Only Python's standard library is needed for the simulator, evaluations, and tests. Plots require matplotlib. Tested with Python 3.11.

## What is intentionally **not** implemented

The official simulator's full hard-constraint schema, soft-question interface, actual event scheduling, multi-stage MSMI feedback, official JSON policy protocol, a real 200-member blossom implementation, and six official scenario variants. These remain implementation-stage tasks. The current policy is **not a submission-ready Round 2 agent**.

## Files

- `raven/core.py` — synthetic environment, graph matching, competing clarification policies, episode runner.
- `run_experiments.py` — paired synthetic comparisons with CSV export.
- `make_figures.py` — two plots from measured CSV results.
- `tests/` — unit tests for invariants and reproducibility.
- `results/` — generated data and charts from the bundled test run.
- `RAVEN_Research_Colab.ipynb` — notebook front door for Colab.
- `METHODS.md` — assumptions, experimental design, limitations, and extension plan.

## External source and assistance

Challenge specification: [The Sequential Matching Problem](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem).

This project was developed with AI-assisted coding and drafting support (OpenAI ChatGPT). Team Jarvis should review, execute, and verify it before presenting it as their own supporting material. Generated synthetic experiments are explicitly independent from the organisers' benchmark.
