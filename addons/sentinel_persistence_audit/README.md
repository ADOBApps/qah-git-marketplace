# Sentinel Persistence Audit

Static audit for autostart/persistence patterns in QAH plugins.

## Checks

- registry `Run`/`RunOnce` keys and `winreg`;
- Startup folder / `shell:startup`;
- scheduled tasks (`schtasks`, TaskScheduler, `Register-ScheduledTask`);
- cron, systemd, `rc.local`;
- macOS LaunchAgents / LaunchDaemons;
- `sitecustomize`/`usercustomize`;
- `atexit.register`;
- `WScript.Shell`, `LoadLibrary`, `CreateProcess`, `ShellExecute`.

No audited code is imported or executed, and no registry or startup state is
changed.
