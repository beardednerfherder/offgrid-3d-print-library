#!/usr/bin/env python3
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("Missing Python package: requests\nInstall with: python3 -m pip install requests")

ROOT = Path("models")
IMPORT_LOG = Path("metadata/import_log.csv")

MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d", ".obj", ".zip"}

DEFAULT_CATEGORIES = [
    "01_Water_Hose_Irrigation",
    "02_PEX_Tubing_NonPressure",
    "03_Garden_Greenhouse",
    "04_Buckets_Barrels_Storage",
    "05_Workshop_Repair_Hardware",
    "06_Electrical_Solar_LowVoltage",
    "07_Chicken_Coop_Livestock",
    "08_Vehicle_Trailer_Utility",
    "09_Radio_Comms_Sensors",
    "10_Parametric_Source_Files",
    "99_Calibration_Test_Prints",
]

def run(cmd, check=False):
    return subprocess.run(cmd, check=check)

def open_path(path):
    try:
        subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass

def open_url(url):
    try:
        subprocess.run(["xdg-open", url], check=False)
    except Exception:
        pass

def ask_yes_no(prompt, default_yes=True):
    suffix = "[Y/n]" if default_yes else "[y/N]"
    answer = input(f"{prompt} {suffix}: ").strip().lower()

    if not answer:
        return default_yes

    return answer in {"y", "yes"}

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"https?://", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s[:90] or "new-model"

def title_to_category_words(name):
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9]+", " ", name)
    words = [w.capitalize() for w in name.split() if w.strip()]
    return "_".join(words) or "New_Category"

def clean_title_from_url(url):
    path = urlparse(url).path.strip("/")
    last = path.split("/")[-1] if path else "new-model"
    last = re.sub(r"^\d+-", "", last)
    return last.replace("-", " ").title()

def detect_site(url):
    host = urlparse(url).netloc.lower()

    if "printables.com" in host:
        return "printables"
    if "thingiverse.com" in host:
        return "thingiverse"
    if "makerworld.com" in host:
        return "makerworld"
    if "github.com" in host:
        return "github"

    return host or "unknown"

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0 offgrid-3d-print-library-importer"}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"WARNING: Could not fetch page metadata: {e}")
        return ""

def html_unescape_basic(s):
    return (
        s.replace("&amp;", "&")
         .replace("&quot;", '"')
         .replace("&#39;", "'")
         .replace("&lt;", "<")
         .replace("&gt;", ">")
    )

def extract_title(html, fallback):
    if not html:
        return fallback

    patterns = [
        r'<meta property="og:title" content="([^"]+)"',
        r'<meta name="twitter:title" content="([^"]+)"',
        r"<title>(.*?)</title>",
    ]

    for p in patterns:
        m = re.search(p, html, re.I | re.S)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            title = html_unescape_basic(title)
            title = title.replace(" | Printables.com", "")
            title = title.replace(" by Prusa Research", "")
            if title:
                return title

    return fallback

def extract_creator(html):
    if not html:
        return ""

    patterns = [
        r'"author"\s*:\s*{\s*"@type"\s*:\s*"Person"\s*,\s*"name"\s*:\s*"([^"]+)"',
        r'"author"\s*:\s*"([^"]+)"',
        r'"userName"\s*:\s*"([^"]+)"',
        r'"username"\s*:\s*"([^"]+)"',
        r'"displayName"\s*:\s*"([^"]+)"',
    ]

    for p in patterns:
        m = re.search(p, html, re.I | re.S)
        if m:
            return html_unescape_basic(m.group(1).strip())

    return ""

def extract_license(html):
    if not html:
        return ""

    haystack = html.replace("\\u002F", "/")
    low = haystack.lower()

    patterns = [
        "CC BY-NC-ND",
        "CC BY-NC-SA",
        "CC BY-NC",
        "CC BY-ND",
        "CC BY-SA",
        "CC BY",
        "CC0",
        "Creative Commons - Attribution - Non-Commercial - No Derivatives",
        "Creative Commons - Attribution - Non-Commercial - Share Alike",
        "Creative Commons - Attribution - Non-Commercial",
        "Creative Commons - Attribution - No Derivatives",
        "Creative Commons - Attribution - Share Alike",
        "Creative Commons - Attribution",
        "Public Domain",
        "All Rights Reserved",
    ]

    for lic in patterns:
        if lic.lower() in low:
            return lic

    return ""

