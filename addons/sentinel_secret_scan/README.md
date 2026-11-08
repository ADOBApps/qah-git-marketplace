# Sentinel Secret Scan

Read-only scan for likely secrets in text files:

- private-key headers;
- AWS access keys;
- GitHub tokens and fine-grained PATs;
- Slack, Google API and OpenAI-style keys;
- bearer tokens;
- generic `password`, `secret`, `token`, `api_key` and `access_key`
  assignments.

Every finding masks the value. The addon never prints the full secret in the
report or data.

## Use

**Plugin Sentinel -> Addons -> Sentinel Secret Scan**, pin it, add a folder or
file, and run.

This is a heuristic scanner, not a guarantee. Review findings before sharing
logs or reports.

## Capabilities

```text
read-files
findings
report
```

Read-only. No network, no subprocesses, no native code.
