// Garden irrigation hose stake 2 by Brian Enigma

// This is the thickest part, up at the top of the stake
OUTSIDE_DIAMETER = 18;

// This is the overall length of the stake
LENGTH = 145;

// This is the height (or thickness, depending on how you look at it) of the 
// tallest part of the stake -- the bar running its length.
HEIGHT = 4.5;

// This is the thickness of all the rest of the stake that isn't a reinforcing
// ring or bar.
THICKNESS = 3.5;

// These are the diameters of the four circles.
CIRCLE1 = 6.5;
CIRCLE2 = 5.5;
CIRCLE3 = 4.5;
CIRCLE4 = 3.5;

// The detail (number of sides) of the circles.
DETAIL = 50;

//###################################################################### 

CIRCLE1_OFFSET = CIRCLE1 / 2 + 2;
CIRCLE2_OFFSET = CIRCLE1 + 2 + CIRCLE2 / 2 + 2;
CIRCLE3_OFFSET = CIRCLE1 + 2 + CIRCLE2 + 2 + CIRCLE3 / 2 + 2;
CIRCLE4_OFFSET = CIRCLE1 + 2 + CIRCLE2 + 2 + CIRCLE3 + 2 + CIRCLE4 / 2 + 2;
BAR_OFFSET = CIRCLE4_OFFSET + CIRCLE4 / 2 + 4;
BAR_LENGTH = LENGTH - BAR_OFFSET - 15;

module body()
{
    union()
    {
        linear_extrude(height = THICKNESS)
            polygon(points = [[OUTSIDE_DIAMETER / 2, 0], [0, -1 * LENGTH], [OUTSIDE_DIAMETER / -2, 0]]);
        translate(v = [-0.5, -1 * BAR_OFFSET - BAR_LENGTH, 0])
            cube(size = [1, BAR_LENGTH, HEIGHT]);
    }
}

module holes()
{
    translate(v = [0, -1 * CIRCLE1_OFFSET, -1])
        cylinder(h = HEIGHT + 2, r = CIRCLE1 / 2, $fn = DETAIL);
    translate(v = [0, -1 * CIRCLE2_OFFSET, -1])
        cylinder(h = HEIGHT + 2, r = CIRCLE2 / 2, $fn = DETAIL);
    translate(v = [0, -1 * CIRCLE3_OFFSET, -1])
        cylinder(h = HEIGHT + 2, r = CIRCLE3 / 2, $fn = DETAIL);
    translate(v = [0, -1 * CIRCLE4_OFFSET, -1])
        cylinder(h = HEIGHT + 2, r = CIRCLE4 / 2, $fn = DETAIL);
    translate(v = [0, 0, -1])
        linear_extrude(height = THICKNESS + 2)
            polygon(points = [
                [CIRCLE1 / 3, 1], 
                [CIRCLE4 / 5, -1 * CIRCLE4_OFFSET], 
                [CIRCLE4 / -5, -1 * CIRCLE4_OFFSET], 
                [CIRCLE1 / -3, 0]]);
}

translate(v = [LENGTH / -2, 0, 0])
rotate(a = [0, 0, 90])
difference()
{
    body();
    holes();
}

