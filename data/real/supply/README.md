# Denmark supply side: population and education completions

Raw fetched responses: `/tmp/dk-data/supply-education/raw/`. Request bodies: `/tmp/dk-data/supply-education/queries/`. Table metadata: `/tmp/dk-data/supply-education/meta/`. Nothing was written to the policy2upskill repo.

## Tables fetched

| Table | Content | Years | Granularity | Classification |
|---|---|---|---|---|
| BEFOLK3 | Population 1 January | 2023-2026 | Municipality (99) and region; sex; single-year age (0-126) | Municipality list from DST |
| UDDAKT10 | Educational activity (completions, status F) | 2023-2025 (series from 2005) | Municipality of residence (BOPOMR); education code (UDDANNELSE); age; sex | DST education codes, hierarchical (H10 to H90 and sub-codes such as H3010, H6039) |
| UDDALL10 | Same content, updated 2026-06-19 | Checked for 2025 | Same | Same |

Checks run:
- BEFOLK3: the 99 municipalities sum exactly to All Denmark in every year.
- UDDAKT10: the 99 municipalities plus "Not stated municipality" (4,983 in 2025) sum to the national total of 253,032. The five regions also sum to the municipalities, so the `Region` rows are aggregates and should not be added to the municipality rows.
- UDDAKT10 and UDDALL10 match for the demo areas in 2025.
- Hierarchy: parent codes (H20) equal the sum of their children, so do not add both.

## Demo municipalities

Population, 1 January (BEFOLK3, KØN=Total, ALDER=Total):

| Area | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| København | 653,664 | 659,350 | 667,099 | 671,714 |
| Aarhus | 361,544 | 367,095 | 373,388 | 378,361 |
| Odense | 207,762 | 209,078 | 210,803 | 213,168 |
| Aalborg | 222,571 | 223,174 | 224,612 | 226,033 |

Completions, all education levels (UDDAKT10, status Completed, residence municipality):

| Area | 2023 | 2024 | 2025 |
|---|---|---|---|
| København | 36,856 | 36,679 | 36,257 |
| Aarhus | 22,380 | 22,315 | 22,259 |
| Odense | 11,997 | 11,926 | 11,576 |
| Aalborg | 12,246 | 12,416 | 12,120 |

Query for the completions file: `queries/q_uddakt10_mun_field_completed.json` (BOPOMR=*, UDDANNELSE=*, ALDER=TOT, KØN=10, FSTATUS=F, Tid=2023-2025).

## Licence

- DST says StatBank data may be reused free of charge, commercially too, with source credit. It describes this as CC BY 4.0 (dst.dk "kildeangivelse" page, via search). I did not read the legal text; confirm before publishing.
- Attribution: "Statistics Denmark, StatBank table [ID]". Say "own calculations" for transformed figures.

## Gaps

- **Time-to-fill: not found.** No DST table, and none found in the catalogue (2,310 active tables) or in web search, gives days to fill a vacancy by occupation or region.
- **Vacancies (LS02, LSK11-15, LS01):** counts or rates by region, sector or industry only. There is no occupation dimension. Quarterly data ends 2026Q2.
- **Occupation matching:** the education codes are fields of study, not occupations. Matching them to occupations needs a crosswalk (for example DISCO-08 to education). I did not find one in these tables.
- **Residence, not place of training:** UDDAKT10 counts graduates by municipality of residence. Municipalities such as København receive graduates who study elsewhere, so this is not a measure of where training happens.
## Can it feed the demo?

Yes for population (2023-2026, single-year age, all four cities) and for completions by field (2023-2025, four cities, field codes available at the H-code level). No for time-to-fill. Occupation matching still needs a crosswalk.
