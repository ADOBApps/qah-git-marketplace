# Sentinel Log Audit

Read-only Sentinel addon that scans logs and text files for:

- critical, fatal, crash, OOM and access-violation lines;
- exceptions, tracebacks, timeouts, permission failures and import errors;
- credential-looking assignments (`password=`, `token=`, `api_key=`, `Bearer ...`);
- private-key headers.

Credential-like values are masked in findings and reports. The addon never
prints the full value.

## Use

1. **Plugin Sentinel -> Addons**.
2. Select **Sentinel Log Audit**, press **Trust & pin hash**.
3. Add log/text files or folders as targets.
4. Press **Run selected**.

## Capabilities

```text
read-files
findings
report
```

Read-only. No network, no subprocesses, no native code.
