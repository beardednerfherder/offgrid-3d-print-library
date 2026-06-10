#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--approved", required=True)
    ap.add_argument("--rejected", required=True)
    args = ap.parse_args()

    with open(args.candidates, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []

    if not fields:
        raise SystemExit(f"No CSV header found in {args.candidates}")

    if "status" not in fields:
        raise SystemExit("CSV is missing required 'status' column")

    approved = []
    rejected = []

    for row in rows:
        status = (row.get("status") or "").strip().lower()

        if status == "approved":
            approved.append(row)
        elif status == "rejected":
            rejected.append(row)

    Path(args.approved).parent.mkdir(parents=True, exist_ok=True)
    Path(args.rejected).parent.mkdir(parents=True, exist_ok=True)

    with open(args.approved, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(approved)

    with open(args.rejected, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rejected)

    print(f"Approved: {len(approved)} -> {args.approved}")
    print(f"Rejected:  {len(rejected)} -> {args.rejected}")
    print(f"Undecided: {len(rows) - len(approved) - len(rejected)}")

if __name__ == "__main__":
    main()
