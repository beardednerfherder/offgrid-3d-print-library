difference() {
    //Basic shape
    union() {
        // Cone, face
        cylinder(d2=55.6, d1=50, h=3.5 );
        // Cylinder, interior clip
        cylinder(d=47.0, h=14.21);
        
        // upper wedge on clip
        translate(v=[0,0,12])
            cylinder(d2=0, d1=50, h=40);
        // lower wedge on clip
        translate(v=[0,0,-28])
            cylinder(d1=0, d2=50, h=40);
    };
    
    // Cut out the interior of interior clip
    translate(v=[0,0,3.5])
        cylinder( d=42, h=100);
    // Slice off top and bottom of the cap
    translate([0,0,-50])
        cube(center=true,[100,100,100]);
    translate([0,0,64.50])
        cube(center=true,[100,100,100]);

    // Cut out 3 Slots using long cubes, rotated three times
    for( i = [0:2]) {
        rotate(a=[0,0,120*i])
            translate([0, 0, 30])
                cube(center=true,[100, 12, 50]);
    };

    //pry point / cut out;
       translate([28, 0, 7])
          cube(center=true,[10, 10, 10]);

    
}