def normalize_license(raw):
    l = (raw or "").lower()

    if not l:
        return "UNKNOWN / NEEDS REVIEW"

    if "cc0" in l or "public domain" in l:
        return "CC0 / Public Domain"

    if "all rights reserved" in l:
        return "All Rights Reserved"

    if "no derivatives" in l and "non-commercial" in l:
        return "CC BY-NC-ND"
    if "share alike" in l and "non-commercial" in l:
        return "CC BY-NC-SA"
    if "non-commercial" in l:
        return "CC BY-NC"
    if "no derivatives" in l:
        return "CC BY-ND"
    if "share alike" in l:
        return "CC BY-SA"
    if "attribution" in l:
        return "CC BY"

    if "by-nc-nd" in l:
        return "CC BY-NC-ND"
    if "by-nc-sa" in l:
        return "CC BY-NC-SA"
    if "by-nc" in l:
        return "CC BY-NC"
    if "by-nd" in l:
        return "CC BY-ND"
    if "by-sa" in l:
        return "CC BY-SA"
    if "cc by" in l or "cc-by" in l:
        return "CC BY"

    return raw or "UNKNOWN / NEEDS REVIEW"

def classify_license(license_name):
    l = (license_name or "").lower()

    if "unknown" in l or "needs review" in l:
        return {
            "class": "UNKNOWN",
            "redistribution": "UNKNOWN / NEEDS REVIEW",
            "commercial": "UNKNOWN / NEEDS REVIEW",
            "remix": "UNKNOWN / NEEDS REVIEW",
            "note": "License has not been confirmed. Treat as personal/private use only until reviewed.",
        }

    if "cc0" in l or "public domain" in l:
        return {
            "class": "OPEN",
            "redistribution": "Yes",
            "commercial": "Yes",
            "remix": "Yes",
            "note": "Open/public-domain style license. Redistribution, commercial use, and remixing are generally allowed.",
        }

    if "by-nc-nd" in l:
        return {
            "class": "RESTRICTED",
            "redistribution": "Yes, with attribution, non-commercial, unmodified only",
            "commercial": "No",
            "remix": "No redistributed derivatives",
            "note": "Attribution required. Non-commercial only. Do not redistribute modified/remixed versions.",
        }

    if "by-nc-sa" in l:
        return {
            "class": "RESTRICTED",
            "redistribution": "Yes, with attribution, non-commercial, share-alike",
            "commercial": "No",
            "remix": "Yes, non-commercial, share-alike",
            "note": "Attribution required. Non-commercial only. Share-alike terms apply.",
        }

    if "by-nc" in l:
        return {
            "class": "RESTRICTED",
            "redistribution": "Yes, with attribution, non-commercial",
            "commercial": "No",
            "remix": "Usually yes, non-commercial, with attribution",
            "note": "Attribution required. Commercial use is not allowed.",
        }

    if "by-nd" in l:
        return {
            "class": "RESTRICTED",
            "redistribution": "Yes, with attribution, unmodified only",
            "commercial": "Usually yes, unmodified only",
            "remix": "No redistributed derivatives",
            "note": "Attribution required. Modified versions should not be redistributed.",
        }

    if "by-sa" in l:
        return {
            "class": "OPEN",
            "redistribution": "Yes, with attribution, share-alike",
            "commercial": "Usually yes",
            "remix": "Yes, share-alike",
            "note": "Open Creative Commons license with attribution and share-alike requirements.",
        }

    if "cc by" in l or "cc-by" in l:
        return {
            "class": "OPEN",
            "redistribution": "Yes, with attribution",
            "commercial": "Usually yes",
            "remix": "Usually yes, with attribution",
            "note": "Open Creative Commons license. Attribution is required.",
        }

    if "all rights reserved" in l:
        return {
            "class": "RESTRICTED",
            "redistribution": "No / explicit permission required",
            "commercial": "No / explicit permission required",
            "remix": "No / explicit permission required",
            "note": "Do not redistribute, remix, or use commercially without permission.",
        }

    return {
        "class": "UNKNOWN",
        "redistribution": "UNKNOWN / NEEDS REVIEW",
        "commercial": "UNKNOWN / NEEDS REVIEW",
        "remix": "UNKNOWN / NEEDS REVIEW",
        "note": "License text was found but could not be confidently classified.",
    }

