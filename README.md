# QAH Git Marketplace

Public plugin registry for **Quantum Analysis Helper**, used by the
[Git Plugin Marketplace](https://github.com/ADOBApps/qah-git-marketplace/releases)
plugin. It stores the catalog (`index.json`) and the `.qplugin.zip` files in
Git instead of Firebase.

## For users

1. Download the latest **`git_plugin_marketplace-*.qplugin.zip`** from
   [Releases](https://github.com/ADOBApps/qah-git-marketplace/releases/latest).
2. In QAH: **Plugins → Import Plugin…** and choose the ZIP.
3. Restart QAH / scan plugins, then open **Git Plugin Marketplace**.
4. The repository is already the default; click **Refresh**, choose a plugin and
   **Install** or **Update**.

No GitHub account or token is needed to browse or install plugins from this
public repository.

## Tool guides

See [`docs/tool_guides.md`](docs/tool_guides.md) for practical usage notes for
**Theme Studio**, **Sentinel Addon Studio**, **Plugin Sentinel** and
**Wheel Plugin Manager**, including publishing and dependency injection.

## Layout

```text
index.json                              catalog
docs/tool_guides.md                     public tool usage guide
plugins/
  <id>/
    manifest.json                       canonical manifest
    README.md                           optional description
    <version>/
      <id>-<version>.qplugin.zip        plugin archive
themes/<id>/...                         theme assets
addons/<id>/...                         Sentinel addon assets
.github/
  CODEOWNERS                            owner review required
  validate_marketplace.py               catalog/ZIP validator
  workflows/validate-marketplace.yml    CI for every PR
```

`index.json` version entries contain the ZIP `path`, `sha256`, `size`,
`changelog` and `published` timestamp. Installs verify the SHA256 and reject
unsafe archives.

## Contributing plugins

**Uploads are pull-request only.** `master` is protected; only the repository
owner can merge or delete. See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact
fork → publish → PR workflow.

The Git Plugin Marketplace plugin can do it automatically: tick **Submit as a
pull request** in the Publish dialog, or run
`git_marketplace_cli.py submit <folder>`. It forks, commits to a branch and
opens the PR; only the owner merges.

Maintainer deletion: only the owner's write token can commit a removal; the
plugin's **Delete from marketplace** action fails with 403 for everyone else.

## Security and licensing

- Publish only plugins you own or are allowed to redistribute.
- A `.qplugin.zip` usually contains Python source; everything in this public
  repository is publicly downloadable. Do **not** submit private, paid or
  NDA-covered code here — use a private staging repository instead.
- Never commit tokens, credentials or private keys.

## Maintainer

Acxel Orozco — [@ADOBApps](https://github.com/ADOBApps)
