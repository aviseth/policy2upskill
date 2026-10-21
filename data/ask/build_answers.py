"""Generate LLM answers for the Ask the data view with the Claude API (Haiku 5.5, effort medium).

Reads the data constants from prototype/index.html (no separate copy), asks each question for each
municipality, and writes data/ask/answers.json. The API key comes from the environment only.

  export ANTHROPIC_API_KEY=...        # never commit it
  python3 data/ask/build_answers.py --dry-run     # print one prompt, send nothing
  python3 data/ask/build_answers.py               # full run, about 100 calls
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = "claude-haiku-5-5"
QUESTIONS = {
    "workforce": "How big is the workforce, and how fast is it changing?",
    "compare": "How does this municipality compare with its region?",
    "rising": "Which skills are rising?",
    "falling": "Which skills are falling?",
    "shortage": "Which occupations are on a shortage list?",
    "completions": "Is training output keeping up with population?",
    "scenario": "What do the scenario assumptions say?",
}
SYSTEM = """You answer questions for Danish policy makers about one municipality, using only the JSON data given.
Rules:
- Use only the figures in the JSON. Do not add facts, names or numbers from outside it.
- Label each figure's source in the sentence: "(real, Statistics Denmark)" for REAL_DATA, "(synthetic)" for everything else.
- Do not forecast. Never say what will happen. Describe what the data shows.
- Scenario rows are assumptions, not observed data. Say so.
- If the data cannot answer the question, say so in one sentence.
- Plain English, at most 90 words, no headings, no bullet lists, no markdown tables.
- Write for a civil servant. Avoid jargon."""


def load_payload():
    payload = ROOT / "data/ask/payload.json"
    if payload.exists():
        return json.loads(payload.read_text())
    # Rebuild from the prototype if the payload file is missing
    html = (ROOT / "prototype/index.html").read_text()
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    cut = js.index("\ninitLevels();")
    stub = ("const mk=()=>new Proxy(function(){}, {get:(t,p)=> (p===Symbol.toPrimitive? ()=>'' : mk()), set:()=>true, apply:()=>mk()});"
            "const document=new Proxy({}, {get:(t,p)=> p==='addEventListener'? ()=>{} : mk()}); const window=new Proxy({}, {get:()=>()=>{}}); const location={hash:''}; const history={replaceState(){}};")
    code = stub + js[:cut] + "\nconsole.log(JSON.stringify({MUNICIPALITIES, SKILLS, INDICATORS, DEMAND, REAL_DATA}));"
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def context_for(data, mid, qid, other=None):
    m = next(x for x in data["MUNICIPALITIES"] if x["id"] == mid)
    skills = [r for r in data["SKILLS"] if r["k"] == mid]
    ctx = {
        "question_id": qid,
        "municipality": {"id": mid, "name": m["name"], "region": m["region"]},
        "REAL_DATA": data["REAL_DATA"].get(mid, {}),
        "skills_synthetic": [{"occupation": r["o"], "skill": r["s"], "category": r["c"], "trend": r["t"],
                              "confidence": r["p"], "scenario": r["sc"], "sources": r["src"]} for r in skills],
        "shortage_synthetic": data["INDICATORS"].get(mid, {}),
        "demand_index_synthetic": data["DEMAND"].get(mid, {}),
    }
    if qid == "compare" and other:
        o = next(x for x in data["MUNICIPALITIES"] if x["id"] == other)
        ctx["compare_with"] = {"id": other, "name": o["name"], "REAL_DATA": data["REAL_DATA"].get(other, {}),
                               "skills_synthetic": [{"occupation": r["o"], "trend": r["t"], "scenario": r["sc"]}
                                                    for r in data["SKILLS"] if r["k"] == other]}
    return ctx


def user_message(qid, ctx):
    return f"Question: {QUESTIONS[qid]}\n\nData (JSON):\n{json.dumps(ctx, ensure_ascii=False, indent=1)}"


def call(client, text):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,  # adaptive thinking counts against max_tokens
        system=SYSTEM,
        messages=[{"role": "user", "content": text}],
        output_config={"effort": "medium"},
    )
    if resp.stop_reason != "end_turn":
        return None, f"stop_reason={resp.stop_reason}"
    return next(b.text for b in resp.content if b.type == "text").strip(), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    data = load_payload()
    mids = [m["id"] for m in data["MUNICIPALITIES"]]
    jobs = []
    for mid in mids:
        region_peer = next((x["id"] for x in data["MUNICIPALITIES"] if x["region"] == next(
            y["region"] for y in data["MUNICIPALITIES"] if y["id"] == mid) and x["id"] != mid), None)
        for qid in QUESTIONS:
            jobs.append((mid, qid, region_peer if qid == "compare" else None))
    if args.dry_run:
        mid, qid, other = jobs[0]
        print(SYSTEM, "\n---\n", user_message(qid, context_for(data, mid, qid, other)))
        print(f"\n[dry run] {len(jobs)} calls would be made to {MODEL}, effort medium.")
        return
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY in the environment. Nothing was sent.")
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    client = anthropic.Anthropic()
    answers, errors = {}, []
    for mid, qid, other in jobs:
        text, err = call(client, user_message(qid, context_for(data, mid, qid, other)))
        if err:
            errors.append({"municipality": mid, "question": qid, "error": err})
            continue
        answers.setdefault(mid, {})[qid] = text
    out = {"model": MODEL, "effort": "medium", "answers": answers, "errors": errors}
    (ROOT / "data/ask/answers.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"wrote data/ask/answers.json: {sum(len(v) for v in answers.values())} answers, {len(errors)} errors")


if __name__ == "__main__":
    main()
