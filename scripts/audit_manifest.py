#!/usr/bin/env python3
"""
audit_manifest.py  - Validate models.csv entries and check local STL presence

Usage:
    python3 scripts/audit_manifest.py
    python3 scripts/audit_manifest.py --csv manifests/models.csv --models models/
"""

import csv, os, sys, argparse, urllib.request, urllib.error

REQUIRED   = ["id", "category_num", "name", "description",
              "material_rec", "source_license", "source_site"]
VALID_LICS = {"CC0", "CC BY", "CC BY-SA", "CC BY-NC", "CC BY-NC-SA", "MIT", "GPL"}
VALID_MATS = {"PLA", "PETG", "ABS", "ASA", "TPU", "NYLON", "PC",
              "PETG or ASA", "ASA or ABS"}


def check_url(url, timeout=5):
    """Return (bool, status_code). True = reachable."""
    try:
        req = urllib.request.Request(url, method="HEAD",
              headers={"User-Agent": "Mozilla/5.0 audit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, r.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception:
        return False, 0


def audit(csv_path="manifests/models.csv",
          models_base="models/",
          check_urls=False):
    errors, warnings = [], []

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"ERROR: CSV not found at {csv_path}")
        return False

    ids_seen = set()

    for i, row in enumerate(rows, 1):
        rid   = row.get("id", "").strip()
        rname = row.get("name", "")

        for field in REQUIRED:
            if not row.get(field, "").strip():
                errors.append(f"Row {i} [{rid}]: missing required field '{field}'")

        if rid in ids_seen:
            errors.append(f"Row {i}: duplicate ID '{rid}'")
        ids_seen.add(rid)

        lic = row.get("source_license", "")
        if lic not in VALID_LICS:
            warnings.append(f"Row {i} [{rid}]: unrecognised license '{lic}'")

        mat = row.get("material_rec", "")
        if mat not in VALID_MATS:
            warnings.append(f"Row {i} [{rid}]: unusual material '{mat}'")

        local = row.get("local_path", "").strip()
        if local:
            full = os.path.join(models_base, local)
            if not os.path.exists(full):
                warnings.append(f"Row {i} [{rid}]: local_path not on disk: {full}")

        infill = row.get("infill_pct", "").strip()
        if infill:
            try:
                v = int(infill)
                if v < 10 or v > 100:
                    warnings.append(f"Row {i} [{rid}]: infill_pct {v} outside 10-100")
            except ValueError:
                warnings.append(f"Row {i} [{rid}]: infill_pct not an integer: {infill}")

        if check_urls:
            for url_field in ("page_url", "download_url"):
                url = row.get(url_field, "").strip()
                if url and not url.startswith("https://www.printables.com/model/search"):
                    ok, code = check_url(url)
                    if not ok:
                        warnings.append(f"Row {i} [{rid}]: {url_field} returned {code}: {url}")

    # Summary
    print(f"Audited {len(rows)} models — {len(errors)} errors, {len(warnings)} warnings")
    for e in errors:   print(f"  ERROR: {e}")
    for w in warnings: print(f"   WARN: {w}")
    return len(errors) == 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Validate models.csv")
    p.add_argument("--csv",    default="manifests/models.csv", help="CSV path")
    p.add_argument("--models", default="models/",              help="Models base dir")
    p.add_argument("--check-urls", action="store_true",        help="HTTP-check all URLs")
    args = p.parse_args()
    ok = audit(args.csv, args.models, args.check_urls)
    sys.exit(0 if ok else 1)
