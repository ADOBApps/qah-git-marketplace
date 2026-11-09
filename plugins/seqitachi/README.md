# SEQItachi

Category: **Analysis** · Version 1.2.0

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

- IR, Raman and VCD spectra with real intensities when the output provides
  them (ORCA `Int`/`T**2`, Gaussian `IR Inten`, ORCA `RAMAN SPECTRUM`,
  ORCA VCD rotational strengths);
- Gaussian, Lorentzian, pseudo-Voigt and delta peak shapes with FWHM/Voigt
  mixing, absorbance or transmittance;
- linear, quadratic and shift frequency scaling with common method/basis
  presets;
- multiple conformers with Boltzmann weights, per-conformer components and a
  weighted total;
- experimental CSV overlay;
- UV/Vis spectrum (Gaussian broadening);
- frequency/excitation tables plus CSV export of peaks and curve data;
- RRHO thermochemistry: ZPE, thermal correction, entropy and Gibbs correction
  from frequencies.

Notes:

- Frequency scaling presets are approximate literature factors; use the manual
  factor to match your method/basis exactly.
- Boltzmann weights use the electronic energy parsed from the outputs
  (`FINAL SINGLE POINT ENERGY`, `SCF Done`, etc.). If any energy is missing,
  equal weights are used and the table shows the reason indirectly via `—`.
- Older ORCA output without the `Int` column uses the printed `T**2` values as
  relative intensities; the summary reports which source was used.

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


## External toolchain (1.1.0)

SEQItachi never bundles ORCA, xtb, CREST, Gaussian, Psi4 or Q-Chem. The **Tools**
tab detects executables from:

1. a custom path saved in `%USERPROFILE%\QAH\seqitachi\toolchain.json`;
2. `QAH_ORCA`/`ORCA`, `QAH_XTB`/`XTB`, `QAH_CREST`/`CREST`, etc.;
3. `PATH`;
4. common install locations.

Missing tool = actionable `ToolNotFoundError`; no job starts. CREST is not
installed on this machine, so conformer search remains unavailable until the
user supplies it or uses a WSL/Linux installation.
