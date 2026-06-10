/********************************************************************
How to use this OpenScad code:                                   
  Call the "socket_holder" module passing your parameters. See 
  below example of 4 socket_holders with connectors to allow for 
  printing on 220mm wide 3D printers and connecting after.
 
DESCRIPTION OF PARAMETERS:
  NUM_SOCKETS = number of holes.
  SOCKET_BOX_WIDTH = X-axis width (in mm) of each box surrounding the socket hole.
  SOCKET_BOX_LENGTH = Y-axis length (in mm) of each box surrounding the socket hole.
  SOCKET_BOX_HEIGHT = Z-axis height (in mm) of each box surrounding the socket hole.
  SOCKET_DIAMETER = array of actual socket sizes (in mm). Measure your sockets and input these values.
  SOCKET_TEXT = array of text to be displayed.
  SOCKET_TEXT_SIZE = Font size of text.
  SOCKET_TEXT_OFFSET_Y = Y-axis offset of text
  SOCKET_TEXT_OFFSET_Z = Z-axis offset of text (play around with these when changing height).
  CONNECTOR_MALE_RIGHT = Add male connector to right
  CONNECTOR_FEMALE_RIGHT = Add female connector to right
  CONNECTOR_MALE_LEFT  = Add male connector to left
  CONNECTOR_FEMALE_LEFT = Add female connector to left
  CONNECTOR_RIGHT_EXTRA = When using female connectors, extend text object to right
  CONNECTOR_LEFT_EXTRA = = When using female connectors, extend text object to left
*******************************************************************/

//Shouldn't need to modify these!
$fn = 100;
SOCKET_RELIEF = 1.5;              //Gap between socket size and hole
BOTTOM_THICKNESS = 2;             //Bottom plate thickness
SOCKET_TEXT_HEIGHT = 1;           //Raised lettering
TEXT_BOX_LENGTH = 10;             //Length of angled text object


/**********************************/
/* EXAMPLE
/**********************************/
//SHALLOW SOCKET HOLDER PART 1
SOCKET_BOX_LENGTH = 35;
socket_holder(
  4,                                          //NUM_SOCKETS
  26,                                         //SOCKET_BOX_WIDTH
  SOCKET_BOX_LENGTH,                          //SOCKET_BOX_LENGTH
  15,                                         //SOCKET_BOX_HEIGHT
  [17.9,17.9,19.9,19.9],                      //SOCKET_DIAMETER
  ["3/8","7/16","1/2","9/16"],                //SOCKET_TEXT
  8,                                          //SOCKET_TEXT_SIZE
  -4,                                         //SOCKET_TEXT_OFFSET_Y
  -6.6,                                       //SOCKET_TEXT_OFFSET_Z
  "FALSE",                                     //CONNECTOR_MALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 0
  "TRUE",                                    //CONNECTOR_FEMALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 5
  "FALSE",                                    //CONNECTOR_MALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 0
  "FALSE",                                    //CONNECTOR_FEMALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 5
  5,                                          //CONNECTOR_RIGHT_EXTRA
  0                                           //CONNECTOR_LEFT_EXTRA
);

//DEEP SOCKET HOLDER PART 1
translate([0,SOCKET_BOX_LENGTH+TEXT_BOX_LENGTH,0])
socket_holder(
  4,                                          //NUM_SOCKETS
  26,                                         //SOCKET_BOX_WIDTH
  SOCKET_BOX_LENGTH,                          //SOCKET_BOX_LENGTH
  40,                                         //SOCKET_BOX_HEIGHT
  [17.9,17.9,19.9,19.9],                      //SOCKET_DIAMETER
  ["3/8","7/16","1/2","9/16"],                //SOCKET_TEXT
  8,                                          //SOCKET_TEXT_SIZE
  13.5,                                       //SOCKET_TEXT_OFFSET_Y
  11.1,                                       //SOCKET_TEXT_OFFSET_Z
  "TRUE",                                     //CONNECTOR_MALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 0
  "FALSE",                                    //CONNECTOR_FEMALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 5
  "FALSE",                                    //CONNECTOR_MALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 0
  "FALSE",                                    //CONNECTOR_FEMALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 5
  0,                                          //CONNECTOR_RIGHT_EXTRA
  0                                           //CONNECTOR_LEFT_EXTRA
);

