# Sentinel Resource Audit

Category: Sentinel addon · Version 1.0.0

A static, read-only audit of QAH plugin folders for heavy scientific imports and
declared dependencies.

## Signals

| Severity | Examples |
|---|---|
| high | `pydft`, `pyqint`, `numba`, `llvmlite`, `torch`, `tensorflow`, `jax`, `cupy`, `pyscf`, `openmm`, `rdkit` |
| medium | `scipy`, `matplotlib`, `pandas`, `ase` |
| info | `numpy` |

It also reports declared `dependencies` and `optional_dependencies` from
`manifest.json`.

## What it cannot do

- It cannot inspect live CPU/RSS.
- It cannot attribute CPU to a specific plugin.
- It cannot call Plugin Sentinel internals.
- It cannot unload, suspend, throttle or kill a process or plugin.

It is deliberately report-only. Use **Resource Watchdog** for runtime
CPU/RSS/module monitoring, and Plugin Sentinel's Runtime tab for process and
plugin-execution inspection.

## Usage

1. Build/install and pin the addon.
2. Open **Plugin Sentinel → Addons**.
3. Select `sentinel_resource_audit`.
4. Add one or more plugin folders as targets.
5. Run.

The result lists high/medium/info resource signals and a markdown report.

## Why not call Sentinel?

Sentinel addons run in an isolated child process with audit hooks and
capability limits. They do not import Sentinel, do not receive its plugin
manager and have no process-control API. Letting them unload or kill would
violate the addon containment model.
