# Plugin Sentinel

Advanced plugin security audit for Quantum Analysis Helper. It extends QAH's
system **Plugin Auditor** with risk scoring, capability mapping, trusted-hash
baselines, policy gates, richer findings and a headless CI-friendly CLI.

> **Scope.** Sentinel is report-and-gate software. It does not block QAH from
> loading a plugin by itself; the Policy tab and CLI exit codes tell you whether
> a plugin should be allowed. The optional sandbox check executes the plugin in a
> separate process with network access blocked.

---

## Install

Copy `plugin_sentinel/` to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\plugin_sentinel\
```

Or import a `.qplugin.zip` through **Plugins → Import Plugin**.

Restart QAH and open **Plugins → Plugin Sentinel**.

---

## Tabs

### Inventory

Every user, system and wheel plugin, plus files you add with **Scan file…**.

| Column | Meaning |
|---|---|
| Risk | 0–100 weighted severity score |
| Grade | A (clean) to F (critical) |
| Verdict | PASS / WARN / BLOCK from the policy |
| Crit/High/Med/Low | Finding counts |
| Baseline | new / trusted / changed |
| Capabilities | Detected capabilities |

Select a row to see the full audit text.

### Findings

All findings from the QAH audit checks plus Sentinel's own checks. Filter by
severity or text; select a finding for its path, line and detail.

### Native

Inspects PE, ELF and Mach-O libraries found in plugins (`.dll`, `.so`, `.dylib`,
`.pyd`):

- architecture, bitness, subsystem and file size
- SHA256 and Shannon entropy
- imports/needed libraries and exports metadata
- signed/unsigned, ASLR/NX/CFG, TLS callbacks, debug metadata
- writable+executable sections, executable stack, RPATH/RUNPATH
- suspicious APIs such as process injection, remote threads, service creation
  and URL download helpers

The parser reads headers only; it never loads the native library.

### Capabilities

A capability matrix detected from the Python AST:

- Network
- Subprocess
- Filesystem
- Native code
- Credentials
- Persistence
- Dynamic code
- GUI
- Database

Combinations are escalated (for example network + credentials, or
subprocess + network).

### Runtime

A live htop-style view:

- CPU and memory gauges
- disk usage and network throughput
- top processes by CPU or memory
- QAH process-tree filter
- process PID, name, CPU, RSS, threads, status and user

Uses `psutil` when available and falls back to native task/ps listings.

### Watchdog

Pin a plugin folder or a native library and let Sentinel recompute its hash on
an interval. Status becomes **changed** when the content drifts, **missing**
when the path disappears, or **error** when it cannot be read.

- Watch a plugin folder or a DLL/SO/dylib
- Choose the check interval
- Start/stop the watchdog or run **Check now**
- Pin the current hash to accept a change

Watch definitions are stored in:

```text
%USERPROFILE%\QAH\plugin_sentinel\watches.json
```

### Sandbox

Runs plugin code in a separate process with:

- Python audit hooks blocking network, subprocess, ctypes and writes outside the
  sandbox
- a temporary working directory and scrubbed environment
- POSIX rlimits or a Windows Job Object memory limit
- a hard timeout and process-tree kill
- captured stdout/stderr and violation list

This is a strong containment harness for Python code. It is **not** a
hypervisor or an OS security boundary against kernel-level native code.

### Baseline

Trust pins a plugin's current SHA256:

- **new** — never trusted
- **trusted** — digest matches the pinned value
- **changed** — the plugin changed after being trusted

Use **Trust selected inventory plugin** to pin the selection, and **Forget
selected baseline** to remove a pin. The baseline is stored in:

```text
%USERPROFILE%\QAH\plugin_sentinel\baseline.json
```

### Policy

- Block at severity: never / low / medium / high / critical
- Maximum risk score
- Require a trusted baseline
- Allowed capabilities

Policy is stored in:

```text
%USERPROFILE%\QAH\plugin_sentinel\policy.json
```

`BLOCK` means at least one rule failed. `WARN` means medium/low findings or a
risk score of 25 or more. `PASS` means clean under the current policy.

### Report

Preview and export JSON, Markdown, HTML or CSV reports. The HTML report is
self-contained and suitable for review or CI artifacts.

### Documentation

Offline guide for the native scanner, runtime monitor, watchdog, sandbox,
external API, system-plugin protection and Linux/macOS notes.

---

## External watchdog API

Other QAH plugins can register watches while Plugin Sentinel is installed:

```python
from plugin_sentinel import sentinel_api

