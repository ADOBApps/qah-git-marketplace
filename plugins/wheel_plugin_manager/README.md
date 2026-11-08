# Wheel Plugin Manager for Quantum Analysis Helper (QAH)

Install, validate, repair, test, build and remove **wheel** (`.whl`) QAH plugins
without a compiler and without relying on the Python interpreter inside the QAH
bundle.

It is designed first for **Windows**, where QAH 2.0.8 packages built with
Briefcase often have **no `python.exe`** in the application directory, but the
same code works on Linux and macOS.

## 1.2.1

- Interpreter selection now prefers the real system Python (`py -3.12`, PATH,
  registry) **before** application-bundled Pythons.
- LibreOffice, OpenOffice, Blender, QGIS, `app_packages`, `site-packages`,
  `node_modules`, WindowsApps, Cygwin and MSYS Pythons are excluded as
  dependency-injection interpreters.
- This prevents `Verify import` from reporting success with LibreOffice's
  `python-core` while QAH itself still cannot see the dependency.
- The verification log now makes clear that the import check uses the system
  Python ABI; QAH activation happens in the running QAH process.

## 1.2.0

- Added **dependency injection into QAH's frozen Python** without rebuilding
  QAH. It resolves pre-built wheels with the system Python/pip for QAH's
  Python version and platform, verifies the wheel tags, and unpacks them under
  `<QAH home>/plugins/vendor/<target>`.
- New CLI: `inject`, `deps`, `deps-path`, `deps-verify`, `deps-remove`.
- New GUI **Dependency injection** panel with Inject, List sets, Verify import,
  Remove package and Remove set.
- Injected paths are activated at QAH startup by the plugin and immediately
  after injection. Example: `psutil` installs as a cp312/win_amd64 wheel with no
  QAH rebuild and no change to the installed application directory.
- Dependency sets are isolated by target name (`global` or a plugin id), can be
  merged, upgraded, verified and removed.

---

## Why the built-in installer fails on some Windows builds

QAH's Windows `pyproject.toml` does not set:

```toml
[tool.briefcase.app.QuantumHelper.windows]
allow_subprocesses = true
```

The Briefcase Windows template then removes `python*.exe` from the support
package. In the installed MSI:

- `python.exe` / `pythonw.exe` are missing,
- `python312.dll` and `app_packages/` are still present,
- `sys.executable` is the GUI launcher, not an interpreter.

QAH's `wheel_installer.python_executable()` correctly rejects the launcher (it
does not print the probe marker), but then falls back to `sys.executable`.
`pip install --target ...` therefore starts another copy of the GUI (or exits 0
doing nothing), the staging directory stays empty, and the plugin never
appears.

This plugin does not need `python.exe`. A wheel is a ZIP file, so the default
install mode validates it and **unpacks it directly** into
`<QAH home>/plugins/wheels/<dist>`.

---

## Files

```text
manifest.json          QAH plugin manifest
__init__.py            QAH entry point (Plugin class)
plugin_ui.py           PySide6 widget: wheel list, console, buttons
installer_core.py      Qt-free install/test/build/doctor logic
qah_wheel_cli.py       Standalone terminal front-end (no Qt, no QAH imports)
qah_wheel_cli.bat      Windows convenience wrapper
qah_wheel_cli.sh       Linux/macOS convenience wrapper
icon.svg               Plugin icon
LICENSE.md             GNU GPL v3
README.md              This file
```

`installer_core.py` only uses the Python standard library. `plugin_ui.py` and
`__init__.py` need PySide6, which QAH already provides.

### Platform support

| Platform | Install / validate / test / fix | Notes |
|---|---|---|
| Windows 10/11 (x64, ARM64) | Yes | Primary target; works without `python.exe` |
| Linux (x86_64, aarch64) | Yes | Handles `manylinux`/`musllinux` wheels, Flatpak `/app`, AppImage `$APPDIR` |
| macOS (Intel, Apple silicon) | Yes | Handles `.app/Contents/Resources` bundles and `macosx_*` wheels |

The plugin id and folder are `wheel_plugin_manager` on every platform. If QAH
stores user data somewhere other than `~/QAH` (e.g. a Flatpak sandbox), point
the CLI at it with `QAH_HOME` or `--qah-home`.

---

## Install the plugin itself

### Option A — copy the folder

Copy this entire `wheel_plugin_manager` folder to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\wheel_plugin_manager\
```

On Linux/macOS:

```text
~/QAH/plugins/python_plugins/wheel_plugin_manager/
```

Restart QAH, then use **Plugins → Scan for new or removed plugins**. The plugin
appears as **Wheel Plugin Manager**.

### Option B — import the ZIP

Build/import `wheel_plugin_manager.qplugin.zip` through QAH's
**Plugins → Import** dialog.

> If QAH uses `%LOCALAPPDATA%\QAH` on your build instead of
> `%USERPROFILE%\QAH`, set `QAH_HOME` or pass `--qah-home` to the CLI.

---

## Terminal usage (recommended first on Windows)

The CLI does not import QAH or PySide6. Any Python 3 works; on Windows use
`py -3`.

```powershell
$cli = "$env:USERPROFILE\QAH\plugins\python_plugins\wheel_plugin_manager\qah_wheel_cli.py"

