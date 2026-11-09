# Protonation Lab

Category: **Analysis**

Structure-based pH-dependent protonation and pKa analysis for proteins and
metalloproteins.

## Features

- PDB and mmCIF import.
- Residue templates for Asp, Glu, His, Lys, Cys, Tyr, Arg and chain termini.
- Histidine state selection (HID/HIE/HIP), disulfide detection.
- Metal/ion fixed charges, including Cu in multicopper oxidases.
- Solvent-accessible surface burial.
- Screened Coulomb electrostatics with distance-dependent dielectric and
  Debye-Hückel ionic screening.
- Mean-field pH titration and Monte Carlo protonation microstates.
- Per-site pKa, protonation, state, burial and warnings.
- Net charge, isoelectric point and titration curves.
- Structure viewer with Cα trace or all-heavy-atom display, coloured by
  protonation, apparent pKa, burial or site type, with metal markers and PNG export.
- CSV, JSON and state-mapped PDB export.

## Use

1. Open **Plugins → Analysis → Protonation Lab**.
2. Load a PDB or mmCIF structure.
3. Set pH, ionic strength and temperature.
4. Press **Run protonation**.
5. Inspect sites, the **Viewer** and titration curves; export from **Report**.

## Model and limitations

This is v0.2 of the analytic continuum model. It uses an approximate
screened-Coulomb/distance-dependent dielectric representation, SASA burial,
Debye-Hückel screening, mean-field titration and Monte Carlo sampling. A
finite-difference Poisson-Boltzmann grid solver is the next planned refinement.

- Missing atoms/hydrogens are not rebuilt. The exported PDB preserves existing
  coordinates/hydrogens and adds state REMARKs and histidine state names.
- Histidine is represented by one neutral tautomer plus the cationic state;
  both neutral tautomers and side-chain rotamers are not fully sampled.
- Metals are fixed charges; protonation-redox coupling is not predicted. Sites
  within 3.5 Å of a metal are flagged as metal sites.
- Modified/oxidized residues such as OHI are reported and are not titrated.
- Glycans and other non-standard hetero groups are read but are not titrated.
- Buried sites, metal centres and residues near the target pH carry the largest
  uncertainty.
- The method is not a substitute for experimental pKa measurement or
  constant-pH MD.

## Validation status

v0.1.1 fixed multi-atom burial parsing (Asp/Glu/His/Arg) and calibrated the
burial term against the public PKAD-2 experimental pKa set. On 1,369 matched
wild-type residues the apparent-pKa MAE is 0.92 and RMSE is 1.26 pKa units.
Because the same public set was used to choose the burial scale, this is a
calibration result, not independent validation. Cysteine and some coupled or
metal-bound sites remain the largest error sources. v0.2.0 adds the structure
viewer and explicit metal/modified-residue reporting without changing the pKa
core.

## License

GPL-3.0-or-later.
