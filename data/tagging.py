"""Occupation trend from SSB table 11619 (employed persons, 2019 vs 2025).

Thresholds are PROPOSED (see research/method-rigour.md) and not validated.
Skill tags (rising / falling / durable / transforming) need skill-mix data,
which this table does not have, so they are not computed here.
"""
import csv
from pathlib import Path

START, END = "2019", "2025"
YEARS = int(END) - int(START)
BAND = 0.05        # +/- 5% a year counts as level (proposed)
MIN_EMPLOYED = 50  # below this in the start year: insufficient data (proposed)


def trend(start: int, end: int) -> str:
    if start < MIN_EMPLOYED:
        return "insufficient data"
    annual = (end / start) ** (1 / YEARS) - 1
    if annual > BAND:
        return "rising"
    if annual < -BAND:
        return "falling"
    return "level"


def main() -> None:
    here = Path(__file__).parent / "ssb"
    rows = list(csv.DictReader((here / "11619-municipalities.csv").open()))
    by = {}
    for r in rows:
        if r["year"] not in (START, END) or r["occupation_code"] == "0-9":
            continue
        # Tromsø and Kristiansand change code over time; SOURCE.md explains the mapping.
        key = (r["municipality_slug"], r["occupation_label"])
        by.setdefault(key, {})[r["year"]] = int(r["employed_persons"]) if r["employed_persons"] else 0
    out = here / "occupation_trend.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["municipality_slug", "occupation_label", "employed_2019", "employed_2025", "annual_growth", "trend"])
        for (slug, occ), v in sorted(by.items()):
            a, b = v.get(START, 0), v.get(END, 0)
            g = "" if a == 0 else f"{(b / a) ** (1 / YEARS) - 1:.4f}"
            w.writerow([slug, occ, a, b, g, trend(a, b)])
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
