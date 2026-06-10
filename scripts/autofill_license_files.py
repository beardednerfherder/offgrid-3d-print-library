#!/usr/bin/env python3
import csv
import re
from pathlib import Path
from datetime import date
from difflib import SequenceMatcher

MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d"}
ROOT = Path("models")
MANIFESTS = Path("manifests")

def norm(s):
    s = (s or "").lower()
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())

def similarity(a, b):
    a = norm(a)
    b = norm(b)
    if not a or not b:
        return 0
    return SequenceMatcher(None, a, b).ratio()

def model_folder_for_file(path: Path) -> Path:
    parts = list(path.parts)
    if "files" in parts:
        return Path(*parts[:parts.index("files")])
    return path.parent

def read_manifest_rows():
    rows = []
    if not MANIFESTS.exists():
        return rows

    for csv_path in MANIFESTS.rglob("*.csv"):
        try:
            with csv_path.open(newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["_manifest_file"] = str(csv_path)
                    rows.append(row)
        except Exception as e:
            print(f"WARNING: could not read {csv_path}: {e}")

    return rows

def get_first(row, keys):
    for k in keys:
        if k in row and str(row[k]).strip():
            return str(row[k]).strip()
    return ""

def extract_url(row):
    for k in [
        "url", "page_url", "source_url", "download_url", "model_url",
        "thingiverse_url", "printables_url", "github_url"
    ]:
        v = get_first(row, [k])
        if v.startswith("http"):
            return v

    joined = " ".join(str(v) for v in row.values())
    m = re.search(r"https?://[^\s,\"']+", joined)
    return m.group(0) if m else ""

def infer_license_label(text):
    t = (text or "").lower()

    if not t:
        return "UNKNOWN / NEEDS REVIEW"

    if "cc0" in t or "public domain" in t:
        return "CC0 / Public Domain"

    if "by-nc-nd" in t or ("noncommercial" in t and "no derivatives" in t):
        return "CC BY-NC-ND"

    if "by-nc-sa" in t:
        return "CC BY-NC-SA"

    if "by-nc" in t or "noncommercial" in t:
        return "CC BY-NC"

    if "by-sa" in t:
        return "CC BY-SA"

    if "cc-by" in t or "creative commons attribution" in t:
        return "CC BY"

    if "mit" in t:
        return "MIT"

    if "apache" in t:
        return "Apache"

    if "bsd" in t:
        return "BSD"

    if "all rights reserved" in t:
        return "All Rights Reserved"

    return text.strip()

def classify_permissions(license_label):
    l = (license_label or "").lower()

    if "unknown" in l or "needs review" in l:
        return {
            "redistribution": "UNKNOWN / NEEDS REVIEW",
            "commercial": "UNKNOWN / NEEDS REVIEW",
            "remix": "UNKNOWN / NEEDS REVIEW",
            "summary": "License has not been confirmed. Treat as personal/private use only until reviewed.",
        }

    if "cc0" in l or "public domain" in l:
        return {
            "redistribution": "Yes",
            "commercial": "Yes",
            "remix": "Yes",
            "summary": "Generally open for redistribution, commercial use, and remixing.",
        }

    if "by-nc-nd" in l:
        return {
            "redistribution": "Yes, with attribution, non-commercial, unmodified only",
            "commercial": "No",
            "remix": "No redistributed derivatives",
            "summary": "Can generally be shared with attribution for non-commercial use only, but modified/remixed versions should not be redistributed.",
        }

    if "by-nc-sa" in l:
        return {
            "redistribution": "Yes, with attribution, non-commercial, share-alike",
            "commercial": "No",
            "remix": "Yes, non-commercial, share-alike",
            "summary": "Can generally be shared/remixed with attribution for non-commercial use, under similar license terms.",
        }

    if "by-nc" in l:
        return {
            "redistribution": "Yes, with attribution, non-commercial",
            "commercial": "No",
            "remix": "Usually yes, non-commercial, with attribution",
            "summary": "Can generally be shared/remixed with attribution for non-commercial use only.",
        }

    if "by-sa" in l:
        return {
            "redistribution": "Yes, with attribution, share-alike",
            "commercial": "Usually yes",
            "remix": "Yes, share-alike",
            "summary": "Can generally be shared/remixed with attribution, but derivatives should use compatible share-alike terms.",
        }

    if "cc by" in l or "cc-by" in l:
        return {
            "redistribution": "Yes, with attribution",
            "commercial": "Usually yes",
            "remix": "Usually yes, with attribution",
            "summary": "Can generally be shared/remixed with attribution.",
        }

    if any(x in l for x in ["mit", "apache", "bsd"]):
        return {
            "redistribution": "Usually yes",
            "commercial": "Usually yes",
            "remix": "Usually yes",
            "summary": "Permissive software-style license. Still verify the original terms.",
        }

    if "all rights reserved" in l:
        return {
            "redistribution": "No / needs explicit permission",
            "commercial": "No / needs explicit permission",
            "remix": "No / needs explicit permission",
            "summary": "Do not redistribute or remix without permission.",
        }

    return {
        "redistribution": "UNKNOWN / NEEDS REVIEW",
        "commercial": "UNKNOWN / NEEDS REVIEW",
        "remix": "UNKNOWN / NEEDS REVIEW",
        "summary": "License text was found but could not be confidently classified.",
    }

def row_search_text(row):
    keys = [
        "name", "title", "model_name", "target", "query", "description",
        "page_url", "url", "source_url", "thing_id", "id", "category", "category_name"
    ]
    return " ".join(get_first(row, [k]) for k in keys)

def find_best_row(model_dir, files, rows):
    folder_text = " ".join([
        str(model_dir),
        model_dir.name,
        " ".join(f.name for f in files),
    ])

    best = None
    best_score = 0

    for row in rows:
        text = row_search_text(row)
        score = similarity(folder_text, text)

        # Small boosts for exact-ish folder/file name matches
        folder_norm = norm(model_dir.name)
        text_norm = norm(text)
        if folder_norm and folder_norm in text_norm:
            score += 0.25

        for f in files:
            stem = norm(f.stem)
            if stem and stem in text_norm:
                score += 0.15

        if score > best_score:
            best = row
            best_score = score

    if best_score < 0.35:
        return None, best_score

    return best, best_score

def main():
    if not ROOT.exists():
        raise SystemExit("No models/ folder found")

    rows = read_manifest_rows()
    print(f"Loaded manifest rows: {len(rows)}")

    model_files = []
    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix.lower() in MODEL_EXTS:
            model_files.append(f)

    model_dirs = {}
    for f in model_files:
        d = model_folder_for_file(f)
        model_dirs.setdefault(d, []).append(f)

    created = 0
    updated = 0
    unknown = 0

    for d, files in sorted(model_dirs.items()):
        best, score = find_best_row(d, files, rows)

        model_name = d.name.replace("_", " ").replace("-", " ").title()
        source_url = ""
        creator = ""
        license_raw = ""
        source_site = ""
        manifest_file = ""
        matched_title = ""

        if best:
            matched_title = get_first(best, ["title", "name", "model_name", "target", "query"])
            model_name = matched_title or model_name
            source_url = extract_url(best)
            creator = get_first(best, ["creator", "author", "username", "user", "maker"])
            license_raw = get_first(best, ["license", "license_name", "detected_license", "original_license"])
            source_site = get_first(best, ["source_site", "source", "site", "source_type"])
            manifest_file = best.get("_manifest_file", "")
        else:
            unknown += 1

        license_label = infer_license_label(license_raw)
        perms = classify_permissions(license_label)

        file_list = "\n".join(f"- `{str(f.relative_to(d))}`" for f in sorted(files))

        content = f"""# License / Attribution

## Model

**Name:** {model_name}

**Model folder:** `{d}`

## Files Covered

{file_list}

## Source

**Source site:** {source_site or "UNKNOWN / NEEDS REVIEW"}

**Original URL:** {source_url or "UNKNOWN / NEEDS REVIEW"}

**Creator / author:** {creator or "UNKNOWN / NEEDS REVIEW"}

**Matched manifest:** {manifest_file or "No manifest match found"}

**Manifest match confidence:** {score:.2f}

## License

**Detected license:** {license_label}

**Original license text:** {license_raw or "UNKNOWN / NEEDS REVIEW"}

## Permission Summary

**Redistribution:** {perms["redistribution"]}

**Commercial use:** {perms["commercial"]}

**Remix / modified redistribution:** {perms["remix"]}

**Plain-English note:** {perms["summary"]}

## Review Status

**Status:** {"AUTO-FILLED / NEEDS HUMAN REVIEW" if best else "UNKNOWN / NEEDS HUMAN REVIEW"}

This file was generated automatically from available local manifest data and file/folder names.

Do not treat this as legal advice or final license verification. Before selling prints, redistributing files, remixing models, or uploading elsewhere, verify the license from the original source page.

## Notes

Added / updated date: {date.today().isoformat()}
"""

        lic = d / "LICENSE.md"
        if lic.exists():
            updated += 1
        else:
            created += 1

        lic.write_text(content, encoding="utf-8")

    print(f"Model folders found: {len(model_dirs)}")
    print(f"LICENSE.md created: {created}")
    print(f"LICENSE.md updated: {updated}")
    print(f"No confident manifest match: {unknown}")
    print()
    print("Next:")
    print("  find models -name LICENSE.md | wc -l")
    print("  git diff -- models | less")
    print("  python3 scripts/check_repo.py")

if __name__ == "__main__":
    main()
