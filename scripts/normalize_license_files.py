#!/usr/bin/env python3
from pathlib import Path
import re
from datetime import date

ROOT = Path("models")

def extract(label, text):
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.*)", text)
    return m.group(1).strip() if m else ""

def classify(license_text):
    l = (license_text or "").lower()

    if not l or "unknown" in l or "needs review" in l:
        return {
            "class": "UNKNOWN",
            "license": "UNKNOWN / NEEDS REVIEW",
            "redistribution": "UNKNOWN / NEEDS REVIEW",
            "commercial": "UNKNOWN / NEEDS REVIEW",
            "remix": "UNKNOWN / NEEDS REVIEW",
            "note": "License has not been confirmed. Treat as personal/private use only until reviewed.",
        }

    if "cc0" in l or "public domain" in l:
        return {
            "class": "OPEN",
            "license": "CC0 / Public Domain",
            "redistribution": "Yes",
            "commercial": "Yes",
            "remix": "Yes",
            "note": "Open/public-domain style license. Redistribution, commercial use, and remixing are generally allowed.",
        }

    if "cc by-nc-nd" in l or "by-nc-nd" in l or ("noncommercial" in l and "no derivatives" in l):
        return {
            "class": "RESTRICTED",
            "license": "CC BY-NC-ND",
            "redistribution": "Yes, with attribution, non-commercial, unmodified only",
            "commercial": "No",
            "remix": "No redistributed derivatives",
            "note": "Restricted Creative Commons license. Attribution required, non-commercial only, and modified versions should not be redistributed.",
        }

    if "cc by-nc-sa" in l or "by-nc-sa" in l:
        return {
            "class": "RESTRICTED",
            "license": "CC BY-NC-SA",
            "redistribution": "Yes, with attribution, non-commercial, share-alike",
            "commercial": "No",
            "remix": "Yes, non-commercial, share-alike",
            "note": "Restricted Creative Commons license. Attribution required, non-commercial only, and share-alike terms apply.",
        }

    if "cc by-nc" in l or "by-nc" in l or "noncommercial" in l:
        return {
            "class": "RESTRICTED",
            "license": "CC BY-NC",
            "redistribution": "Yes, with attribution, non-commercial",
            "commercial": "No",
            "remix": "Usually yes, non-commercial, with attribution",
            "note": "Restricted Creative Commons license. Attribution required and commercial use is not allowed.",
        }

    if "cc by-nd" in l or "by-nd" in l or "no derivatives" in l:
        return {
            "class": "RESTRICTED",
            "license": "CC BY-ND",
            "redistribution": "Yes, with attribution, unmodified only",
            "commercial": "Usually yes, unmodified only",
            "remix": "No redistributed derivatives",
            "note": "Restricted Creative Commons license. Modified versions should not be redistributed.",
        }

    if "cc by-sa" in l or "by-sa" in l:
        return {
            "class": "OPEN",
            "license": "CC BY-SA",
            "redistribution": "Yes, with attribution, share-alike",
            "commercial": "Usually yes",
            "remix": "Yes, share-alike",
            "note": "Open Creative Commons license with attribution and share-alike requirements.",
        }

    if "cc by" in l or "cc-by" in l or "creative commons attribution" in l:
        return {
            "class": "OPEN",
            "license": "CC BY",
            "redistribution": "Yes, with attribution",
            "commercial": "Usually yes",
            "remix": "Usually yes, with attribution",
            "note": "Open Creative Commons license. Attribution is required.",
        }

    if any(x in l for x in ["mit", "apache", "bsd", "gpl"]):
        return {
            "class": "OPEN",
            "license": license_text,
            "redistribution": "Usually yes, under license terms",
            "commercial": "Usually yes, under license terms",
            "remix": "Usually yes, under license terms",
            "note": "Open/permissive or free-software style license. Keep required notices and follow the original terms.",
        }

    if "all rights reserved" in l:
        return {
            "class": "RESTRICTED",
            "license": "All Rights Reserved",
            "redistribution": "No / explicit permission required",
            "commercial": "No / explicit permission required",
            "remix": "No / explicit permission required",
            "note": "Do not redistribute, remix, or use commercially without permission.",
        }

    return {
        "class": "UNKNOWN",
        "license": license_text,
        "redistribution": "UNKNOWN / NEEDS REVIEW",
        "commercial": "UNKNOWN / NEEDS REVIEW",
        "remix": "UNKNOWN / NEEDS REVIEW",
        "note": "License text was found but could not be confidently classified.",
    }

updated = 0
counts = {"OPEN": 0, "RESTRICTED": 0, "UNKNOWN": 0}

for path in sorted(ROOT.rglob("LICENSE.md")):
    text = path.read_text(encoding="utf-8", errors="ignore")

    name = extract("Name", text) or path.parent.name
    folder = extract("Model folder", text) or str(path.parent)
    source_site = extract("Source site", text) or "UNKNOWN / NEEDS REVIEW"
    original_url = extract("Original URL", text) or "UNKNOWN / NEEDS REVIEW"
    creator = extract("Creator / author", text) or "UNKNOWN / NEEDS REVIEW"
    matched_data = extract("Matched data file", text) or "UNKNOWN / NEEDS REVIEW"
    confidence = extract("Match confidence", text) or "UNKNOWN / NEEDS REVIEW"
    raw_license = extract("License", text) or extract("Original license text", text)

    # Preserve the file list block
    files_block = ""
    m = re.search(r"## Files Covered\n\n(.*?)\n\n## Source", text, re.S)
    if m:
        files_block = m.group(1).strip()
    else:
        files_block = "- Files not listed"

    info = classify(raw_license)
    counts[info["class"]] += 1

    new_text = f"""# License / Attribution

## Model

**Name:** {name}

**Model folder:** `{folder}`

## Files Covered

{files_block}

## Source

**Source site:** {source_site}

**Original URL:** {original_url}

**Creator / author:** {creator}

**Matched data file:** {matched_data}

**Match confidence:** {confidence}

## License

**License class:** {info["class"]}

**License:** {info["license"]}

**Original license text:** {raw_license or "UNKNOWN / NEEDS REVIEW"}

## Permission Summary

**Redistribution:** {info["redistribution"]}

**Commercial use:** {info["commercial"]}

**Remix / modified redistribution:** {info["remix"]}

**Plain-English note:** {info["note"]}

## Review Status

**Status:** {"OK" if info["class"] == "OPEN" else "REVIEW REQUIRED"}

This file was normalized automatically from existing license metadata.

This is not legal advice. Before selling prints, redistributing files outside this repo, remixing models, or uploading elsewhere, verify the license from the original source when possible.

## Notes

Normalized: {date.today().isoformat()}
"""

    path.write_text(new_text, encoding="utf-8")
    updated += 1

print(f"Updated LICENSE.md files: {updated}")
print(f"OPEN:       {counts['OPEN']}")
print(f"RESTRICTED: {counts['RESTRICTED']}")
print(f"UNKNOWN:    {counts['UNKNOWN']}")
