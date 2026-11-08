# QAH Tool Guides

Practical, public usage notes for the four main QAH tools.

| Tool | Purpose |
|---|---|
| **Theme Studio** | Create, preview, export and publish QAH themes |
| **Sentinel Addon Studio** | Create, test, package and publish Plugin Sentinel addons |
| **Plugin Sentinel** | Audit plugins, inspect native code, sandbox, baseline, watchdog and manage addons |
| **Wheel Plugin Manager** | Install, validate, repair, build and test wheel plugins; inject runtime dependencies |

> Security note: plugins run with QAH/user privileges. Addons run in Sentinel's
> isolated addon host. Only install code you trust. Themes are passive JSON +
> QSS, but a hostile theme can still make the UI unusable.

---

## Theme Studio

Theme Studio edits QAH themes and keeps compatibility with the legacy Theme
Manager format: `theme.json` + `theme.css`.

### Workflow

1. Open **Theme Studio**.
2. Set id, name, version, author, description, font family, font size and radius.
3. Edit the 14 color tokens:
   `background`, `surface`, `surface_alt`, `text`, `text_muted`, `accent`,
   `accent_text`, `border`, `hover`, `selection`, `error`, `warning`, `success`,
   `code_bg`.
4. Watch the live preview.
5. Press **Regenerate CSS from tokens**, or edit custom QSS directly.
6. Export a theme folder or a `.qtheme.zip`.
7. Publish to the Git Marketplace.

### Export formats

Legacy folder:

```text
theme.json
theme.css
preview.svg
README.md
```

Marketplace package:

```text
<id>-<version>.qtheme.zip
  theme.json
  theme.css
  preview.svg
  README.md
```

### Install layout

Marketplace themes install flat so the existing Theme Manager sees them without
a QAH restart:

```text
%USERPROFILE%\QAH\themes\<id>.json
%USERPROFILE%\QAH\themes\<id>.css
```

Linux/macOS: `~/QAH/themes/<id>.json` and `<id>.css`.

### Publish

```powershell
$cli = "C:\path\to\git_plugin_marketplace\git_marketplace_cli.py"
py -3 $cli publish-theme "C:\path\to\my_theme" --changelog "My Theme 1.0.0"
py -3 $cli list-themes --refresh
py -3 $cli install-theme my_theme
```

### Compatibility rules

- keep the legacy top-level keys;
- `css_file` must name the CSS file;
- use plain QSS; no JavaScript, Python or remote imports;
- do not install themes into subdirectories;
- test light and dark text contrast.

---

## Sentinel Addon Studio

Addon Studio is a separate developer plugin for **Plugin Sentinel addons**. It
does not put authoring tools inside Sentinel's runtime.

### Addon package

```text
<id>-<version>.qah   (ZIP)
  addon.json
  main.py
  README.md
```

`addon.json`:

```json
{
  "format": "qah-sentinel-addon",
  "id": "my_addon",
  "name": "My Addon",
  "version": "1.0.0",
  "api_version": 1,
  "author": "Author",
  "description": "What the addon audits.",
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
    for target in context.get("targets", []):
        findings.append({
            "severity": "info",
            "title": str(target),
            "detail": "checked",
        })
    return {
        "status": "ok",
        "summary": "checked",
        "findings": findings,
        "report": "",
        "data": {},
    }
```

### Workflow

1. Fill in the project form and press **New project**.
2. Edit `main.py`.
3. Select the smallest capability set.
4. Add test targets if using `read-files`.
5. Press **Test in Sentinel**.
6. Press **Build .qah**.
7. Press **Install in Sentinel** to install and pin the hash.
8. Press **Publish to Marketplace**.

### Capabilities

```text
read-files, write-files, network, findings, report, policy, watchdog
```

Subprocesses, native library loading, registry access and undeclared network
access are blocked. Writes are limited to the addon data directory.

### CLI publishing

```powershell
py -3 $cli publish-addon "C:\path\to\my_addon" --changelog "My Addon 1.0.0"
py -3 $cli list-addons --refresh
py -3 $cli install-addon my_addon
```

### Trust states

- `unpinned`: local import, cannot run until pinned.
- `ok`: pinned and unchanged.
- `modified`: changed after pinning, blocked until re-pinned.
- `disabled`: pinned but disabled.
- `invalid`: bad manifest/API/main/capability.

Marketplace installs are pinned automatically. Marketplace updates re-pin from
the new install record; plain local edits remain `modified`.

### Addon interpreter

QAH is a frozen launcher, so inside QAH `sys.executable` is the QAH executable,
not `python.exe`. Sentinel addons and the sandbox run in a separate real Python
process. Sentinel resolves it from:

1. `QAH_SENTINEL_PYTHON` or `QAH_PYTHON`;
2. `python3` / `python` on `PATH`;
3. the Windows `py -3` launcher.

If no interpreter is found, the result is an immediate error with instructions
instead of a 60 s timeout. Install Python 3.8+ or point
`QAH_SENTINEL_PYTHON` at an interpreter.

### Injected dependencies in Sentinel

Wheel Plugin Manager can inject pre-built wheels for QAH's frozen Python under
`plugins/vendor/<target>`. These are **packages**, not QAH plugins, so they do
not appear in Sentinel Inventory or Plugin Executions. Plugin Sentinel 1.2.4+
shows them in the **Dependencies** tab with target, package, version,
Python/platform and path, plus open/copy actions.

---

## Plugin Sentinel

Plugin Sentinel is a metaplugin for plugin security, runtime inspection and
Sentinel addons.

### Tabs

| Tab | What it does |
|---|---|
| **Inventory** | Recursive plugin discovery, source, versions, risk score, grade, verdict |
| **Findings** | Detailed findings with severity and remediation |
| **Native** | DLL/SO/dylib headers, imports, exports, entropy, security flags, suspicious APIs |
| **Capabilities** | Network, subprocess, filesystem, native, credentials, persistence, dynamic code, GUI, database |
| **Runtime** | CPU/memory/disk/network, top processes, QAH process tree; visible-only sampling with a 0.5/1/2/5/10 s interval and Pause |
| **Runtime -> Plugin Executions** | Plugin source, loaded state, QAH PID, unload selected user plugin |
| **Watchdog** | Two subtabs: hash watches and the Watchdog Builder |
| **Sandbox** | Run plugin code in a separate process with audit hooks and limits |
| **Baseline** | Trusted SHA256 baselines and drift detection |
| **Policy** | Block severity, max risk, trusted-baseline requirement, capability allowlist |
| **Report** | JSON / Markdown / HTML / CSV export |
| **Addons** | Two subtabs: Sentinel addons and Health Guard |
| **Dependencies** | View and remove packages injected for QAH's frozen Python |
| **Documentation** | Built-in reference |

### Audit workflow

1. Open **Plugin Sentinel -> Inventory**.
2. Press **Refresh** and **Scan all**.
3. Review **Findings**, **Capabilities**, **Native** and the risk grade.
4. Use **Baseline -> Trust** for known-good plugins.
5. Configure **Policy** for CI or release gates.
6. Use **Sandbox** for a process-isolated import test.
7. Use **Runtime -> Plugin Executions** to unload a user plugin.
8. Export a report from **Report**.

### Risk and policy

- weighted risk score and letter grade;
- capability mapping and dangerous combinations;
- native header/import inspection;
- manifest and archive hygiene;
- duplicate plugin id detection;
- trusted baselines and drift;
- policy gates and capabilities allowlists.

### Runtime sampling

Runtime metrics are sampled only while the Runtime tab is visible. Hiding the
tab stops the timer, so Sentinel does not poll processes in the background. The
toolbar offers a 0.5/1/2/5/10 second interval (default 2 s) and a Pause
checkbox; both persist in `runtime_settings.json`. The source label reports
psutil or the tasklist/ps fallback, and the status line shows the current
interval and process count.

### Sandbox

The sandbox is a containment harness, not a hypervisor:

- fresh temporary workdir and scrubbed environment;
- audit hooks block network, subprocesses, ctypes, registry and writes outside
  the sandbox;
- sensitive credential paths are read-protected;
- POSIX rlimits or Windows Job Object memory/CPU limits;
- hard timeout and process-tree kill.

Native code is blocked by the audit hook, but no in-process sandbox is a
guarantee against every kernel-level escape.

### CLI

```powershell
py -3 sentinel_cli.py --all --format text
py -3 sentinel_cli.py C:\path\plugin.qplugin.zip --fail-on high --max-risk 50
py -3 sentinel_cli.py --all --format json --output sentinel-report.json
```

Exit codes: `0` no BLOCK verdicts, `1` at least one BLOCK, `2` no targets/CLI
error.

### Watchdog API

Other plugins can register watches while Sentinel is installed. See the built-in
**Documentation** tab and the `sentinel_api` module.

---

## PyDFT Molecule Lab

Category: **Analysis**. A pydft-based single-point electronic-structure
workbench for small organic molecules and hormones.

### Molecules

Water, benzene, caffeine, estrone (E1), 17β-estradiol (E2), ethinylestradiol
(EE2), estriol (E3), testosterone and progesterone. Geometries are PubChem 3D
conformers; custom XYZ files can be imported.

### Output

