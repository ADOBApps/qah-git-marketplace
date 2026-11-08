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

Plugin Sentinel 1.2.11 also adds QAH's `app/` directory to the sandbox import
path. Plugins that use host APIs such as
`from plugins.libs.plugin_manager import PluginInfo` now load inside the
sandbox; older versions failed with `ModuleNotFoundError: No module named
'plugins'`. The sandbox still blocks network, process creation, native loading
and writes outside its work directory.

### Injected dependencies in Sentinel

Wheel Plugin Manager can inject pre-built wheels for QAH's frozen Python under
`plugins/vendor/<target>`. These are **packages**, not QAH plugins, so they do
not appear in Sentinel Inventory or Plugin Executions. Plugin Sentinel 1.2.4+
shows them in the **Dependencies** tab with target, package, version,
Python/platform and path, plus open/copy actions.

### Sentinel addon catalog (25)

All addons are report-only. Twenty use `read-files`, `findings`, `report`. Five
capability addons additionally use `write-files`, `network`, `policy` or
`watchdog`. No addon can call Sentinel internals, spawn processes, unload
plugins or kill anything. `write-files` is limited to the addon data directory;
`network` requires the capability; `policy` and `watchdog` are advisory markers.

| Addon | Purpose |
|---|---|
| `sentinel_file_audit` | File hashes, empty/large files, executable/script extensions |
| `sentinel_log_audit` | Log errors, crashes, timeouts and masked credentials |
| `sentinel_manifest_audit` | Manifest fields, ids, versions, entry points and duplicates |
| `sentinel_output_inventory` | Output file inventory and sizes |
| `sentinel_checksum_verify` | SHA256 checksum verification |
| `sentinel_secret_scan` | Private keys, cloud keys, tokens and generic secrets |
| `sentinel_resource_audit` | Heavy imports/dependencies (`pydft`, `pyqint`, `numba`, …) |
| `sentinel_dependency_audit` | Vendor manifest/dist-info consistency, duplicate/shadowed packages |
| `sentinel_network_audit` | Network imports/endpoints and undeclared network capability |
| `sentinel_archive_audit` | ZIP traversal, symlinks, encryption, zip bombs, executables |
| `sentinel_persistence_audit` | Registry Run keys, startup folders, scheduled tasks, cron/LaunchAgents, atexit |
| `sentinel_dangerous_api_audit` | `eval`/`exec`, pickle/marshal/yaml, shell, ctypes, winreg, dynamic import |
| `sentinel_capability_audit` | Declared capabilities vs static source evidence |
| `sentinel_import_audit` | Third-party imports not declared in manifest dependencies |
| `sentinel_lifecycle_audit` | Fast timers, `while True`, blocking sleeps, threads without cleanup, heavy imports |
| `sentinel_privacy_audit` | Hard-coded home paths, emails, credentials, secret logging, clipboard |
| `sentinel_diff_audit` | Compare two plugin folders: files, version, capabilities, dependencies, imports |
| `sentinel_license_audit` | Manifest/license/README/icon/version metadata |
| `sentinel_supply_chain_audit` | Install record, archive hash, source URL, version agreement, backup hygiene |
| `sentinel_crypto_audit` | MD5/SHA1, weak ciphers, ECB, disabled TLS verification, hard-coded keys |
| `sentinel_artifact_writer` | **write-files**: JSON/Markdown artifact with manifests, sizes, SHA-256 and aggregate digest |
| `sentinel_network_diagnostics` | **network**: bounded HEAD-only HTTPS reachability and latency checks |
| `sentinel_policy_gate` | **policy**: allow/review/deny decisions for imports, ids, manifest, license, size and native libraries |
| `sentinel_watchdog_planner` | **watchdog**: SHA-256 baselines and a `watches.json`-compatible plan (not installed) |
| `sentinel_evidence_bundle` | **policy + watchdog + write-files**: combined JSON/Markdown evidence bundle |

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
- hard timeout and process-tree kill;
- QAH's `app_packages` and DLL search directories in the child, so plugins that
  import `PySide6` work;
- sandbox interpreter selection prefers a Python that can import QAH's PySide6;
  incompatible Anaconda/MSYS Pythons are skipped;
- `ModuleNotFoundError: No module named 'PySide6'` was fixed in Sentinel 1.2.9.

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

The **Watchdog Builder** generates hash watchdogs (SHA256 baseline + QTimer +
`report.json`); its template and examples are documented in
`plugin_sentinel/WATCHDOG_BUILDER.md`. It does not monitor CPU/RAM.

---

## PyDFT Molecule Lab

Category: **Analysis**. A pydft-based single-point electronic-structure
workbench for small organic molecules and hormones.

### Molecules

Water, benzene, caffeine, estrone (E1), 17β-estradiol (E2), ethinylestradiol
(EE2), estriol (E3), testosterone and progesterone. Geometries are PubChem 3D
conformers; custom XYZ files can be imported.

### How to use