def existing_categories():
    categories = []

    if ROOT.exists():
        for p in ROOT.iterdir():
            if p.is_dir() and re.match(r"^\d{2}_", p.name):
                categories.append(p.name)

    for cat in DEFAULT_CATEGORIES:
        if cat not in categories:
            categories.append(cat)

    def sort_key(cat):
        m = re.match(r"^(\d{2})_", cat)
        return int(m.group(1)) if m else 999

    return sorted(categories, key=sort_key)

def next_category_number(categories):
    nums = []

    for cat in categories:
        m = re.match(r"^(\d{2})_", cat)
        if m:
            nums.append(int(m.group(1)))

    nums = [n for n in nums if n < 99]
    return max(nums, default=0) + 1

def make_category_folder_name(display_name, categories):
    number = next_category_number(categories)
    words = title_to_category_words(display_name)
    return f"{number:02d}_{words}"

def choose_category():
    categories = existing_categories()

    print()
    print("Choose a category:")
    print("  0. Create a new category folder")

    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")

    while True:
        choice = input("Category number: ").strip()

        if choice == "0":
            raw_name = input("New category name, example 'Craft Textile Tools': ").strip()

            if not raw_name:
                print("Category name cannot be blank.")
                continue

            new_cat = make_category_folder_name(raw_name, categories)
            print()
            print(f"New category will be: {new_cat}")

            if not ask_yes_no("Create this category?", True):
                continue

            (ROOT / new_cat).mkdir(parents=True, exist_ok=True)
            return new_cat

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            selected = categories[int(choice) - 1]
            (ROOT / selected).mkdir(parents=True, exist_ok=True)
            return selected

        print("Invalid choice.")

def list_model_files(files_dir):
    if not files_dir.exists():
        return []

    found = []

    for f in sorted(files_dir.rglob("*")):
        if f.is_file() and f.suffix.lower() in MODEL_EXTS:
            found.append(f)

    return found

def format_files_block(model_dir):
    files_dir = model_dir / "files"
    files = list_model_files(files_dir)

    if not files:
        return "- No printable/CAD files found in `files/`."

    return "\n".join(f"- `files/{f.relative_to(files_dir)}`" for f in files)

def write_license(model_dir, title, url, site, creator, license_raw):
    license_name = normalize_license(license_raw)
    info = classify_license(license_name)
    files_block = format_files_block(model_dir)

    content = f"""# License / Attribution

## Model

**Name:** {title}

**Model folder:** `{model_dir}`

## Files Covered

{files_block}

## Source

**Source site:** {site}

**Original URL:** {url}

**Creator / author:** {creator or "UNKNOWN / NEEDS REVIEW"}

## License

**License class:** {info["class"]}

**License:** {license_name}

**Original license text:** {license_raw or "UNKNOWN / NEEDS REVIEW"}

## Permission Summary

**Redistribution:** {info["redistribution"]}

**Commercial use:** {info["commercial"]}

**Remix / modified redistribution:** {info["remix"]}

**Plain-English note:** {info["note"]}

## Review Status

**Status:** {"OK" if info["class"] == "OPEN" else "REVIEW REQUIRED"}

This file was generated during import from the original model URL.

This is not legal advice. Before selling prints, redistributing files outside this repo, remixing models, or uploading elsewhere, verify the license from the original source when possible.

## Notes

Imported/updated: {date.today().isoformat()}
"""

    (model_dir / "LICENSE.md").write_text(content, encoding="utf-8")

def write_metadata(model_dir, data):
    (model_dir / "source.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

def append_import_log(data):
    IMPORT_LOG.parent.mkdir(parents=True, exist_ok=True)
    exists = IMPORT_LOG.exists()

    fields = [
        "date",
        "title",
        "url",
        "site",
        "creator",
        "license",
        "license_class",
        "model_folder",
    ]

    with IMPORT_LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)

        if not exists:
            writer.writeheader()

        writer.writerow({
            "date": date.today().isoformat(),
            "title": data["title"],
            "url": data["url"],
            "site": data["site"],
            "creator": data["creator"],
            "license": data["license"],
            "license_class": data["license_class"],
            "model_folder": data["model_folder"],
        })