sentinel_api.watch_plugin("my_plugin")
sentinel_api.watch_library(r"C:\path\native.dll")
sentinel_api.watch_execution("simulation output", r"C:\path\out.log")

sentinel_api.subscribe(lambda event: print("changed:", event))
sentinel_api.poll()
```

Watches are shared with the Watchdog tab through `watches.json`. Callbacks are
in-process and fire while both plugins are loaded; cross-process consumers can
read `events.jsonl`. An execution watch is a path watchdog for an output/log/
script/executable, not a process supervisor.

**System-plugin protection:** Sentinel is report-only and never unloads,
disables or blocks a plugin. The Git Marketplace also disables update/version
install for system and wheel plugins.

---

## What Sentinel adds to Plugin Auditor

- Weighted risk score and letter grade
- Capability mapping and dangerous-combination detection
- Native DLL/SO/dylib header and import inspection
- Secret scanning (`PRIVATE KEY`, AWS/GitHub tokens and generic credentials)
- Manifest hardening and archive hygiene (backup files, bytecode, native files)
- Duplicate plugin-id detection across user/system/wheel sources
- Trusted SHA256 baselines, drift detection and a file/library watchdog
- Policy gates with capability allowlists
- Process sandbox with audit hooks and resource limits
- Live htop-style runtime monitor
- JSON / Markdown / HTML / CSV reports
- Headless CLI with policy exit codes
- Recursive discovery of plugins in nested user-plugin subfolders
- Windows, Linux and macOS code paths

The base checks (`manifest`, `archive`, `static`, `deps`, optional `sandbox`)
come from QAH's bundled `plugins.libs.plugin_audit`.

---

## CLI

The CLI is useful for CI or for scanning a downloaded archive before installing:

```powershell
cd $env:USERPROFILE\QAH\plugins\python_plugins\plugin_sentinel

# Scan every installed plugin
python sentinel_cli.py --all --format text

# Gate a release
python sentinel_cli.py C:\path\my_plugin.qplugin.zip `
  --checks manifest archive static deps `
  --fail-on high --max-risk 50

# JSON artifact
python sentinel_cli.py --all --format json --output sentinel-report.json
```

Exit codes:

- `0` — no BLOCK verdicts
- `1` — at least one BLOCK verdict
- `2` — no targets or CLI error

Useful flags:

```text
--checks manifest archive static deps sandbox
--format text|json|md|html|csv
--baseline PATH
--policy PATH
--fail-on never|low|medium|high|critical
--max-risk 0..100
--require-trusted
--trust
```

The sandbox check is **not** enabled by default because it executes the plugin
in a restricted subprocess. Use it only for plugins you are prepared to run.

---

## Security model

- Static analysis never imports or executes plugin code.
- The optional sandbox check runs in a separate process with a timeout, memory
  limits and network blocked; review QAH's sandbox implementation for details.
- Baseline hashes are local trust decisions, not signatures. They detect drift,
  not a compromised author.
- Secret scanning is heuristic and may produce false positives; treat findings
  as leads to review, not proof.

---

## Files

```text
manifest.json
__init__.py
sentinel_core.py      Qt-free engine: checks, risk, capabilities, baseline, policy
native_scan.py        PE / ELF / Mach-O header and import inspection
sandbox_runner.py     process sandbox harness and resource limits
runtime_monitor.py    htop-style live runtime tab
watchdog_monitor.py   hash watchdog tab
sentinel_widget.py    PySide6 multi-tab dashboard
sentinel_cli.py       headless scanner and CI gate
icon.svg
README.md
```

---

Version: 1.1.0  
Author: Acxel Orozco
