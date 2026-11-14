# ADOBMD GUI

Complete Graphic User Interface for Advanced Development of Binary Molecular Dynamics, includes a 3D Visualizer for ADOBMD unified data files - View molecular structures, QM/MM regions, and bonds. And Converter from CIF, PDB, SDF and XYZ files to ADOBMD unified data format for MD/ONIOM simulations (DATA).

## Installation
1. Download the plugin ZIP file
2. In Quantum Analyzer Helper, go to Plugins → Import Plugin...
3. Select the ZIP file
4. The plugin will appear in the Plugins menu

## Usage
1. Open the plugin from the Plugins menu
2. Use the interface to interact with the plugin
3. Configure settings as needed

## Configuration
Edit the `manifest.json` file to change plugin settings.

## Development
This plugin was created with the Plugin Maker tool.

### Key Changes
1. **Centralized Python Utilities**: All shared Python code moved to `plugins.libs.python_utils`
2. **Unified Plugin Management**: All plugin-related utilities in `plugins.libs`
3. **Better Separation**: Core libraries vs. individual plugins
4. **Easier Maintenance**: Shared code updates affect all plugins

## Plugin Structure

### Core Plugin Files in `plugins.libs/`

| File | Purpose |
|------|---------|
| `base_plugin.py` | Abstract base classes for all plugins |
| `lua_bridge.py` | Lua 5.4+ integration bridge |
| `luajit_bridge.py` | LuaJIT (Lua 5.1) integration bridge |
| `plugin_manager.py` | Main plugin lifecycle management |
| `import_manager.py` | Plugin import/export functionality |
| `import_dialog.py` | UI for plugin import operations |
| `one_click_importer.py` | Simplified plugin installation |
| `debug_plugin_import.py` | Debug utilities for plugin loading |

Version: 1.0.0
Author: Acxel Orozco
Created: 2026-03-19


## Importers

The **Importers** tab contains three front ends, backed by the modules in
`importers/` (no external executables):

- **KIM (OpenKIM)** — load a `.txz`/`.zip` model archive, inspect the
  charges/Buckingham pairs, and export an ADOBMD `periodic.params`.
- **VASP** — POSCAR/CONTCAR (+ optional OUTCAR energy/forces) to
  `system.data`, `system.ff`, `periodic.params`, `system.conf`,
  `reference.json`; accepts `--charges` or a Bader `ACF.dat`.
- **Quantum ESPRESSO** — `pw.x` input (+ optional output) with the same
  outputs.
- **ORCA** — optimized XYZ + `.hess` + `.property.txt` to a molecule-specific
  force field (`.ff`, `.data`, `.conf`, `molff` parameters), with the same
  Hessian fit/frequency validation as `orca2adobmd`.

`periodic.params` from the KIM tab can be passed to the VASP/QE tabs so the
generated force field uses the same parameter set.


## Creating a molecule force field from ORCA files

A molecule potential is **parameter-driven**: one generic plugin (`molff`)
serves every molecule, and the per-molecule data live in
`<stem>_molff.params`. No per-molecule shared library is compiled.

### Required ORCA output

All three files must come from the **same** calculation, at the same level of
theory:

| file | produced by | content |
|---|---|---|
| `*.xyz` | `Opt` / `Opt Freq` | optimized geometry (the CLI can read the ORCA output instead with `--out`) |
| `*.hess` | `Freq` / `AnFreq` | Cartesian Hessian (Eh/bohr^2) and harmonic frequencies |
| `*.property.txt` | MBIS or CHELPG | per-atom charges (`$SCF_MBIS_Population_Analysis` / `$SCF_CHELPG_Population_Analysis`) |

Minimal ORCA input:

```
! PBE0 def2-SVP def2/J D4 Opt Freq
%output Print[P_MBIS] 1 end
* xyzfile 0 1 molecule.xyz
```

The geometry must be a true minimum; a saddle point carries an imaginary mode
into the fit.

### Command line

`orca2adobmd_cli.py` (also available as `importers/orca2adobmd_cli.py`):

```bash
OPT="--xyz molecule.xyz --hess molecule.hess"
OPT="$OPT --property molecule.property.txt --charges mbis"

python3 orca2adobmd_cli.py info     $OPT   # atoms, topology, charge sum
python3 orca2adobmd_cli.py topology $OPT   # explicit bond list (1-based)
python3 orca2adobmd_cli.py fit      $OPT   # force constants + frequency RMSE
python3 orca2adobmd_cli.py validate $OPT   # same comparison, no output files
python3 orca2adobmd_cli.py export   $OPT \
    --outdir adobmd --stem molecule
```

`export` writes:

| file | content |
|---|---|
| `molecule.json` | full parameter set and metadata |
| `molecule_molff.params` | bonds, angles, torsions, exclusions, 1-4 scaling |
| `molecule.ff` | atom types, `<Plugins>`, `<NonBonded>`; bonded blocks are comments (the plugin owns them) |
| `molecule.data`, `molecule.conf` | coordinates/topology and run control |
| `molecule_validation.json` | mode-by-mode ORCA vs FF comparison |

Run from the export directory with `adobmd.x molecule.conf`; the generated
`.ff` refers to `./molff.so` (Linux) or `./molff.dll` (Windows). `export` copies
the bundled plugin into the output directory, so the run directory is
self-contained.

