#!/usr/bin/env python3
"""Generate municipality briefings from core-model rows with the Claude API.

Dry run (no network, no key needed):
  python3 generate.py --input sample_bodo.json --dry-run

Live run (key comes from the ANTHROPIC_API_KEY environment variable only):
  export ANTHROPIC_API_KEY=...
  python3 generate.py --input municipalityr.json --model sonnet --out briefings.json
"""
import argparse
import json
import os
import re
import sys

MODELS = {"sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
SECTIONS = ["what_is_changing", "what_to_fund_this_year", "what_we_are_unsure_about"]
CATEGORIES = {"rising", "falling", "durable", "transforming"}
TRENDS = {"rising", "falling", "level"}
FORBIDDEN = re.compile(
    r"\b(will|expect\w*|forecast\w*|predict\w*|likely|going to|projected|future|by 20\d\d)\b",
    re.I,
)

SYSTEM_PROMPT = """You write a short briefing for Danish policy makers about skills and occupations in one municipality. You describe the input data. You do not forecast.

Rules:
1. Use only the JSON in the user message. Add no facts, causes, figures or sources that are not in it.
2. Every claim cites one or more ids from the input: r1, r2, ... for skill rows and d1, d2, ... for demand rows. Cite only ids that exist.
3. Describe the data as it stands. Use present tense ("Heat-pump installation is tagged rising"). Never use future tense, "expected", "likely", "forecast", "predict", "projected", or a year after the data. Never say what will happen.
4. A row with scenario true is a what-if assumption, not an observation. Use kind "assumption" and say "assumption" in the text. Never present it as an observed trend.
5. A row with confidence below 0.5 is uncertain. Use kind "uncertain" and state its confidence value.
6. Kind "observed" cites only rows with scenario false and confidence 0.5 or higher.
7. what_is_changing: kind "observed" only. what_to_fund_this_year: kind "observed" only. Name the skill and its row. Name skill areas that the observed rows support. Promise no outcome, return or job count.
8. what_we_are_unsure_about: kind "uncertain" or "assumption" only.
9. The demand index is 2019 = 100. Compare the municipality with its region and with Denmark only as the numbers show. Do not say the index caused anything.
10. If the input has no observed rows, set status "insufficient_data" and return empty lists.
11. Two to four claims per list. One or two plain sentences per claim. No hype.
12. Keep occupation and skill names exactly as given.

Return only JSON that matches the output schema."""

CLAIM = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "kind": {"type": "string", "enum": ["observed", "assumption", "uncertain"]},
        "cites": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["text", "kind", "cites"],
    "additionalProperties": False,
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok", "insufficient_data"]},
        "municipality": {"type": "string"},
        **{s: {"type": "array", "items": CLAIM} for s in SECTIONS},
    },
    "required": ["status", "municipality", *SECTIONS],
    "additionalProperties": False,
}


def index_payload(municipality):
    """Validate one municipality and assign stable ids: r1.. for skill rows, d1.. for demand."""
    for key in ("municipality", "region", "rows"):
        if key not in municipality:
            raise ValueError(f"missing field: {key}")
    rows = []
    for i, r in enumerate(municipality["rows"], 1):
        if r["category"] not in CATEGORIES or r["trend"] not in TRENDS:
            raise ValueError(f"row {i}: bad category or trend")
        if not 0 <= float(r["confidence"]) <= 1:
            raise ValueError(f"row {i}: confidence outside 0..1")
        rows.append({
            "id": f"r{i}",
            "occupation": r["occupation"],
            "skill": r["skill"],
            "category": r["category"],
            "trend": r["trend"],
            "confidence": float(r["confidence"]),
            "scenario": bool(r["scenario"]),
            "sources": list(r.get("sources", [])),
        })
    demand = [{"id": f"d{i}", **d} for i, d in enumerate(municipality.get("demand", []), 1)]
    return {"municipality": municipality["municipality"], "region": municipality["region"], "rows": rows, "demand": demand}


def user_message(indexed):
    return ("Municipality input (JSON):\n"
            + json.dumps(indexed, ensure_ascii=False, indent=2)
            + "\n\nWrite the briefing.")


