"""Generate the PRISM Level 1 dataset from the final-context1 saved brains.

For each question in the run, pull the real windowed retrieval context and the
gold from the LongMemEval dataset, and write a JSONL record (context -> gold).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")

RUN = "/usr/local/devel/positronic/consumers/benchmarks/results/longmemeval/final-context1"
BENCH = "/usr/local/devel/positronic/consumers/benchmarks"
OUT = "/usr/local/devel/positronic/positronic-research/papers/positronic-prism/dataset/level1/train.jsonl"


def extraction_class(gold: str, q: str) -> str:
    g = gold.lower().strip()
    if q.lower().startswith(("how many", "how much") ):
        if any(x in g for x in ("hours", "minute", "year", "month", "week", "days")):
            return "durative"
        return "counting"
    if any(x in g for x in ("yes", "no")):
        return "boolean"
    if any(x in g for x in ("'s", " ")) and len(g.split()) <= 3:
        return "name"
    return "exact-value"


def main():
    sys.path.insert(0, BENCH)
    from suites.longmemeval.real_driver import _load_real
    from memeng.store import SQLiteStore
    from memeng.engine import MemoryEngine

    data = _load_real(n=50, offset=0)
    records = []
    for idx, row in enumerate(data):
        q, gold = row["question"], row["answer"]
        dbs = list(Path(RUN).glob(f"tmp-{idx}/*.db"))
        if not dbs:
            continue
        e = MemoryEngine(SQLiteStore(str(dbs[0])))
        hits = e.activate({"text": q}, k=8, context_window=1)
        if not hits:
            continue
        ctx = "\n---\n".join((h.get("snippet") or "")[:800] for h in hits[:8])
        g = gold.lower()
        in_ctx = g[:12] in ctx.lower() or g.split()[0].lower() in ctx.lower()
        records.append({
            "id": f"prism-l1-{idx:04d}",
            "source": f"longmemeval/q{idx}",
            "question_type": row.get("question_type", "single-session-user"),
            "question": q,
            "context": ctx,
            "gold": gold,
            "gold_in_context": in_ctx,
            "extraction_class": extraction_class(gold, q),
            "difficulty": "hard" if not in_ctx else "easy",
            "note": "seed record from final-context1 run",
        })

    with open(OUT, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(records)} records -> {OUT}")
    cls = {}
    for r in records:
        cls[r["extraction_class"]] = cls.get(r["extraction_class"], 0) + 1
    print("extraction classes:", cls)


if __name__ == "__main__":
    main()