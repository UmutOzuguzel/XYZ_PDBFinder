# XYZ_PDBFinder
This Python script is developed for computational chemistry applications, specifically to interface between XYZ and PDB molecular structure file formats.
# Match XYZ to PDB and Calculate Bond Lengths

This Python script is developed for computational chemistry applications, specifically to interface between a smaller XYZ file and a larger PDB file that contains the atoms in XYZ file.

The script can also give an Ash constraints to be inputted for MD or QM/MM applications. 

## Related Resources

For input related to the Ash molecular simulation tool, see the Ash repository: [Ash Input Repository](https://github.com/RagnarB83/ash)

## Features

- **Atom Matching Between XYZ and PDB**: Locates and matches atoms from an XYZ file with their counterparts in a PDB file, based on 3D coordinates.

- **Sequence and Residue Number Extraction**: Identifies each matched atom from the XYZ file in the PDB file, extracting both the sequence number and the residue number.

- **Bond Length Calculation**: Calculates the bond lengths between pairs of atoms defined in the `atom_pairs` list, using the spatial coordinates of atoms in the XYZ file.

- **Constraints for Ash**: Generates a list of constraints suitable for use in Ash, a molecular simulation tool, based on the calculated bond lengths.

- **Useful for Molecular Dynamics and QM/MM Simulations**: Facilitates the handling of large numbers of atoms in a PDB file, streamlining simulations and analyses.

## Usage Instructions

### Preparing Your Data

1. **Visualize PDB Structure**: Use PyMOL or similar software to identify the site of interest in your PDB file.

2. **Export XYZ**: Export the coordinates of the targeted atoms into an XYZ file.

3. **Note Atom Sequence Numbers**: Record the sequence numbers of these atoms from simplified XYZ file for later use.

### Setting Up

1. **Install Required Packages**: Ensure all dependencies are installed:

'pip install -r requirements.txt'

2. **Configure Script**: Modify the `atom_pairs` list in the script to include your atom pairs for bond lengths between them / constraints. Set `xyz_file_name` and `pdb_file_name` to your file names. Input the atom indices you want to find from the XYZ file in the PDB file.

### Running the Script

1. **Execute**: Run `python script_name.py` in your Python environment, include the .xyz and .pdb file in the directory.

2. **Review Output**: Check the script's output for matched sequence numbers, residue numbers, bond lengths, and constraints for Ash.

## To be done
Input for Orca bond constraints

