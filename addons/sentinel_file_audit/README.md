# Sentinel File Audit

A read-only **Plugin Sentinel addon** that audits files and folders.

- hashes files up to 200 MB (SHA256)
- flags empty files and files larger than 100 MB
- flags executable/installer extensions (`exe`, `dll`, `msi`, `ps1`, …)
- flags script extensions as medium severity
- summarizes folder file counts, total bytes and top extensions
- returns a markdown report and structured findings

It uses only the standard library and the Sentinel addon API v1. It never
writes outside its addon data directory and never uses the network.

## Install

**Plugin Sentinel → Addons → Import .qah…**, or install it from
**Git Plugin Marketplace → Addons**.

Then select the addon, press **Trust & pin hash**, add target files/folders and
press **Run selected**.

## Capabilities

```text
read-files
findings
report
```

## Package

`sentinel_file_audit-1.0.0.qah`
