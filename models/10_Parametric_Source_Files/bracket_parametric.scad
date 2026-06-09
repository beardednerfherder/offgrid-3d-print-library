// ============================================================
//  bracket_parametric.scad
//  Off-Grid 3D Print Library - Parametric Mounting Bracket
//  License: CC0 Public Domain
//  Recommended material: PETG or ASA for outdoor use
// ============================================================

/* [Main Dimensions] */
arm_h       = 40;   // Vertical arm height (mm)
arm_w       = 40;   // Horizontal arm width (mm)
depth       = 25;   // Bracket depth (mm)
thick       = 3;    // Wall thickness (mm)

/* [Gusset] */
gusset      = true;     // Add diagonal gusset?
gusset_t    = 3;        // Gusset thickness (mm)

/* [Mounting Holes] */
add_holes   = true;     // Drill mounting holes?
hole_d      = 4.5;      // Hole diameter - 4.5mm passes M4 bolt
hole_margin = 8;        // Distance from edge to hole center (mm)

/* [Render] */
$fn = 32;

module rounded_rect(w, d, h, r=2) {
    hull() {
        for (xx = [r, w-r])
            for (yy = [r, d-r])
                translate([xx, yy, 0]) cylinder(r=r, h=h);
    }
}

module bracket_body() {
    union() {
        cube([thick, depth, arm_h]);        // vertical arm
        cube([arm_w,  depth, thick]);       // horizontal arm
        if (gusset) {
            translate([thick, 0, thick])
                rotate([0, 0, 0])
                linear_extrude(depth)
                    polygon([[0,0],[arm_w-thick,0],[0,arm_h-thick]]);
        }
    }
}

module bracket() {
    difference() {
        bracket_body();
        if (add_holes) {
            // Vertical arm hole
            translate([thick/2, depth/2, arm_h - hole_margin])
                rotate([0, 90, 0])
                    cylinder(d=hole_d, h=thick+2, center=true);
            translate([thick/2, depth/2, hole_margin])
                rotate([0, 90, 0])
                    cylinder(d=hole_d, h=thick+2, center=true);
            // Horizontal arm holes
            translate([arm_w - hole_margin, depth/2, thick/2])
                cylinder(d=hole_d, h=thick+2, center=true);
            translate([hole_margin + thick, depth/2, thick/2])
                cylinder(d=hole_d, h=thick+2, center=true);
        }
    }
}

bracket();
