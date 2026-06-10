//Title: Canning Jar Sprouter
//Author: Alex English - ProtoParadigm
//Date: 8-12-2012
//License: GPL2

//Notes: This uses canning jar lid module found in http://www.thingiverse.com/thing:19105.  **Make sure to comment out the last line of canning_jar_lids.scad so it doesn't render the cap from there; it will cause the mesh not to render here.**

// This also relies on Fine Mesh Screen (http://www.thingiverse.com/thing:27805).  Like in the other file, make sure to comment out the lines that render the module in order to use it.

//While this is set up to be generated as a wide-mouth or a regular sized lid, a wide mouth lid is recommended if you have jars in both sizes available because the greater surface area drains through sprout seeds much faster.

include <canning_jar_lids.scad>;
include <meshscreen.scad>;

tracewidth = 0.45;
layerheight = 0.2;

module sprouter(rad)
{
	difference() {
		cap(rad);
		translate([0,0,-0.1]) cylinder(r=(rad-9), 3);
	}
	intersection()
	{
		mesh_raw(h=1.2,mesh_w=tracewidth,mesh_space=1,width=(rad-9)*2,layer_h=layerheight);
		translate([0,0,-0.1]) cylinder(r=(rad-9), 3);
	}
}

//sprouter(reg);
sprouter(wide);


