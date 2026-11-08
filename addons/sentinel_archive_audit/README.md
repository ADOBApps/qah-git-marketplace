# Sentinel Archive Audit

Read-only inspection of plugin/addon ZIP central directories.

## Checks

- absolute paths and `..` traversal;
- symlink entries;
- encrypted entries;
- duplicate names;
- suspicious compression ratios / zip bombs;
- total uncompressed size and entry count;
- nested archives;
- executable/native files;
- missing root `manifest.json`;
- empty archives and VCS/cache metadata.

Nothing is extracted or executed. Supports `.qplugin.zip`, `.qah`, `.zip`,
`.whl`, `.qtheme` and folders containing archives.
