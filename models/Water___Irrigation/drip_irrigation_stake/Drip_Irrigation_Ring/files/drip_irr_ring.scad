//Drip Irrigation Ring for Containerized plants

diam=100;          // diameter of irrigaiton ring, mm (e.g. 100)  
orificediam =0.9;  // diameter of each drip orfice, mm (e.g., 0.9)
orificedeg=10;     // arc measure/angle between orfices, deg (e.g. 10, 15 or 30) cnrls # of orfices 

$fa = 1;
$fs = 1.2;
$fn=72;

difference(){
union(){    
    rotate([180,0,0]) hydra_ring(); // main ring
    rotate([180,0,-90+26/2])donutshape(diam/2-2,5,26);  // plug for cutout
    // mounting tabs
    translate([-6,diam/2-4,-2]) roundedcube(12 ,14 ,2,3);   
    translate([diam/2-4,-6,-2]) roundedcube(14 ,12 ,2,3); 
    translate([-diam/2-10,-6,-2]) roundedcube(14 ,12 ,2,3);
    }    
union(){
    translate([0,0,-2])rotate([0,0,-90-22/2])wedge(10, diam/2+1, 22);    // ring cutout
    translate([0,diam/2-5,3])cylinder(h=6,d=3,center=true);              // barb water inlet
    for ( i = [0 : orificedeg : 90] ){
    translate([0,0,1])rotate([0,90,i]) cylinder(h=diam-10,d=orificediam,center=true);  // orfices nozzles
    }  
    for ( i = [0 : -orificedeg : -90] ){
    translate([0,0,1])rotate([0,90,i]) cylinder(h=diam-10,d=orificediam,center=true);  // orfices nozzles
    }
    // holes for mouting tabs
    translate([0,diam/2+5,0])cylinder(h=10,d=5,center=true);
    translate([diam/2+5,0,0])cylinder(h=10,d=5,center=true);
    translate([-(diam/2+5),0,0])cylinder(h=10,d=5,center=true);    
    }    
}


// =============================================================
// Supporting functions/modules
// =============================================================

module hydra_ring(){
difference(){
    rotate([0,0,-15])donutshell(diam/2,10,360);
    rotate([0,0,-15+3])donutshape(diam/2-2,5,360);  
}
    translate([0,-diam/2+5.0,-10/2-5]) barb();
}


module donutshape(wheel_radius,tyre_diameter,tyre_angle){
  rotate_extrude(angle=tyre_angle) {
    translate([wheel_radius - tyre_diameter/2, 0])
    rotate([0,0,90])dring(tyre_diameter);  
  }
}

module donutshell(wheel_radius,tyre_diameter,tyre_angle){
  rotate_extrude(angle=tyre_angle) {
    translate([wheel_radius - tyre_diameter/2, 0])
    rotate([0,0,90])dring1(tyre_diameter);  
  }
}

module dring(ring_diameter){
difference(){
circle(d=ring_diameter);
translate([0,-ring_diameter/2]) square(ring_diameter);
     
} 
} 
module dring1(ring_diameter){
difference(){
circle(d=ring_diameter);
translate([0,-ring_diameter/2]) square(ring_diameter);
}
translate([0,-ring_diameter/2]) square([2,ring_diameter]);
} 

module barb(){
//rotate(a=[0,180,0])    
difference(){
union(){
cylinder(h=6,d=4,$fn=48);//pipe
cylinder(h=2.0,d1=4,d2=5,$fn=48);//barb
}

cylinder(h=7,d=2.5,$fn=48);//hole
}
}

module roundedcube(xdim ,ydim ,zdim,rdim){
  hull(){
  translate([rdim,rdim,0])cylinder(h=zdim,r=rdim);
  translate([xdim-rdim,rdim,0])cylinder(h=zdim,r=rdim);
  translate([rdim,ydim-rdim,0])cylinder(h=zdim,r=rdim);
  translate([xdim-rdim,ydim-rdim,0])cylinder(h=zdim,r=rdim);
  }
}

module wedge_180(h, r, d)
{
	rotate(d) difference()
	{
		rotate(180-d) difference()
		{
			cylinder(h = h, r = r);
			translate([-(r+1), 0, -1]) cube([r*2+2, r+1, h+2]);
		}
		translate([-(r+1), 0, -1]) cube([r*2+2, r+1, h+2]);
	}
}

module wedge(h, r, d)
{
	if(d <= 180)
		wedge_180(h, r, d);
	else
		rotate(d) difference()
		{
			cylinder(h = h, r = r);
			translate([0, 0, -1]) wedge_180(h+2, r+1, 360-d);
		}
}