# Off-Grid 3D Print Library

A curated, safety-first collection of useful 3D-printable parts for homesteads, off-grid properties, small farms, gardens, workshops, solar setups, radio/comms projects, and remote repair use.

The goal of this repo is simple:

> Download the library, browse the folders, open the files in your slicer or CAD software, and print the parts that are useful to you.

This library focuses on practical utility parts: clips, brackets, caps, organizers, mounts, holders, jigs, guides, trays, adapters, and repair pieces.

## Download the Full Library

To download everything from GitHub:

```bash
git clone https://github.com/beardednerfherder/offgrid-3d-print-library.git
cd offgrid-3d-print-library
```

Or use GitHub’s **Code → Download ZIP** button if you do not use Git.

Once downloaded, browse the `models/` folder. The files are organized by use case.

## Browse the Model Library

| Folder                                   | Contents                                                                                                           |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `models/01_Water_Hose_Irrigation/`       | Hose caps, drip clips, irrigation stakes, hose guides, rain barrel helpers. Low-pressure/non-pressurized use only. |
| `models/02_PEX_Tubing_NonPressure/`      | PEX/tubing clips, supports, labels, bend guides. Not for pressurized potable systems.                              |
| `models/03_Garden_Greenhouse/`           | Greenhouse clips, poly tunnel clamps, shade cloth clips, plant markers, trellis parts, row-cover helpers.          |
| `models/04_Buckets_Barrels_Storage/`     | Bucket handles, lid tools, bucket hooks, jar accessories, funnels, trays, storage labels.                          |
| `models/05_Workshop_Repair_Hardware/`    | Brackets, knobs, spacers, shims, tool holders, drill guides, organizers, cable clips, zip-tie mounts.              |
| `models/06_Electrical_Solar_LowVoltage/` | Solar cable clips, MC4 dust caps, Powerpole holders, DIN rail mounts, low-voltage cable management.                |
| `models/07_Chicken_Coop_Livestock/`      | Coop hooks, feeder brackets, fence clips, egg tray parts, waterer helpers, poultry utility tools.                  |
| `models/08_Vehicle_Trailer_Utility/`     | Trailer plug dust caps, hitch pin holders, grommets, panel clips, non-structural vehicle/trailer utility parts.    |
| `models/09_Radio_Comms_Sensors/`         | Antenna winders, dipole insulators, SDR cases, Meshtastic cases, ESP32 cases, sensor mounts, weather hoods.        |
| `models/10_Parametric_Source_Files/`     | Editable source files such as STEP, STP, OpenSCAD, FreeCAD, Fusion, or other CAD files where available.            |
| `models/99_Calibration_Test_Prints/`     | Calibration cubes, first-layer tests, retraction tests, and other printer setup files.                             |

## File Types

Some models include only print-ready files. Others include editable CAD/source files.

| File Type        | Use                                                                               |
| ---------------- | --------------------------------------------------------------------------------- |
| `.stl`           | Most common slicer-ready 3D print file. Good for printing, not ideal for editing. |
| `.3mf`           | Slicer-ready file that may include more model/print information than STL.         |
| `.step` / `.stp` | Best format for modifying parts in CAD software. Preferred when available.        |
| `.scad`          | OpenSCAD parametric source file. Useful for changing dimensions.                  |
| `.FCStd`         | FreeCAD source file. Useful for modifying the original design.                    |
| `.f3d`           | Fusion 360 source file. Useful for modifying the original design.                 |

For long-term usefulness, STEP/STP or parametric files are preferred over STL-only models.

## Safety First

Printed parts are not automatically safe just because they fit.

Do **not** use printed parts for:

* Pressurized potable water systems.
* Mains voltage or certified electrical enclosures.
* Vehicle or trailer load-bearing components.
* Suspension, braking, steering, towing, or lifting parts.
* Structural supports where failure could injure someone.
* Food contact unless your filament, printer, nozzle, and cleaning process are appropriate.
* Livestock-critical parts where failure could trap, injure, or deprive animals of water/feed.

Printed parts are best used for:

* Organization.
* Dust caps.
* Low-voltage cable management.
* Low-pressure irrigation helpers.
* Garden and greenhouse clips.
* Workshop jigs.
* Labels and holders.
* Sensor/camera/radio mounts.
* Non-structural repair aids.

Read `docs/SAFETY.md` before using any printed part near water, electricity, livestock, vehicles, trailers, or structural loads.

## Material Quick Reference

