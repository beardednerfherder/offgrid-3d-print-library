# Off-Grid Homestead 3D Print Library — Model Manifest

62 curated, community-reviewed models across 9 categories. Every model here
has real makes/reviews on Thingiverse or Printables. No generated placeholders.

## Quick Start

### Step 1 — Get a Thingiverse API Token (free, 2 min)
1. Go to https://www.thingiverse.com/apps/create
2. Create an app (any name) → copy the **Client ID**
3. Visit this URL in your browser (replace `YOUR_CLIENT_ID`):
   ```
   https://www.thingiverse.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=token
   ```
4. Log in → copy the `access_token=XXXXXXXX` value from the redirect URL

### Step 2 — Download Thingiverse models automatically
```bash
python3 download_manifest.py --token YOUR_TOKEN
```

Filter to a single category:
```bash
python3 download_manifest.py --token YOUR_TOKEN --category 09
```

Preview without downloading:
```bash
python3 download_manifest.py --token YOUR_TOKEN --dry-run
```

### Step 3 — Download Printables models (opens browser tabs)
```bash
python3 download_manifest.py --printables-only
```
This opens each Printables page in your browser. Manually click Download on each.
Save the files to the matching folder shown in the terminal output.

### List all models without downloading
```bash
python3 download_manifest.py --list
```

---

## Categories

| # | Category | Models | Key Items |
|---|---|---|---|
| 01 | Water / Hose / Irrigation | 7 | GHT hose cap, drip clips, drip stakes, goof plugs |
| 02 | PEX / Tubing | 2 | Support clips, label tags |
| 03 | Garden / Greenhouse | 7 | Raised bed corners, film clips, hoop clips, shade cloth clips |
| 04 | Buckets / Storage | 6 | Bucket handle, lid opener, bag clips, mason jar lids, funnel |
| 05 | Workshop / Hardware | 9 | Star knobs, spacers, drill guide, sandpaper block, wall hooks |
| 06 | Electrical / Solar | 7 | MC4 caps (locking), Powerpole mounts, DIN clips, project boxes |
| 07 | Chicken Coop | 4 | Nipple wrench, T-post insulators, feeder bracket |
| 08 | Vehicle / Trailer | 5 | 7-pin trailer cap, hitch keeper, grommets, panel clips |
| 09 | Radio / Comms | 9 | Wire winder, dipole insulator, Heltec V3 case, RTL-SDR case |
| 99 | Calibration | 5 | XYZ cube, first layer test, temp tower, retraction test |

---

## Safety Rules (baked into every entry)
- **Water fittings**: low-pressure / irrigation only. Not for household supply.
- **Electrical**: dust caps and cable management only. No mains/AC parts.
- **Vehicle**: dust caps and organizers only. Nothing structural.
- **Solar**: MC4 covers are for dust/moisture protection, not load-bearing.
- **Livestock**: replace any cracked or chewed parts immediately.

---

## Filament Guide

| Use Case | Material | Why |
|---|---|---|
| Outdoor / UV year-round | ASA | Best UV resistance; needs enclosure to print |
| General outdoor utility | PETG | Good moisture/UV; easy to print |
| Flexible clips, grommets, pads | TPU 95A | Proper flex and grip |
| Indoor jigs, labels | PLA+ | Easy print; degrades outdoors in AB winters |
| High-load tool holders | PETG at 5 walls + 40% | Or PA-CF for max strength |

**Alberta winter note**: PLA becomes brittle below -10°C. Replace any PLA outdoor
parts before winter with PETG or ASA.

**Drying guide**:
- PETG: 65°C for 8-12h before printing
- ASA: 70°C for 8-12h
- TPU: 50°C for 4-6h

---

## Adding Models

To add a model to the manifest, append a row to `models.csv`:
```
id,category_num,category_name,name,description,material_rec,infill_pct,
supports_needed,source_site,thing_id,page_url,notes
```

The `source_site` field controls download behavior:
- `thingiverse` → auto-downloaded via API
- `printables` → browser opened for manual download
- `makerworld` → browser opened
- `github` → future support; use page_url directly

---

## Folder Structure (after download)
```
models/
  01_Water_Hose_Irrigation/
    Garden_Hose_Cap_GHT_female/
      *.stl
    Drip_Line_Clips/
      *.stl
    ...
  03_Garden_Greenhouse/
    ...
  09_Radio_Comms_Sensors/
    Heltec_V3_Case_Meshtastic/
      *.stl
    ...
```
