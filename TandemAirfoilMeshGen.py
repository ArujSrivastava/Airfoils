import math
import re
import os

# Function to scale airfoil coordinates
def scale_airfoil(coords, scale_factor_x, scale_factor_y=1.0):
    return [(x * scale_factor_x, y * scale_factor_y) for x, y in coords]

# Function to rotate coordinates
def rotate(coords, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for x, y in coords]

# Function to read coordinates from a file
def read_airfoil_coordinates(input_file):
    main_coords = []
    flap_coords = []
    with open(input_file, 'r') as fin:
        header1 = fin.readline().strip()  # Read the first header
        fin.readline()  # Skip the second header
        for line in fin:
            coords = list(map(float, line.split()))
            main_coords.append(coords[:2])
            if len(coords) > 2:
                flap_coords.append(coords[2:])
    return header1, main_coords, flap_coords

# Function to generate the output file name
def generate_file_name(header1, aoa_main, aoa_flap, chord_main, chord_flap, xflap_shift, yflap_shift, inverted):
    sanitized_header = header1.replace(" ", "").replace("\t", "")
    aoa_part = f"{int(aoa_main)}{int(aoa_flap)}_"
    chord_part = f"{str(chord_main).replace('.', '')}{str(chord_flap).replace('.', '')}_"
    shift_part = f"{int(xflap_shift)}{int(yflap_shift)}_"
    inverted_flag = "I_" if inverted else ""
    return f"{sanitized_header}_{aoa_part}{chord_part}{shift_part}{inverted_flag}"

# Function to generate the .geo file
def generate_geo_file(input_file_path, output_dir, main_chord_length=1.0, flap_chord_length=1.0,
                      angle_of_attack_main=10, angle_of_attack_flap=45, xflap_shift=0.5, yflap_shift=0.2, inverted=True):
    # Read coordinates
    header1, main_coords, flap_coords = read_airfoil_coordinates(input_file_path)

    # Invert airfoil coordinates if required
    inverted_main_coords = [(x, -y) for x, y in main_coords] if inverted else main_coords
    inverted_flap_coords = [(x, -y) for x, y in flap_coords] if inverted else flap_coords

    # Scale airfoils based on chord length
    scaled_main_coords = scale_airfoil(inverted_main_coords, main_chord_length)
    scaled_flap_coords = scale_airfoil(inverted_flap_coords, flap_chord_length)

    # Rotate airfoils for specified AoA
    rotated_main_coords = rotate(scaled_main_coords, angle_of_attack_main)
    rotated_flap_coords = rotate(scaled_flap_coords, angle_of_attack_flap)

    # Shift flap airfoil for tandem configuration
    shifted_flap_coords = [(x + xflap_shift, y + yflap_shift) for x, y in rotated_flap_coords]

    # Generate dynamic file name
    output_file_name = generate_file_name(
        header1, angle_of_attack_main, angle_of_attack_flap,
        main_chord_length, flap_chord_length, xflap_shift, yflap_shift, inverted
    )
    output_file_path = os.path.join(output_dir, f"{output_file_name}.geo")

    # Check if the file already exists
    if os.path.exists(output_file_path):
        print(f"File '{output_file_path}' already exists.")
        return  # Exit the function if the file exists

    # Write the output file if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file_path, 'w') as fout:
        # Write main airfoil points
        for i, c in enumerate(rotated_main_coords):
            fout.write('Point (%i) = {%f, %f, 0, 1};\n' % (i + 1, c[0], c[1]))

        # Write flap airfoil points
        for i, c in enumerate(shifted_flap_coords):
            fout.write('Point (%i) = {%f, %f, 0, 1};\n' % (i + len(rotated_main_coords) + 1, c[0], c[1]))

        # Define splines
        fout.write('Spline (1) = {%s};\n' % ','.join(map(str, range(1, len(rotated_main_coords) + 1))))
        fout.write('Spline (2) = {%s};\n' % ','.join(map(str, range(len(rotated_main_coords) + 1,
                                                                    len(rotated_main_coords) + len(shifted_flap_coords) + 1))))

    print(f"File written: {output_file_path}")

# Example usage
input_file = 'ch10sm_naca6412.txt'
output_dir = 'bin'

generate_geo_file(
    input_file_path=input_file,
    output_dir=output_dir,
    main_chord_length=1,  # Chord length for main airfoil
    flap_chord_length=1,  # Chord length for flap airfoil
    angle_of_attack_main=5,  # AoA for main airfoil
    angle_of_attack_flap=10,  # AoA for flap airfoil
    xflap_shift=1,  # Shift in x-direction for flap
    yflap_shift=1,  # Shift in y-direction for flap
    inverted=True  # Whether the airfoil is inverted
)
