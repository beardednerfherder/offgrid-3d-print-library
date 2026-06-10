#!/usr/bin/env python3
from pathlib import Path
from datetime import date

MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d"}
ROOT = Path("models")

def model_folder_for_file(path: Path) -> Path:
    parts = list(path.parts)
    if "files" in parts:
        return Path(*parts[:parts.index("files")])
    return path.parent

if not ROOT.exists():
    raise SystemExit("No models/ folder found")

model_dirs = set()

for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix.lower() in MODEL_EXTS:
        model_dirs.add(model_folder_for_file(f))

created = 0
skipped = 0

for d in sorted(model_dirs):
    lic = d / "LICENSE.md"

    if lic.exists():
        skipped += 1
        continue

    files = []
    for f in sorted(d.rglob("*")):
        if f.is_file() and f.suffix.lower() in MODEL_EXTS:
            files.append(str(f.relative_to(d)))

    file_list = "\n".join(f"- `{x}`" for x in files) if files else "- No model files found"

    content = f"""# License / Attribution

## Model Folder

`{d}`

## Files Covered

{file_list}

## License Status

**NEEDS REVIEW**

The license for this model has not yet been confirmed.

Until confirmed, treat this model as:

- Personal / private use only.
- Not approved for commercial use.
- Not approved for redistribution outside this repository.
- Not approved for remixing or modified redistribution.

## Source / Attribution

Original source URL:

Creator / author:

Original license:

License URL:

Downloaded / added date: {date.today().isoformat()}

## Notes

Add any source, creator, license, remix, or print notes here.

If this model is confirmed to be original work created specifically for this repository, update this file to say so and mark the license as CC0 or the chosen project license.

If this model came from a community model site, check the original model page before selling prints, redistributing files, modifying/remixing, or uploading elsewhere.
"""

    lic.write_text(content, encoding="utf-8")
    created += 1

print(f"Created LICENSE.md files: {created}")
print(f"Skipped existing LICENSE.md files: {skipped}")
