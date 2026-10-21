# policy2upskill

A Danish labour-market explorer for policy makers. It shows, at national, region and municipality level, how employment moves and which occupation skills are rising or falling. A demo prototype, not a forecasting product.

**Open it:** open `prototype/index.html` in a browser. One static file, no build step, no network calls. The demo click path is in `DEMO.md`.

**Data sources:** Statistics Denmark (Danmarks Statistik) StatBank tables LBESK354 (employees by municipality of residence, 2023-2025), BEFOLK3 (population) and UDDAKT10 (completed education). Licence CC BY 4.0, credit Statistics Denmark. Extracts and notes: `data/real/`. Proposed data contract: `data/contract.md`.

**What is synthetic:** occupation-level skill rows, demand indices, shortage flags, time to fill, briefings and alerts. Scenario rows are what-if assumptions and are always marked. Employee totals, change in employees, population and completions are real. Each panel carries a badge: green "Real · Statistics Denmark" or amber "Synthetic".

Lines after 2025 are a trend extension from the 2023-2025 average annual change, with an illustrative range. They are not a forecast.

Other files: `briefing/` (briefing generator, dry run needs no key), `ROLLOUT.md` (30-day plan and log), `IDEAS.md`.

Status: demo prototype. Predictive claims wait for the backtest (see `ROLLOUT.md`).
