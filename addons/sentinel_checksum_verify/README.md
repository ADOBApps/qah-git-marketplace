# Sentinel Checksum Verify

Verifies SHA256 checksum manifests without modifying anything.

Supported formats:

```text
<64 hex>  path/to/file
SHA256 (path/to/file) = <64 hex>
```

Recognized manifest names include `SHA256SUMS`, `sha256sums.txt`,
`checksums.sha256` and `*.sha256`. Relative paths are resolved against the
manifest's folder.

## Use

1. **Plugin Sentinel -> Addons -> Sentinel Checksum Verify**.
2. Pin the addon hash.
3. Add a checksum file or a folder containing checksum manifests.
4. Run.

## Results

- `critical`: at least one checksum mismatch.
- `warning`: missing files, unreadable files or no checksum manifest.
- `ok`: every entry matched.

## Capabilities

```text
read-files
findings
report
```

Read-only. No network, no subprocesses, no native code.