//SHALLOW SOCKET HOLDER PART 2
translate([118,0,0])
socket_holder(
  4,                                          //NUM_SOCKETS
  35,                                         //SOCKET_BOX_WIDTH
  SOCKET_BOX_LENGTH,                          //SOCKET_BOX_LENGTH
  15,                                         //SOCKET_BOX_HEIGHT
  [23.9,23.9,27.9,29.9],                      //SOCKET_DIAMETER
  ["5/8","11/16","3/4","13/16"],              //SOCKET_TEXT
  8,                                          //SOCKET_TEXT_SIZE
  -4,                                         //SOCKET_TEXT_OFFSET_Y
  -6.6,                                       //SOCKET_TEXT_OFFSET_Z
  "FALSE",                                    //CONNECTOR_MALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 0
  "FALSE",                                    //CONNECTOR_FEMALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 5
  "TRUE",                                    //CONNECTOR_MALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 0
  "FALSE",                                     //CONNECTOR_FEMALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 5
  0,                                          //CONNECTOR_RIGHT_EXTRA
  0                                           //CONNECTOR_LEFT_EXTRA
);

//DEEP SOCKET HOLDER PART 2
translate([118,SOCKET_BOX_LENGTH+TEXT_BOX_LENGTH,0])
socket_holder(
  4,                                          //NUM_SOCKETS
  35,                                         //SOCKET_BOX_WIDTH
  SOCKET_BOX_LENGTH,                          //SOCKET_BOX_LENGTH
  40,                                         //SOCKET_BOX_HEIGHT
  [23.9,23.9,27.9,29.9],                      //SOCKET_DIAMETER
  ["5/8","11/16","3/4","13/16"],              //SOCKET_TEXT
  8,                                          //SOCKET_TEXT_SIZE
  13.5,                                       //SOCKET_TEXT_OFFSET_Y
  11.1,                                       //SOCKET_TEXT_OFFSET_Z
  "FALSE",                                    //CONNECTOR_MALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 0
  "FALSE",                                    //CONNECTOR_FEMALE_RIGHT. If TRUE, set CONNECTOR_RIGHT_EXTRA = 5
  "FALSE",                                    //CONNECTOR_MALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 0
  "TRUE",                                     //CONNECTOR_FEMALE_LEFT. If TRUE, set CONNECTOR_LEFT_EXTRA = 5
  0,                                          //CONNECTOR_RIGHT_EXTRA
  5                                           //CONNECTOR_LEFT_EXTRA
);









//MODULE
module socket_holder (NUM_SOCKETS,SOCKET_BOX_WIDTH,SOCKET_BOX_LENGTH,SOCKET_BOX_HEIGHT,SOCKET_DIAMETER,SOCKET_TEXT,SOCKET_TEXT_SIZE,SOCKET_TEXT_OFFSET_Y,SOCKET_TEXT_OFFSET_Z,CONNECTOR_MALE_RIGHT,CONNECTOR_FEMALE_RIGHT,CONNECTOR_MALE_LEFT,CONNECTOR_FEMALE_LEFT,CONNECTOR_RIGHT_EXTRA,CONNECTOR_LEFT_EXTRA){

