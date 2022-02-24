#!/usr/env/python3
import MDAnalysis as mda

pdb_in="preopt_structure.pdb"
lichem_in_xyz="optimization_output.xyz"
lichem_out_pdb="updated_coords.pdb"

def load_XYZ(lichem_in_xyz):
    """
    Load in the LICHEM XYZ.

    Parameters
    ----------
    lichem_in_xyz: str
        The path to/name of the optimized LICHEM XYZ file.

    Returns
    -------
    system : MDAnalysis.core.universe.Universe
        The LICHEM XYZ.
    """
    system = mda.Universe(lichem_in_xyz, format="XYZ", dt=1.0, in_memory=True)
    #
    for atom in system.atoms:
        atom.segment.segid = ''
    #
    ## Set to final XYZ frame
    system.universe.trajectory[-1]
    #
    return system

def read_orig_PDB(pdb_in):
    """
    Load in the PDB file with manipulated atom coordinates.

    Parameters
    ----------
    pdb_in : str
        A PDB file from before LICHEM/TINKER conversion.
    Returns
    -----
    og_sys : MDAnalysis.core.universe.Universe
        The PDB file.
    """
    og_sys = mda.Universe(pdb_in, format="PDB", dt=1.0, in_memory=True)
    return og_sys

def integrate_movements(system, og_sys, lichem_out_pdb):
    """
    Generate the PDB file with the replacement QM atom coordinates.

    Parameters
    ----------
    system : MDAnalysis.core.universe.Universe
        The LICHEM XYZ.
    og_sys : MDAnalysis.core.universe.Universe
        The original PDB.
    lichem_out_pdb : str
        Name for the output file.
    Saves
    -----
    lichem_out_pdb : PDB file
        A PDB file with the updated optimized QM/MM coordinates.
    """
    og_sys.atoms.positions = system.atoms.positions
    og_sys.atoms.write(lichem_out_pdb)

## Run the script!

system = load_XYZ(lichem_in_xyz)
og_sys = read_orig_PDB(pdb_in)
integrate_movements(system, og_sys, lichem_out_pdb)
