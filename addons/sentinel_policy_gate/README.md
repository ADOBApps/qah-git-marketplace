# Sentinel Policy Gate

Category: Sentinel addon - Version 1.0.0

Evaluates selected plugin folders against a declarative policy and returns
`allow`, `review` or `deny` with the evidence behind each decision. It is the
reference example for the `policy` capability.

## Policy keys

| Key | Default | Effect |
|---|---|---|
| `deny_ids` | `[]` | Plugin ids that must be denied |
| `allow_ids` | `[]` | When set, ids outside the list need review |
| `deny_imports` | `[]` | Imported modules that trigger deny |
| `review_imports` | `ctypes`, `subprocess`, `socket`, `pickle`, `marshal`, `ftplib`, `telnetlib` | Imports that trigger review |
| `require_manifest` | `true` | Missing `manifest.json` is a deny |
| `require_license` | `false` | Missing license field is a review |
| `deny_native_libs` | `false` | Any `.dll` / `.so` / `.dylib` is a deny |
| `max_files` | `2000` | Scan cap per target |
| `max_total_mb` | `250` | Size above this is a review |

Example:

```json
{
  "policy": {
    "deny_ids": ["bad_plugin"],
    "deny_imports": ["telnetlib"],
    "review_imports": ["ctypes", "subprocess"],
    "require_license": true,
    "deny_native_libs": false
  }
}
```

## Guarantees

- Static read-only scan; target code is never imported or executed.
- Decisions are advisory. This addon cannot enforce a Sentinel policy gate,
  unload a plugin or edit a manifest.
- Findings are capped by the addon host; the full decision table is in the
  report and `data.decisions`.