1. Restart QAH after installation.
2. Open **Plugins → Analysis → PyDFT Molecule Lab**.
3. Press **Probe dependencies**.
4. Select **water** first and press **Run calculation**.
5. Review energy, HOMO/LUMO, gap, charges, dipole and orbital slices.
6. Select a heavier molecule only after the water/benzene smoke test.
7. Use **Stop after current SCF step** or **Pause** to control load.
8. Export Markdown/JSON/PNG/SVG from the report and orbital tabs.

### Output

- total energy (Ha/eV);
- HOMO, LUMO and HOMO–LUMO gap;
- hardness, softness, electronegativity and electrophilicity;
- Mulliken charges and dipole moment;
- HOMO±3 orbital window, 2D orbital slices and orbital-energy diagram;
- Markdown/JSON reports and PNG/SVG orbital plots.

pydft Kohn–Sham is the only SCF engine. There is no Hartree–Fock fallback;
non-converged results are marked and can be retried with a higher iteration cap
or looser tolerance.

### CPU limits

pydft/pyqint are CPU-only. The header reports the number of logical CPU threads
detected by the OS, and the selector can use any value from 1 to that total. The
plugin defaults to one native thread, a low-power grid, a bounded SCF iteration
cap, a pause between SCF steps and a **Stop after current SCF step** button. It
never starts a calculation on load. Heavy hormones
(E2/EE2/E3/testosterone/progesterone) require confirmation and can run for
minutes; use the low-power preset and an external temperature watchdog. Start
with water or benzene.

### GPU?

No. pydft/pyqint have no GPU backend. An integrated GPU has no CUDA path; GPU
quantum chemistry requires a separate CUDA stack such as GPU4PySCF on an NVIDIA
GPU.

### Dependencies

Inject `pydft` with Wheel Plugin Manager into `global` or the private
`pydft_molecule_lab` target. pydft brings pyqint, pylebedev, numpy, scipy and
numba. matplotlib is optional for plots and is normally bundled with QAH.

```powershell
$wpm = "C:\path\to\wheel_plugin_manager\qah_wheel_cli.py"
py -3 $wpm inject pydft --target pydft_molecule_lab
py -3 $wpm deps-verify pydft_molecule_lab pydft
```

Use the private target to avoid shadowing QAH's numpy/scipy. If QAH already
provides the whole stack, `--no-deps` keeps the injection minimal; check the
result with **Probe dependencies**.

---

## SEQItachi

Category: **Analysis**. A QAH-native structure and quantum-chemistry workbench
inspired by **SEQCROW** for ChimeraX.

SEQCROW is **GPL-3.0** open source (`QChASM/SEQCROW`). SEQItachi is an
independent GPL-3.0 implementation; no SEQCROW code is copied and it bundles
neither SEQCROW nor AaronTools.

### Implemented

- XYZ import, 3D ball-and-stick view, atom/bond tables;
- add/delete atoms, change element, add/remove bonds, bond order and length,
  rotate/translate/center;
- formula, molecular weight, center of mass, radius of gyration;
- distance, angle, dihedral;
- approximate Sterimol L/B1–B5, cone angle and buried-volume voxels;
- QM input builders for Gaussian, ORCA, Psi4, Q-Chem, xTB and sqm;
- output parsing for Gaussian, ORCA, Psi4 and Q-Chem: energy, geometry,
  HOMO/LUMO, frequencies and excited states;
- broadened IR and UV/Vis plots;
- RRHO thermochemistry: ZPE, thermal correction, entropy and Gibbs correction;
- Gaussian cube import and 2D X/Y/Z slices;
- optional external-tool detection for ORCA, xtb, CREST, Gaussian, Psi4 and
  Q-Chem. Paths are stored in `%USERPROFILE%\QAH\seqitachi\toolchain.json`;
  missing tools raise an actionable error and no job is started. SEQItachi never
  bundles or auto-installs these executables.

### How to use

1. Open **Plugins → Analysis → SEQItachi**.
2. In **Structure**, load an XYZ file or a Gaussian/ORCA/Psi4/Q-Chem output.
3. Inspect atoms/bonds in **Edit**; add/delete atoms, change elements, edit
   bonds, rotate or translate.
4. Use **Analysis** for formula, MW, COM, radius of gyration, distance, angle,
   dihedral, and approximate Sterimol/cone/buried volume.
5. In **QM Input**, select software/method/basis/job, preview and save.
6. In **Results**, load an output file for energy, HOMO/LUMO, frequencies,
   excitations, IR/UV plots and RRHO thermochemistry.
7. In **Cube**, load a Gaussian cube and slice along X/Y/Z.
8. In **Tools**, press **Detect tools**; missing executables are reported but do
   not crash the plugin.

### Tools and external executables

SEQItachi does **not** bundle ORCA, xtb, CREST, Gaussian, Psi4 or Q-Chem.
Detection order:

1. custom path in `%USERPROFILE%\QAH\seqitachi\toolchain.json`;
2. environment variables such as `QAH_ORCA`, `QAH_XTB`, `QAH_CREST`;
3. `PATH`;
4. common install locations.

