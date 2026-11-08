# Sentinel Watchdog Planner

Category: Sentinel addon - Version 1.0.0

Computes SHA-256 baselines for selected plugins or libraries and writes a
`watches.json`-compatible plan. It is the reference example for the `watchdog`
capability.

## Output

```text
%USERPROFILE%\QAH\plugin_sentinel\addon_data\sentinel_watchdog_planner\
  watchdog_plan.json
```

The plan uses the same format as Plugin Sentinel's `watches.json`:

```json
{
  "format": "qah-plugin-sentinel-watches",
  "version": 1,
  "interval": 5,
  "watches": [
    {
      "key": "plugin:C:\\path\\to\\plugin",
      "type": "plugin",
      "path": "C:\\path\\to\\plugin",
      "label": "plugin",
      "digest": "…",
      "current": "…",
      "status": "ok"
    }
  ]
}
```

## Configuration

| Key | Default | Meaning |
|---|---|---|
| `interval` | `5` | Proposed check interval in seconds |
| `max_files` | `3000` | File cap per target |
| `max_total_mb` | `512` | Hashed byte cap per target |

## Boundaries

- Proposes baselines only; it cannot add, run, pause or remove a live watch.
- Reads only the selected targets and writes only its own data directory.
- Hash drift detects change, not maliciousness. A changed digest can be a
  legitimate update.
