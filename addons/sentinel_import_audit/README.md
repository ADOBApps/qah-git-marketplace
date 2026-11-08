# Sentinel Import Audit

Static import consistency audit:

- third-party imports not declared in `manifest.json`;
- heavy imports (`pydft`, `pyqint`, `numba`, `torch`, `scipy`, …);
- wildcard imports;
- local/framework/stdlib exclusions.

Static only. Dynamic imports and runtime path changes may be missed.
