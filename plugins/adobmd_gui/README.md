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
