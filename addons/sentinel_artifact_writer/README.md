# Sentinel Artifact Writer

Category: Sentinel addon - Version 1.0.0

Exports a point-in-time audit artifact for the selected plugin folders or files
into the addon data directory. It is the reference example for the `write-files`
capability.

## Output

```text
%USERPROFILE%\QAH\plugin_sentinel\addon_data\sentinel_artifact_writer\
  artifact-YYYYmmdd-HHMMSS.json   full inventory and SHA-256 hashes
  artifact-YYYYmmdd-HHMMSS.md     human summary
  latest-artifact.json            most recent JSON
  latest-artifact.md              most recent summary
```

Each artifact records the target manifest, file sizes, per-file SHA-256 (files
up to 32 MB) and an aggregate digest. Use it to diff a plugin before and after
an update.

## Configuration

| Key | Default | Meaning |
|---|---|---|
| `label` | `QAH audit artifact` | Free-text label stored in the artifact |
| `hash_files` | `true` | Compute per-file SHA-256 |
| `max_files` | `400` | Per-target file cap |

```json
{"label": "before update", "hash_files": true, "max_files": 400}
```

## Guarantees

- Writes only inside its own addon data directory.
- Never imports or executes the target plugin.
- Never deletes, renames or modifies plugin files.
- Cannot spawn processes, load native libraries or use the network.
