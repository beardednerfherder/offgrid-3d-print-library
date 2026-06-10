#!/usr/bin/env python3
"""
Offgrid STL/STEP candidate search v3

This version deliberately avoids DuckDuckGo/Google scraping because those results
can be noisy and blocked. It does two safer things:

1. Searches Thingiverse through the Thingiverse API when --thingiverse-token is supplied.
2. Generates manual search rows for Printables/GitHub/Thangs/MakerWorld instead of pretending
   bad search-engine hits are valid model candidates.

Output is still a review CSV. Nothing is approved automatically.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, quote_plus

import requests
from tqdm import tqdm

THINGIVERSE_API = "https://api.thingiverse.com"
UA = "offgrid-stl-curator/0.3"
SOURCE_EXTS = (".step", ".stp", ".scad", ".f3d", ".fcstd", ".sldprt")
MODEL_EXTS = (".stl", ".3mf", ".obj")

JUNK_WORDS = {
    "toy", "miniature", "minifigure", "figurine", "statue", "ornament", "cosplay",
    "warhammer", "dnd", "d&d", "pokemon", "keychain", "decor", "decoration",
    "minecraft", "lego", "doll", "action figure", "fantasy", "sword", "skull",
    "dragon", "star wars", "model railway", "model train", "rc car", "benchy",
    "cookie cutter", "vase", "lamp", "candle", "fidget", "prop", "replica",
}

GOOD_WORDS = {
    "repair", "clip", "bracket", "mount", "adapter", "cap", "holder", "support",
    "guide", "jig", "case", "cover", "strain", "relief", "outdoor", "garden", "irrigation",
    "solar", "greenhouse", "bucket", "hose", "drip", "pex", "powerpole", "mc4",
    "sensor", "antenna", "meshtastic", "esp32", "sdr", "funnel", "hook", "organizer",
    "water", "rain", "barrel", "tube", "tubing", "wire", "cable", "din", "rail",
    "camera", "tripod", "pole", "coop", "feeder", "nipple", "mason", "jar",
}

STOP = {"the", "and", "for", "with", "stl", "print", "3d", "model", "models", "set", "assortment"}

@dataclass
class Target:
    category: str
    target_item: str
    priority: str = ""
    notes: str = ""


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s[:80] or "item"


def make_id(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:12]


def tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower())) - STOP


def split_compound_target(item: str) -> list[str]:
    """Turn 'A / B / C' style rows into more searchable atomic phrases."""
    raw = item.strip()
    parts = re.split(r"\s*/\s*|\s*,\s*|\s+and\s+", raw)
    cleaned = []
    for p in parts:
        p = p.strip(" -")
        if len(p) >= 4:
            cleaned.append(p)
    # If splitting created only tiny pieces, keep original.
    if not cleaned:
        cleaned = [raw]
    # Keep original too when it is not too long.
    if raw not in cleaned and len(raw) <= 80:
        cleaned.insert(0, raw)
    return list(dict.fromkeys(cleaned))


def read_targets(path: str, expand: bool = True) -> list[Target]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    targets: list[Target] = []
    for r in rows:
        target = (r.get("target_item") or r.get("target") or r.get("name") or "").strip()
        if not target:
            continue
        base = Target(
            category=(r.get("category") or r.get("category_name") or "Uncategorized").strip(),
            target_item=target,
            priority=(r.get("priority") or "").strip(),
            notes=(r.get("notes") or "").strip(),
        )
        if expand:
            for part in split_compound_target(target):
                targets.append(Target(base.category, part, base.priority, base.notes))
        else:
            targets.append(base)
    # de-dupe category + target
    seen = set()
    out = []
    for t in targets:
        k = (t.category.lower(), t.target_item.lower())
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def score_title(target: Target, title: str, description: str = "") -> tuple[int, str]:
    text = f"{title} {description}".lower()
    score = 0
    reasons = []

    overlap = len(tokens(target.target_item) & tokens(text))
    if overlap:
        score += overlap * 4
        reasons.append(f"target-overlap:{overlap}x4")

    for w in sorted(GOOD_WORDS):
        if w in text:
            score += 2
            reasons.append(f"good:{w}")

    for w in sorted(JUNK_WORDS):
        if w in text:
            score -= 20
            reasons.append(f"junk:{w}")

    # Prefer short utilitarian titles over huge SEO soup.
    word_count = len(tokens(title))
    if 2 <= word_count <= 10:
        score += 2
        reasons.append("concise-title")
    elif word_count > 18:
        score -= 4
        reasons.append("title-too-broad")

    return score, "; ".join(reasons[:16])


def tv_request(path: str, token: str, params: dict | None = None) -> object | None:
    headers = {"User-Agent": UA, "Authorization": f"Bearer {token}"}
    url = THINGIVERSE_API + path
    try:
        r = requests.get(url, headers=headers, params=params or {}, timeout=25)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"WARN: Thingiverse request failed: {url} {e}", file=sys.stderr)
        return None


def thingiverse_search(term: str, token: str, per_page: int = 10) -> list[dict]:
    """Try several known Thingiverse API search shapes because the API has changed over time."""
    encoded = quote(term)
    attempts = [
        (f"/search/{encoded}", {"type": "things", "per_page": per_page, "page": 1}),
        (f"/search/{encoded}/things", {"per_page": per_page, "page": 1}),
        ("/search", {"q": term, "type": "things", "per_page": per_page, "page": 1}),
    ]
    for path, params in attempts:
        data = tv_request(path, token, params)
        if not data:
            continue
        if isinstance(data, dict):
            candidates = data.get("hits") or data.get("results") or data.get("things") or data.get("data") or []
        elif isinstance(data, list):
            candidates = data
        else:
            candidates = []
        if candidates:
            return candidates
    return []


def normalize_tv_item(item: dict) -> dict | None:
    thing_id = item.get("id") or item.get("thing_id")
    title = item.get("name") or item.get("title") or ""
    if not thing_id or not title:
        return None
    return {
        "thing_id": str(thing_id),
        "title": title,
        "url": item.get("public_url") or f"https://www.thingiverse.com/thing:{thing_id}",
        "snippet": item.get("description") or item.get("thumbnail") or "",
        "creator": (item.get("creator") or {}).get("name") if isinstance(item.get("creator"), dict) else "",
        "license": item.get("license") or "",
        "like_count": item.get("like_count") or item.get("likes") or "",
        "make_count": item.get("make_count") or item.get("makes") or "",
    }



def thingiverse_file_summary(thing_id: str, token: str) -> dict:
    """Return a light file-format summary for a Thingiverse model."""
    data = tv_request(f"/things/{thing_id}/files", token) or []
    formats = set()
    source_files = []
    printable_files = []
    total = 0
    if isinstance(data, list):
        for f in data:
            name = (f.get("name") or "").strip()
            if not name:
                continue
            total += 1
            lower = name.lower().split("?")[0]
            ext = ""
            for suffix in SOURCE_EXTS + MODEL_EXTS:
                if lower.endswith(suffix):
                    ext = suffix.lstrip(".")
                    formats.add(ext.upper())
                    break
            if lower.endswith(SOURCE_EXTS):
                source_files.append(name)
            if lower.endswith(MODEL_EXTS):
                printable_files.append(name)
    return {
        "file_formats": ";".join(sorted(formats)),
        "source_file_count": str(len(source_files)),
        "printable_file_count": str(len(printable_files)),
        "has_step": "yes" if any(x.lower().endswith((".step", ".stp")) for x in source_files) else "no",
        "has_parametric_source": "yes" if source_files else "no",
        "file_notes": f"{len(source_files)} editable/source files; {len(printable_files)} printable mesh files; {total} total files",
    }

def manual_search_rows(target: Target, sources: Iterable[str]) -> list[dict]:
    q = quote_plus(target.target_item + " STL 3D print")
    mapping = {
        "printables": f"https://www.printables.com/search/models?q={q}",
        "github": f"https://github.com/search?q={quote_plus(target.target_item + ' stl 3mf step')}&type=code",
        "thangs": f"https://thangs.com/search/{q}?scope=all",
        "makerworld": f"https://makerworld.com/en/search/models?keyword={q}",
    }
    out = []
    for src in sources:
        if src not in mapping:
            continue
        out.append({
            "candidate_id": make_id(src, target.category, target.target_item),
            "status": "manual_search",
            "category": target.category,
            "target_item": target.target_item,
            "priority": target.priority,
            "source": src,
            "score": 0,
            "title": f"Manual search: {target.target_item} on {src}",
            "url": mapping[src],
            "thing_id": "",
            "license": "",
            "creator": "",
            "like_count": "",
            "make_count": "",
            "snippet": target.notes,
            "why_matched": "manual-search-link-only; do not approve until page/files/license are checked",
            "folder_slug": slug(target.target_item),
            "file_formats": "manual", "source_file_count": "", "printable_file_count": "",
            "has_step": "unknown", "has_parametric_source": "unknown", "file_notes": "manual search row; check page yourself",
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--thingiverse-token", default="", help="Thingiverse API token. Required for real Thingiverse candidates.")
    ap.add_argument("--sources", default="thingiverse,printables,github", help="Comma list: thingiverse,printables,github,thangs,makerworld")
    ap.add_argument("--per-target", type=int, default=8)
    ap.add_argument("--min-score", type=int, default=6)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--no-expand", action="store_true", help="Do not split slash/comma compound target rows")
    ap.add_argument("--manual-only", action="store_true", help="Only write manual search links; no API calls")
    ap.add_argument("--check-files", action="store_true", help="For Thingiverse candidates, call the files endpoint and record STL/3MF/STEP/SCAD availability")
    ap.add_argument("--prefer-step", action="store_true", help="When --check-files is used, boost candidates that include STEP/STP/SCAD/F3D/FCStd source files")
    args = ap.parse_args()

    sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    targets = read_targets(args.targets, expand=not args.no_expand)
    rows: list[dict] = []
    seen = set()

    for target in tqdm(targets, desc="targets"):
        # Real API-backed Thingiverse candidates
        if "thingiverse" in sources and args.thingiverse_token and not args.manual_only:
            found = []
            for term in [target.target_item, target.target_item.replace("/", " ")]:
                found.extend(thingiverse_search(term, args.thingiverse_token, per_page=args.per_target))
                time.sleep(args.sleep)
            for raw in found:
                tv = normalize_tv_item(raw)
                if not tv:
                    continue
                key = (target.category, target.target_item, tv["url"])
                if key in seen:
                    continue
                seen.add(key)
                score, reason = score_title(target, tv["title"], tv["snippet"])
                file_summary = {
                    "file_formats": "", "source_file_count": "", "printable_file_count": "",
                    "has_step": "unknown", "has_parametric_source": "unknown", "file_notes": "not checked"
                }
                if args.check_files:
                    file_summary = thingiverse_file_summary(tv["thing_id"], args.thingiverse_token)
                    if int(file_summary.get("printable_file_count") or 0) > 0:
                        score += 4
                        reason += "; has-printable-files"
                    if args.prefer_step and file_summary.get("has_step") == "yes":
                        score += 10
                        reason += "; has-step-source"
                    elif args.prefer_step and file_summary.get("has_parametric_source") == "yes":
                        score += 6
                        reason += "; has-editable-source"
                if score < args.min_score:
                    continue
                row = {
                    "candidate_id": make_id("thingiverse", tv["thing_id"], target.target_item),
                    "status": "candidate",
                    "category": target.category,
                    "target_item": target.target_item,
                    "priority": target.priority,
                    "source": "thingiverse",
                    "score": score,
                    "title": tv["title"],
                    "url": tv["url"],
                    "thing_id": tv["thing_id"],
                    "license": tv["license"],
                    "creator": tv["creator"],
                    "like_count": tv["like_count"],
                    "make_count": tv["make_count"],
                    "snippet": tv["snippet"],
                    "why_matched": reason,
                    "folder_slug": slug(tv["title"]),
                }
                row.update(file_summary)
                rows.append(row)

        # Manual search links for sources where API/download is not reliable.
        manual_sources = [s for s in sources if s != "thingiverse"]
        rows.extend(manual_search_rows(target, manual_sources))

    # Sort useful candidates first, manual links last.
    rows.sort(key=lambda r: (r["status"] == "manual_search", r["category"], r["target_item"], -int(r.get("score") or 0)))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "candidate_id", "status", "category", "target_item", "priority", "source", "score",
        "title", "url", "thing_id", "license", "creator", "like_count", "make_count",
        "snippet", "why_matched", "folder_slug",
        "file_formats", "source_file_count", "printable_file_count", "has_step", "has_parametric_source", "file_notes",
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.out}")
    print("candidate = API/search result to review; manual_search = search page only, not a model")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