| Environment                   | Recommended    | Avoid                   |
| ----------------------------- | -------------- | ----------------------- |
| Outdoor / UV exposed          | ASA, PETG      | PLA                     |
| Alberta winter / freeze-thaw  | PETG, ASA, ABS | PLA outdoors            |
| Coop / barn heat and moisture | ASA, PETG      | PLA                     |
| Solar and low-voltage mounts  | ASA, PETG      | PLA, soft TPU           |
| Flexible clips or gaskets     | TPU 95A        | brittle rigid filaments |
| High-heat areas               | ASA, ABS, PC   | PLA                     |
| Indoor jigs and organizers    | PLA+, PETG     | Usually fine indoors    |

See `docs/FILAMENT_GUIDE.md` for more detail.

## Community Model Licenses

This library may contain a mix of:

1. Original models created for this repo.
2. Downloaded community models.
3. Links/manifests pointing to models hosted elsewhere.

Community models retain their original licenses. Check the original source page and any local `SOURCE.md` file before redistributing, remixing, selling, or uploading elsewhere.

When in doubt, use the source link and respect the creator’s license.

## Recommended Use

A practical workflow:

1. Browse the folder that matches your project.
2. Open the model in your slicer or CAD software.
3. Check the source notes and safety notes.
4. Choose a filament suitable for the environment.
5. Print one test part.
6. Inspect fit, strength, and brittleness.
7. Reprint in PETG/ASA/TPU if needed.
8. Replace any outdoor part that cracks, warps, or becomes brittle.

## Maintainer Notes

The scripts and manifests are mainly for maintaining and expanding the library.

Main files:

| Path                                | Purpose                                                                |
| ----------------------------------- | ---------------------------------------------------------------------- |
| `manifests/wanted_targets.csv`      | List of model types this library is trying to collect.                 |
| `manifests/candidates.csv`          | Search results that still need human review.                           |
| `manifests/approved_models.csv`     | Models approved for download or inclusion.                             |
| `manifests/rejected_models.csv`     | Bad matches, toys, unsafe models, wrong files, or bad-license entries. |
| `manifests/download_audit.csv`      | Audit of downloaded files.                                             |
| `scripts/search_candidates_v3.py`   | Finds candidate models.                                                |
| `scripts/build_review_page.py`      | Builds a review page from the candidate CSV.                           |
| `scripts/split_review_decisions.py` | Splits approved and rejected rows.                                     |
| `scripts/download_approved.py`      | Downloads approved models where possible.                              |
| `scripts/audit_downloads.py`        | Checks downloaded model folders and files.                             |

Maintainer workflow:

```bash
source .venv/bin/activate

python3 scripts/search_candidates_v3.py \
  --targets manifests/wanted_targets.csv \
  --out manifests/candidates.csv \
  --thingiverse-token "$THINGIVERSE_TOKEN" \
  --sources thingiverse,printables,github \
  --per-target 5 \
  --min-score 8 \
  --prefer-step

python3 scripts/build_review_page.py \
  --candidates manifests/candidates.csv \
  --out review.html

python3 scripts/split_review_decisions.py \
  --candidates manifests/candidates.csv \
  --approved manifests/approved_models.csv \
  --rejected manifests/rejected_models.csv

python3 scripts/download_approved.py \
  --approved manifests/approved_models.csv \
  --out models \
  --thingiverse-token "$THINGIVERSE_TOKEN" \
  --prefer-source \
  --open-manual

python3 scripts/audit_downloads.py \
  --models models \
  --out manifests/download_audit.csv
```

Before committing, check for oversized files:

```bash
find . -type f -size +95M -not -path "./.git/*" -print
```

GitHub rejects files over 100 MB. Large community files should usually be left out of the repo and documented with a source link instead.

## Contributing

Pull requests are welcome for:

* New useful model links.
* Better category organization.
* STEP/STP or parametric source alternatives.
* Better print settings.
* Field-tested notes.
* Safety improvements.
* Removal of bad or unsafe models.
* License corrections.

Preferred model status labels:

| Status         | Meaning                                                             |
| -------------- | ------------------------------------------------------------------- |
| `candidate`    | Found by search, not reviewed yet.                                  |
| `approved`     | Human-reviewed and worth downloading.                               |
| `downloaded`   | Files downloaded locally.                                           |
| `sliced_ok`    | Opened successfully in slicer.                                      |
| `printed_ok`   | Successfully printed.                                               |
| `field_tested` | Actually used in the real world.                                    |
| `rejected`     | Wrong, unsafe, decorative, toy/model, bad license, or poor quality. |

## License

Original models and documentation created specifically for this repository are released under CC0 1.0 Universal unless otherwise noted.

Community models linked, referenced, or downloaded from third-party sites retain their original licenses. Check each model’s source page and local `SOURCE.md` before redistributing, remixing, selling, or uploading files.
