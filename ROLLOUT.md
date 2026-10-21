# policy2upskill: 30-day rollout plan

> **Denmark pivot (note added 21 Oct, 18:45):** the project is for Denmark. The Danish sources named below (Jobnet, Danmarks Statistik, shortage list) must be re-researched for Denmark. Candidates to check: Danmarks Statistik (StatBank), Jobindex and Jobnet for job ads, and the government shortage list (Positivlisten). The prototype data is synthetic.


Status: draft v1, 2026-10-21. Day 0 = demo (tonight, synthetic data). Day 1 = 2026-10-22. Day 30 = 2026-11-20.
Update this file as work lands. Each update gets a dated entry in the log at the bottom.

## Principles

- Nothing is presented as a prediction until the backtest says so.
- Every number on screen carries its source and confidence, or says it is synthetic.
- Roles, not names, own lanes: Data, Explorer, Briefing, Method, Pitch.

## Day 0: demo tonight (status 18:25: fixes applied and checked in browser)

- Fix before the demo (from IDEAS.md): relabel planned sources; say "synthetic" not "observed"; cap the offshore-wind scenario at 0.30; derive heat-pump tags by rule, not by hand.
- Fix the explorer: narrow-width layout, keyboard expand, contrast on the transforming colour.
- Briefings are shown as saved samples, labelled as such.
- Presenter lines: see "Say this, not that" in IDEAS.md.

## Week 1 (days 1-7): foundations

| Day | Work | Owner | Gate |
|---|---|---|---|
| 1-2 | Agree the data contract (`data/contract.md`, `data/sample.json`; drafted 21 Oct) | Data + Method | Contract signed off by the team |
| 2-3 | Pull real Danish employment data for the demo municipalities (done for 12 municipalities, employees only; no occupation breakdown yet) | Data | Real employment layer loads in the explorer |
| 3-4 | Write the tagging rules as code, with thresholds marked proposed | Method | Rules reproduce the demo tags |
| 4-5 | DONE 21 Oct: keyboard expand, narrow layout, contrast. Still open: decide English or Danish UI | Explorer | Decision on language recorded |
| 5-7 | Send a request for a job-ad feed token (not the deprecated public token) | Data | Request sent |

Gate 1 (day 7): contract agreed, real employment layer in the explorer, tagging rules in code.

## Week 2 (days 8-14): core model v0

| Day | Work | Owner | Gate |
|---|---|---|---|
| 8-10 | Core model v0 from Danmarks Statistik employment: municipality x occupation x place, with rule-based tags and confidence | Data + Method | Every row has a source and a rule |
| 10-12 | Briefing generator on real rows: validator on, Sonnet 5.5 default, saved JSON output | Briefing | Validator passes on the 4 municipalities |
| 12-14 | Find 2-3 pilot users: one municipality official, one regional or ministry adviser | Pitch | Three conversations booked |

Gate 2 (day 14): core model v0 runs end to end; pilot users agreed.

## Week 3 (days 15-21): evidence

| Day | Work | Owner | Gate |
|---|---|---|---|
| 15-18 | Backtest: freeze 2019, score 2019-2022 direction against "no change" and "last trend" baselines | Method | Result table with counts and intervals |
| 18-19 | Add public labour-market statistics as national context | Data | Labelled "national context" on screen |
| 19-21 | Write the one-page methods note, with backtest results and what they do not show | Method + Pitch | Note reviewed by one person outside the team |

Gate 3 (day 21): backtest result known. If the hit rate is no better than baselines, the pitch changes to "a tool to test signals", and we say so.

## Week 4 (days 22-30): pilot

| Day | Work | Owner | Gate |
|---|---|---|---|
| 22-25 | Pilot sessions: pilot users walk the explorer and briefing; record what they ask | Pitch | Notes from 2-3 sessions |
| 25-27 | Fix the top three issues from the sessions | Explorer + Briefing | Changes shipped to main |
| 27-29 | Quarterly white-paper template, generated from the core model | Method | Template reviewed |
| 30 | Go / no-go decision for the next 60 days | Team | Decision recorded in this file |

## Metrics

- Pilot users who return for a second session.
- Share of briefing sentences that pass the validator without edits.
- Backtest hit rate versus the two baselines, with counts.
- Time to produce one municipality briefing, from input to saved JSON.

## Risks

- **Danmarks Statistik rounds small cells** to 0 or 3 for privacy. Small occupation counts are approximate.
- **Occupation detail is 1-digit only** in Danmarks Statistik employment table. Skills stay synthetic or demo-only until a finer source is found.
- **Jobnet job-ad data needs a token.** If the request is refused, the job-ad signal stays out of the rollout.
- **Municipality codes change over time.** Check the Danish municipality codes by year before any time series.
- **Tags may look arbitrary** if thresholds are not validated. Show them as proposed.

## Log

- 2026-10-21: draft v1 written from the research outputs (data sources, method rigour, explorer UX, briefing, demo and pitch).
- 2026-10-21 (evening): data contract v0.1 drafted and committed to `data/`. Contract published on the prototype page and on the Miro board.
- 2026-10-21 (late): data-source research (first pass) superseded by the Denmark pivot. Danish sources are being fetched.
- 2026-10-21 (18:25): prototype demo fixes applied and checked in the browser (`1823365`). Pushed to origin/main (this entry first said "Nothing pushed"; that was wrong).
- 2026-10-21 (evening): pushed to origin/main: Danish pivot and Norway removal (`aab6433`, `75c2b86`), real LBESK354 employees (`fc2a5f8`), BEFOLK3 and UDDAKT10 extracts (`d4f8312`), Danish fact-check fixes and `briefing/` (`f1ef447`), LS02 and Positivlisten extracts (`30ef39b`), national/region/municipality views with the Lolland and Frederiksberg demo pair (`271aee4`, `5916d42`, `ee18596`).
- 2026-10-21 (night): demo build pushed to origin/main. Real figures (`data/real/demo_municipalities.json`, 12 municipalities, embedded as `REAL_DATA`) now drive the totals, compare, region and national tables. Copenhagen corrected to the municipality figures (it was the wider Province Byen København). Synthetic employment totals removed. Past/future line chart at all three levels (trend extension, not a forecast). Per-panel Real/Synthetic badges. `DEMO.md`, `.gitignore`, `briefing/` rename fix. Still open: UI language, Danish briefing word list, real occupation series, Femern "after opening" framing.
