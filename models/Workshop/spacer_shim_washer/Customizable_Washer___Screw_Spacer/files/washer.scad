// Simple Customizable Washer
// by Mark Thompson

washer_outside_diameter = 9;
washer_hole_diameter = 5;
washer_thickness = 5;

$fn = 72;

difference() {
    translate([0,0,washer_thickness/2])
        cylinder(washer_thickness,washer_outside_diameter/2,washer_outside_diameter/2,true);
    
    translate([0,0,washer_thickness/2])
        cylinder(washer_thickness+0.1,washer_hole_diameter/2,washer_hole_diameter/2,true);
}
