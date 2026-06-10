#!/usr/bin/env python3
from pathlib import Path

MODEL_EXTS = {".stl", ".3mf", ".step", ".stp", ".scad", ".fcstd", ".f3d"}
ROOT = Path("models")

problems = []

if not ROOT.exists():
    raise SystemExit("No models/ folder found")

model_count = 0

for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix.lower() in MODEL_EXTS:
        model_count += 1
        size = f.stat().st_size

        if size > 100 * 1024 * 1024:
            problems.append(f"ERROR over 100MB: {f}")
        elif size > 50 * 1024 * 1024:
            problems.append(f"WARNING over 50MB: {f}")

if problems:
    print("\n".join(problems))
    raise SystemExit(1)

print(f"Repo check passed: {model_count} model files found and no oversized files.")
