# Category 99 — Calibration & Test Prints

Standard calibration prints. Run these on a new printer, after a hotend swap,
after a firmware update, or whenever print quality drops.

## Recommended Order

1. **`bed_level_5_point.stl`** — Print this first on any new bed or after tramming
2. **`first_layer_test_50x50.stl`** — Confirm Z offset and first-layer squish
3. **`first_layer_test_100x100.stl`** — Full-bed level check (reveals tram errors)
4. **`retraction_tower_5x5x25.stl`** — Tune retraction before printing thin parts
5. **`calibration_cube_20mm.stl`** — Verify XYZ dimensional accuracy

## Reading the Calibration Cube
- Measure with calipers on all three axes
- Target: 20.00 ±0.20mm
- If off: check steps/mm in firmware or flow multiplier in slicer

## Print Settings for Calibration Prints
Use your "standard" profile — the goal is to evaluate real-world settings.
- **No brim** (measuring outer dims)
- **No supports**
- Layer height 0.2mm
- 3 perimeters, 20% infill, 3 top/bottom layers
- Print in PLA or PETG (whatever is your default)

## Included STL Files
| File | Purpose |
|------|---------|
| `calibration_cube_20mm.stl` | XYZ dimensional accuracy |
| `first_layer_test_50x50.stl` | First layer / Z offset |
| `first_layer_test_100x100.stl` | Full bed level check |
| `retraction_tower_5x5x25.stl` | Retraction tuning |
| `bed_level_5_point.stl` | 5-point bed tramming confirmation |