def check(out, indexed):
    """Return a list of rule violations. An empty list means the briefing passes."""
    errors = []
    rows = {r["id"]: r for r in indexed["rows"]}
    known = set(rows) | {d["id"] for d in indexed["demand"]}
    if out.get("municipality") != indexed["municipality"]:
        errors.append("municipality name differs from input")
    if out.get("status") == "insufficient_data" and any(out.get(s) for s in SECTIONS):
        errors.append("insufficient_data status with non-empty sections")
    for section in SECTIONS:
        for c in out.get(section, []):
            tag = f"{section}: {c['text'][:50]}"
            kind = c["kind"]
            if not c["cites"]:
                errors.append(f"no citation | {tag}")
            for cid in c["cites"]:
                if cid not in known:
                    errors.append(f"unknown id {cid} | {tag}")
            if FORBIDDEN.search(c["text"]):
                errors.append(f"predictive wording | {tag}")
            cited = [rows[i] for i in c["cites"] if i in rows]
            scen = any(r["scenario"] for r in cited)
            low = any(r["confidence"] < 0.5 for r in cited)
            if scen and kind != "assumption":
                errors.append(f"scenario row not marked assumption | {tag}")
            if kind == "assumption" and not scen:
                errors.append(f"assumption cites no scenario row | {tag}")
            if kind == "observed" and low:
                errors.append(f"observed claim cites low-confidence row | {tag}")
            if kind == "uncertain" and not low:
                errors.append(f"uncertain claim cites no low-confidence row | {tag}")
            if kind == "assumption" and "assumption" not in c["text"].lower():
                errors.append(f"assumption claim does not say assumption | {tag}")
            if kind == "uncertain":
                for r in cited:
                    if r["confidence"] < 0.5 and f"{r['confidence']:.2f}" not in c["text"]:
                        errors.append(f"uncertain claim omits confidence {r['confidence']:.2f} of {r['id']} | {tag}")
            if section in ("what_is_changing", "what_to_fund_this_year") and kind != "observed":
                errors.append(f"{kind} claim in {section} | {tag}")
            if section == "what_we_are_unsure_about" and kind == "observed":
                errors.append(f"observed claim in unsure section | {tag}")
    return errors


def call_model(indexed, model_id):
    """One Messages API call with structured output. Returns (briefing_dict, error_string)."""
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    resp = client.messages.create(
        model=model_id,
        max_tokens=16000,  # adaptive thinking counts against max_tokens; 4000 can truncate
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message(indexed)}],
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
    )
    if resp.stop_reason != "end_turn":
        return None, f"stop_reason={resp.stop_reason}"
    text = next(b.text for b in resp.content if b.type == "text")
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="JSON file: one municipality object or a list of them")
    ap.add_argument("--model", choices=sorted(MODELS), default="sonnet")
    ap.add_argument("--out", default="briefings.json")
    ap.add_argument("--dry-run", action="store_true", help="print the prompt and schema; send nothing")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        municipalityr = json.load(f)
    if isinstance(municipalityr, dict):
        municipalityr = [municipalityr]
    model_id = MODELS[args.model]

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it in your shell. Nothing was sent.")

    results = []
    for k in municipalityr:
        indexed = index_payload(k)
        if args.dry_run:
            print(f"=== {indexed['municipality']} | model {model_id} | no request sent ===")
            print("--- system prompt ---")
            print(SYSTEM_PROMPT)
            print("--- user message ---")
            print(user_message(indexed))
            print("--- output schema ---")
            print(json.dumps(OUTPUT_SCHEMA, indent=2))
            continue
        out, err = call_model(indexed, model_id)
        if out is None:
            results.append({"municipality": indexed["municipality"], "model": model_id, "status": "failed", "error": err})
            continue
        errors = check(out, indexed)
        results.append({
            "municipality": indexed["municipality"],
            "model": model_id,
            "status": "ok" if not errors else "failed_validation",
            "errors": errors,
            "briefing": out,
        })

    if not args.dry_run:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"wrote {len(results)} briefing(s) to {args.out}")


if __name__ == "__main__":
    main()
