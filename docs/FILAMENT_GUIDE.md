# Filament Guide for Off-Grid Applications

Choosing the right filament for the environment is as important as the print settings.
This guide is specific to homestead, off-grid, and northern Canadian climate use.

---

## Quick Selector

| Use Case | Best Choice | Budget Choice | Avoid |
|----------|------------|--------------|-------|
| Outdoor, UV exposed | **ASA** | PETG | PLA |
| Alberta winter (−40 °C) | **PETG** | ASA, ABS | PC (brittle at −40°C) |
| Direct sun / high heat | **ASA** | ABS | PETG, PLA |
| Wet environment | **ASA, PETG** | ABS | PLA (hydrolyzes) |
| Flexible clips / gaskets | **TPU 95A** | TPU 85A | Rigid materials |
| Electronics enclosures | **PETG** | ASA | PLA |
| Chicken coop | **ASA** | PETG | PLA |
| Near heat lamp | **ASA or ABS only** | — | PLA, PETG |
| Food-adjacent (seed trays etc) | **Certified food-safe PETG** | — | Standard filament |

---

## Material Deep Dives

### PLA
- ✅ Easy to print, cheap, widely available, good surface finish
- ❌ UV degrades in 6–18 months outdoors (becomes brittle, chalky)
- ❌ Heat deflection ~45–55°C — fails in direct sun in an Alberta summer
- ❌ Not moisture resistant over time
- **Use for**: calibration prints, indoor parts only, prototypes

### PETG
- ✅ UV resistant (several years outdoors)
- ✅ Excellent cold-weather performance to −40°C
- ✅ Moisture resistant
- ✅ Good layer adhesion, relatively forgiving to print
- ❌ Slightly hygroscopic — dry before printing (4h at 65°C)
- ❌ Softer than ASA at high temperatures (starts to deform ~70–75°C under load)
- **Recommended brands**: Prusament PETG, Polymaker PolyLite PETG, Hatchbox PETG
- **Print temp**: 230–250°C nozzle, 70–85°C bed, no cooling for first layers

### ASA
- ✅ Best UV resistance of common materials — lasts years in direct sun
- ✅ High heat resistance (~95–105°C under load)
- ✅ Moisture and chemical resistant
- ❌ Warps significantly — requires enclosure and draft-free environment
- ❌ Fumes during printing — ventilate or use enclosure with filtration
- **Use for**: any outdoor part, solar mounts, coop parts near heat lamps
- **Print temp**: 240–260°C nozzle, 90–110°C bed, enclosed printer strongly recommended

### ABS
- ✅ High heat resistance (~90–100°C)
- ✅ Widely available, affordable
- ❌ Poor UV resistance (cracks and yellows outdoors within a year)
- ❌ Warps badly, needs enclosure
- ❌ Fumes — ventilate
- **Use for**: high-temp indoor parts where ASA is unavailable

### TPU (Shore 95A)
- ✅ Flexible, impact resistant, excellent vibration dampening
- ✅ Good cold-weather flexibility (stays flexible at −30°C)
- ✅ Abrasion resistant
- ❌ Slow to print, needs direct-drive extruder or short/stiff Bowden
- ❌ Hygroscopic — dry thoroughly (8–12h at 45°C) or get stringing/bubbles
- **Print temp**: 220–240°C nozzle, 30–60°C bed, slow (20–30 mm/s)
- **Use for**: gaskets, door seals, vibration mounts, flexible cable clips

### PC (Polycarbonate)
- ✅ Highest heat resistance of common materials (~110–120°C)
- ✅ Very strong and impact resistant
- ❌ Requires high-temp printer (280°C+), all-metal hotend, high-temp bed (110°C+)
- ❌ Becomes brittle at −40°C — not ideal for Alberta outdoor use
- ❌ Very hygroscopic
- **Use for**: high-temperature applications where ASA isn't enough

---

## Drying Guidelines

Moisture in filament causes: stringing, under-extrusion, bubbles, weak layers, poor surface.
In Alberta's humid summers, even "sealed" spools absorb moisture.

| Material | Temp | Duration |
|----------|------|----------|
| PLA | 45°C | 4–6h |
| PETG | 65°C | 4–8h |
| ASA / ABS | 70°C | 6–8h |
| TPU | 45°C | 8–12h |
| PC | 80°C | 8–12h |

Use a food dehydrator or purpose-built filament dryer. A standard oven struggles to hold
consistent low temperatures.

---

## Recommended Print Settings for Outdoor Parts

| Setting | Value |
|---------|-------|
| Perimeters / walls | 4 minimum (3mm effective wall at 0.4mm nozzle = 4 perims at 0.45mm width) |
| Top/Bottom layers | 5 minimum |
| Infill | 30–40% for clips; 50%+ for load-bearing; 100% for safety items |
| Layer height | 0.2mm standard; 0.15mm for fine detail |
| Infill pattern | Gyroid or honeycomb (handles multi-directional stress) |
| Seam position | Rear or aligned (improves weather resistance) |

---

## Sourcing in Canada

- **Polymaker** — widely distributed; good PETG, ASA, TPU
- **Prusament** — excellent quality; ships from Czech Republic (2–3 weeks) or US
- **Hatchbox** — available via Amazon.ca, reliable PETG
- **Matter3D / 3DXTech** — specialty materials available to Canada
- **Local**: B.C. Filaments, Proto-Pasta ship domestically

---

## Colour Considerations

- **Black ASA/PETG** runs ~10–15°C hotter in direct sun than white. Factor into heat
  deflection decisions for solar or roof-mounted parts.
- **UV-stable pigments** are not universal — even within a brand, dark colours may fade.
  Test a sample outdoors for 1–2 months if colour stability matters.
