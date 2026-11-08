# Sentinel Dependency Audit

Report-only audit of QAH vendor dependency sets and plugin metadata.

## Checks

- stale `qah_dependencies.json` package list;
- installed `*.dist-info` missing from the manifest;
- manifest package with no `*.dist-info`;
- missing version in `METADATA`;
- duplicate manifest packages;
- `no_deps` set while packages exist;
- manifest target/folder mismatch;
- loose top-level package folders;
- same package installed in multiple targets (private/global shadowing).

It does not import vendor packages, run pip, modify manifests or unload
anything. Targets can be `plugins/vendor`, a specific vendor target folder, or a
plugin folder with `manifest.json`.
