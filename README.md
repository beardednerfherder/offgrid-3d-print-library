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
* Sensor, camera, and radio mounts.
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

## Recommended Use

A practical workflow:

1. Browse the folder that matches your project.
2. Open the model in your slicer or CAD software.
3. Choose a filament suitable for the environment.
4. Print one test part.
5. Inspect fit, strength, brittleness, and heat/UV suitability.
6. Reprint in PETG, ASA, ABS, TPU, or another suitable material if needed.
7. Replace any outdoor part that cracks, warps, or becomes brittle.

## Adding New Files

This repo is intended to stay simple.

To add new models:

1. Choose the most appropriate folder under `models/`.
2. Create a clear folder name for the part.
3. Add the printable files.
4. Prefer STEP/STP, SCAD, FreeCAD, Fusion, or other editable source files when available.
5. Avoid huge files where possible.
6. Do not add files over 100 MB, because GitHub rejects them.
7. Run the repo check script before committing.

Example:

```bash
mkdir -p "models/03_Garden_Greenhouse/shade_cloth_clip/files"
cp ~/Downloads/shade_cloth_clip.stl "models/03_Garden_Greenhouse/shade_cloth_clip/files/"
python3 scripts/check_repo.py
git add models/03_Garden_Greenhouse/shade_cloth_clip
git commit -m "Add shade cloth clip"
git push
```

## Repo Check

Before committing new files, run:

```bash
python3 scripts/check_repo.py
```

This checks for oversized model files.

GitHub rejects files over 100 MB. Files over 50 MB should be avoided unless they are truly worth keeping.

## Community Files and Use

This repository is maintained as a practical 3D print file library.

Some files may originate from community model sources and may retain their original creator licenses. If you plan to redistribute, sell, remix, or use files commercially, verify the source and license yourself before doing so.

This repo is intended as a practical personal/off-grid print library, not a legal license database.

## Contributing

Pull requests are welcome for:

* Useful utility models.
* Better category organization.
* STEP/STP or parametric source alternatives.
* Better print settings.
* Field-tested notes.
* Safety improvements.
* Removal of bad, unsafe, broken, or oversized models.

Good contributions should be practical, printable, and useful for real-world homestead/off-grid/shop/garden use.

## License

Original models and documentation created specifically for this repository are released under CC0 1.0 Universal unless otherwise noted.

Community models may retain their original licenses. Verify before commercial use, redistribution, or remixing.
