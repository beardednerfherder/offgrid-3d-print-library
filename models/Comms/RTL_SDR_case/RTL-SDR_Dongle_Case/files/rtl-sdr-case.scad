// Case for RTL-SDR
// OK1CDJ

board_length=63 + 0.5; // 
board_width=22 + 0.5; // 
board_thickness=2; // 
board_clearance_top=2;
board_clearance_bottom=2;

dongle_clearance_top=2;

usb_width=12.6; // 12.6
usb_height=4.7; // 4.7
usb_relative_z=0;

antenna_width=6.5; // 
antenna_height=8; // 
antenna_relative_z=-1;

wall_strength=1.2;

lip_strength=1;

corner_radius=1;

$fn=32;

module rounded_bottom_box(w, l, h, r) {
	inner_length = l - 2 * r;
	inner_width = w - 2 * r;
	inner_height = h - r;
	
	hull() {
		translate([-inner_width / 2, -inner_length/2, r]) cylinder(r=r, h=inner_height);
		translate([inner_width / 2, -inner_length/2, r]) cylinder(r=r, h=inner_height);
		translate([inner_width / 2, inner_length/2, r]) cylinder(r=r, h=inner_height);
		translate([-inner_width / 2, inner_length/2, r]) cylinder(r=r, h=inner_height);
		
		translate([-inner_width / 2, -inner_length/2, r]) sphere(r=r);
		translate([inner_width / 2, -inner_length/2, r]) sphere(r=r);
		translate([inner_width / 2, inner_length/2, r]) sphere(r=r);
		translate([-inner_width / 2, inner_length/2, r]) sphere(r=r);
	}
}

module case_bottom() {
	case_bottom_width=board_width + 2 * wall_strength;
	case_bottom_length=board_length + 2 * wall_strength;
	case_bottom_height=board_thickness + board_clearance_bottom + board_clearance_top + wall_strength;

	difference() {
		rounded_bottom_box(case_bottom_width, case_bottom_length, case_bottom_height, corner_radius);
		translate([0, 0, wall_strength + case_bottom_height / 2]) cube(size=[board_width - 2 * lip_strength, board_length - 2 * lip_strength, case_bottom_height], center=true); // resting area
		translate([0, 0, wall_strength + board_clearance_bottom + case_bottom_height / 2]) cube(size=[board_width, board_length, case_bottom_height], center=true); // board cutout
		
		// usb cutout
		translate([0, board_length * 0.5, wall_strength + board_clearance_bottom + usb_relative_z + usb_height / 2]) cube(size=[usb_width, 20, usb_height], center=true);
		
		// antenna cutout
	translate([10, -15, wall_strength + board_clearance_bottom + antenna_relative_z + antenna_height / 2]) cube(size=[antenna_width, 22, antenna_height], center=true);

		// lock left
		hull() {
			translate([-board_width/2, -2.5, case_bottom_height - lip_strength / 2]) sphere(r=0.4, center=true);
			translate([-board_width/2, 2.5, case_bottom_height - lip_strength / 2]) sphere(r=0.4, center=true);
		}

		// lock right
		hull() {
			translate([board_width/2, -2.5, case_bottom_height - lip_strength / 2]) sphere(r=0.3, center=true);
			translate([board_width/2, 2.5, case_bottom_height - lip_strength / 2]) sphere(r=0.3, center=true);
		}
	}
	
}

module case_top() {
	antenna_height_remainder = antenna_height - (board_thickness - antenna_relative_z) - board_clearance_top;
	usb_height_remainder = usb_height - (board_thickness - usb_relative_z) - board_clearance_top;

	// bottom part
	case_top_width=board_width + 2 * wall_strength;
	case_top_length=board_length + 2 * wall_strength;
	case_top_height=antenna_height_remainder + wall_strength + dongle_clearance_top;
	
	// top/lip part
	case_top_width_lip=case_top_width - 2 * lip_strength - 0.5;
	case_top_length_lip=case_top_length - 2 * lip_strength - 0.5;
	case_top_height_lip=case_top_height + lip_strength;
	
	union() {
		difference() {
			union() {
				rounded_bottom_box(case_top_width, case_top_length, case_top_height, corner_radius);
				translate([0,0,(case_top_height_lip - wall_strength) / 2 + wall_strength]) cube(size=[case_top_width_lip, case_top_length_lip, case_top_height_lip - wall_strength], center=true);
			}
			translate([0,0,wall_strength + case_top_height / 2]) cube(size=[case_top_width - 2 * wall_strength - 2 * lip_strength, case_top_length - 2 * wall_strength - 2 * lip_strength, case_top_height], center=true);
			
			// usb cutout
			translate([0, board_length * 0.5, wall_strength + dongle_clearance_top + antenna_height_remainder - usb_height_remainder + usb_height / 2]) cube(size=[usb_width, 20, usb_height], center=true);
			
			// antenna cutout
		translate([-10, -15, wall_strength + dongle_clearance_top + antenna_height / 2]) cube(size=[antenna_width, 22, antenna_height], center=true);


			// logo
			rotate([0,0,180]) translate([-1, 0.5]) scale([0.37, 0.37, 1.5]) import("logo.stl");
		}
		
		// lock left
		hull() {
			translate([-case_top_width/2 + wall_strength, -2.5, case_top_height_lip - lip_strength / 2]) sphere(r=0.2, center=true);
			translate([-case_top_width/2 + wall_strength, 2.5, case_top_height_lip - lip_strength / 2]) sphere(r=0.2, center=true);
		}

		// lock right
		hull() {
			translate([case_top_width/2 - wall_strength, -2.5, case_top_height_lip - lip_strength / 2]) sphere(r=0.2, center=true);
			translate([case_top_width/2 - wall_strength, 2.5, case_top_height_lip - lip_strength / 2]) sphere(r=0.2, center=true);
		}


	}
}

case_bottom();
translate([board_width + 2 * wall_strength + 5, 0, 0]) case_top(); 
