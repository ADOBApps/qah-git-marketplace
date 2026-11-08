# Injecting Dependencies from the GUI

This guide shows how to inject a package like **pydft** with Wheel Plugin
Manager, reuse QAH's existing scientific packages, verify it, and delete it
again.

No QAH rebuild is required.

---

## 1. Open Wheel Plugin Manager

In QAH:

```text
Plugins → Wheel Plugin Manager
```

Scroll to:

```text
Dependency injection into QAH's frozen Python
```

The header shows the detected target, for example:

```text
CPython 3.12 / win_amd64 (system Python 3.12.5)
```

---

## 2. Full injection: pydft with all dependencies

Use this when QAH does not already provide the package stack.

Fields:

```text
Package: pydft
Target : global
```

Leave **No deps (reuse QAH packages)** unchecked.

Press **Inject**.

Wheel Plugin Manager will resolve and unpack pydft and its dependencies
(pyqint, pylebedev, numpy, scipy, numba, llvmlite, ...) into:

```text
%USERPROFILE%\QAH\plugins\vendor\global\
```

This is simple but larger, and may duplicate packages QAH already bundles.

---

## 3. Small injection: reuse QAH's numpy/scipy/numba

QAH already bundles:

```text
numpy
scipy
numba
```

For pydft, only these are normally missing:

```text
pydft
pyqint
pylebedev
```

Use the **No deps (reuse QAH packages)** checkbox and list all needed packages:

```text
Package: pydft pyqint pylebedev
Target : global
No deps (reuse QAH packages): checked
```

Press **Inject**.

This downloads only the three named wheels:

```text
pydft-1.2.0-py3-none-any.whl
pyqint-1.5.1-cp312-cp312-win_amd64.whl
pylebedev-1.1.0-py3-none-any.whl
```

The resulting vendor set is much smaller than a full dependency injection.

Only use **No deps** when QAH already satisfies the package requirements. For
pydft, QAH's numpy/scipy/numba are reused.

---

## 4. Use a private target

If only one plugin needs pydft, use its plugin id as the target:

```text
Package: pydft pyqint pylebedev
Target : pydft_workbench
No deps (reuse QAH packages): checked
```

The plugin checks both its private target and `global`.

---

## 5. Verify the import

Keep the same target and use a module name:

```text
Package: pydft
Target : global
```

Press **Verify import**.

Expected:

```text
OK: pydft 1.2.0
  file: C:\Users\HP\QAH\plugins\vendor\global\pydft\__init__.py
  system Python: C:\Python312\python.exe
```

For a private set:

```text
Package: pydft
Target : pydft_workbench
```

`Verify import` uses the system Python ABI check. QAH itself activates the
vendor path at startup and immediately after injection.

---

## 6. Open the dependency in Plugin Sentinel

Plugin Sentinel 1.2.4+ has a **Dependencies** tab:

```text
Plugin Sentinel → Dependencies
```

It lists:

```text
Target | Package | Version | Python | Platform | Path
```

This is read-only. It does not activate anything.

---

## 7. Use the dependency in a plugin

A plugin can import normally after the vendor path is active:

```python
import pydft
print(pydft.__version__)
```

For a lazy, safe check:

```python
import importlib.util

if importlib.util.find_spec("pydft") is None:
    raise RuntimeError("pydft is not injected; use Wheel Plugin Manager")
```

For a plugin that should work before injection, include a fallback bootstrap:

```python
import importlib
import importlib.util
import os
import sys
from pathlib import Path


def activate_vendor(targets=("global",)):
    home = Path(os.environ.get("QAH_HOME") or (Path.home() / "QAH"))
    root = home / "plugins" / "vendor"
    for target in targets:
        path = root / target
        if path.is_dir() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
    importlib.invalidate_caches()


def has_pydft():
    activate_vendor(("pydft_workbench", "global"))
    return importlib.util.find_spec("pydft") is not None
```

---

## 8. Use PyDFT Workbench

Install **PyDFT Workbench** from the marketplace, then:

1. Open **PyDFT Workbench**.
2. If pydft is missing, the badge says `pydft not injected` and Run is disabled.
3. Inject pydft from Wheel Plugin Manager.
4. Press **Detect dependencies**.
5. Press **Run DFT demo**.

Expected CO/STO-3G result:

```text
Energy : about -110.85 Ha
HOMO   : about -0.198 Ha
LUMO   : about +0.034 Ha
Gap    : about 0.232 Ha
```

Molecules: CO, H2O, H2, N2. Functionals: svwn5, svwn3, pbe.

---

## 9. Delete injected dependencies

### Delete one package

In the dependency panel:

```text
Package: pydft
Target : global
```

Press **Remove package**.

The package and its `dist-info` records are removed from that target.

### Delete the whole set

Set the target:

```text
Target: global
```

Press **Remove set**.

This removes the entire vendor set:

```text
%USERPROFILE%\QAH\plugins\vendor\global\
```

### CLI equivalent

```powershell
$wcli = "C:\Users\HP\QAH\plugins\python_plugins\wheel_plugin_manager\qah_wheel_cli.py"

py -3 $wcli deps-remove global --package pydft
py -3 $wcli deps-remove global
```

After deletion, restart QAH or reopen the plugin. Other packages in the same set
remain unless you remove the whole set.

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `Verify import` uses LibreOffice Python | Upgrade Wheel Plugin Manager to 1.2.1+; it excludes LibreOffice/OpenOffice/Blender/QGIS Pythons. |
| `zlib.dll` missing | The selected interpreter was an application-bundled Python. Use the real system Python, e.g. `C:\Python312\python.exe`. |
| No pydft wheel | Only pre-built wheels are accepted; check the package name and Python/platform. |
| Import fails after injection | Check target, press Verify import, and confirm QAH restarted. |
| QAH is slow after full injection | Use `--no-deps` with pydft + pyqint + pylebedev, or close the heavy plugin tab when not in use. |
| Package not visible in Sentinel | Use Sentinel's **Dependencies** tab; Inventory/Plugin Executions only list plugins. |
| Delete fails | Close QAH if a native `.pyd` is loaded, then remove the set. |

---

## Quick reference

```text
Full pydft injection:
  Package: pydft
  Target : global
  No deps: unchecked

Small pydft injection:
  Package: pydft pyqint pylebedev
  Target : global
  No deps: checked

Private target:
  Package: pydft pyqint pylebedev
  Target : pydft_workbench
  No deps: checked

Delete package:
  Package: pydft
  Target : global
  → Remove package

Delete whole set:
  Target: global
  → Remove set
```
