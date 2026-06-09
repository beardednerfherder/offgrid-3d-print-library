#!/usr/bin/env python3
"""
download_manifest.py  - Download STL files listed in manifests/models.csv

Usage:
    python3 scripts/download_manifest.py
    python3 scripts/download_manifest.py --category 6
    python3 scripts/download_manifest.py --csv manifests/models.csv --output models/

Rows with an empty download_url will be skipped with a note of the page_url to
visit manually.
"""

import csv, os, sys, time, argparse, urllib.request, urllib.error


def download_models(csv_path="manifests/models.csv",
                    output_base="models/",
                    category=None,
                    dry_run=False):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        models = list(reader)

    downloaded = skipped = failed = 0

    for model in models:
        cat = model.get("category_num", "").strip()
        if category is not None and cat != str(category).zfill(2):
            continue

        name      = model.get("name", "unknown")
        url       = model.get("download_url", "").strip()
        page      = model.get("page_url", "").strip()
        folder_hint = model.get("local_path", "").strip()

        if not url:
            page_note = f" -> visit: {page}" if page else ""
            print(f"  [SKIP] {name} — no download_url{page_note}")
            skipped += 1
            continue

        # Build output folder
        cat_name = model.get("category_name", cat)
        folder_key = f"{cat.zfill(2)}_{cat_name}"
        # Find matching models/ subfolder
        folder = output_base
        for d in os.listdir(output_base):
            if d.startswith(cat.zfill(2) + "_"):
                folder = os.path.join(output_base, d)
                break

        os.makedirs(folder, exist_ok=True)

        raw_name = url.split("/")[-1].split("?")[0]
        filename = raw_name if raw_name.lower().endswith(".stl") else                    model.get("id", "model") + "_" + name.replace(" ", "_") + ".stl"
        out_path = os.path.join(folder, filename)

        if os.path.exists(out_path):
            print(f"  [EXISTS] {filename}")
            skipped += 1
            continue

        if dry_run:
            print(f"  [DRY-RUN] Would download: {name} -> {out_path}")
            continue

        print(f"  [GET] {name}")
        print(f"        {url}")
        print(f"        -> {out_path}")
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 offgrid-3dp-library/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            with open(out_path, "wb") as fout:
                fout.write(data)
            print(f"        OK ({len(data)//1024} KB)")
            downloaded += 1
            time.sleep(0.75)  # polite delay
        except urllib.error.HTTPError as e:
            print(f"        FAIL HTTP {e.code}: {e.reason}")
            failed += 1
        except Exception as e:
            print(f"        FAIL: {e}")
            failed += 1

    print(f"\nDone: {downloaded} downloaded, {skipped} skipped, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Download models from manifest CSV")
    p.add_argument("--csv",      default="manifests/models.csv",  help="Path to CSV")
    p.add_argument("--output",   default="models/",               help="Output base dir")
    p.add_argument("--category", type=int, default=None,           help="Filter to category N")
    p.add_argument("--dry-run",  action="store_true",              help="List what would be done")
    args = p.parse_args()
    ok = download_models(args.csv, args.output, args.category, args.dry_run)
    sys.exit(0 if ok else 1)
