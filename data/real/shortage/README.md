# DK shortage list and vacancy data (fetched 2026-10-21)

Raw files: /tmp/dk-data/shortage-vacancies/

## A. Positivlisten (shortage occupations)

- Owner: SIRI (Styrelsen for International Rekruttering og Integration). Basis: STAR arbejdsmarkedsbalance.
- Official page: nyidanmark.dk/da/Du-vil-ansøge/Arbejde/Positivlisterne/Positivlisten-for-faglærte
- Updated 1 Jan and 1 Jul.

Edition counts (SIRI news pages):

| Effective | Higher-education | Faglærte |
|---|---|---|
| 1 Jan 2023 | 40 | 36 |
| 1 Jul 2023 | 30 | 36 |
| 1 Jan 2024 | 72 | 38 |
| 1 Jul 2024 | 141 | 61 |
| 1 Jan 2025 | 162 | 48 |
| 1 Jul 2025 | 187 | 66 |
| 1 Jul 2026 | 164 | 63 |

- Codes: only the 1 Jul 2026 list is fetched. The faglærte page gives DISCO-08 codes for 63 titles, parsed to positivlisten_faglaerte_jul2026_page.csv. The higher-education page gives 164 coded titles. Codes for 2023 to 2025 editions are missing.
- Licence: none stated on the pages. Treat as unverified public-authority content.
- Granularity: national occupation list, no regional or municipal field.

## B. Vacancies

### Danmarks Statistik (open)

- Terms (dst.dk kildeangivelse page): free reuse, including commercial. Credit "Kilde: Danmarks Statistik" with a link. Page names CC 4.0 BY.
- Access: StatBank API, no key.
- Tables (quarterly, "Ledige stillinger, antal"): LSK14 (DB25 20 groups, 2010K1 to 2026K2), LSK11 (10 groups by size), LSK13 and LSK12 (region by branch or sector, 2026 only). Annual: LS02 (region, 2010 to 2025) and LS01 (branch and size).
- Coverage break: public-sector branches (P to TUV) enter only in 2026. Totals are not comparable. LSK14 total 2025K4 = 46,514; 2026K1 = 68,640.
- No municipal table found.

LS02 (antal, annual, raw_LS02_all.csv):

| Area | 2023 | 2024 | 2025 |
|---|---|---|---|
| Hele landet | 53,254 | 51,884 | 50,504 |
| Hovedstaden | 22,102 | 21,984 | 21,455 |
| Sjælland | 4,473 | 5,270 | 5,068 |
| Syddanmark | 9,350 | 9,620 | 9,135 |
| Midtjylland | 10,907 | 9,579 | 9,223 |
| Nordjylland | 3,522 | 3,027 | 3,350 |
| Fiktive enheder | 2,900 | 2,405 | 2,273 |

### Jobindex (not accessed)

- Handelsbetingelser (2026): Jobindex claims full copyright and rights to "anden data" from its products, and sells a paid "Robotscanningsaftale".
- No explicit scraping ban in the fetched text. robots.txt has no blanket disallow.
- Skipped: ownership claims and paid robot access mean no open licence.

### Jobnet / STAR (not accessed)

- No official open API or licence found. The jobnet.dk fetch returned a NemLog-in error. No terms found.
- Third-party scrapers exist. Not used.

## Gaps

- Codes for 2023 to 2025 editions.
- SIRI reuse licence.
- Jobnet and Jobindex full terms.
- Eurostat (mentioned by DST, not fetched).

## Demo municipalities

- Vacancies: regional only. København maps to Hovedstaden, Aarhus to Midtjylland, Odense to Syddanmark, Aalborg to Nordjylland.
- Positivlisten: national, no geography. Joins on occupation codes only.
