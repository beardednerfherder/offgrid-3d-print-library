# Safety Guidelines

**Read before printing anything intended for real-world off-grid use.**

---

## General Principles

FDM 3D-printed parts are **layer-bonded plastics**. They are not equivalent to
injection-moulded, machined, or cast parts of the same material. They:

- Have **reduced strength along the Z axis** (between layers)
- Are **not food-safe** unless using certified food-safe filament + hardware
- Are **not pressure-rated** for water, gas, or hydraulic systems
- **Degrade in UV** (PLA within months, PETG/ASA in years)
- Can **creep under sustained load**, especially at elevated temperatures

Always test a prototype before relying on a part in a safety-critical application.

---

## Water and Irrigation

| Application | Acceptable | Not Acceptable |
|-------------|-----------|----------------|
| Gravity drip (< 5 PSI) | PETG, ASA | PLA |
| Rain barrel overflow routing | PETG, ASA | PLA |
| Hose guides and clips (not under pressure) | PETG, ASA | PLA |
| Municipal water lines | **Never — use plumbing-rated fittings** | All filaments |
| Pressurized irrigation (mains pressure) | **Never** | All filaments |
| Potable water contact | **Only certified food-safe filament** | Standard filament |

---

## Electrical and Solar

- **Never** use 3D-printed parts on or near mains (120V/240V AC) circuits.
- Low-voltage DC (12V/24V solar, Meshtastic, sensors) is acceptable with appropriate
  wire management.
- Battery terminal covers must be printed at minimum **50% infill** and **3 perimeters**.
  They are safety items — verify fitment before use.
- MC4 connector covers are dust/weather protection only — they do not replace proper
  disconnect procedures. De-energize before connecting or disconnecting.
- Solar panel clips are **retention aids only** — not structural mounts in high-wind
  or roof-mounted installations. Use certified racking for roof installs.

---

## Livestock and Coop

- No 3D-printed components in **waterers for livestock** (contamination risk,
  unless certified food-safe).
- Coop latches are a **convenience feature only** — predator-proof latches must be
  metal hardware.
- Heat lamp guards: print only in **ASA or ABS** (heat deflection > 95°C).
  PLA and PETG are fire hazards near heat lamps.
- All coop parts should be checked every 3–6 months for UV degradation and layer
  delamination. Replace any cracked or brittle parts immediately.

---

## Vehicle and Trailer

- Trailer jack foot pads support **stabiliser jacks only** — not load-bearing
  functions. Never use under a jack lift point.
- Ratchet strap keepers are organizer accessories only. Never rely on a 3D-printed
  part as part of a cargo tie-down system.

---

## Temperature Limits (approximate, FDM parts)

| Material | Max continuous service temp |
|----------|-----------------------------|
| PLA | ~45–55 °C (avoid outdoor summer use) |
| PETG | ~70–75 °C |
| ABS | ~90–100 °C |
| ASA | ~95–105 °C |
| PC | ~110–120 °C |
| TPU (95A) | ~80 °C |

Alberta summer direct-sun surface temperatures can exceed 60°C — use ASA or PETG
minimum for any outdoor parts.
