#!/usr/bin/env python3
import csv
import re
import json
from pathlib import Path
from datetime import date
from difflib import SequenceMatcher
from urllib.parse import urlparse

MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d"}
ROOT = Path("models")
MANIFESTS = Path("manifests")

def norm(s):
    s = str(s or "").lower()
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())

def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def model_folder_for_file(path):
    parts = list(path.parts)
    if "files" in parts:
        return Path(*parts[:parts.index("files")])
    return path.parent

def first(row, names):
    for n in names:
        if n in row and str(row[n]).strip():
            return str(row[n]).strip()
    return ""

def extract_any_url(row):
    preferred = [
        "original_url", "url", "page_url", "source_url", "model_url",
        "download_url", "thingiverse_url", "printables_url", "github_url"
    ]
    for k in preferred:
        v = first(row, [k])
        if v.startswith("http"):
            return v

    blob = json.dumps(row, ensure_ascii=False)
    m = re.search(r"https?://[^\s,\"')\]]+", blob)
    return m.group(0) if m else ""

def source_site_from_url(url):
    host = urlparse(url or "").netloc.lower()
    if "thingiverse" in host:
        return "thingiverse"
    if "printables" in host:
        return "printables"
    if "github" in host:
        return "github"
    if "makerworld" in host:
        return "makerworld"
    if "cults3d" in host:
        return "cults3d"
    return host or ""

def normalize_license(s):
    s = str(s or "").strip()
    low = s.lower()

    if not s:
        return "UNKNOWN / NEEDS REVIEW"

    if "cc0" in low or "public domain" in low:
        return "CC0 / Public Domain"
    if "attribution - non-commercial - no derivatives" in low:
        return "CC BY-NC-ND 4.0"
    if "by-nc-nd" in low:
        return "CC BY-NC-ND"
    if "attribution - non-commercial - share alike" in low:
        return "CC BY-NC-SA"
    if "by-nc-sa" in low:
        return "CC BY-NC-SA"
    if "attribution - non-commercial" in low:
        return "CC BY-NC"
    if "by-nc" in low:
        return "CC BY-NC"
    if "attribution - share alike" in low:
        return "CC BY-SA"
    if "by-sa" in low:
        return "CC BY-SA"
    if "creative commons - attribution" in low or "creative commons attribution" in low:
        return "CC BY"
    if "cc-by" in low or "cc by" in low:
        return "CC BY"
    if "gnu - gpl" in low or low == "gpl" or "gnu general public" in low:
        return "GPL"
    if "mit" in low:
        return "MIT"
    if "apache" in low:
        return "Apache"
    if "bsd" in low:
        return "BSD"
    if "all rights reserved" in low:
        return "All Rights Reserved"

    return s

def permission_summary(lic):
    l = lic.lower()

    if "unknown" in l or "needs review" in l:
        return (
            "UNKNOWN / NEEDS REVIEW",
            "UNKNOWN / NEEDS REVIEW",
            "UNKNOWN / NEEDS REVIEW",
            "License has not been confirmed. Treat as personal/private use only until reviewed."
        )

    if "cc0" in l or "public domain" in l:
        return ("Yes", "Yes", "Yes", "Generally open for redistribution, commercial use, and remixing.")

    if "by-nc-nd" in l:
        return (
            "Yes, with attribution, non-commercial, unmodified only",
            "No",
            "No redistributed derivatives",
            "Attribution required. Non-commercial only. Do not redistribute modified/remixed versions."
        )

    if "by-nc-sa" in l:
        return (
            "Yes, with attribution, non-commercial, share-alike",
            "No",
            "Yes, non-commercial, share-alike",
            "Attribution required. Non-commercial only. Remixes should use compatible share-alike terms."
        )

    if "by-nc" in l:
        return (
            "Yes, with attribution, non-commercial",
            "No",
            "Usually yes, non-commercial, with attribution",
            "Attribution required. Non-commercial use only."
        )

    if "by-sa" in l:
        return (
            "Yes, with attribution, share-alike",
            "Usually yes",
            "Yes, share-alike",
            "Attribution required. Share-alike terms may apply."
        )

    if "cc by" in l or "cc-by" in l:
        return (
            "Yes, with attribution",
            "Usually yes",
            "Usually yes, with attribution",
            "Attribution required. Commercial use and remixing are usually allowed, but verify original terms."
        )

    if "gpl" in l:
        return (
            "Yes, under GPL terms",
            "Usually yes, under GPL terms",
            "Yes, under GPL terms",
            "GPL terms apply. Keep license notices and share source/derivatives as required."
        )

    if any(x in l for x in ["mit", "apache", "bsd"]):
        return (
            "Usually yes",
            "Usually yes",
            "Usually yes",
            "Permissive license. Keep attribution/license notice where required."
        )

    if "all rights reserved" in l:
        return (
            "No / needs explicit permission",
            "No / needs explicit permission",
            "No / needs explicit permission",
            "Do not redistribute or remix without permission."
        )

    return (
        "UNKNOWN / NEEDS REVIEW",
        "UNKNOWN / NEEDS REVIEW",
        "UNKNOWN / NEEDS REVIEW",
        "License text found, but not confidently classified. Verify manually."
    )