def wait_for_files(files_dir):
    print()
    print("Download/copy the printable files into this folder:")
    print(f"  {files_dir}")
    print()
    print("The script will wait here. Press ENTER after the files are in place.")
    print("You can also type 'skip' to continue without files or 'cancel' to stop.")

    open_path(files_dir)

    while True:
        answer = input("Ready? ").strip().lower()

        if answer == "cancel":
            raise SystemExit("Cancelled.")

        if answer == "skip":
            return []

        files = list_model_files(files_dir)

        if files:
            print()
            print("Found files:")
            for f in files:
                size_mb = f.stat().st_size / 1024 / 1024
                print(f"  - {f.name} ({size_mb:.1f} MB)")

            if ask_yes_no("Use these files and update LICENSE.md?", True):
                return files

            print("Okay, add/remove files and press ENTER again.")
        else:
            print("No printable/CAD files found yet.")
            print("Expected file types:")
            print("  " + ", ".join(sorted(MODEL_EXTS)))
            if ask_yes_no("Open the folder again?", True):
                open_path(files_dir)

def maybe_run_existing_script(script_path):
    path = Path(script_path)
    if path.exists():
        subprocess.run(["python3", str(path)], check=False)

def git_has_changes():
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return bool(result.stdout.strip())

def git_commit_and_push():
    print()
    if not git_has_changes():
        print("No Git changes to commit.")
        return

    subprocess.run(["git", "status", "--short"], check=False)

    if not ask_yes_no("Commit these changes?", True):
        return

    msg = input("Commit message [Add printable model files]: ").strip() or "Add printable model files"

    subprocess.run(["git", "add", "models", "metadata", "scripts"], check=False)
    commit = subprocess.run(["git", "commit", "-m", msg], check=False)

    if commit.returncode != 0:
        print("Git commit did not complete. Check the message above.")
        return

    if ask_yes_no("Push to GitHub now?", True):
        subprocess.run(["git", "push"], check=False)

def import_one(url=None):
    if not url:
        url = input("Paste model URL: ").strip()

    if not url.startswith("http"):
        print("Please provide a full URL starting with http or https.")
        return False

    if not ROOT.exists():
        raise SystemExit("No models/ folder found.")

    site = detect_site(url)
    fallback_title = clean_title_from_url(url)

    print()
    print(f"Fetching metadata from: {url}")
    html = fetch_page(url)

    title = extract_title(html, fallback_title)
    creator = extract_creator(html)
    license_raw = extract_license(html)
    license_name = normalize_license(license_raw)
    license_info = classify_license(license_name)

    print()
    print("Detected:")
    print(f"  Title:         {title}")
    print(f"  Site:          {site}")
    print(f"  Creator:       {creator or 'UNKNOWN'}")
    print(f"  License:       {license_name}")
    print(f"  License class: {license_info['class']}")

    if not ask_yes_no("Continue with this model?", True):
        return False

    category = choose_category()

    default_slug = slugify(title)
    print()
    folder_name = input(f"Model folder name [{default_slug}]: ").strip() or default_slug
    folder_name = slugify(folder_name)

    model_dir = ROOT / category / folder_name
    files_dir = model_dir / "files"

    if model_dir.exists():
        print(f"WARNING: folder already exists: {model_dir}")
        if not ask_yes_no("Continue and update it?", False):
            return False

    files_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "title": title,
        "url": url,
        "site": site,
        "creator": creator or "UNKNOWN / NEEDS REVIEW",
        "license": license_name,
        "license_raw": license_raw or "UNKNOWN / NEEDS REVIEW",
        "license_class": license_info["class"],
        "model_folder": str(model_dir),
        "imported": date.today().isoformat(),
        "download_note": "Files were manually downloaded/copied into the files folder.",
    }

    write_metadata(model_dir, data)

    print()
    print("Created/updated:")
    print(f"  {model_dir}")
    print(f"  {files_dir}")
    print(f"  {model_dir / 'source.json'}")
    print()
    print("Opening model page and destination folder...")
    open_url(url)
    open_path(files_dir)

    wait_for_files(files_dir)

    write_license(model_dir, title, url, site, creator, license_raw)
    append_import_log(data)

    print()
    print("Updated:")
    print(f"  {model_dir / 'LICENSE.md'}")
    print(f"  {IMPORT_LOG}")

    # Run helper scripts if present
    maybe_run_existing_script("scripts/refresh_license_file_lists.py")
    maybe_run_existing_script("scripts/license_status_report.py")

    print()
    print("Import complete.")
    print(f"Model folder: {model_dir}")

    return True

def main():
    first_url = sys.argv[1].strip() if len(sys.argv) > 1 else None

    while True:
        imported = import_one(first_url)
        first_url = None

        print()
        if not ask_yes_no("Add another model?", False):
            break

    if ask_yes_no("Commit/push changes to GitHub automatically?", False):
        git_commit_and_push()

    print()
    print("Done.")

if __name__ == "__main__":
    main()
