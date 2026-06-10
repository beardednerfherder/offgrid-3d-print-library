
//$fn=100;
$fa=2; 
$fs=0.2;



wall_thickness = 2.5;
spout_height= 20;
spout_dia = 70.5;
funnel_height = 30;
funnel_dia = 110;

union() {
  difference(){
    cylinder(h=spout_height, r=(spout_dia/2)+wall_thickness, center=true);
    cylinder(h=spout_height+2, r=(spout_dia/2), center=true);
  }

  translate([0,0,(funnel_height+spout_height)/2]) {
    difference(){
      cylinder(h=funnel_height, r1=(spout_dia/2)+wall_thickness, r2=(funnel_dia/2)+wall_thickness, center=true);
      cylinder(h=funnel_height+2, r1=(spout_dia/2), r2=(funnel_dia/2), center=true);
    }
  }
  
    translate([0,0,(spout_height)/2]) 
    rotate_extrude(convexity=10) 
      translate([(spout_dia+1)/2,0,0]) rotate(45) circle(1);

   translate([0,0,funnel_height+spout_height/2]) 
    rotate_extrude(convexity=10) 
      translate([ (funnel_dia+wall_thickness-1)/2,0,0]) rotate(45) circle(wall_thickness-0.7);
}

// Inside Fillet 
module fillet(ct,cr,r,pad) {
translate([0,0,-ct])
difference() {
rotate_extrude(convexity=10) 
translate([cr-ct-r+pad,ct-pad,0]) square(r+pad,r+pad);
rotate_extrude(convexity=10) 
translate([cr-ct-r,ct+r,0]) circle(r=r);
}

}