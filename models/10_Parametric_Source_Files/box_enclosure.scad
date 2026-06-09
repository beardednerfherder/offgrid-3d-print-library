// ============================================================
//  box_enclosure.scad
//  Off-Grid 3D Print Library - Parametric Box Enclosure + Lid
//  License: CC0 Public Domain
//  Good for: electronics, sensors, Meshtastic nodes, junction boxes
// ============================================================

/* [Interior Dimensions] */
box_w       = 80;   // Inner width  (mm)
box_d       = 60;   // Inner depth  (mm)
box_h       = 40;   // Inner height (mm)

/* [Wall and Lid] */
wall_t      = 2.5;      // Wall thickness (mm)
lid_overlap = 6;        // How far lid overlaps into box (mm)
tol         = 0.25;     // Fit tolerance each side (mm)

/* [Features] */
corner_r    = 3;        // Corner fillet radius (mm)
screw_d     = 3.2;      // Screw hole diameter (M3 = 3.2)
screw_posts = true;     // Add corner screw boss posts?
post_od     = 8;        // Outer diameter of screw posts (mm)
cable_entry = false;    // Add 10mm cable entry notch?
cable_dia   = 10;       // Cable entry diameter (mm)

/* [Output] */
print_box   = true;
print_lid   = true;
separation  = 15;       // Space between box and lid when printing

/* [Render] */
$fn = 48;

module rounded_slab(w, d, h, r) {
    hull()
        for (x=[r, w-r], y=[r, d-r])
            translate([x, y, 0]) cylinder(r=r, h=h);
}

module screw_post(h) {
    difference() {
        cylinder(d=post_od, h=h);
        cylinder(d=screw_d, h=h+1);
    }
}

OW = box_w + 2*wall_t;
OD = box_d + 2*wall_t;
OH = box_h + wall_t;
OR = corner_r + wall_t;

module box_body() {
    difference() {
        rounded_slab(OW, OD, OH, OR);
        translate([wall_t, wall_t, wall_t])
            rounded_slab(box_w, box_d, box_h+1, corner_r);
        if (cable_entry)
            translate([OW/2, -1, OH * 0.4])
                rotate([-90,0,0])
                    cylinder(d=cable_dia, h=wall_t+2);
    }
    if (screw_posts) {
        post_h = box_h - 1;
        for (px=[wall_t+post_od/2, OW-wall_t-post_od/2],
             py=[wall_t+post_od/2, OD-wall_t-post_od/2])
            translate([px, py, wall_t]) screw_post(post_h);
    }
}

LW = OW;
LD = OD;
LH = wall_t + lid_overlap;
inner_lw = box_w - 2*tol;
inner_ld = box_d - 2*tol;
inner_lr = max(corner_r - tol, 1);

module lid() {
    difference() {
        union() {
            rounded_slab(LW, LD, wall_t, OR);
            translate([wall_t+tol, wall_t+tol, wall_t])
                rounded_slab(inner_lw, inner_ld, lid_overlap, inner_lr);
        }
        if (screw_posts) {
            for (px=[wall_t+post_od/2, LW-wall_t-post_od/2],
                 py=[wall_t+post_od/2, LD-wall_t-post_od/2])
                translate([px, py, -1])
                    cylinder(d=screw_d, h=wall_t+2);
        }
    }
}

if (print_box)
    box_body();

if (print_lid)
    translate([print_box ? OW + separation : 0, 0, 0])
        lid();
