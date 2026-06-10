//Title: Canning Jar Fruit Fly Trap
//Author: Alex English - ProtoParadigm
//Date: 3-16-2012
//License: GPL2

//Notes: This uses canning jar lid module found in http://www.thingiverse.com/thing:19105.  **Make sure to comment out the last line of canning_jar_lids.scad so it doesn't render the cap from there; it will cause the mesh not to render here.**

include <canning_jar_lids.scad>;

module fruit_fly_trap(rad)
{
	difference()
	{
		union()
		{
			cap(rad);
			cylinder(r1=rad/2, r2=0, 50); //the main cone
		}
		translate([0,0,-3]) cylinder(r1=rad/2, r2=0, 50); //hollow out the cone
		translate([0,0,43]) cylinder(r=5,10); //flatten top of cone
	}
	
}

fruit_fly_trap(reg);
//fruit_fly_trap(wide);