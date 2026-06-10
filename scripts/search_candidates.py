#!/usr/bin/env python3
"""
Search the web for 3D-print model candidates for an off-grid/homestead STL library.

Outputs a review CSV. This script DOES NOT download files and DOES NOT approve models.
It is designed to find possible matches, score them, and filter obvious junk.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import sys
import time
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import quote_plus, urlparse, unquote

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

USER_AGENT = "offgrid-stl-candidate-search/0.1 (+personal library curation)"

SOURCES = {
    "github": "site:github.com",
    "thingiverse": "site:thingiverse.com/thing",
    "printables": "site:printables.com/model",
    "makerworld": "site:makerworld.com",
}

MODEL_EXTENSIONS = (".stl", ".3mf", ".step", ".stp", ".scad", ".obj")

JUNK_WORDS = {
    "toy", "miniature", "minifigure", "figurine", "statue", "ornament", "cosplay",
    "warhammer", "dnd", "d&d", "pokemon", "keychain", "decor", "decoration",
    "minecraft", "lego", "doll", "action figure", "fantasy", "sword", "skull",
    "dragon", "star wars", "model railway", "model train", "rc car", "benchy",
}

GOOD_WORDS = {
    "repair", "clip", "bracket", "mount", "adapter", "cap", "holder", "support",
    "guide", "jig", "case", "cover", "strain relief", "outdoor", "garden", "irrigation",
    "solar", "greenhouse", "bucket", "hose", "drip", "pex", "powerpole", "mc4",
    "sensor", "antenna", "meshtastic", "esp32", "sdr", "funnel", "hook", "organizer",
}

SOURCE_WEIGHTS = {
    "github": 6,       # usually most automatable if files/license are present
    "thingiverse": 4, # automatable with API token
    "printables": 3,  # good quality, often manual download
    "makerworld": 1,  # useful, but less automation-friendly
    "other": 0,
}

@dataclass
class Target:
    category: str
    target_item: str
    priority: str = ""
    notes: str = ""


def read_targets(path: str) -> list[Target]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    targets: list[Target] = []
    for r in rows:
        # Support both your wanted_targets.csv format and simple one-column lists.
        target = (r.get("target_item") or r.get("target") or r.get("name") or "").strip()
        if not target:
            continue
        targets.append(Target(
            category=(r.get("category") or r.get("category_name") or "Uncategorized").strip(),
            target_item=target,
            priority=(r.get("priority") or "").strip(),
            notes=(r.get("notes") or "").strip(),
        ))
    return targets


def ddg_search(query: str, max_results: int = 10) -> list[dict]:
    """DuckDuckGo HTML endpoint. No API key. Slow but simple."""
    url = "https://duckduckgo.com/html/?q=" + quote_plus(query)
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        print(f"WARN: search failed for {query!r}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    out: list[dict] = []
    for result in soup.select(".result"):
        a = result.select_one("a.result__a")
        if not a:
            continue
        title = " ".join(a.get_text(" ", strip=True).split())
        href = a.get("href") or ""
        snippet_el = result.select_one(".result__snippet")
        snippet = " ".join(snippet_el.get_text(" ", strip=True).split()) if snippet_el else ""
        clean_url = clean_ddg_url(href)
        if clean_url:
            out.append({"title": title, "url": clean_url, "snippet": snippet})
        if len(out) >= max_results:
            break
    return out


def clean_ddg_url(url: str) -> str:
    if not url:
        return ""
    # DDG sometimes gives /l/?uddg=<encoded>
    if "uddg=" in url:
        m = re.search(r"uddg=([^&]+)", url)
        if m:
            return unquote(m.group(1))
    return html.unescape(url)


def classify_source(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "github.com" in host or "raw.githubusercontent.com" in host:
        return "github"
    if "thingiverse.com" in host:
        return "thingiverse"
    if "printables.com" in host:
        return "printables"
    if "makerworld.com" in host:
        return "makerworld"
    return "other"


def token_overlap(a: str, b: str) -> int:
    aw = set(re.findall(r"[a-z0-9]+", a.lower()))
    bw = set(re.findall(r"[a-z0-9]+", b.lower()))
    stop = {"the", "and", "for", "with", "stl", "print", "3d", "model"}
    aw -= stop
    bw -= stop
    return len(aw & bw)


def score_candidate(target: Target, title: str, url: str, snippet: str) -> tuple[int, str]:
    text = f"{title} {url} {snippet}".lower()
    score = 0
    reasons = []

    source = classify_source(url)
    score += SOURCE_WEIGHTS[source]
    reasons.append(f"source:{source}+{SOURCE_WEIGHTS[source]}")

    overlap = token_overlap(target.target_item, title + " " + snippet)
    if overlap:
        score += overlap * 3
        reasons.append(f"target-overlap:{overlap}x3")

    for w in GOOD_WORDS:
        if w in text:
            score += 2
            reasons.append(f"good:{w}")

    for w in JUNK_WORDS:
        if w in text:
            score -= 12
            reasons.append(f"junk:{w}")

    if any(ext in text for ext in MODEL_EXTENSIONS):
        score += 3
        reasons.append("file-ext-hint")

    if "thingiverse.com/thing:" in url:
        score += 2
        reasons.append("thingiverse-thing-url")

    if "printables.com/model/" in url:
        score += 2
        reasons.append("printables-model-url")

    if "github.com" in url:
        score += 2
        reasons.append("github-url")

    return score, "; ".join(reasons[:12])


def make_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def build_queries(target: Target, sources: Iterable[str]) -> list[tuple[str, str]]:
    base = target.target_item
    queries: list[tuple[str, str]] = []
    for src in sources:
        site_filter = SOURCES[src]
        queries.append((src, f'{site_filter} "{base}" STL 3D print'))
        # A slightly looser query catches pages without exact title phrasing.
        queries.append((src, f'{site_filter} {base} printable model'))
    return queries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True, help="CSV with target_item/category/priority/notes columns")
    ap.add_argument("--out", required=True, help="Output candidates CSV")
    ap.add_argument("--sources", default="github,thingiverse,printables", help="Comma list: github,thingiverse,printables,makerworld")
    ap.add_argument("--limit-per-query", type=int, default=6)
    ap.add_argument("--max-candidates-per-target", type=int, default=12)
    ap.add_argument("--sleep", type=float, default=1.2)
    ap.add_argument("--min-score", type=int, default=0, help="Write only rows with this score or higher")
    args = ap.parse_args()

    sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    for s in sources:
        if s not in SOURCES:
            raise SystemExit(f"Unknown source {s!r}. Valid: {', '.join(SOURCES)}")

    targets = read_targets(args.targets)
    seen_urls: set[str] = set()
    rows: list[dict] = []

    for target in tqdm(targets, desc="targets"):
        target_rows: list[dict] = []
        for src, query in build_queries(target, sources):
            results = ddg_search(query, max_results=args.limit_per_query)
            time.sleep(args.sleep)
            for r in results:
                url = r["url"].split("#")[0]
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                source = classify_source(url)
                if source == "other":
                    continue
                score, reason = score_candidate(target, r["title"], url, r["snippet"])
                if score < args.min_score:
                    continue
                target_rows.append({
                    "candidate_id": make_id(url),
                    "category": target.category,
                    "target_item": target.target_item,
                    "priority": target.priority,
                    "source": source,
                    "score": score,
                    "title": r["title"],
                    "url": url,
                    "snippet": r["snippet"],
                    "score_reason": reason,
                    "target_notes": target.notes,
                    "status": "candidate",
                    "review_notes": "",
                })
        target_rows.sort(key=lambda x: int(x["score"]), reverse=True)
        rows.extend(target_rows[:args.max_candidates_per_target])

    fieldnames = [
        "candidate_id", "category", "target_item", "priority", "source", "score",
        "title", "url", "snippet", "score_reason", "target_notes", "status", "review_notes"
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} candidates to {args.out}")
    print("Next: python3 scripts/build_review_page.py --candidates manifests/candidates.csv --out review.html")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
