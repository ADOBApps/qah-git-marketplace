# Sentinel Addon Studio

## 1.0.2

- Added a **line-number gutter** and **Python syntax highlighting** to the
  `main.py` editor.
- Added a current **Ln / Col** indicator.
- Added **Validate** to the toolbar.
- Added a **Deploy** panel showing the configured Git Marketplace repository,
  branch and token state without exposing the token.
- `Publish to Marketplace` now preflights the marketplace configuration and
  clearly delegates publishing to Git Plugin Marketplace.
- Added **Check Marketplace**, **Open packages**, **Copy .qah path** and the
  built package path field.
- Added shortcuts: `Ctrl+S` save, `Ctrl+B` build, `Ctrl+T` test, `Ctrl+I`
  install in Sentinel, `Ctrl+Shift+P` publish.
- The editor remains inside the scrollable responsive workbench.

## 1.0.1

A separate developer plugin for building **Plugin Sentinel addons** without
putting authoring tools inside Sentinel's runtime.

- scaffold `.qah` addon projects
- edit `addon.json`, `main.py` and `README.md`
- choose capabilities and a timeout
- test in **Sentinel's isolated addon host** (same sandbox as the Addons tab)
- build a hash-verifiable `.qah` package
- install it in Sentinel and pin its hash
- publish it to the **Git Plugin Marketplace → Addons** catalog

## Why a separate plugin

Sentinel stays small and strict: it loads, pins and runs addons. Addon Studio is
the authoring environment. This keeps the attack surface of the runtime small
and lets the Studio evolve independently.

## Addon API

`addon.json`:

```json
{
  "format": "qah-sentinel-addon",
  "id": "dft_output_checks",
  "name": "DFT Output Checks",
  "version": "1.0.0",
  "api_version": 1,
  "author": "You",
  "description": "Checks DFT output files",
  "main": "main.py",
  "entry": "run",
  "timeout": 30,
  "capabilities": ["read-files", "findings", "report"]
}
```

`main.py`:

```python
def run(context):
    findings = []
    for target in context["targets"]:
        ...
    return {
        "status": "ok",
        "summary": "3 files checked",
        "findings": findings,
        "report": "optional markdown",
        "data": {"any": "json"},
    }
```

Context keys: `addon_id`, `addon_name`, `addon_version`, `api_version`,
`capabilities`, `addon_dir`, `data_dir`, `workdir`, `targets`, `config`.

Capabilities: `read-files`, `write-files`, `network`, `findings`, `report`,
`policy`, `watchdog`. Subprocesses, native libraries, registry access and
undeclared network access are always blocked. Targets are read-only by default.

## Workflow

1. Fill in the project form and press **New project**.
2. Edit `main.py`.
3. Add test targets if the addon uses `read-files`.
4. Press **Test in Sentinel** to run it in the addon sandbox.
5. Press **Build .qah** to create the package.
6. Press **Install in Sentinel** to install and pin it for the Addons tab.
7. Press **Publish to Marketplace** to commit it to the configured Git catalog.

## Files

```text
%USERPROFILE%\QAH\sentinel_addon_studio\projects\<id>\
%USERPROFILE%\QAH\sentinel_addon_studio\packages\<id>-<version>.qah
```

Projects are plain folders; you can also open an existing addon folder.

## Requirements

- Plugin Sentinel 1.2.0 or newer (for testing/installing).
- Git Plugin Marketplace 1.2.0 or newer (for publishing).

Version: 1.0.1

## 1.0.1

- Added a vertical scrollbar to the project form so the full workbench fits on
  small screens.
- The action toolbar now collapses overflow into its extension menu instead of
  forcing a wide window.
- The header text wraps and can shrink.

## 1.0.0
