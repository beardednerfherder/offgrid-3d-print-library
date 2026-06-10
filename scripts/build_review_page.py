#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, html
from collections import defaultdict

CSS = """
body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:24px;line-height:1.35;background:#fafafa;color:#222}
h1{margin-bottom:0}.small{color:#666}.target{margin-top:28px;background:white;border:1px solid #ddd;border-radius:12px;padding:16px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{border-top:1px solid #e5e5e5;padding:8px;vertical-align:top}th{text-align:left;background:#f4f4f4}
.score{font-weight:700}.high{color:#116b25}.mid{color:#8a5b00}.low{color:#9a1e1e}.url{word-break:break-all}.notes{color:#555}
.badge{display:inline-block;padding:2px 7px;border-radius:8px;background:#eee;margin-right:4px}.github{background:#e6f0ff}.thingiverse{background:#eaffea}.printables{background:#fff0dc}.makerworld{background:#f0eaff}
code{background:#eee;padding:2px 4px;border-radius:4px}
"""

def esc(x): return html.escape(str(x or ""))
def score_class(score):
    try: s=int(score)
    except: return "low"
    return "high" if s>=18 else "mid" if s>=10 else "low"

ap=argparse.ArgumentParser()
ap.add_argument("--candidates", required=True)
ap.add_argument("--out", required=True)
args=ap.parse_args()

rows=[]
with open(args.candidates, newline='', encoding='utf-8') as f:
    rows=list(csv.DictReader(f))

groups=defaultdict(list)
for r in rows:
    groups[(r.get('category',''), r.get('target_item',''))].append(r)

parts=["<!doctype html><meta charset='utf-8'><title>Offgrid STL Candidate Review</title><style>",CSS,"</style>"]
parts.append("<h1>Offgrid STL Candidate Review</h1>")
parts.append(f"<p class='small'>{len(rows)} candidates. Open this beside <code>manifests/candidates.csv</code>. Change <code>status</code> to <code>approved</code> or <code>rejected</code> in the CSV, then run <code>split_review_decisions.py</code>.</p>")
parts.append("<p class='small'>Do not approve a model until the page title matches, files exist, and license allows your intended use. For Printables, expect manual download.</p>")

for (cat,target), items in groups.items():
    items.sort(key=lambda r:int(r.get('score') or 0), reverse=True)
    parts.append(f"<section class='target'><h2>{esc(cat)} — {esc(target)}</h2>")
    parts.append("<table><tr><th>Status</th><th>Score</th><th>Source</th><th>Title / URL</th><th>Snippet</th><th>Why it matched</th></tr>")
    for r in items:
        src=esc(r.get('source',''))
        sc=esc(r.get('score',''))
        parts.append("<tr>")
        parts.append(f"<td><code>{esc(r.get('status','candidate'))}</code></td>")
        parts.append(f"<td class='score {score_class(sc)}'>{sc}</td>")
        parts.append(f"<td><span class='badge {src}'>{src}</span></td>")
        parts.append(f"<td><b>{esc(r.get('title',''))}</b><br><a class='url' href='{esc(r.get('url',''))}' target='_blank'>{esc(r.get('url',''))}</a></td>")
        parts.append(f"<td>{esc(r.get('snippet',''))}</td>")
        parts.append(f"<td class='notes'>{esc(r.get('score_reason',''))}</td>")
        parts.append("</tr>")
    parts.append("</table></section>")

with open(args.out,'w',encoding='utf-8') as f: f.write('\n'.join(parts))
print(f"Wrote {args.out}")
