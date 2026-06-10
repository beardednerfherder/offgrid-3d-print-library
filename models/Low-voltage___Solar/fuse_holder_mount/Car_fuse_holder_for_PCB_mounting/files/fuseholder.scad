//////////////////////////////////////////////////////////////////////////////////////
///
///  FUSEHOLDER: Fuse holder for standard automotive fuses
///
///  This little project is a fuse holder for placing a standard automotive
///  5A/10A/20A fuse onto a PCB.
///
///  The contacts to the fuse spades are made by 3mm large solder tabs.  These
///  are bent around the fuse tabs in "M" shape, and the the ends are pushed
///  through the diagonal channel that lead to the solder cavities underneath
///  the fuse holer.  Then, the automotive fuse is used to push the solder tabs
///  into place. Two short pieces of 20ga (~0.8mm diameter) solid copper wire
///  are inserted through the vertical wire holes and horizontal channels to
///  overlap with the solder tabs in the solder cavities. Soldering has to be done
///  quickly in order not to melt the ABS plastic.
///
///  The distance between the wires is 0.4in / 10mm, and the placement of the wires
///  is done somewhat asymmetric, in order to fit the space on the PCB when
///  replacing the 11A auto-resetting PTC fuse on a RAMPS 1.4 board.
///
//////////////////////////////////////////////////////////////////////////////////////
///
///  2014-10-17 Heinz Spiess, Switzerland
///
///  released under Creative Commons - Attribution - Share Alike licence
//////////////////////////////////////////////////////////////////////////////////////


// a cube which is centered only on X and Y, not on Z
module cubecxy(size){
   translate([0,0,size[2]/2])cube(size,true);
}
   

module chamfered_cube(size,d=1){
   hull(){
     translate([d,d,0])cube(size-2*[d,d,0]);
     translate([0,d,0])cube(size-2*[0,d,d/2]);
     translate([d,0,0])cube(size-2*[d,0,d/2]);
   }
}


// model of a standard car fuse - used to carve out e avity 
// (the argument eps gives an additional size increase for smooth insertion) 
module carfuse(eps=[0,0,0]){
    cubecxy([18.2,5,2]+eps);
    cubecxy([18.2,1.1,10.5]+eps);
    difference(){
    cubecxy([18.2,3.5,6]+eps);
    cubecxy([16,3.6,6.1]+eps);
    }
    cubecxy([16.5,2.8,12]+eps);
    cubecxy([6.5,3.6,12]+eps);
    difference(){
      cubecxy([15.2,1.0,18.5]+eps);
      cubecxy([3.8,1.2,18.6]+eps);
    }
}


// constructs the fuse holder
module fuseholder(
  sp=4*2.54,          // wire hole spacing on PCB
  off=2,              // offset of wire holes
  size=[23,9,20],     // outer size of fuse holder
  tab=[3.5,.7],       // width and thickness of solder tabs
  wd=1.5              // diameter of wire holes 
  ){

   difference(){
      // main body
      translate([-size[0]/2,-size[1]/2,0])chamfered_cube(size);
      // grip cavity for removing fuse
      translate([0,0,size[2]-5])cubecxy([6.5,size[1]+1,6]);
      // fuse cavity 
      translate([0,0,size[2]+1])scale([1,1,-1])carfuse(eps=[0.2,0.2,0]);
      // solder tab cavities
      for(sx=[-1,1])for(sy=[-1,1])scale([1,sy,1])translate([sx*sp/2-tab[0]/2,.4,-1]){
         // diagonal channels for contact blade
         translate([0,3,0])rotate([11,0,0])cube([tab[0],tab[1],size[2]]);
	 // cavities for soldering blade to wire
         translate([0,2,0])cube([tab[0],3,3]);
	 // space for tab blades around fuse spades
         translate([0,-0.5,2])cube([tab[0],tab[1],size[2]]);
	 // horizontal wire channel
         translate([-off+tab[0],2.2,2])cubecxy([off+tab[0]+1,wd,wd]);
	 // vertical wire hole
         translate([-off,2.2,0])cylinder(r=wd/2,h=4,$fn=6);
      }
   }
}

fuseholder();
