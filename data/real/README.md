# Real Danish data

- `lbesk354_raw.csv`: Statistics Denmark table LBESK354, employees by municipality of residence, quarterly, 2023Q1 to 2025Q4. Downloaded from the StatBank API.
- `lbesk354_municipal_employees.json`: annual averages of the four quarters for the four demo municipalities. Copenhagen is the municipality row "Copenhagen" in the source (368,220 / 373,979 / 378,725). An earlier version used "Province Byen København", a wider area that includes Frederiksberg; that was wrong and is corrected.
- Licence: CC BY 4.0. Credit: Statistics Denmark (Danmarks Statistik). Processed data is labelled as processed.
- No occupation field in this table, so occupation trends still need a source.
- `demo_municipalities.json`: the demo municipalities with annual-average employees (LBESK354), population on 1 January (BEFOLK3) and completed education (UDDAKT10, see `supply/README.md`). Copenhagen population and completions come from the same BEFOLK3 and UDDAKT10 extracts in `supply/`. The prototype embeds this file as `REAL_DATA`.
- National total for the chart ("All Denmark" employees, annual average of quarters): 2,994,702 / 3,024,145 / 3,061,004, computed from `lbesk354_raw.csv`.
