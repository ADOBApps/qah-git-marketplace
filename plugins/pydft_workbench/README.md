# PyDFT Workbench

An educational **pydft** demo for QAH.

It detects a pydft installation from an injected Wheel Plugin Manager vendor set,
then runs a small restricted Kohn-Sham DFT calculation:

```text
Molecule   : CO / H2O / H2 / N2
Basis      : STO-3G
Functional : svwn5 / svwn3 / pbe
SCF tol    : 1e-3 / 1e-4 / 1e-5
```

Results:

- total electronic energy (Hartree)
- HOMO / LUMO and gap
- electron count
- SCF iteration count
- calculation time

## Inject pydft from the GUI

1. Open **Wheel Plugin Manager**.
2. Go to **Dependency injection into QAH's frozen Python**.
3. Set:

   ```text
   Package: pydft
   Target : global
   ```

4. Press **Inject**.
5. Open **PyDFT Workbench**.
6. Press **Detect dependencies**.
7. Press **Run DFT demo**.

No QAH rebuild is required. The plugin loads even when pydft is missing and
shows these instructions instead of crashing.

## Dependency details

`pydft` is pure Python, but it needs:

```text
pyqint>=1.5.1
pylebedev
numpy
scipy>=1.15
numba
```

Wheel Plugin Manager resolves them as pre-built wheels for QAH's Python/ABI.
QAH already bundles numpy, scipy and numba; the injected set still keeps a
self-contained vendor directory so it does not modify the installed QAH
application.

If the calculation needs too much memory or time, use `CO`/STO-3G first, then
try H2O or N2.

## Files

```text
manifest.json
__init__.py          QAH entry point
pydft_widget.py      dependency probe, UI, worker and demo calculation
icon.svg
README.md
```

## Security

This plugin performs scientific calculations only. It does not end processes,
run subprocesses or modify the QAH application directory. pydft and pyqint are
third-party GPL-compatible scientific packages; review their licenses before
redistribution.

License: GPLv3 or later.