py -3 $cli doctor
py -3 $cli paths
py -3 $cli list
```

On Linux/macOS use `python3` or the shell wrapper:

```sh
cli="$HOME/QAH/plugins/python_plugins/wheel_plugin_manager/qah_wheel_cli.py"
chmod +x "$(dirname "$cli")/qah_wheel_cli.sh"

python3 "$cli" doctor
# or
"$(dirname "$cli")/qah_wheel_cli.sh" doctor
```

### Install a wheel

```powershell
py -3 $cli install "C:\path\to\test_wheel_plugin-1.0.0-cp310-abi3-win_amd64.whl" --force
```

Default mode is `unpack`:

- validates the wheel filename and platform/Python tags,
- extracts package + `.dist-info` into a staging directory,
- atomically promotes it to `%USERPROFILE%\QAH\plugins\wheels\<dist>`,
- writes an `INSTALLER` marker,
- never calls pip, `python.exe`, or a compiler.

Then restart QAH (or run `rescan` from the GUI).

### Test before installing

```powershell
py -3 $cli test "C:\path\to\plugin.whl"
```

This installs into a temporary sandbox, reads the `qah.plugins` entry point,
imports the plugin class, and deletes the sandbox.

### Validate / repair a wheel

`install` and `test` now refuse a wheel whose `qah.plugins` entry point targets
a package that is not inside the wheel. This catches the common maturin mistake
where a mixed Rust/Python project is built without:

```toml
[tool.maturin]
python-source = "python"
module-name = "my_plugin._core"
```

The resulting wheel contains `_core/` at its root, no `my_plugin/` package, and
installs as a plugin QAH can never import.

```powershell
# Structural check only (no install)
py -3 $cli validate "C:\path\to\plugin.whl"

# Repair the project config, rebuild, validate, and install
py -3 $cli fix "C:\path\to\my_plugin" --install

