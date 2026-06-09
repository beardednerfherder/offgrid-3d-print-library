# Category 10 — Parametric OpenSCAD Source Files

Fully customizable source files for generating your own variants.
All files are CC0 Public Domain.

## Requirements
- [OpenSCAD](https://openscad.org) 2021.01 or newer (free, cross-platform)
- Or use [OpenSCAD Online](https://openscad.org/openscad.html) for quick preview

## Included Files

### `bracket_parametric.scad`
Adjustable mounting bracket with optional gusset and mounting holes.
Parameters: arm_h, arm_w, depth, thick, gusset, hole_d, hole_margin.

### `clip_parametric.scad`
C-clip / U-clip for any pipe or wire diameter.
Parameters: inner_d, wall_t, clip_len, open_angle, mount_tab, hole_d.

### `box_enclosure.scad`
Parametric box + lid for electronics enclosures, junction boxes, etc.
Parameters: box_w, box_d, box_h, wall_t, corner_r, screw_posts, cable_entry.

## Usage
1. Open file in OpenSCAD
2. Edit values in the `/* [Section] */` parameter blocks
3. Press F6 to render
4. File > Export > Export as STL
