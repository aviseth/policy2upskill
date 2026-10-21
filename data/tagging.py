"""Occupation trend from synthetic Danish employment data (2019 vs 2025).

Thresholds are PROPOSED (see the method note) and not validated.
Skill tags (rising / falling / durable / transforming) need skill-mix data,
which this file does not have, so they are not computed here.
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
    here = Path(__file__).parent / "synthetic"
    rows = list(csv.DictReader((here / "employment_dk.csv").open()))
    out = here / "occupation_trend.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["municipality_slug", "occupation_group", "employed_2019", "employed_2025", "annual_growth", "trend"])
        for r in rows:
            if r["occupation_group"] == "All occupations":
                continue
            a, b = int(r["employed_2019"]), int(r["employed_2025"])
            g = "" if a == 0 else f"{(b / a) ** (1 / YEARS) - 1:.4f}"
            w.writerow([r["municipality_slug"], r["occupation_group"], a, b, g, trend(a, b)])
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