- total energy (Ha/eV);
- HOMO, LUMO and HOMO–LUMO gap;
- hardness, softness, electronegativity and electrophilicity;
- Mulliken charges and dipole moment;
- HOMO±3 orbital window, 2D orbital slices and orbital-energy diagram;
- Markdown/JSON reports and PNG/SVG orbital plots.

pydft Kohn–Sham is the primary engine; PyQInt Hartree–Fock is available as a
fallback when DFT does not converge.

### Thermal safety

pydft/pyqint are CPU-only. The plugin defaults to one native thread, a
low-power grid, a bounded SCF iteration cap, a pause between SCF steps and a
**Stop after current SCF step** button. It never starts a calculation on load.
Heavy hormones (E2/EE2/E3/testosterone/progesterone) require confirmation and
can run for minutes; use the low-power preset and an external temperature
watchdog. Start with water or benzene.

### GPU?

No. pydft/pyqint have no GPU backend. An integrated GPU has no CUDA path; GPU
quantum chemistry requires a separate CUDA stack such as GPU4PySCF on an NVIDIA
GPU.

### Dependencies

Inject `pydft` with Wheel Plugin Manager into `global` or the private
`pydft_molecule_lab` target. pydft brings pyqint, pylebedev, numpy, scipy and
numba. matplotlib is optional for plots and is normally bundled with QAH.

---

## Wheel Plugin Manager

Wheel Plugin Manager installs, validates, repairs, builds and tests QAH `.whl`
plugins without requiring `python.exe` in the QAH bundle.

### Install a wheel

```powershell
$wcli = "C:\path\to\wheel_plugin_manager\qah_wheel_cli.py"
py -3 $wcli install "C:\path\to\plugin-1.0.0-cp312-abi3-win_amd64.whl"
py -3 $wcli list
py -3 $wcli test "C:\path\to\plugin.whl"
py -3 $wcli uninstall plugin_name
```

Default mode is direct unpack into:

```text
%USERPROFILE%\QAH\plugins\wheels\<dist>\
```

No pip and no `python.exe` are required.

### Validate and repair

```powershell
py -3 $wcli validate "C:\path\to\plugin.whl"
py -3 $wcli fix "C:\path\to\project" --install
py -3 $wcli clean --broken
```

`validate` checks that every `qah.plugins` entry point resolves to a package in
the wheel. It catches the maturin "`_core/` at wheel root" bug. `fix` adds the
missing mixed-project settings, rebuilds, validates and optionally installs.

### Build a wheel

Building needs Rust/maturin and a real system Python, not the QAH bundle:

```powershell
py -3.12 -m pip install --upgrade maturin
py -3 $wcli build "C:\path\to\test_wheel_plugin"
```

Use the same Python minor version as QAH (normal 2.0.8 is CPython 3.12). A
`cp313` wheel will not load in a 3.12 bundle.

### Dependency injection for QAH's frozen Python

Wheel Plugin Manager 1.2.2 can inject pre-built dependencies without rebuilding
QAH:

```powershell
py -3 $wcli inject psutil --target global
py -3 $wcli deps
py -3 $wcli deps-verify global psutil
```

Linux/macOS:

```bash
python3 "$HOME/QAH/plugin_projects/wheel_plugin_manager/qah_wheel_cli.py" \
    inject psutil --target global
```

It resolves wheels with the system Python/pip, matching QAH's Python version and
platform tags, verifies them, unpacks them under:

```text
%USERPROFILE%\QAH\plugins\vendor\<target>\
```

and activates that path at QAH startup and immediately after injection. No QAH
rebuild and no installed application directory change.

Wheel Plugin Manager 1.2.1+ deliberately skips application-bundled Pythons such
as LibreOffice/OpenOffice, Blender, QGIS, `app_packages`, `site-packages`,
WindowsApps, Cygwin and MSYS. `Verify import` should report the real system
Python, for example `C:\Python312\python.exe`, not LibreOffice `python-core`.

Remove one package or a whole set:

```powershell
py -3 $wcli deps-remove global --package psutil
py -3 $wcli deps-remove global
```

Limits: pre-built wheels only; OS/CPU and Python ABI must match.

### GUI

The GUI exposes wheel installation, validation, repair/build, testing,
uninstallation, doctor and the dependency-injection panel.

### Diagnostics

```powershell
py -3 $wcli doctor
py -3 $wcli paths
py -3 $wcli tags
```

---

## Related files

- Marketplace catalog: [`../index.json`](../index.json)
- GUI dependency injection guide: [`gui_dependency_injection.md`](gui_dependency_injection.md)
- Plugin entries: [`../plugins/`](../plugins/)
- Theme entries: [`../themes/`](../themes/)
- Addon entries: [`../addons/`](../addons/)
- Validator: [`.github/validate_marketplace.py`](../.github/validate_marketplace.py)
