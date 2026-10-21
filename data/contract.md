# policy2upskill data contract v0.1.0 (proposal, not yet agreed)

All values in sample.json are synthetic.

## Grain
Skill rows per (municipality, occupation, skill). Demand rows per (municipality, occupation). National is a column.

## Fields
| field | type | rule |
|---|---|---|
| municipality | string | `municipalities[].id`, lowercase ASCII slug |
| occupation | string | English label, shared across municipalities |
| skill | string | free text |
| category | enum | rising, falling, durable, transforming. Kind of change to the skill |
| trend | enum | rising, falling, level. Direction of demand for this skill in this occupation |
| confidence | number | 0 to 1. Below 0.5 renders as low |
| scenario | bool | true = what-if assumption, not observed |
| sources | string[] | non-empty. Scenario rows need an entry starting "Scenario:". Observed rows must have none |
| index_municipality, index_region, index_national | int | 1 to 150. Base 2019=100 |
| municipalities[] | object | id, name, region, briefing as [label, text] pairs |

## Decision: category vs trend
Keep both as independent per-row fields.
- The board lists two tag sets: skill tags (rising, falling, durable, transforming) and rising, falling, level.
- The prototype comment says trend is the "occupation direction". The data contradicts it. København Electricians has rising, falling and rising rows, so trend is per row.
- Deriving trend from the demand index would contradict the København briefing (heat-pump rising, Electricians index 104). Not in v0.1.
- Finding: in all 22 prototype rows, trend is a fixed function of category. The fields carry the same information today. Keep them separate anyway, because job-ad signals will split them. Open item.

## Region correction
"Syddanmark" is stale. Syddanmark and Finnmark separated on 1 January 2024. The sample uses Syddanmark for Odense. Four regions remain. This is the only deliberate change to prototype values. The Odense demand numbers are unchanged.

## Synthetic vs scenario
- `synthetic` (top-level flag): the whole file is fabricated demo data.
- `scenario` (per row): a what-if assumption inside the data. The board uses "synthetic" for scenarios. Don't.

## Loader mapping for Lane 2 (explorer)
- `MUNICIPALITIES` = `municipalities`, unchanged.
- `SKILLS` rows: k=municipality, o=occupation, s=skill, c=category, t=trend, p=confidence, sc=scenario, src=sources.
- `DEMAND[municipality][occupation]` = [index_municipality, index_region, index_national].
- No explorer code changes.

## Checks
validate.py (outside the repo) passes: 8 municipalities, 4 regions, 8 occupations, 45 skill rows, 24 demand rows. The 22 prototype rows and 12 demand values match index.html exactly, except Odense's region. Indices are constant per occupation (national) and per region (region).

## Open items
- v0.2: derive trend from occupation demand, once job-ad data arrives.
- Danmarks Statistik municipality code and STYRK codes: not added, not verified.
- Sources are placeholder adapter names.
- Not agreed with the team.