`_molff.params` is the authoritative model: bonds, angles, torsions,
1-2/1-3 exclusions, 1-4 scaling, plus one `site i sigma epsilon charge` line per
atom (Angstrom, kcal/mol, e). The `.ff` only supplies the atom types and the
plugin routing; its bonded blocks are comments, so the host does not double
count the intramolecular terms.

Validated with 1 ps NVT runs (300 K set-point, 1 fs): aligned RMSD 0.08 A (E2),
0.15 A (EE2), 0.07 A (TMS); all bonds stay within 0.05 A.

Options: `--plugin-name` / `--plugin-path` change the plugin reference,
`--intramolecular-nonbonded` enables the molecule's own LJ/Coulomb terms (needed
in the condensed phase, not for a pure Hessian fit), and `--nsteps`,
`--temperature`, `--dt-fs`, `--box` and `--material` fill the `.conf` template.

### GUI

**Importers → ORCA** exposes the same options:

| field | default |
|---|---|
| Optimized XYZ (required) | — |
| ORCA Hessian (required) | — |
| ORCA charges (required) | — |
| Charge method | MBIS |
| Intramolecular nonbonded | off |
| Output directory / File stem | — / `molecule` |
| Material | `MOL` |
| Plugin name / path | `molff` / `./molff.so` |
| Steps / Temperature / dt | 10000 / 300 K / 1.0 fs |
| Ewald accuracy / Slab correction | 1e-6 / off |

1. select the three files;
2. **Info** — check atom count, charge sum and topology;
3. **Fit** — read the Hessian correlation and frequency RMSE in the log;
4. **Export force field** — also copies the bundled `molff.so`/`molff.dll`
   into the output directory.

### Validation

Fit quality is judged by the Hessian correlation (> 0.99) and the frequency
RMSE (< ~100 cm^-1). Values for the set used here: 52, 48 and 95 cm^-1 at
correlations 0.997, 0.997 and 0.999. Also check that the charge sum equals the
molecular charge and that a short NVE run conserves energy.

### Limitations

Harmonic bonds/bends/torsions, OPLS-AA element LJ, fixed MBIS/CHELPG charges;
no impropers, polarization, charge transfer or bond breaking. One conformer, so
torsional barriers away from the minimum are approximate. Elements: H, C, N, O,
F, S, P, Cl, Br, I, Si, Al, Mg, Li, Na, K, Ca, Ti, Zr, Sn; others fall back to
a default covalent radius and the inferred topology must be checked. Metals,
open-shell and strongly correlated systems are not validated.


## Adsorption

The **Adsorption** tab computes the rigid-slab adsorption energy of a molecule
on a periodic slab:

```
E_ads = E(complex) - E(slab) - E(molecule, gas)
```

Inputs: the complex `CONTCAR`, the molecule `.ff` and `.data`, its
`_molff.params`, and the `periodic_ff.so` plugin. The nonbonded terms use the
periodic plugin (Ewald + Buckingham/LJ, 1-2/1-3 exclusions); the molecule's
harmonic bonded terms come from its `.ff`. The result is reported in eV and
kcal/mol together with the component energies.


## Method notes: use the same level of theory

An adsorption energy is
`E_ads = E(complex) - E(slab) - E(molecule)`, a difference of three large
numbers. It is only meaningful if the three terms use the **same level of
theory**:

- same functional (and Hubbard `U`, if any);
- same basis set / pseudopotentials and plane-wave cutoff;
- same dispersion correction (D3/D4);
- same charge model (MBIS, Bader/DDEC, or formal);
- same cell, vacuum and k-mesh; the gas molecule in a box large enough that
  its images do not interact, but otherwise identical settings.

Do not mix, for example, a PBE+U slab with a PBE0-D4 gas molecule, or a DFT
complex with a force-field slab: those differences are not adsorption.

The rule also applies inside the force field: the molecule force field and the
slab parameters must come from the same level (or be calibrated against it),
and the gas reference must use the same charge and Lennard-Jones model as the
complex. A **rigid** comparison at the DFT geometry is the strict test;
comparing a force-field-relaxed minimum with a DFT single point mixes two
geometries and two energy surfaces.

## Appendix: worked example (E2 / EE2 on TiO2(101))

System: 2x1 anatase TiO2(101) slab (72 atoms) + E2 (44) / EE2 (46) = 116/118
atoms, 40 A vacuum.

1. **Importers -> VASP (or Quantum ESPRESSO)**: convert the complex `CONTCAR`,
   the bare slab and the gas molecule with the same charge model.
2. **Importers -> ORCA**: fit the molecule force field from the optimized XYZ,
   the `.hess` and the `.property.txt`; check the reported Hessian correlation
   and frequency RMSE.
3. **Adsorption**: select the complex, the molecule `.ff`/`.data`/
   `_molff.params` and `periodic_ff`; compute `E_ads` (rigid), optionally
   relax the molecule (slab fixed, threaded).

Rigid results at the DFT geometry:

| molecule | orientation | E_ads (FF) | E_ads (DFT, prelim.) |
|---|---|---:|---:|
| E2 | upright | -0.136 eV | -0.287 eV |
| EE2 | upright | -0.137 eV | -0.403 eV |

The E2 OH-down value agrees with DFT to 0.02 eV. The force-field-relaxed value
(-0.445 eV) is deeper because the classical model lacks electronic/steric
repulsion; it must be compared with a DFT-relaxed complex, not with a DFT
single point.
