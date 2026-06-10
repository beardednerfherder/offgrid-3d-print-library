// License:  Creative Commons Attribtion-NonCommercial-ShareAlike
// http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode
//
// Author: Jetty, 7th July, 2012
//
//
// U Clip, to clip sheeting to PVC piping

quantity = 9;	//Quantity is set to 1 or 9

insideDiameter = 25.4;
thickness = 3;
length = 60;
flangeDistanceMult = 0.75;
flangeTerminateMult = 0.5;


manifoldCorrection = 0.04;

$fn = 80;

cubeSize = insideDiameter + thickness * 2;
distanceBetween = insideDiameter + thickness * 2 + 3;


if ( quantity == 9 )
{
	for ( x = [0:2] )
	{
		for ( y = [0:2] )
		{
			translate( [x * distanceBetween, y * distanceBetween, 0] )
				pvcClip();
		}
	}
}
else	pvcClip();


//Creates a Pvc Clip

module pvcClip()
{
	difference()
	{
		union()
		{
			hollowCylinder( r = insideDiameter / 2 + thickness, h = length, thickness = thickness );
		
			translate( [0, flangeDistanceMult * insideDiameter, 0] )
				hollowCylinder( r = insideDiameter / 2 + thickness, h = length, thickness = thickness );
		}
	
		translate( [0, 0, -manifoldCorrection] )
			cylinder( r = insideDiameter / 2, h = length + manifoldCorrection * 2);

		translate( [0, flangeDistanceMult * insideDiameter, -manifoldCorrection] )
			cylinder( r = insideDiameter / 2, h = length + manifoldCorrection * 2);

		translate( [-cubeSize / 2, -cubeSize / 2 - insideDiameter * flangeTerminateMult, -manifoldCorrection] )
			cube( [cubeSize, cubeSize, length + manifoldCorrection * 2] );
	}
}



//Creates a hollow cylinder

module hollowCylinder(r, h, thickness)
{
	difference()
	{
		cylinder( r=r, h = h);
		translate( [0, 0, -manifoldCorrection] )
			cylinder( r=r-thickness, h = h + manifoldCorrection * 2 );
	}
}

