# Resource Watchdog

Category: **Tools** · Version 1.0.0

Read-only runtime monitor for QAH. It reports:

- QAH PID, CPU %, RSS, thread count;
- child processes (PID, name, CPU, RSS);
- heavy modules currently loaded in QAH, including `pydft`, `pyqint`, `numba`,
  `scipy`, `matplotlib`, `torch`, `tensorflow`, `jax`, `cupy`, `pyscf`, `rdkit`
  and others;
- warning thresholds for CPU % and RSS;
- a JSON report at `%USERPROFILE%\QAH\resource_watchdog\report.json`.

## Important limitation

QAH plugins run inside the **same process**. CPU and RSS belong to QAH as a
whole, not to one plugin. The watchdog can show that `pyqint`/`pydft` are
loaded and that QAH is using CPU, but it cannot prove which plugin caused it.
A child process can be attributed more precisely because it has its own PID.

## Safety

This plugin **never kills, unloads, suspends or throttles** anything. It is a
monitor and report writer. Monitoring is off until you press **Start
monitoring**. The interval defaults to 5 seconds.

## Why not an addon?

Sentinel addons run in an isolated host with `read-files`, `findings` and
`report` capabilities. They cannot read live process state, spawn processes,
call Sentinel internals or unload plugins. A static addon can flag heavy imports
(`sentinel_resource_audit` does that), but runtime measurement belongs in a
native QAH plugin like this one.

## psutil

`psutil` is optional. Inject it into `global` or `resource_watchdog` with Wheel
Plugin Manager. Without psutil the plugin still lists loaded heavy modules but
cannot sample CPU/RSS.

## Relation to Watchdog Builder

Sentinel's **Watchdog Builder** currently generates **hash watchdogs**: it pins
a target path SHA256, checks it on a QTimer, and writes `report.json`. This
plugin is a separate example of a **process/resource watchdog** and does not
alter Sentinel's builder.
