# SEQItachi

Category: **Analysis** · Version 1.0.0

A QAH-native structure and quantum-chemistry workbench inspired by
**SEQCROW** for ChimeraX. It is an independent implementation: no SEQCROW code
is copied, and it is not affiliated with the SEQCROW authors.

## SEQCROW license verification

SEQCROW (`QChASM/SEQCROW`) is **GPL-3.0** open source. Its GitHub metadata
declares `GPL-3.0`, and the project is a ChimeraX bundle built on AaronTools.
SEQItachi is GPL-3.0 or later and does not bundle SEQCROW or AaronTools.

## Implemented in 1.0.0

### Structure

- XYZ import and export;
- molecule table with element and Cartesian coordinates;
- inferred covalent bonds and 3D ball-and-stick view;
- formula, molecular weight, center of mass, radius of gyration.

### Editing

- add/delete atoms;
- change element;
- add/remove bonds and bond order;
- set bond length;
- rotate and translate;
- center at origin.

### Analysis

- distance, angle, dihedral from atom indices;
- approximate Sterimol L/B1–B5;
- approximate cone angle;
- approximate buried volume by VDW voxel counting.

### QM input

Build input files for:

- Gaussian;
- ORCA;
- Psi4;
- Q-Chem;
- xTB;
- sqm.

### QM output

Parse:

- Gaussian: energy, geometry, HOMO/LUMO, frequencies, excited states;
- ORCA: energy, geometry, orbital energies, frequencies, absorption table;
- Psi4: energy, geometry, frequencies;
- Q-Chem: energy, geometry, frequencies, excited states.

Display:

- IR spectrum (Gaussian broadening);
- UV/Vis spectrum (Gaussian broadening);
- frequency and excitation tables;
- RRHO thermochemistry: ZPE, thermal correction, entropy and Gibbs correction
  from frequencies.

### Cube files

- Gaussian cube import;
- 2D slices along X/Y/Z;
- use cube atoms as a structure.

## Not yet implemented (roadmap)

- ChimeraX-style mouse modes and command language;
- 2D sketcher and full bond editor UX;
- AaronTools fragment/ligand library;
- conformer search through CREST;
- transition-state interpolation;
- normal-mode animation;
- full 3D orbital isosurfaces (currently 2D cube slices);
- point-group detection;
- complete ligand Sterimol library and exact Tolman cone-angle algorithm.

SEQItachi is not a drop-in SEQCROW replacement; it covers the core structure,
QM-input/output, spectra and thermochemistry workflows with QAH-native code.

## Notes

- No external QM executable is launched. The plugin only builds input files and
  parses outputs.
- AA/geometry parsers are tolerant but not exhaustive; open an issue with the
  output file if a format is missed.
- Approximate Sterimol/cone/buried-volume values are geometric estimates, not
  the exact published algorithms.

## License

GPL-3.0 or later. SEQCROW is GPL-3.0; see
`https://github.com/QChASM/SEQCROW` and the 2021 J. Comput. Chem. citation.