  for (i=[0:1:NUM_SOCKETS-1]){
    difference() {  
      //SOCKET CUBE
      //translate([i*SOCKET_BOX_WIDTH,TEXT_BOX_LENGTH,0]) cube([SOCKET_BOX_WIDTH,SOCKET_BOX_LENGTH,SOCKET_BOX_HEIGHT]);
      translate([i*SOCKET_BOX_WIDTH,TEXT_BOX_LENGTH,0]) cube([SOCKET_BOX_WIDTH,SOCKET_BOX_LENGTH,SOCKET_BOX_HEIGHT]);
      
      //SOCKET HOLES
      translate([(i*SOCKET_BOX_WIDTH)+(SOCKET_BOX_WIDTH/2),SOCKET_BOX_LENGTH/2+TEXT_BOX_LENGTH, BOTTOM_THICKNESS-0.1]) cylinder(d = SOCKET_DIAMETER[i]+SOCKET_RELIEF, h = SOCKET_BOX_HEIGHT - BOTTOM_THICKNESS + 1);  
    }
      
      //TEXT
      rotate([45,0,0]) translate([i*(SOCKET_BOX_WIDTH)+(SOCKET_BOX_WIDTH/2)-(len(SOCKET_TEXT[i])*2.5),TEXT_BOX_LENGTH+SOCKET_TEXT_OFFSET_Y,TEXT_BOX_LENGTH+SOCKET_TEXT_OFFSET_Z]) linear_extrude(SOCKET_TEXT_HEIGHT) text(SOCKET_TEXT[i],SOCKET_TEXT_SIZE);
  }

  //TEXT CUBE    
  translate([SOCKET_BOX_WIDTH*NUM_SOCKETS+CONNECTOR_RIGHT_EXTRA,0,0]) rotate([0,-90,0]) linear_extrude(SOCKET_BOX_WIDTH*NUM_SOCKETS+CONNECTOR_LEFT_EXTRA+CONNECTOR_RIGHT_EXTRA) polygon(points=[[0,0],[0,TEXT_BOX_LENGTH],[SOCKET_BOX_HEIGHT,TEXT_BOX_LENGTH],[SOCKET_BOX_HEIGHT-10,0]], paths=[[0,1,2,3]]);
  
  //CONNECTORS
  if(CONNECTOR_MALE_RIGHT == "TRUE"){
    difference() {  
      rotate([0,0,180]) translate([((NUM_SOCKETS*SOCKET_BOX_WIDTH)*-1),-28,0]) cylinder(r=10, h=SOCKET_BOX_HEIGHT, $fn=3);
      
      translate([((NUM_SOCKETS-1)*SOCKET_BOX_WIDTH)+(SOCKET_BOX_WIDTH/2),SOCKET_BOX_LENGTH/2+TEXT_BOX_LENGTH, BOTTOM_THICKNESS-0.1]) cylinder(d = SOCKET_DIAMETER[NUM_SOCKETS-1]+SOCKET_RELIEF, h = SOCKET_BOX_HEIGHT - BOTTOM_THICKNESS + 1); 
    }
  }  
  if(CONNECTOR_MALE_LEFT == "TRUE"){
    difference() {  
      translate([0,28,0]) cylinder(r=10, h=SOCKET_BOX_HEIGHT, $fn=3);
      
      translate([(SOCKET_BOX_WIDTH/2),SOCKET_BOX_LENGTH/2+TEXT_BOX_LENGTH, BOTTOM_THICKNESS-0.1]) cylinder(d = SOCKET_DIAMETER[0]+SOCKET_RELIEF, h = SOCKET_BOX_HEIGHT - BOTTOM_THICKNESS + 1);   
    }
  }
  if(CONNECTOR_FEMALE_RIGHT == "TRUE"){      
    difference() {  
      translate([NUM_SOCKETS*SOCKET_BOX_WIDTH,TEXT_BOX_LENGTH,0]) cube([CONNECTOR_RIGHT_EXTRA,SOCKET_BOX_LENGTH,SOCKET_BOX_HEIGHT]);
      
      translate([(NUM_SOCKETS*SOCKET_BOX_WIDTH)+5,28,-0.5]) cylinder(r=10, h=SOCKET_BOX_HEIGHT+1, $fn=3);       
    }
  }
  if(CONNECTOR_FEMALE_LEFT == "TRUE"){
    difference() {  
       translate([-CONNECTOR_LEFT_EXTRA,TEXT_BOX_LENGTH,0]) cube([CONNECTOR_LEFT_EXTRA,SOCKET_BOX_LENGTH,SOCKET_BOX_HEIGHT]);
      
      rotate([0,0,180]) translate([(SOCKET_BOX_WIDTH/2)-13,-28,-0.5]) cylinder(r=10, h=SOCKET_BOX_HEIGHT+1, $fn=3);
    }
  }
}

