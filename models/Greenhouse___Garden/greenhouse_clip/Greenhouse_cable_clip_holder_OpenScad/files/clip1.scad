// base to fit on standard cut off 2litre plastic bottle
// h is height of whole shape
h=20;

difference(){
    cylinder(h, 10, 10, $fn=80);
    cylinder(h, 8, 8, $snf=80);
    translate([-15,4,0]){
    cube([30,30,40]);
    // thickness of base
  
}}
translate([8,0,0]){
    difference(){
    cube([2,30,20]);
    translate([0,20,10]){
    rotate([0,90,0]){
    cylinder(20, 3, 3);
}}}}

translate([2,27,0]){
 difference(){
    cylinder(h, 10, 10, $fn=80);
    cylinder(h, 8, 8, $snf=80);
    translate([-15,-16,0]){
    cube([30,20,40]);
    translate([23,10,0]){
        cube([25,20,20]);}
    // thickness of base
  
 }}
 translate([6,6,0]){
    difference(){
    cube([2,24,20]);
    translate([0,14,10]){
    rotate([0,90,0]){
    cylinder(20, 3, 3);
 }}}}
}