# Same from a wheel inside <project>\dist
py -3 $cli fix "C:\path\to\my_plugin\dist\my_plugin-1.0.0-cp310-abi3-win_amd64.whl" --install
```

`fix` adds the missing `[tool.maturin]` keys, keeps a one-time backup
(`pyproject.toml.qah-bak`), rebuilds, and rejects any wheel that is still
malformed. `build` performs the same repair automatically.

`clean --broken` removes installed wheel folders that cannot provide a plugin
(left behind by the bundle's broken pip installer).

### Inspect / uninstall

```powershell
py -3 $cli info "C:\path\to\plugin.whl"
py -3 $cli info test_wheel_plugin
py -3 $cli uninstall test_wheel_plugin
```

Close QAH before uninstalling a plugin whose `.pyd`/`.so` is loaded; Windows
locks the file until the process exits.

### Dependencies

There are two different cases.

**1. Dependencies of a wheel plugin.** QAH installs plugin wheels with
`--no-deps` on purpose: PySide6, numpy, etc. come from the host. Use `--deps`
only for a genuinely optional small dependency:

```powershell
py -3 $cli install "C:\path\to\plugin.whl" --deps
```

That uses pip. If the bundle has no `python.exe`, the CLI falls back to pip
**in-process** (pip is pure Python). It never launches the GUI stub.

**2. Extra runtime dependencies for the frozen QAH interpreter.** This is the
new injection path. It downloads pre-built wheels with the **system Python**,
but selects tags for **QAH's Python version and platform**, then unpacks them:

```powershell
$cli = "C:\path\to\wheel_plugin_manager\qah_wheel_cli.py"
py -3 $cli inject psutil --target global
py -3 $cli deps
py -3 $cli deps-verify global psutil
```

It writes to:

```text
<QAH home>\plugins\vendor\global\
```

and adds that directory to `sys.path` at QAH startup and immediately after
injection. Use a plugin id as the target for a private set:

```powershell
py -3 $cli inject "psutil>=5.9" --target my_plugin
```

Remove one package or the whole set:

```powershell
py -3 $cli deps-remove global --package psutil
py -3 $cli deps-remove global
```

How it works:

1. detects QAH's Python version (for example CPython 3.12) from the bundle;
2. detects the platform wheel tag (`win_amd64`, `linux_x86_64`, ...);
3. runs `pip download --only-binary=:all:` with the target `--python-version`,
   `--abi` and `--platform` when the system Python differs;
4. rejects any wheel whose tags do not match the QAH target;
5. unpacks all resolved wheels into a staging vendor directory;
6. atomically promotes the staging directory and activates it.

Limits:

- pre-built wheels only; source distributions are rejected;
- the OS/CPU must match the QAH bundle;
- native wheels must match QAH's Python ABI (normally cp312/abi3);
- it never modifies the installed QAH application directory;
- no QAH rebuild is required.

### Build a wheel

Only this step needs Rust/maturin, and it uses your **system** Python, not the
QAH bundle:

```powershell
py -3.12 -m pip install --upgrade maturin
py -3 $cli build "C:\path\to\test_wheel_plugin"
```

`build` first checks the project and adds the maturin mixed-project settings
when they are missing (backup: `pyproject.toml.qah-bak`). It validates the
produced wheel and, if one build tool emits a malformed wheel, tries the next
available tool instead of returning it.

Or directly:

```powershell
cd C:\path\to\test_wheel_plugin
py -3.12 -m maturin build --release --out dist
```

If you build directly, make sure `pyproject.toml` contains the
`[tool.maturin]` block shown above; otherwise the wheel will be rejected by
`validate`/`install`.

Use the same Python minor version as the QAH bundle (normal 2.0.8 is CPython
3.12). A `cp313` wheel will not load in a 3.12 bundle.

On a Ryzen 3, set `$env:CARGO_BUILD_JOBS = "2"` if memory is tight. The example
plugin is small.

---

## GUI usage

Open **Plugins → Wheel Plugin Manager**. The tab contains:

- installed wheel list,
- **Install .whl…**, **Test .whl…**, **Build from project…**, **Repair build…**,
- **Uninstall selected**, **Refresh**,
- **Doctor**, **Open wheels folder**, **Rescan QAH**, **Clear console**,
- a command console with history (Up/Down).

Console commands:

```text
help
doctor
paths
python
tags
list
info <wheel|name>
validate <wheel>
install <wheel> [--deps] [--pip] [--force] [--allow-broken]
test <wheel> [--instantiate]
uninstall <name|path>
build <project>
fix <project|wheel> [--install]
clean [--broken]
rescan
open [path]
clear
```

Drag a `.whl` onto the tab to fill the path.

Install/test/build run in a background thread; the GUI stays responsive.

---

## Wheel compatibility rules

Match the wheel tag to the QAH bundle, not to your system Python.

| QAH bundle | Accepted tags |
|---|---|
| CPython 3.12 x64 (normal 2.0.8) | `cp312-cp312-win_amd64`, `cp311-abi3-win_amd64`, `cp310-abi3-win_amd64`, `py3-none-any` |
| CPython 3.12 ARM64 | `...-win_arm64` equivalents |
| 32-bit QAH | `...-win32` |

A Linux wheel (`manylinux`, `linux_x86_64`), a macOS wheel, or a
`cp313-cp313-win_amd64` wheel cannot be installed/loaded on a CPython 3.12
Windows bundle. Rebuild on Windows.

For Rust/PyO3 plugins, enable `abi3-py310` (or lower) so one wheel works on
Python 3.10+:

```toml
pyo3 = { version = "0.23", features = ["extension-module", "abi3-py310"] }
```

Then:

```powershell
py -3.12 -m maturin build --release --out dist
```

---

## Diagnostics

`doctor` reports:

- current interpreter, `sys.executable`, prefix, platform,
- whether `sys.executable` is the Briefcase launcher,
- whether `python.exe` exists next to the launcher,
- QAH home and wheels directory,
- the first interpreter candidates and whether they pass the marker probe,
- pip/packaging availability,
- installed wheel plugins and broken entries,
- maturin availability.

On a broken Windows bundle, expect:

```text
launcher detected        : True
python.exe next to it    : False
-> This Briefcase bundle was built without allow_subprocesses=true...
   This plugin's default 'unpack' mode does not need them.
```

---

## Permanent fix for a future QAH build

For a future release (not required for the installed 2.0.8 build), add to
`[tool.briefcase.app.QuantumHelper.windows]`:

```toml
allow_subprocesses = true
```

That keeps `python.exe`/`pythonw.exe` in the bundle, and the existing
`wheel_installer` works normally.

Optionally harden `wheel_installer.py`:

- if no candidate prints the probe marker, do **not** fall back to
  `sys.executable`; raise a clear error or use direct unpacking;
- in `install_wheel()`, fall back to direct wheel unpacking when no real
  interpreter exists.

The plugin in this folder already implements the direct-unpack fallback, so it
fixes the current installation without a rebuild.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `is not a wheel` | Selected a directory or `.zip` | Select the `.whl` file |
| `targets [...] but this Python is ...` | Wrong platform/Python wheel | Rebuild on Windows; use `win_amd64` + `abi3` |
| `entry point 'x' targets 'x', but the wheel has no 'x/' package` | maturin built a pure-Rust wheel (`_core/` at the root) because `[tool.maturin]` was missing | `qah_wheel_cli.py fix <project> --install` |
| Installed but QAH does not list it | Restart/scan not done, or no `qah.plugins` entry point | `list`, `info`, restart QAH, check `entry_points.txt` |
| `.pyd` import fails in `test` | Wrong Python ABI/arch, missing DLL | Use `abi3-py310`, 64-bit, check `python3XX.dll` |
| Uninstall fails with permission error | Plugin loaded, file locked | Close QAH and retry |
| `pip` mode fails | No real interpreter and pip missing | Use default unpack mode; avoid `--deps` |
| Build fails | maturin not installed in the selected Python | `py -3 -m pip install maturin`, or put `maturin` on PATH |

Report the output of `doctor`, the exact wheel filename, and the full
traceback if something still fails.
