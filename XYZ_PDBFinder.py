import pandas as pd
import os
import math

atom_pairs = [(78, 49), (51, 54)]  # Define atom pairs
find_pdb_atoms = [78, 49, 51, 54]  # Replace with your list of atom indices from the XYZ file

# Function to read the XYZ file and extract atom information
def read_xyz(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        atom_data = [line.split() for line in lines[2:]]  # Skip the first two lines
        df_xyz = pd.DataFrame(atom_data, columns=['Atom', 'X', 'Y', 'Z'])
        df_xyz[['X', 'Y', 'Z']] = df_xyz[['X', 'Y', 'Z']].astype(float)
    return df_xyz

# Function to read the PDB file and extract relevant atom information
def read_pdb(file_path):
    atom_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                sequence_number = int(line[6:11].strip())
                atom_label = line[12:16].strip()  # Atom label (e.g., CG, ND1, CD2)
                residue_number = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                atom_lines.append([sequence_number, atom_label, residue_number, x, y, z])
    
    df_pdb = pd.DataFrame(atom_lines, columns=['Sequence', 'AtomLabel', 'Residue', 'X', 'Y', 'Z'])
    return df_pdb

# Function to match atoms from XYZ to PDB based on coordinates
def match_atoms_by_coordinates(xyz_df, pdb_df, atom_indices):
    matched_atoms = []

    for index in atom_indices:
        if index - 1 < len(xyz_df):
            xyz_atom_coords = xyz_df.iloc[index - 1][['X', 'Y', 'Z']].astype(float).round(3)

            # Find the corresponding atom in the PDB file
            matched_atom = pdb_df[(pdb_df['X'].round(3) == xyz_atom_coords['X']) &
                                  (pdb_df['Y'].round(3) == xyz_atom_coords['Y']) &
                                  (pdb_df['Z'].round(3) == xyz_atom_coords['Z'])]

            # If a match is found, format and add to the results
            if not matched_atom.empty:
                seq = matched_atom.iloc[0]['Sequence']
                atom_label = matched_atom.iloc[0]['AtomLabel']
                residue = matched_atom.iloc[0]['Residue']
                matched_atoms.append([f"Input Index: {index}", f"Seq: {seq}", f"Atom: {atom_label}", f"Residue: {residue}"])
            else:
                # If no match is found, add a placeholder indicating so
                matched_atoms.append([f"Input Index: {index}", "No match found"])
        else:
            # If the index is out of range of the XYZ file
            matched_atoms.append([f"Input Index: {index}", "Index out of range"])

    return matched_atoms

# Function to calculate the distance between two atoms
def calculate_distance(df_xyz, atom_index1, atom_index2):
    if atom_index1 - 1 < len(df_xyz) and atom_index2 - 1 < len(df_xyz):
        atom1 = df_xyz.iloc[atom_index1 - 1]
        atom2 = df_xyz.iloc[atom_index2 - 1]

        distance = math.sqrt((atom2['X'] - atom1['X']) ** 2 + 
                             (atom2['Y'] - atom1['Y']) ** 2 + 
                             (atom2['Z'] - atom1['Z']) ** 2)
        return round(distance, 3)
    else:
        return "Index out of range"

def calculate_distance_for_ash(df_xyz, atom_index1, atom_index2):
    return calculate_distance(df_xyz, atom_index1 - 1, atom_index2 - 1)

# Main function, modify only this part with your parameters:
def main():
    findsequence = True
    findbondlength = True

    xyz_file_name = "Final_Active.xyz"  # Replace with your XYZ file name
    pdb_file_name = "finalsystem.pdb"  # Replace with your PDB file name

    # Check if files exist in the current directory
    if not os.path.exists(xyz_file_name) or not os.path.exists(pdb_file_name):
        print(f"Files not found in the current directory.")
        return

    df_xyz = read_xyz(xyz_file_name)
    df_pdb = read_pdb(pdb_file_name)

    if findsequence:
        # PDB atoms for sequence matching
        matched_results = match_atoms_by_coordinates(df_xyz, df_pdb, find_pdb_atoms)
        for result in matched_results:
            print(result)

    if findbondlength:
        constraints = {'bond': []}
        for atom_index1, atom_index2 in atom_pairs:
            # Get matched results for each atom
            matched_result1 = match_atoms_by_coordinates(df_xyz, df_pdb, [atom_index1])
            matched_result2 = match_atoms_by_coordinates(df_xyz, df_pdb, [atom_index2])

            # Check if matches are found for both atoms
            if "No match found" not in matched_result1[0] and "No match found" not in matched_result2[0]:
                pdb_seq1 = matched_result1[0][1].split(": ")[1]
                pdb_seq2 = matched_result2[0][1].split(": ")[1]
                
                # Calculate distance
                distance = calculate_distance(df_xyz, atom_index1, atom_index2)
                print(f"Distance between atoms {atom_index1} and {atom_index2}: {distance} Angstroms")
                
                # Update constraints with adjusted sequence numbers and distance
                constraints['bond'].append([int(pdb_seq1) - 1, int(pdb_seq2) - 1, distance])
            else:
                print(f"No match found for atom pair ({atom_index1}, {atom_index2}). Skipping.")

        print("Constraints for Ash:")
        print("bondconstraints:",constraints)

# Running the main function
if __name__ == "__main__":
    main()