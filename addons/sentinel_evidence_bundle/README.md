# Sentinel Evidence Bundle

Category: Sentinel addon - Version 1.0.0

One run produces a reviewable evidence bundle combining policy evaluation, hash
baselines and proposed watches. It is the reference example for combining
`policy`, `watchdog` and `write-files` in a single addon.

## Output

```text
%USERPROFILE%\QAH\plugin_sentinel\addon_data\sentinel_evidence_bundle\
  evidence-YYYYmmdd-HHMMSS.json   canonical bundle
  evidence-YYYYmmdd-HHMMSS.md     human summary
  latest-evidence.json
  latest-evidence.md
```

Each target entry contains:

- manifest summary (`id`, `name`, `version`, `category`, dependencies, license)
- aggregate SHA-256 baseline and file/byte counts
- policy decision (`allow` / `review` / `deny`) with reasons
- a proposed `plugin:<path>` or `library:<path>` watchdog entry

## Configuration

```json
{
  "max_files": 600,
  "policy": {
    "deny_ids": [],
    "deny_imports": [],
    "review_imports": ["ctypes", "subprocess", "socket", "pickle", "marshal"],
    "require_manifest": true
  }
}
```

## Use it for

- Attaching a deterministic before/after record to a release or ticket.
- Reviewing a contributor plugin before merging it.
- Keeping a known-good baseline before testing an update.

It is read-only and advisory: it cannot enforce a policy gate, install a watch,
unload a plugin or modify target files.
