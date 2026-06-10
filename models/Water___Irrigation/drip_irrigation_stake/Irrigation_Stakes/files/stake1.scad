// Garden irrigation hose stake by Brian Enigma
// The defaults are designed for a 1/4" hose.  Feel free to adjust as needed.

// This is the inside diameter of the hook part.  Coincidentally, it's also the
// outside diameter of your hose.
INSIDE_DIAMETER = 6;

// This is the overall length of the stake
LENGTH = 110;

// This is the height (or thickness, depending on how you look at it) of the 
// tallest part of the stake -- the thickness of the reinforcing ring and
// bars.
HEIGHT = 5;

// This is the thickness of all the rest of the stake that isn't a reinforcing
// ring or bar.
THICKNESS = 2;

// This is the diameter of the biggest plastic circle.
CLIP_OUTSIDE_DIAMETER = 12;

// This is the clearance you get on the slot to insert the hose.  A smaller
// value gives you a tighter fit, but it also makes the hose more difficult
// to insert.
SLOT_DIAMETER = 4;

// The detail (number of sides) of the circles.
DETAIL = 50;

//###################################################################### 

REINFORCEMENT_OUTSIDE_DIAMETER = INSIDE_DIAMETER + THICKNESS;

module clip()
{
    union()
    {
        // Cylinder for holding the hose
        cylinder(h = HEIGHT, r = REINFORCEMENT_OUTSIDE_DIAMETER / 2, $fn = DETAIL);
        // Outermost cylinder
        cylinder(h = THICKNESS, r = CLIP_OUTSIDE_DIAMETER / 2, $fn = DETAIL);
        // Y-axis reinforcement bar
        translate(v = [THICKNESS / -2, 0, 0])
            cube(size = [THICKNESS, CLIP_OUTSIDE_DIAMETER / 2, HEIGHT]);
        // X-axis reinforcement bar
        translate(v = [CLIP_OUTSIDE_DIAMETER / -2, THICKNESS / -2, 0])
            cube(size = [CLIP_OUTSIDE_DIAMETER, THICKNESS, HEIGHT]);
    }
}

module clip_hole()
{
    translate(v = [0, 0, -1])
        cylinder(h = HEIGHT + 2, r = INSIDE_DIAMETER / 2, $fn = DETAIL);
    translate(v = [0, SLOT_DIAMETER / -2, -1])
        cube(size = [CLIP_OUTSIDE_DIAMETER, SLOT_DIAMETER, HEIGHT + 2]);
}

module stake()
{
    linear_extrude(height = THICKNESS)
        polygon(points = [[CLIP_OUTSIDE_DIAMETER / 2, 0], [0, -1 * LENGTH], [CLIP_OUTSIDE_DIAMETER / -2, 0]]);
    linear_extrude(height = HEIGHT)
        polygon(points = [[THICKNESS / 2, 0], [0, -1 * LENGTH], [THICKNESS / -2, 0]]);

}

translate(v = [LENGTH / -2, 0, 0])
rotate(a = [0, 0, 90])
difference()
{
    union()
    {
        clip();
        stake();
    }
    clip_hole();
}

