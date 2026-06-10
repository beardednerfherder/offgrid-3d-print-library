
length = 50;
pipe_od = 25;
pipe_thickness = 1.9;

difference() {
    union() {
        cylinder(h=length, d=pipe_od);
        rotate([0,90,0]) cylinder(h=length, d=pipe_od);
        rotate([0,90,90]) cylinder(h=length, d=pipe_od);
        intersection() {
            translate([-pipe_od/2, -pipe_od/2, -pipe_od/2]) cube(pipe_od/2);
            sphere((pipe_od/2));
        };
    }
    cylinder(h=length, d= (pipe_od-(2*pipe_thickness)));
    rotate([0,90,0]) cylinder(h=length, d= (pipe_od-(2*pipe_thickness)));
    rotate([0,90,90]) cylinder(h=length, d= (pipe_od-(2*pipe_thickness)));
    sphere((pipe_od-pipe_thickness)/2);
}

module support() {
    linear_extrude(pipe_thickness)
    polygon(points=[[pipe_od/2,pipe_od/2],[pipe_od/2,length-(pipe_od/2)],[length-(pipe_od/2),pipe_od/2]]);
    
}

support();
rotate([0,-90,0]) support();
rotate([90,0,0]) support();
