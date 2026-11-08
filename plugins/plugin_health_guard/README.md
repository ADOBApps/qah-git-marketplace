# Plugin Health Guard

A **headless** QAH plugin. It has no window and no widget: shortly after QAH
starts it checks the installed plugin manifests and writes a machine-readable
report. Two menu actions are available:

- **Run plugin health check**
- **Open health report**

This is a deliberately non-GUI plugin: it is useful because it runs without
opening a tab, catches broken/duplicate plugins early, and leaves a JSON report
for support or CI.

---

## What it checks

- `manifest.json` missing, invalid JSON or not an object
- missing/invalid plugin id and non-semver versions
- missing `main` entry point or `__init__.py`
- missing declared icon
- duplicate plugin ids across user, system and wheel plugins
- URL/VCS/local-path dependencies
- backup files (`.stable`, `.old`)
- stale `__pycache__` / `.pyc` files
- top-level legacy plugin folders without a manifest

## Report

```text
%USERPROFILE%\QAH\plugin_health_guard\health.json
```

The report contains:

```json
{
  "counts": {"plugins": 12, "issues": 3, "high": 1},
  "plugins": [],
  "issues": []
}
```

A summary is also written to the QAH log.

## Why a non-GUI plugin?

Non-GUI plugins are valuable when the job is background maintenance rather than
user interaction:

- no tab or window to open
- starts automatically with QAH
- zero-click manifest/integrity check
- writes reports and logs for later review
- can expose menu actions only when needed

They are not a replacement for security auditing; use **Plugin Sentinel** for
native inspection, risk scoring, policy gates, watchdogs and sandboxing.

## Install

Copy `plugin_health_guard/` to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\plugin_health_guard\
```

or import a `.qplugin.zip` through **Plugins → Import Plugin**.

Restart QAH. The startup check runs about 1.5 seconds after QAH initializes.

## Platform

Windows, Linux and macOS. It uses QAH's platform plugin paths when available and
falls back to `~/QAH/plugins/python_plugins`.

---

Version: 1.0.0  
Author: Acxel Orozco
