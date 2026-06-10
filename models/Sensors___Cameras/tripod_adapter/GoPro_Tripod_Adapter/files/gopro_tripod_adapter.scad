union(){
rotate([90,0,90])linear_extrude(height = 37, center = true, convexity = 10)
polygon(points=[[-18.5,0],[18.5,0],[18.5,3],[13.5,8],[18,10],[-18,10],[-13.5,8],[-18.5,3]], paths=[[0,1,2,3,4,5,6,7]]);
translate([-5, 0, 0])rotate([90, 0, 0])linear_extrude(height = 27, center = true, convexity = 10)
polygon(points=[[-13.5, 8], [-13.5, 10], [-18, 10]], paths=[[0,1,2]]);

translate([5, 0, 0])rotate([90, 0, 0])linear_extrude(height = 27, center = true, convexity = 10)
polygon(points=[[13.5, 8], [13.5, 10], [18, 10]], paths=[[0,1,2]]);
translate([0,1,-0.75])difference(){
	translate([-390,-72,0])import("fixed_large_v1.stl");
	translate([-40,-30,-9.4])cube([70,60,20]);
}
}