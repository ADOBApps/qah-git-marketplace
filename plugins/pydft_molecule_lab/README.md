# PyDFT Molecule Lab

Category: **Analysis** · Version 1.0.2

A pydft-based electronic-structure workbench for small organic molecules and
hormones. It runs **single-point** Kohn–Sham calculations, reports electronic
descriptors, and draws molecular-orbital slices.

## Molecules

| ID | Name | Formula | Family | Load |
|---|---|---|---|---|
| `water` | Water | H2O | Reference | tiny |
| `benzene` | Benzene | C6H6 | Aromatic reference | small |
| `caffeine` | Caffeine | C8H10N4O2 | Alkaloid | moderate |
| `estrone` | Estrone (E1) | C18H22O2 | Hormone | heavy |
| `estradiol` | 17β-Estradiol (E2) | C18H24O2 | Hormone | heavy |
| `ethinylestradiol` | Ethinylestradiol (EE2) | C20H24O2 | Hormone | heavy |
| `estriol` | Estriol (E3) | C18H24O3 | Hormone | heavy |
| `testosterone` | Testosterone | C19H28O2 | Hormone | heavy |
| `progesterone` | Progesterone | C21H30O2 | Hormone | heavy |

Geometries are PubChem 3D conformers (public data). Custom XYZ files can be
imported from the Library tab.

## What is computed

- total electronic energy (Ha and eV);
- HOMO, LUMO and HOMO–LUMO gap;
- chemical hardness, softness, electronegativity and electrophilicity;
- Mulliken atomic charges;
- dipole moment from density-matrix dipole integrals;
- molecular-orbital window (HOMO−3 … LUMO+3);
- two-dimensional orbital slices on the heavy-atom best-fit plane;
- orbital-energy diagram;
- Markdown/JSON reports and PNG/SVG orbital plot export.

The plugin uses only the **pydft Kohn–Sham DFT** engine. There is no
Hartree–Fock fallback; a non-converged SCF is reported as indicative and the
user can raise the iteration cap or loosen the tolerance.

## CPU limits and temperature

pydft and pyqint are CPU-only. The header reports the number of logical CPU
threads detected by the OS, and the thread selector can use any value from 1 up
to that total. The plugin defaults to:

- one native thread (`OMP_NUM_THREADS=1`, Numba/BLAS capped);
- low-power grid by default;
- bounded SCF iteration cap (30 by default);
- a **Stop after current SCF step** button;
- optional pause between SCF iterations (250 ms by default);
- no calculation starts on plugin load or molecule selection;
- heavy molecules require confirmation before running.

A 60 °C CPU limit is very tight for E2/EE2. Use the low-power preset, one
thread, and your external watchdog. Prefer water/benzene for first tests.

## GPU?

No. pydft/pyqint have no GPU backend. An integrated GPU has no CUDA path, and
GPU quantum chemistry would require a separate CUDA-capable stack such as
GPU4PySCF on an NVIDIA GPU.

## Dependency injection

Inject `pydft` with Wheel Plugin Manager:

```text
Package: pydft
Target : global          (shared with other pydft plugins)
         pydft_molecule_lab  (private, if only this plugin needs it)
Mode   : normal dependency resolution
```

pydft brings `pyqint`, `pylebedev`, `numpy`, `scipy` and `numba`. The plugin
checks `plugins/vendor/pydft_molecule_lab` first, then `plugins/vendor/global`.
Press **Probe dependencies** after injection; a QAH restart is not required.

## Files

```text
manifest.json
__init__.py                 Plugin class and menu action
molecule_lab.py             Qt-free engine: geometry, SCF, properties, slices
molecule_lab_widget.py      PySide6 library/calculation/properties/orbitals UI
molecules/*.xyz             PubChem 3D conformers and reference geometries
icon.svg
README.md
```

## Method and limitations

- Single-point pydft Kohn–Sham; no geometry optimization, solvent, dispersion or
  thermochemistry.
- pydft is an educational localized-orbital DFT code. Absolute energies and
  gaps are indicative, not publication-grade.
- SCF convergence is not guaranteed for every molecule. The UI marks
  non-converged results; raise the iteration cap or loosen the tolerance.
  There is no alternate SCF engine.
- Orbital plots are 2D slices, not isosurfaces.
- Dipole moments use density-matrix dipole integrals and nuclear charges.

## License

Plugin code: GPLv3 or later. pydft/pyqint are GPLv3; PubChem geometry data is
public data. See upstream projects for their licenses.
