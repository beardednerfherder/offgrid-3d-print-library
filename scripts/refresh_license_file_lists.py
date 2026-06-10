#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path("models")
MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d", ".obj"}

updated = 0

for lic in sorted(ROOT.rglob("LICENSE.md")):
    model_dir = lic.parent
    files_dir = model_dir / "files"

    files = []
    if files_dir.exists():
        for f in sorted(files_dir.rglob("*")):
            if f.is_file() and f.suffix.lower() in MODEL_EXTS:
                files.append(f"- `files/{f.relative_to(files_dir)}`")

    files_block = "\n".join(files) if files else "- No printable/CAD files found in `files/`."

    text = lic.read_text(encoding="utf-8", errors="ignore")

    new_text = re.sub(
        r"## Files Covered\n\n.*?\n\n## Source",
        f"## Files Covered\n\n{files_block}\n\n## Source",
        text,
        flags=re.S,
    )

    if new_text != text:
        lic.write_text(new_text, encoding="utf-8")
        updated += 1

print(f"Updated file lists in LICENSE.md files: {updated}")
