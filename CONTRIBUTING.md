# Contributing to Off-Grid 3D Print Library

Thank you for contributing! This library lives and grows through community additions.

---

## Ways to Contribute

1. **Add a model link** — Add a row to `manifests/models.csv`
2. **Add an original model** — Place your `.stl` in the correct category folder and open a PR
3. **Add a parametric source** — Add an `.scad` file to `10_Parametric_Source_Files/`
4. **Fix documentation** — Improve safety notes, print settings, or README files
5. **Report a safety issue** — Open an issue immediately; tag it `safety`

---

## Adding a Model Link (manifests/models.csv)

Copy the schema from `manifests/schema.json`. Required fields:

| Field | Notes |
|-------|-------|
| `id` | Next sequential `OG-NNN` |
| `category_num` | 01–10 or 99 |
| `name` | Short descriptive name |
| `description` | One sentence, what it does |
| `material_rec` | PETG / ASA / PLA / TPU / ABS / ASA |
| `source_license` | CC0 / CC BY / CC BY-SA / CC BY-NC / MIT |
| `source_site` | Printables / Thingiverse / GitHub / Makerworld |
| `page_url` | Link to model page |

Optional but encouraged: `download_url`, `infill_pct`, `supports_needed`, `notes`.

**License check**: Only add models with CC0, CC BY, or CC BY-SA licenses unless
clearly labelled as non-commercial.

---

## Adding an Original Model

1. Place `.stl` in the correct `models/NN_Category/` folder.
2. Name it descriptively: `thing_dimension_variant.stl` e.g. `hose_clip_25mm_petg.stl`
3. Add a `MODEL_NOTES.md` beside it (copy from `templates/MODEL_NOTES_TEMPLATE.md`)
4. Print settings, material, and wall thickness must be documented.
5. Model must be your original work and licensed CC0.

---

## Safety Policy

Any model touching **water pressure**, **electrical mains**, **structural loads**, 
**animal containment**, or **fire/heat** must include a safety disclaimer in its
`MODEL_NOTES.md`. When in doubt, open an issue before submitting.

---

## Pull Request Checklist

- [ ] Model prints without errors in PrusaSlicer or OrcaSlicer
- [ ] Model is named per convention
- [ ] `MODEL_NOTES.md` is filled out
- [ ] If adding to CSV: license is compatible, page_url is valid
- [ ] No files over 25MB (prefer .scad sources for large parametric parts)

---

## Code of Conduct

Be helpful, be honest about print failures, credit original designers.
