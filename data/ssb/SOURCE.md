# SSB table 11619 (employed persons, Q4)

- Source: Statistics Norway (SSB), table 11619, "Employed persons, Q4, by region, sex, age, occupation and year". Updated 2026-02-26.
- Licence: CC BY 4.0. Credit: "Source: SSB".
- Extract: `11619-municipalities.csv`, produced from the cached PxWeb json-stat response for 7 municipality codes, 11 occupation groups, 2015-2025.
- Municipality codes change over time. `municipality_slug` maps each code to the prototype municipality. Tromsø uses 1902, 5401 and 5501 in different years; Kristiansand uses 1001 and 4204. Don't mix codes in one series.
- Privacy: SSB rounds small one- and two-digit cells to 0 or 3 to protect individuals. Treat small occupation cells as approximate.
- Occupation detail is one-digit STYRK-08 major groups only. Skills are not in this table.
- Known gap: SSB has no occupation for many self-employed workers, and reporting changed in 2019, so the "Unknown" group falls sharply between 2018 and 2019.
