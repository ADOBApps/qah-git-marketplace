# QAHtop

## 1.0.2

- Reduced UI load: fixed table column widths instead of per-row
  `ResizeToContents`, batched table updates, and preserved selection/scroll.
- Default refresh is 3 s; 1.5 s and 5 s remain selectable.
- Auto-refresh stops while the QAHtop tab is hidden and restarts when shown.
- This fixes QAH becoming sluggish while QAHtop stayed open in a background tab.

A lightweight **htop-style read-only process monitor** for QAH.

It lists processes, CPU, memory, disk and process counts. It never ends or
modifies a process.

## Optional dependency: psutil

QAHtop does **not** require psutil. It prefers it:

- **With psutil>=5.9.0:** CPU, memory, per-process CPU, RSS, thread count, user
  and status come from psutil.
- **Without psutil:** it falls back to Windows `tasklist` or POSIX `ps`, and
  shows the metrics those tools provide.

The manifest marks this explicitly:

```json
"dependencies": ["psutil>=5.9.0"],
"optional_dependencies": ["psutil>=5.9.0"],
"dependency_mode": "optional"
```

That distinguishes QAHtop from plugins where psutil is mandatory.

This makes QAHtop a useful **injection probe**:

1. Open Wheel Plugin Manager.
2. Inject the dependency:

   ```text
   Package: psutil
   Target : global
   ```

3. Open QAHtop.
4. Press **Detect dependencies**.

The dependency badge changes from:

```text
fallback (no psutil)
```

to:

```text
psutil 7.2.2
```

If QAHtop was already open before injection, **Detect dependencies** re-scans the
vendor paths and retries the import without restarting QAH. A restart is still
recommended for other plugins that import psutil during their own startup.

## How detection works

QAHtop contains a small optional bootstrap:

```python
def activate_vendor(targets=("qahtop", "global")):
    root = qah_home() / "plugins" / "vendor"
    for target in targets:
        path = root / target
        if path.is_dir() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
    importlib.invalidate_caches()


def probe_psutil(force=False):
    activate_vendor()
    try:
        import psutil
        return psutil
    except Exception:
        return None
```

This is intentionally optional. A future plugin can copy the same pattern, or
simply rely on Wheel Plugin Manager's startup activation and import psutil
lazily.

## Features

- CPU, memory, disk and process-count summary
- PID, process, user, CPU %, memory MB, threads and status columns
- sort by CPU, memory, PID or name
- filter by name, user or PID
- 1.5 s / 3 s / 5 s refresh, pause and manual refresh
- **Detect dependencies** probe
- read-only: no kill, suspend or priority changes
- highlights the QAH process
- selection is preserved across refreshes

## Files

```text
manifest.json
__init__.py          QAH entry point
qahtop_widget.py     UI, optional psutil probe and tasklist/ps fallback
icon.svg
README.md
```

## Security

QAHtop runs with normal QAH plugin privileges. It invokes `tasklist` or `ps`
only in fallback mode and only to list processes. It does not execute any
process control operation.

License: GPLv3 or later.
