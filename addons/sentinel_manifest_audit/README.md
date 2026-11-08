# Sentinel Manifest Audit

Audits plugin and addon manifests without loading or executing them.

Checks:

- required plugin fields and id format;
- `main` entry file exists;
- declared icon exists;
- dependencies are a list and do not use risky references;
- addon format, API version, id, entry, capabilities and timeout;
- duplicate ids across targets;
- `.stable`, `.old` and `__pycache__` artifacts.

## Use

**Plugin Sentinel -> Addons -> Sentinel Manifest Audit**, pin it, then add plugin
or addon folders as targets and run.

## Capabilities

```text
read-files
findings
report
```

Read-only. No network, no subprocesses, no native code.
