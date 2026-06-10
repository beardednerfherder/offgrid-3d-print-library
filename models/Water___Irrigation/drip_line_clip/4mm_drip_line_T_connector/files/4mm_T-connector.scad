// barbed connectors for 4mm drip line

// What kind of connector do we want?
connections = 2; // [1:End plug, 2:Straight connector, 3:T-connector, 4:X-connector, 5:5-way connector, 6:6-way connector]

// Dimensions
// outer diameter of shaft
od=4.5; // [4:0.1:6]
// inner diameter of shaft
id=2.4; // [0:0.1:4]
// barb min dia
bd_min=3.2; // [0:0.1:4]
// barb max dia
bd_max=5.6; // [4:0.1:8]
// barb length
blen=4.6; // [1:0.1:8]
// connector length
len=12.7; // [2:0.1:20]
// join block dimension (len, wid, height all equal)
jd=5.6; // [4:0.1:10]

module __Customizer_Limit__ () {}  // nothing else is customizable
    
// epsilon: for overlap to ensure unambigous joins
eps=0.01;
// minimum angle and side length globals
$fa=1;
$fs=0.02;

lines_out = connections-1;

// what direction for each subsequent line out? North, South, East, West, Up, Down
rotations = [[90,0,0],[-90,0,0],[0,90,0],[0,-90,0],[0,0,0],[180,0,0]];

// cross section for debuging?
cross_section = false;

// a barbed connection
module connection() {
    difference() {
        union() {
            cylinder(h=len-blen+eps, d=od, center=false);
            translate([0,0,len-blen]) cylinder(h=blen, d1=bd_max, d2=bd_min, center=false);
        }
        translate([0,0,-eps]) cylinder(h=len+2*eps, d=id, center=false);
    }
}


difference(){
    union() {
        // the join block
        difference() {
            intersection() { cube([jd, jd, jd+2*eps], center=true); sphere(d=jd*sqrt(2)*.99); } 
            for(i=[0:lines_out])
                rotate(rotations[i]) translate([0,0,-eps]) cylinder(h=jd/2+2*eps, d=id, center=false);
        }
        // Add connections:
        for(i=[0:lines_out])
            rotate(rotations[i]) translate([0,0,jd/2-eps]) connection();
    }
 if(cross_section) translate([-20,-20,0]) cube([40,40,20], center=false); 
 }