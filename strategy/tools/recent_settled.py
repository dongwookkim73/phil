"""List forecasts settled since a UTC timestamp, for retros.

Usage: python3 strategy/tools/recent_settled.py <since ISO, e.g. 2026-10-16T00:15>

Prints one line per settled forecast: id, est/mid at record, skip reason,
result, dBrier vs the recorded mid (own - market; >0 means worse than market),
and the start of the note. Read-only.
"""
import json
import sys


def main():
    since = sys.argv[1] if len(sys.argv) > 1 else ""
    rows = [json.loads(line) for line in open("journal/forecasts.jsonl", encoding="utf-8") if line.strip()]
    for r in rows:
        st = r.get("settled_ts") or ""
        if r.get("status") not in ("won", "lost") or st < since:
            continue
        y = 1.0 if r["status"] == "won" else 0.0
        p, m = r["est_prob"], r.get("market_prob_at_record")
        d = (p - y) ** 2 - (m - y) ** 2 if m is not None else float("nan")
        print(f"{r['id']} {r['ts'][:16]} {r['outcome'][:12]:12} est={p:.3f} mid={m} "
              f"{r.get('skip_reason')} {r['status']} dB={d:+.3f} rev_by={r.get('superseded_by') or r.get('revised_by') or ''}")
        print(f"    {r['question'][:90]} | {r.get('category')}")
        print(f"    {(r.get('note') or '')[:400]}")


if __name__ == "__main__":
    main()
