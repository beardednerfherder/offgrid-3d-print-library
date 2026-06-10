difference(){
    translate([-8,-23,0]) cube([16,14,15]);
    union(){
        translate([-6,-20.7,10]) cube([12,6.35,15]);
        translate([0,-14.35,7.5]) rotate([90,30,0]) cylinder(6.35,7,7,$fn=6);
        translate([0,-8,8]) rotate([90,0,0]) cylinder(20,3.2,3.2,$fn=30);
    }
}
translate([-30,-9,0]) cube([60,15,15]);
translate([0,6,7.5]) rotate([-90,0,0])
union(){
    cylinder(1.5,7.5,7.5,$fn=50);
    cylinder(8,5,5,$fn=50);
}