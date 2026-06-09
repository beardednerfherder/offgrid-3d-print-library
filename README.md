# Off-Grid 3D Print Library

A curated, safety-first library of 3D-printable models for homesteads, off-grid properties,
small farms, and remote workshop use.

> **Safety first**: See [`docs/SAFETY.md`](docs/SAFETY.md) before printing anything used near
> water, electrical systems, livestock, or load-bearing applications.

---

## What's In This Repo

| Folder | Contents |
|--------|----------|
| `models/01_Water_Hose_Irrigation/` | Gravity-feed drip clips, hose guides (non-pressurized only) |
| `models/02_PEX_Tubing_NonPressure/` | PEX strap clips for drainage / grey water |
| `models/03_Garden_Greenhouse/` | Film clips, hoop ends, trellis hardware |
| `models/04_Buckets_Barrels_Storage/` | Bucket-rim clips, trays, label holders |
| `models/05_Workshop_Repair_Hardware/` | Brackets, cable clips, trays, zip-tie anchors |
| `models/06_Electrical_Solar_LowVoltage/` | Wire clips, conduit saddles, solar corner clips |
| `models/07_Chicken_Coop_Livestock/` | Hooks, feed trays, fence wire clips |
| `models/08_Vehicle_Trailer_Utility/` | Trailer jack pads, strap keepers |
| `models/09_Radio_Comms_Sensors/` | SMA cap trays, antenna strain relief |
| `models/10_Parametric_Source_Files/` | OpenSCAD parametric source files |
| `models/99_Calibration_Test_Prints/` | Calibration cube, first-layer tests, retraction tower |
| `manifests/models.csv` | Curated link manifest for community models |
| `scripts/` | Download and audit scripts |
| `docs/` | Safety guide, filament guide |

---

## Quick Start

```bash
git clone https://github.com/YOUR_USER/offgrid-3d-print-library.git
cd offgrid-3d-print-library
# Browse models/ and open any .stl in your slicer
```

### Downloading community models from the manifest

```bash
pip3 install requests
python3 scripts/download_manifest.py
# Add --category 6 to download only category 06, etc.
```

---

## Material Quick Reference

| Environment | Recommended | Avoid |
|-------------|-------------|-------|
| Outdoors / UV exposed | **ASA**, PETG | PLA |
| Coop / barn (heat + moisture) | **ASA**, PETG | PLA |
| Solar/electrical mounts | **ASA**, PETG | PLA, TPU |
| Flexible clips / gaskets | **TPU 95A** | rigid filaments |
| High-heat (>80 °C) | **ASA**, ABS, PC | PETG, PLA |
| Alberta winters (−40 °C) | **PETG**, ASA, ABS | brittle at temp: PC |

See [`docs/FILAMENT_GUIDE.md`](docs/FILAMENT_GUIDE.md) for full detail.

---

## Included STL Files

These original models are included in the repo and are **CC0 Public Domain**:

### 99 — Calibration
- `calibration_cube_20mm.stl` — 20mm XYZ calibration cube
- `first_layer_test_50x50.stl` — 50×50mm first-layer adhesion test
- `first_layer_test_100x100.stl` — 100×100mm full-bed level confirmation
- `retraction_tower_5x5x25.stl` — 5×5×25mm retraction tower
- `bed_level_5_point.stl` — 5-point bed leveling squares

### 01 — Water / Irrigation
- `hose_stake_clip_19mm.stl` — ¾″ hose guide clip for garden stakes
- `dual_drip_line_guide_6mm.stl` — Dual 6mm drip-line guide clip
- `drip_emitter_plug_8mm.stl` — Push-fit plug for unused 8mm emitter holes

### 02 — PEX (non-pressure)
- `pex_support_clip_12mm.stl` — Support strap for 12mm OD PEX (gravity drainage only)

### 03 — Garden / Greenhouse
- `greenhouse_film_clip_16mm.stl` — Poly film clip for 16mm EMT hoops
- `row_cover_hoop_clip_9mm.stl` — End clip for 9mm row-cover hoops

### 04 — Buckets / Storage
- `bucket_rim_label_clip.stl` — Label holder that hooks over bucket rim
- `screw_organizer_tray_80x50.stl` — Open-top parts tray

### 05 — Workshop
- `l_bracket_30x30x3mm.stl` — General-purpose L-bracket
- `cable_clip_5mm_id.stl` — U-channel cable management clip
- `parts_tray_50x30x8.stl` — Small parts organizer tray
- `zip_tie_anchor.stl` — Zip-tie loop base anchor

### 06 — Electrical / Solar
- `wire_wall_clip_3mm.stl` — Wall-mount clip for 3mm wire
- `solar_panel_corner_clip.stl` — Corner retention clip for solar panels
- `conduit_saddle_16mm_emt.stl` — Wall saddle for ½″ EMT conduit

### 07 — Chicken Coop / Livestock
- `j_hook_fence_hanger.stl` — J-hook for coop/fence hanging
- `feed_supplement_tray_80x50.stl` — Small supplement feed tray
- `fence_wire_u_clip.stl` — U-clip for hardware cloth attachment

### 08 — Vehicle / Trailer
- `trailer_jack_foot_pad_120mm.stl` — 120mm jack foot pad for soft ground
- `ratchet_strap_hook_keeper.stl` — Keeps strap hooks captured when stored

### 09 — Radio / Comms
- `sma_cap_organizer_tray.stl` — 3-compartment SMA dust-cap tray
- `sma_pigtail_strain_relief.stl` — Strain relief bracket for SMA pig-tails

### 10 — Parametric OpenSCAD Sources
- `bracket_parametric.scad` — Fully parametric mounting bracket
- `clip_parametric.scad` — Parametric C-clip / U-clip for any pipe/wire size
- `box_enclosure.scad` — Parametric box + lid for electronics

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). PRs welcome for new models, manifest entries,
improved print settings, or documentation.

---

## License

Original models in this repo: **CC0 1.0 Universal (Public Domain)** — see [`LICENSE`](LICENSE).

Community models linked via `manifests/models.csv` retain their original licenses (noted per row).
Always verify license before commercial use.