If a tool is missing, actions that need it raise `ToolNotFoundError`; no job
starts. CREST is not installed by default and is normally a Linux executable.
On Windows use WSL/Linux CREST or the RDKit + xtb alternative planned for a
later release.

### Optional future dependencies

The 1.1.0 core is pure QAH/numpy/scipy/matplotlib. The planned ChimeraX-level
features will use optional wheels injected into the private `seqitachi` target:

```powershell
$wpm = "C:\path\to\wheel_plugin_manager\qah_wheel_cli.py"

# GPL-3.0; exact Sterimol/cone/buried volume/ligand library/normal modes/orbitals
py -3 $wpm inject AaronTools --no-deps --target seqitachi

# BSD-3; 2D sketcher, SMILES, ETKDG 3D embedding
py -3 $wpm inject rdkit --no-deps --target seqitachi

# BSD/MIT; 3D picking, mouse modes, isosurfaces
py -3 $wpm inject vtk pyvista pyvistaqt qtpy pooch scooby --no-deps --target seqitachi

# BSD-3; marching cubes for orbital isosurfaces
py -3 $wpm inject scikit-image --no-deps --target seqitachi
```

`--no-deps` avoids duplicating QAH's numpy/scipy/matplotlib. Verify imports with
**Tools**/**Probe** before use. WPM cannot inject CREST/ORCA/xtb; those remain
user-supplied executables.

### Roadmap, not yet implemented

ChimeraX mouse modes and commands, 2D sketcher, AaronTools fragment library,
CREST conformer search, transition-state interpolation, normal-mode animation,
full 3D orbital isosurfaces, point groups, and the complete ligand Sterimol
library. SEQItachi is **core-equivalent**, not a drop-in SEQCROW clone.

---

## Resource Watchdog

Category: **Tools**. A read-only runtime monitor for QAH.

- QAH PID, CPU %, RSS and thread count;
- child processes with PID, name, CPU and RSS;
- heavy modules currently loaded in QAH (`pydft`, `pyqint`, `numba`, `scipy`,
  `matplotlib`, `torch`, `tensorflow`, `jax`, `cupy`, `pyscf`, `rdkit`);
- CPU/RSS warning thresholds and a JSON report;
- monitoring is off until **Start monitoring** is pressed; default interval 5 s.

QAH plugins share one process, so CPU is attributed to QAH as a whole. The
watchdog can show that pyqint/pydft are loaded and QAH is busy, but not which
plugin caused it. It **never kills, unloads, suspends or throttles** anything.

### How to use

1. Open **Plugins → Tools → Resource Watchdog**.
2. Read the QAH PID, CPU, RSS, thread count and loaded heavy modules.
3. Set **Interval**, **CPU warning** and **RSS warning**.
4. Press **Start monitoring**; monitoring is off by default.
5. Press **Check now** for a one-shot sample.
6. Open `%USERPROFILE%\QAH\resource_watchdog\report.json` from **Open report**.
7. Press **Stop** when finished.

psutil is optional; inject it into `global` or `resource_watchdog`:

```powershell
py -3 $wpm inject psutil --target resource_watchdog
py -3 $wpm deps-verify resource_watchdog psutil
```

Without psutil, loaded heavy modules are still listed but CPU/RSS are not
sampled.

### Static resource audit addon

`sentinel_resource_audit` is a report-only Sentinel addon. It scans plugin
folders for heavy imports and declared dependencies. It cannot inspect live CPU,
call Sentinel internals or unload/kill anything.

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

### What WPM can inject

WPM installs **pre-built wheels**, not source packages:

| Wheel kind | Example | Notes |
|---|---|---|
| Pure Python `py3-none-any` | AaronTools | Easiest; no ABI issues |
| CPython C/C++ `cp312-cp312-win_amd64` | RDKit, VTK, scikit-image | Must match QAH's Python and platform |
| Rust/maturin/PyO3 `cp312` or `abi3` | native helper | Works like any native wheel; no Rust compiler needed for injection |
| `abi3` | compatible native wheels | Forward-compatible within the CPython ABI |

Rejected: source distributions (`.tar.gz`), sdists, wheels for another Python
minor, and wheels for another OS/architecture. Building a wheel needs
Rust/maturin or the project's native toolchain; injecting a finished wheel does
not.

External programs are **not wheels** and cannot be injected:
ORCA, xtb, CREST, Gaussian, Psi4 and Q-Chem must be installed by the user and
selected in the plugin's tool settings.

### Private targets and `--no-deps`

Prefer a private target per plugin:

```powershell
py -3 $wcli inject pydft --target pydft_molecule_lab
py -3 $wcli inject psutil --target resource_watchdog
py -3 $wcli inject AaronTools --no-deps --target seqitachi
```

`--no-deps` avoids duplicating QAH's numpy/scipy/matplotlib in the vendor path.
Vendor paths are prepended to `sys.path`; a duplicate numpy/scipy can shadow
QAH's copy. After injection always run:

```powershell
py -3 $wcli deps
py -3 $wcli deps-verify <target> <package>
```

Then restart QAH or press the plugin's dependency-probe button.

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
