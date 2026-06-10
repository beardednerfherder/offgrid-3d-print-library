#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv
from pathlib import Path
EXTS={'.stl','.3mf','.step','.stp','.scad','.obj'}
ap=argparse.ArgumentParser()
ap.add_argument('--models', default='models')
ap.add_argument('--out', default='manifests/download_audit.csv')
args=ap.parse_args()
base=Path(args.models)
rows=[]
for src in base.rglob('SOURCE.md'):
    folder=src.parent
    files=[p for p in (folder/'files').rglob('*') if p.is_file() and p.suffix.lower() in EXTS] if (folder/'files').exists() else []
    tiny=[p for p in files if p.stat().st_size < 1024]
    rows.append({
        'folder': str(folder),
        'source_md': 'yes',
        'model_file_count': len(files),
        'tiny_file_count': len(tiny),
        'status': 'ok' if files and not tiny else 'needs_files' if not files else 'check_tiny_files',
        'files': '; '.join(str(p.relative_to(folder)) for p in files[:20]),
    })
with open(args.out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['folder','source_md','model_file_count','tiny_file_count','status','files'])
    w.writeheader(); w.writerows(rows)
print(f"Audited {len(rows)} model folders -> {args.out}")
missing=sum(1 for r in rows if r['status']!='ok')
print(f"Needs attention: {missing}")