def load_all_csv_rows():
    rows = []
    if not MANIFESTS.exists():
        return rows

    for path in MANIFESTS.rglob("*.csv"):
        try:
            with path.open(newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["_csv_file"] = str(path)
                    rows.append(row)
        except Exception as e:
            print(f"WARNING: could not read {path}: {e}")

    return rows

def row_text(row):
    keys = [
        "model_folder", "folder", "path", "local_path", "files", "filename",
        "file", "model_name", "name", "title", "target", "query",
        "description", "page_title_or_repo", "source_site", "source_type",
        "url", "page_url", "source_url", "original_url", "thing_id"
    ]
    return " ".join(first(row, [k]) for k in keys) + " " + json.dumps(row, ensure_ascii=False)

def best_match_for_model(model_dir, files, rows):
    folder_blob = " ".join([
        str(model_dir),
        model_dir.name,
        " ".join(f.name for f in files),
        " ".join(f.stem for f in files),
    ])

    best = None
    best_score = 0.0

    folder_norm = norm(model_dir.name)
    file_stems = [norm(f.stem) for f in files]

    for row in rows:
        rt = row_text(row)
        score = sim(folder_blob, rt)

        rt_norm = norm(rt)

        # Exact or near-exact folder name boost
        if folder_norm and folder_norm in rt_norm:
            score += 0.45

        # File stem boost
        for stem in file_stems:
            if stem and stem in rt_norm:
                score += 0.35

        # URL/source rows with useful license info are preferred
        if first(row, ["license", "detected_license", "original_license", "license_name"]):
            score += 0.08

        if extract_any_url(row):
            score += 0.05

        if score > best_score:
            best = row
            best_score = score

    return best, best_score

def main():
    if not ROOT.exists():
        raise SystemExit("No models/ folder found")

    rows = load_all_csv_rows()
    print(f"Loaded CSV rows: {len(rows)}")

    model_dirs = {}

    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix.lower() in MODEL_EXTS:
            d = model_folder_for_file(f)
            model_dirs.setdefault(d, []).append(f)

    print(f"Model folders with printable/CAD files: {len(model_dirs)}")

    report_rows = []
    created_or_updated = 0
    low_conf = 0

    for d, files in sorted(model_dirs.items()):
        match, score = best_match_for_model(d, files, rows)

        model_name = d.name.replace("_", " ").replace("-", " ").title()
        source_site = "UNKNOWN / NEEDS REVIEW"
        original_url = "UNKNOWN / NEEDS REVIEW"
        creator = "UNKNOWN / NEEDS REVIEW"
        license_raw = "UNKNOWN / NEEDS REVIEW"
        matched_csv = "No CSV match found"

        if match and score >= 0.35:
            matched_csv = match.get("_csv_file", "unknown csv")
            model_name = first(match, ["model_name", "name", "title", "target", "query", "page_title_or_repo"]) or model_name
            original_url = extract_any_url(match) or original_url
            source_site = first(match, ["source_site", "source", "site", "source_type"]) or source_site
            if source_site == "UNKNOWN / NEEDS REVIEW" and original_url != "UNKNOWN / NEEDS REVIEW":
                source_site = source_site_from_url(original_url) or source_site
            creator = first(match, ["creator", "author", "username", "user", "maker"]) or creator
            license_raw = first(match, ["license", "detected_license", "original_license", "license_name"]) or license_raw
        else:
            low_conf += 1

        lic = normalize_license(license_raw)
        redistribution, commercial, remix, note = permission_summary(lic)

        file_list = "\n".join(f"- `{str(f.relative_to(d))}`" for f in sorted(files))

        content = f"""# License / Attribution

## Model

**Name:** {model_name}

**Model folder:** `{d}`

## Files Covered

{file_list}

## Source

**Source site:** {source_site}

**Original URL:** {original_url}

**Creator / author:** {creator}

**Matched data file:** {matched_csv}

**Match confidence:** {score:.2f}

## License

**License:** {lic}

**Original license text:** {license_raw}

## Permission Summary

**Redistribution:** {redistribution}

**Commercial use:** {commercial}

**Remix / modified redistribution:** {remix}

**Plain-English note:** {note}

## Review Status

**Status:** {"AUTO-FILLED FROM EXISTING DATA" if score >= 0.35 else "UNKNOWN / NEEDS HUMAN REVIEW"}

This file was generated automatically from the repo's existing CSV/manifests and local model files.

This is not legal advice. Before selling prints, redistributing files outside this repo, remixing models, or uploading elsewhere, verify the license from the original source when possible.

## Notes

Updated: {date.today().isoformat()}
"""

        (d / "LICENSE.md").write_text(content, encoding="utf-8")
        created_or_updated += 1

        report_rows.append({
            "model_folder": str(d),
            "model_name": model_name,
            "file_count": len(files),
            "source_site": source_site,
            "original_url": original_url,
            "creator": creator,
            "license": lic,
            "matched_data_file": matched_csv,
            "match_confidence": f"{score:.2f}",
            "status": "AUTO-FILLED" if score >= 0.35 else "NEEDS REVIEW",
        })

    out = Path("license_fill_report.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        fields = [
            "model_folder", "model_name", "file_count", "source_site",
            "original_url", "creator", "license", "matched_data_file",
            "match_confidence", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"LICENSE.md files written: {created_or_updated}")
    print(f"Low/no confidence matches: {low_conf}")
    print(f"Wrote report: {out}")
    print()
    print("Open report with:")
    print("  libreoffice license_fill_report.csv")
    print()
    print("Find unresolved files with:")
    print("  grep -R \"UNKNOWN / NEEDS\" models --include='LICENSE.md' | head -50")

if __name__ == "__main__":
    main()
