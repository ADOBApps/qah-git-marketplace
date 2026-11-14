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
