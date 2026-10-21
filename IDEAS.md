# policy2upskill: ideas for the next 1-2 weeks

Brainstorm from Fable. Builds on the agreed architecture (signals -> core model -> views) and the three lanes. Effort is S/M/L. Nothing here changes the demo target.

## Data sources and signals

- **NAV job-ad signal (real data).** Adapter that pulls public job ads from arbeidsplassen.no / NAV open data, maps titles to STYRK-08 occupation codes and extracts skill mentions. Why: the most direct "demand" signal, and it is Norwegian, per kommune. Effort: M. Risk: licence and rate limits; title-to-occupation mapping is noisy.
- **NAV Bedriftsundersøkelsen (reported shortages).** Adapter for the annual enterprise survey that estimates unfilled positions by occupation and county. Why: the official shortage figure ministers already quote. Effort: S. Risk: county, not kommune, granularity; annual cadence.
- **SSB employment-by-occupation and population projections.** Adapter via SSB's PxWeb API (registered employment by kommune and sector; population by age). Why: gives the supply side and lets us say "retirement wave in occupation X in kommune Y". Effort: M. Risk: occupation detail is thinner at kommune level than at county level.
- **ESCO skills taxonomy as the skill dimension.** Use ESCO (EU, open) as the canonical skill list so ads, education data and foreign studies line up. Why: makes every signal comparable and makes the white paper citable. Effort: S. Risk: Norwegian-language matching is imperfect.
- **Scenario signal library.** Three or four hand-built what-ifs (highway rerouted, battery plant opens, hospital merger, fishing quota cut) encoded as the same signal interface. Why: this is what a minister will ask for first. Effort: S. Risk: easy to mistake for a forecast; must be labelled as assumptions.

## Core model and tagging method

- **Written tagging rules.** One page defining rising / falling / durable / transforming in measurable terms (for example demand growth, skill-mix churn), with worked examples. Why: policy makers will ask what "transforming" means, and the answer must be stable. Effort: S. Risk: thresholds chosen on synthetic data will not transfer.
- **Confidence derived from signal agreement.** Confidence = how many independent signals point the same way, weighted by coverage and lag, not a hand-typed number. Why: honest and explainable. Effort: M. Risk: with one real signal the score is trivially low; it must still display well.
- **Provenance on every cell.** Each kommune x occupation x skill row keeps the list of signals that touched it. Why: ministers get challenged in parliament, and "where does that come from" needs a one-click answer. Effort: S. Risk: none serious; the data contract gains a field.

## Evaluation and rigour

- **Backtest harness on real history.** Freeze the model at a past date (e.g. 2019 Q1) using only NAV/SSB data available then, tag every occupation, then score against what happened by 2023. Report precision per tag. Why: the only honest answer to "can it predict". Effort: L. Risk: the historical ad archive may be incomplete; results may be humbling.
- **Naive baselines.** Always show "last year's trend continues" and "no change" alongside the model. Why: without baselines a 60% hit rate sounds good and means nothing. Effort: S.
- **"What this prototype shows" statement.** A short, prominent section in the README, the explorer and the briefing: the synthetic dataset demonstrates the pipeline and the user experience, not predictive power; predictive claims wait for the backtest. Effort: S. Risk: the pitch feels weaker; that is the point.
- **Tag-stability check.** Re-run tagging with small perturbations of the inputs and report how often tags flip. Why: unstable tags are worse than no tags for planning. Effort: M. Risk: it may reveal that the method is fragile.

## Policy-maker experience

- **Three-question briefing.** Rewrite the briefing prompt around what a kommune director asks: what is changing here, what should we fund this budget year, what are we unsure about. Effort: S. Risk: generic LLM prose; needs strict grounding in the core model.
- **Compare to neighbours and to the county.** In the explorer, every kommune figure sits next to its region and national value. Why: a kommune official's first question is "is this just us". Effort: S. Risk: small kommuner have noisy numbers.
- **Action mapping.** Link a rising or transforming skill to concrete levers: fagskole courses, NAV training, apprenticeship quotas. Why: turns a chart into a decision. Effort: M. Risk: course data is scattered and partly unlicensed.
- **Uncertainty shown as a range, not a dot.** Low-confidence tags render visibly different. Why: prevents over-reading. Effort: S. Risk: visual clutter.

## Presentation and distribution

- **One-page methods note** published with the demo. Effort: S.
- **Quarterly white paper template** generated from the core model, with the methods note and backtest scores attached. Effort: M. Risk: publishing before the backtest invites fair criticism.
- **Open data contract and sample dataset** on GitHub so researchers can plug in signals. Effort: S. Risk: licence of the included samples.

## Top three

1. **Backtest harness.** It is the single thing that turns a demo into a claim, and it answers the board's hardest open question.
2. **NAV job-ad signal.** One real adapter proves the plug-in pattern works and gives the backtest something to work with.
3. **"What this prototype shows" statement.** It costs almost nothing and protects credibility with the audience most likely to probe it.

## Open questions for the team

1. Which NAV job-ad source is allowed: the arbeidsplassen.no API, NAV open data exports, or scraped Finn.no (likely not permitted under its terms)?
2. Is SSB data under NLOD / CC BY 4.0 sufficient for redistribution inside our dataset, and do we need attribution text in the explorer?
3. Does SSB publish occupation-by-kommune at the detail we need, or must we model down from county level and say so?
4. Which kommune do we commit to for the demo, and does it have a documented shock we can show in the backtest?
5. Can Kompetansebehovsutvalget or HK-dir sanity-check the tagging definitions before the white paper?
6. Who owns the Claude API cost and prompt-grounding checks for the briefing lane?

## Research learnings (2026-10-21, 18:05)

From the demo-pitch and method-rigour research. Data-sources, data-contract, explorer-ux and briefing research still running.

### Fix before the demo
- Skill-row sources read as connected data. Relabel them as planned sources.
- Header says "observed skill signals". All values are synthetic, so say so.
- Offshore wind scenario has confidence 0.41, above the proposed 0.30 scenario cap.
- Heat-pump tag differs by kommune (transforming in Bodø, rising in Stavanger and Kristiansand). Tags are hand-set; derive them from rules.
- Briefing is hand-written sample text. Say so in the demo.

### Method (proposed, not validated)
- Occupation trend: 3-year growth in share of job ads, with a ±5% a year band. "Level" means under 5% a year volume change, not "safe".
- Under 50 ads gives "insufficient data", never "level".
- Confidence = agreement × coverage × lag. One source caps at 0.33. Worked example: one signal 0.22, three signals 0.68.
- Scenario rows cap at 0.30 and never count as observed.
- Smallest real backtest (about one week): freeze at 2019 using SSB employment by occupation; score 2019–2022 direction against "no change" and "last trend" baselines.
  - Can claim: directional hit rates with counts and intervals.
  - Cannot claim: skill-tag accuracy, kommune accuracy, causation, shortage prediction.
- Check before committing: SSB publishes occupation employment at roughly 20 groups by fylke.

### Say this, not that
- Not "the model predicts shortages". Say "the prototype shows how signals would combine".
- Not "backtested". Say "backtest planned, about a week of work".
- Not "real data". Say "synthetic data; real sources being checked".
