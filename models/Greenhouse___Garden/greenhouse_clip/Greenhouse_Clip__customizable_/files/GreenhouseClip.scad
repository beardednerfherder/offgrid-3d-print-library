//
// hook for greenhouse C-profiles
//

$fa=1*1;
$fs=0.25*1;


// thickness of plate and hook
clip_thickness = 3;

// thickness of greenhouse profile
thn_profile = 1.0;

// width of hammer nut
w_base = 6.3;

// length of hammer nut
l_base = 10;

// diameter of base plate
d_plate = 20;

// height of hook
h_clip = 25;

// diameter of hook hole
d_clip_hole = 10;

// hook orientation (rotate hammer nut)
hook_orientation = 0; // [0:90]

hook();
base();
support();

module base() {
    translate([0,0,thn_profile])
        cylinder(clip_thickness, d=d_plate);
    cylinder(thn_profile, d=w_base);

    rotate([0, 0, hook_orientation])
        translate([0,0,-clip_thickness])
            linear_extrude(clip_thickness)
                polygon(points=[[-w_base/2,-l_base/2], [-w_base/2,l_base/4], 
                    [-w_base/4,l_base/2], [w_base/2,l_base/2], 
                    [w_base/2,-l_base/4], [w_base/4,-l_base/2]]);
}    
    

module support() {
 
    r_offset = 1;
    translate([0, clip_thickness/2, clip_thickness + thn_profile]) 
    rotate([90, 0, 0])
        linear_extrude(clip_thickness)
            polygon(points=[[-d_plate/2+r_offset, 0], [0, d_plate/2], [d_plate/2-r_offset, 0]]);
    
    
}

module hook() {
 
    translate([-clip_thickness/2, 0, h_clip-d_plate/2 + clip_thickness + thn_profile])
    rotate([0,90,0])
    difference() {
        union() {
            cylinder(clip_thickness, d=d_plate);
            translate([0,-d_plate/2,0])
                cube([h_clip-d_plate/2,d_plate,clip_thickness]);
        }
        translate([0,0,-0.01])
            cylinder(clip_thickness+0.02, d=d_clip_hole);   
    }
}
    
    