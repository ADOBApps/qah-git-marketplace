# SEQItachi

Category: **Analysis** · Version 1.2.8

A QAH-native structure and quantum-chemistry workbench inspired by
**SEQCROW** for ChimeraX. It is an independent implementation: no SEQCROW code
is copied, and it is not affiliated with the SEQCROW authors.

## SEQCROW license verification

SEQCROW (`QChASM/SEQCROW`) is **GPL-3.0** open source. Its GitHub metadata
declares `GPL-3.0`, and the project is a ChimeraX bundle built on AaronTools.
SEQItachi is GPL-3.0 or later and does not bundle SEQCROW or AaronTools.

## 1.2.8 — the plot follows the file

- Loading an output now **auto-selects the matching plot**: an NMR-only file
  switches to 1H/13C NMR, a UV-only file shows the broadened UV/Vis. Before,
  the selector stayed on *Absorbance* and the tab looked like it had ignored
  the file.
- Realistic NMR line widths: **1H 0.01 ppm**, **13C 0.05 ppm** (about 4 Hz at
  400/100 MHz). The previous 1.0 ppm 13C default merged nearby lines into a
  band.
- New **sticks** overlay (on by default) draws one vertical line per computed
  nucleus, as in a normal NMR spectrum.
- The line-width control now has a Hz/ppm hint in its tooltip.

## 1.2.7 — TMS reference at the same level

- The sigma(NMR) reference is now taken from the TMS calculation at the same
  level of theory (`molecular/TMS/01_nmr.out`, PBE0-D4/def2-SVP, RKS):
  **1H sigma_ref = 31.053 ppm**, **13C sigma_ref = 191.054 ppm**,
  **29Si sigma_ref = 375.953 ppm**.
- New **"From output…"** button next to *NMR ref.*: point it at a TMS (or other
  reference) ORCA output and the mean shielding of the selected element becomes
  sigma_ref. Use it whenever the target run uses another functional/basis or a
  solvent model.
- δ = sigma_ref − sigma; equivalent nuclei are averaged.

With these references the E2 spectrum gives 1H −0.3 … 6.6 ppm and
13C 9.0 … 149.2 ppm (17-C at 79.3 ppm, C18 at 9.0 ppm).

## 1.2.6 — UV/Vis and NMR

- **Fixed ORCA 6 UV/Vis parsing.** The absorption table now accepts the
  three-token transition label (`0-1A -> 1-3A`) and the extra `Energy (eV)`
  column that ORCA 6 introduced. Previously every row was discarded and the
  panel reported "No excitations" even though the output contained the table.
- Optional `multiplicity` and `energy_cm` are kept per excitation.
- **UV/Vis broadening is now done in energy (eV, default σ = 0.20 eV)** instead
  of a constant 0.15 nm, which produced needles in the visible.
- A UV/Vis-only output uses the full figure instead of an empty half panel, and
  exports an excitation table plus the broadened curve as CSV.
- **New 1H and 13C NMR spectra** from ORCA `! NMR` isotropic shieldings
  (`Diagonalized sT*s matrix ... iso=`). δ = σ_ref − σ with an editable
  reference (defaults 31.8 ppm for 1H and 195.0 ppm for 13C) and an editable
  ppm line width. Peak table and CSV export are included.
- The reference must be computed at the same level of theory (TMS). Version
  1.2.7 replaces the initial approximate defaults with the TMS values of
  `molecular/TMS` and adds the *From output…* button.

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
- auto-detected x-axis range around the active peaks with manual min/max
  override (default auto, rounding outward to 50 cm⁻¹ with 8% padding);
- linear, quadratic and shift frequency scaling with common method/basis
  presets;
- multiple conformers with Boltzmann weights, per-conformer components and a
  weighted total;
- experimental CSV overlay;
- UV/Vis spectrum (broadened in energy) and 1H/13C NMR from isotropic
  shieldings (ORCA `! NMR`), with editable reference and line width;
- frequency/excitation tables plus CSV export of peaks and curve data;
- **Save plot…** for the current figure as PDF/SVG (vector) or PNG, plus JPEG/TIFF when Pillow is available, with a configurable DPI;
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
- ORCA 6 outputs with blank lines and a `Scaling factor for frequencies` line
  before the mode list are parsed correctly; this was verified on real
  B3LYP/BP86/HF water frequency outputs.
- Every tab is wrapped in a scroll area with horizontal and vertical bars as
  needed, so the workbench remains usable on small screens. Tables, plots and
  text panes keep their own scrollbars.

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
