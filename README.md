# Airfoil Geometry Generator for Tandem Configuration

This Python script generates `.geo` files for airfoil geometries, considering various transformations such as rotation (for angle of attack), scaling (for chord lengths), and shifting (for tandem configurations). It also includes the option to invert the airfoils vertically. The generated files are used for computational fluid dynamics (CFD) simulations or mesh generation in programs like OpenFOAM or GMSH.

## Features

- **Scaling**: Adjusts the chord length of both the main and flap airfoils.
- **Rotation**: Rotates the airfoils by a specified angle of attack (AoA).
- **Translation**: Shifts the flap airfoil for tandem configuration.
- **Inversion**: Option to flip the airfoils vertically (as in mirrored configurations).
- **File Naming**: Dynamic generation of the output file name based on the parameters, ensuring unique and informative filenames.

## File Format

The input data is read from a `.txt` file containing airfoil coordinates. The output is a `.geo` file with the following properties:
- Points defining the geometry of both the main and flap airfoils.
- Spline definitions for both airfoils.
- A unique file name based on the provided parameters (AoA, chord lengths, shifts, and inversion).

## Requirements

- Python 3.x
- No additional libraries are required as the script uses built-in Python modules (`math`, `os`, `re`).

## Usage

### Step 1: Prepare the Input File
- The input file must be in the following format:
  - The first line should contain a header (e.g., `ch10sm`).
  - The second line should be empty or can contain any other text (it will be skipped).
  - Subsequent lines should contain airfoil coordinates, where each line consists of:
    - X and Y coordinates for the main airfoil.
    - (Optional) Additional X and Y coordinates for the flap airfoil.


### Step 2: Modify Parameters in the Script
Modify the parameters in the script to match your airfoil's characteristics:

- `main_chord_length` (Default: `1.0`): The chord length for the main airfoil (in meters).
- `flap_chord_length` (Default: `1.0`): The chord length for the flap airfoil (in meters).
- `angle_of_attack_main` (Default: `10`): Angle of attack for the main airfoil (in degrees).
- `angle_of_attack_flap` (Default: `45`): Angle of attack for the flap airfoil (in degrees).
- `xflap_shift` (Default: `0.5`): Horizontal shift for the flap airfoil (in meters).
- `yflap_shift` (Default: `0.2`): Vertical shift for the flap airfoil (in meters).
- `inverted` (Default: `True`): Whether to invert the airfoil vertically (set to `True` for inversion).

### Step 3: Run the Script

To generate the `.geo` file, run the script.
