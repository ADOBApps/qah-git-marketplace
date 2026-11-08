# Runtime Forge

Isolated, **per-plugin Python runtimes** for QAH with hash-locked wheels and a
JSON-RPC host.

Runtime Forge is the installer side of the dependency story: Plugin Sentinel is
the audit/security side. Forge never imports heavy packages into QAH; it builds
a per-plugin `site-packages` and runs plugin code in a separate interpreter.

> **MVP scope.** Wheels only. No pip, setup.py, sdists, cargo or build scripts.
> There is no automatic dependency resolver: the lock must list every wheel.

---

## Why

Some plugins need modules that are not in QAH, for example `pydft` (pure Python)
or numpy/scipy wheels. Installing them into QAH's shared `app_packages` risks
version conflicts and ABI problems. Runtime Forge keeps each plugin’s packages
separate.

## Layout

```text
%USERPROFILE%\QAH\runtimes\<plugin_id>\
  current.json
  versions\<build>\
    site-packages\
    bin\
    lock.json
    build.json
```

Previous builds are retained for rollback.

## Lock file

```json
{
  "format": "qah-runtime-lock",
  "version": 1,
  "plugin_id": "pydft_plugin",
  "runtime": "python",
  "python": "3.12.5",
  "interpreter": "C:\\Python312\\python.exe",
  "wheels": [
    {
      "filename": "pydft-0.1.0-py3-none-any.whl",
      "sha256": "...",
      "size": 12345,
      "python_tag": "py3",
      "abi_tag": "none",
      "platform_tag": "any"
    }
  ]
}
```

Wheels are checked against the interpreter Python version and the host platform
tags before extraction. SHA256 is verified at install time.

## Python interpreter

Runtime Forge probes `python3`, `python`, and on Windows `py -3`. QAH's Briefcase
Windows bundle often has no `python.exe`; select a portable/system Python in the
Builder. The interpreter is shared, while `site-packages` is isolated per plugin.

## UI

- **Runtimes** — active builds, doctor, rollback, remove, open folder.
- **Builder** — plugin id, interpreter, wheel list, lock preview, install.
- **Host** — ping, import, call and execute code in the isolated runtime.
- **Documentation** — protocol, lock format, Rust/native notes, limitations.

## CLI

```powershell
python runtime_forge_cli.py list
python runtime_forge_cli.py lock --plugin pydft_plugin --wheels *.whl --out pydft.lock.json
python runtime_forge_cli.py install pydft.lock.json --wheel-dir .
python runtime_forge_cli.py doctor pydft_plugin
python runtime_forge_cli.py ping pydft_plugin
python runtime_forge_cli.py import pydft_plugin pydft
python runtime_forge_cli.py call pydft_plugin pydft add --args "[1,2]"
```

## Sentinel integration

After install, Runtime Forge registers the runtime build directory and native
files with `plugin_sentinel.sentinel_api`. Run the host under Sentinel's sandbox
for behavioural testing.

## Rust / native

Rust has no runtime to install. Ship a prebuilt wheel (maturin) or platform
binary; validate it with Plugin Sentinel's native scanner. Do not require cargo
on the user machine.

## Limitations

- No dependency resolver; list all wheels in the lock.
- Wheels only; no source builds.
- Shared interpreter; only `site-packages` is isolated.
- No automatic Python download in this MVP.
- A Python environment is not a security boundary.

---

Version: 1.0.0  
Author: Acxel Orozco
