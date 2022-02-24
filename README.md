# Emmett Leddin Dissertation Code

The included Python 3 scripts are all crucial for the
quantum mechanics/molecular mechanics (QM/MM) calculations with LICHEM, as
described in my dissertation,
"Chapter 3: Nucleotide Addition of DNA polymerase &kappa;
with 2 Mg<sup>2+</sup> Ions".

## `pdbxyz-for-amber.py`

This script uses an AMBER force field parameter file distributed with Tinker in  
order to convert a PDB file into a Tinker XYZ file.

## `generate_TINKER_parameters.py`

This script creates a Tinker parameter file from the information in an
AMBER prmtop file.
It can also be used to create the file using the information found in one of
the AMBER `leaprc` files.

## `pdbxyz4amber-pmd-params.py`

This script is a shorter version of `pdbxyz-for-amber.py` to be used with
parameter sets created through `generate_TINKER_parameters.py`.

## `create-reg.py`

This script reads in the original PDB used for TINKER XYZ conversion and the
TINKER XYZ.
Several variables are set, including the indices of the metal(s) used for the
shell of unfrozen atoms, the QM charge and multiplicity, and information
about the QM regions for the Gaussian `BASIS` file.
The `select_QM`, and `select_higher_basis`
functions have all been modified to select the QM region and basis sets
definitions used for the QSM results.

The script writes out three files:
- `regions.inp_backup`: the `regions.inp` file template including parameters
   and assignments for QM, boundary, pseudobond, and frozen atoms.
   Using `lichem -convert` creates a blank `regions.inp` file, so the `_backup`
   suffix is added to avoid the complete file being overwritten.
- `BASIS`: the `BASIS` file to use with Gaussian when the `GEN` keywords is
   specified.
- `BASIS_verification.txt`: a file that maps residue and atom names to the
   indices used by (1) Gaussian for the `BASIS` file, (2) VMD and LICHEM, (3)
   Tinker in the XYZ. It also prints how it will be treated in the QM region.
   ```
   BASIS_ID Regions_ID TINKER_ID ResName ResNum AtomName Type
   1        1428       1429      ILE     88     CA       PB
   2        1443       1444      ILE     88     C        REG
   ```
   PB = pseudobond atom, REG = regular basis set, HIGH = higher basis set

## `vmd-regions.py`

This script parses a LICHEM `regions.inp` file to create a `.vmd` file
containing selection keywords for the QM, pseudobond, boundary, frozen, and
unfrozen atoms.

## `mda-qm-part1.py` and `mda-qm-part2.py`

The first of these scripts (`mda-qm-part1.py`) reads the LICHEM XYZ file and
then creates a new PDB file containing just the atoms in the QM subsystem.
That PDB can then be modified in an external program, such as GaussView or VMD,
and resaved as a new PDB.
The second script (`mda-qm-part2.py`) will then take those new coordinates for
the QM atoms into the original LICHEM XYZ and save it as a new file.
These two scripts are particularly useful when building an intermediate or
product from an optimized reactant structure.

## `swapsies.py`

This script is used to swap a QM region for another QM region while retaining
the original MM region.
For example, if you have a reactant and a product structure that were optimized
independently, but the MM region changes drastically between the two structures,
you can use `swapsies.py` to re-optimize the product's QM region in the
reactant's MM region.
"Reverse swapsies", where the reactant QM is put in to the product MM, is also
possible by toggling some comments at the beginning and end of the script.

## `stitching.py`

LICHEM builds an initial path guess using the reactant MM for all path beads
except the product.
If the reactant and product MM regions are drastically different, this can
lead to issues with the path optimization.
This script can help build a smoother path by building a specified number
of beads using the product MM region.

## `xyzpdb-lichem.py`

This script updates the coordinates in the original pre-conversion PDB file
with the coordinates in the optimized LICHEM XYZ and saves them as a new
PDB file.
The resulting PDB retains the original residue information.

## Abbreviations Used

Abbreviation | Meaning
-------------|--------
PDB          | Protein Data Bank (here, a file type)
QM/MM        | Quantum Mechanics/Molecular Mechanics
QSM          | Quadratic String Method
VMD          | Visual Molecular Dynamics
