// ============================================================
//  clip_parametric.scad
//  Off-Grid 3D Print Library - Parametric C-Clip / U-Clip
//  License: CC0 Public Domain
//  Adjust inner_d for pipe/wire size; controls opening gap for snap-fit
// ============================================================

/* [Clip Geometry] */
inner_d     = 12;   // Inner channel diameter (mm) - set to pipe/wire OD
wall_t      = 3;    // Wall thickness (mm)
clip_len    = 25;   // Length along extrusion axis (mm)
open_angle  = 100;  // Total opening angle (degrees, 60-120 typical)

/* [Mounting Tab] */
mount_tab   = true;     // Add flat mounting tab?
tab_w       = 24;       // Tab width (mm)
tab_t       = 4;        // Tab thickness (mm)
hole_d      = 4.5;      // Screw hole diameter (mm)
hole_inset  = 6;        // Hole center inset from tab edge (mm)

/* [Render] */
$fn = 64;

r_i = inner_d / 2;
r_o = r_i + wall_t;
half_open = open_angle / 2;

module clip_2d() {
    difference() {
        circle(r = r_o);
        circle(r = r_i);
        // Cut opening wedge at top
        rotate(90 - half_open)
            translate([-r_o - 1, 0])
                square([2*(r_o+1), r_o+1]);
        mirror([1, 0])
            rotate(90 - half_open)
                translate([-r_o - 1, 0])
                    square([2*(r_o+1), r_o+1]);
    }
}

module mounting_tab_2d() {
    translate([-tab_w/2, -r_o - tab_t])
        difference() {
            square([tab_w, tab_t]);
            translate([hole_inset, tab_t/2])       circle(d=hole_d);
            translate([tab_w-hole_inset, tab_t/2]) circle(d=hole_d);
        }
}

module clip() {
    linear_extrude(height = clip_len) {
        clip_2d();
        if (mount_tab) mounting_tab_2d();
    }
}

clip();
