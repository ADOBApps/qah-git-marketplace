# Git Plugin Marketplace

A **Git-backed alternative** to QAH's Firebase Plugin Marketplace. It keeps the
same job — browse, install, update and remove plugins — but the catalog and the
plugin ZIPs live in a Git repository (GitHub) instead of Firebase.

- Works inside QAH (PySide6 widget)
- Works headless from the CLI (no Qt, no QAH imports)
- Reads public repositories without credentials
- Writes (publish/delete/init) with a GitHub token
- One Git commit per publish/delete, so the history is the audit log
- Linux / macOS / Windows

## 1.2.1

- The UI now also blocks deleting `git_plugin_marketplace` from its own catalog,
  in addition to blocking install/update/uninstall of its running folder.
- Core install/uninstall still refuses to touch the running marketplace folder.

## 1.2.0

- Added **Sentinel addons** as a first-class asset: `addons` catalog section,
  **Addons** filter, `.qah` install/update/uninstall/version selection, and
  `addons/<id>/<version>/<id>-<version>.qah` repository layout.
- Addons install to `%USERPROFILE%\QAH\plugin_sentinel\addons\<id>\` and are
  hash-pinned automatically from the install record; the Sentinel Addons tab is
  refreshed after install.
- Added addon publishing: `list-addons`, `install-addon`, `uninstall-addon`,
  `publish-addon`.
- **Self-update guard:** the marketplace refuses to install, downgrade or
  uninstall `git_plugin_marketplace` from its own running UI/process, and
  excludes itself from **Update all**. Use QAH's system marketplace, the manual
  ZIP importer, or update with QAH closed.
- **Update all** now covers user plugins, themes and Sentinel addons.
- Old catalogs without `addons` remain valid.

## 1.1.4

- Added first-class **theme assets**: `themes` catalog section, `.qtheme.zip`
  install/update/uninstall, `themes/<id>/<version>/` repository layout.
- Themes install flat into the user theme directory (`theme.json` + CSS) so the
  existing Theme Manager sees them without a QAH restart; Theme Manager is
  refreshed after install.
- Added theme publishing CLI: `list-themes`, `install-theme`,
  `uninstall-theme`, `publish-theme`.
- After installing/updating a loaded user plugin, the marketplace offers
  **Reload now** (via QAH PluginManager) or **Restart later**. System/wheel
  plugins and the marketplace itself are never auto-reloaded.
- Old catalogs without `themes` remain valid; old marketplace clients ignore the
  new section.

## 1.1.3

- Added **Install version** selection: choose any published version, including
  an older one, and replace the current user-plugin copy.
- Update/version-install is disabled for system and wheel plugins; **Update all**
  only touches user-installed plugins. System plugins stay owned by the QAH
  installer and cannot be shadowed or blocked from the marketplace.

## 1.1.2

- Fixed a QThread cleanup race: after a successful publish, the refresh task
  could start before the previous task's `finished` signal was handled. The old
  handler then deleted the new running thread, which could abort QAH with a Qt
  fatal error (`Qt6Core.dll`, `0xc0000409`).
- Publish now defers its catalog refresh until the publish worker has finished.

---

## Why Git instead of Firebase

| | Firebase marketplace | Git marketplace |
|---|---|---|
| Catalog | Cloud Functions + Firestore | `index.json` in the repo |
| Plugin files | Firebase Storage | ZIPs committed to the repo |
| Upload auth | shared admin secret | GitHub token (`contents: write`) |
| Delete | Cloud Function | a commit that removes the entry |
| History / audit | limited | full `git log` |
| Hosting | Google Cloud | any GitHub account/org, public or private |
| Payments | Mercado Pago integration | **not implemented** (metadata only) |

The paid-plugin fields (`price`, `currency`, `price_model`, `license`) are kept
for compatibility and display, but the Git marketplace does **not** process
payments. Treat it as a free/private registry.

---

## Repository layout

```text
index.json                              catalog (see below)
README.md                               auto-generated on init
plugins/
  <id>/
    manifest.json                       canonical manifest
    README.md                           optional description
    <version>/
      <id>-<version>.qplugin.zip        plugin archive
themes/
  <id>/
    <version>/
      <id>-<version>.qtheme.zip         theme archive
addons/
  <id>/
    addon.json                          canonical Sentinel addon manifest
    README.md                           optional description
    <version>/
      <id>-<version>.qah                Sentinel addon archive
```

`index.json`:

```json
{
  "schema": 1,
  "name": "QAH Git Marketplace",
  "description": "",
  "updated": "2026-11-06T12:00:00Z",
  "plugins": [
    {
      "id": "wheel_plugin_manager",
      "name": "Wheel Plugin Manager",
      "version": "1.1.1",
      "author": "Acxel Orozco",
      "description": "...",
      "category": "development",
      "dependencies": [],
      "price": 0,
      "currency": "USD",
      "price_model": "free",
      "license_type": "free",
      "homepage": "https://github.com/ADOBApps/wheel_plugin_manager",
      "versions": [
        {
          "version": "1.1.1",
          "path": "plugins/wheel_plugin_manager/1.1.1/wheel_plugin_manager-1.1.1.qplugin.zip",
          "url": "",
          "sha256": "...",
          "size": 53558,
          "changelog": "First release",
          "published": "2026-11-06T12:00:00Z",
          "yanked": false
        }
      ]
    }
  ]
}
```

A version may also use `"url"` instead of `"path"` to point at a GitHub Release
asset or any HTTPS ZIP; `sha256` is verified when present.

---

## Install the plugin itself

Copy this folder to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\git_plugin_marketplace\
```

Linux/macOS:

```text
~/QAH/plugins/python_plugins/git_plugin_marketplace/
```

Restart QAH, then **Plugins → Scan for new or removed plugins**. The plugin
appears as **Git Plugin Marketplace**.

You can also import `git_plugin_marketplace.qplugin.zip` through
**Plugins → Import**.

---

## Configure the repository

The plugin ships with the public catalog as its default:

```text
owner  : ADOBApps
repo   : qah-git-marketplace
branch : master
```

You only need to change this if you run your own marketplace. Open
**Plugins → Git Plugin Marketplace → Settings**, or use the CLI:

```powershell
py -3 git_marketplace_cli.py config --owner ADOBApps --repo qah-marketplace
py -3 git_marketplace_cli.py doctor
```

Fields:

| Field | Meaning |
|---|---|
| Owner | GitHub user or organisation |
| Repository | repository that stores `index.json` |
| Branch | usually `main` |
| Token | optional; needed for private repos and for publishing |
| API base | `https://api.github.com` (change only for GitHub Enterprise) |
| Catalog cache | seconds before re-reading `index.json` |

Token resolution order:

1. the token saved in Settings (unless *Remember* is off),
2. `QAH_GIT_MARKETPLACE_TOKEN`,
3. `GITHUB_TOKEN`, then `GH_TOKEN`,
4. `gh auth token` if the GitHub CLI is installed.

Create a **fine-grained token** with:

- *Repository access*: the marketplace repository (and your fork, if you submit
  pull requests),
- *Permissions*:
  - **Contents: Read and write** on the marketplace (owner) or on your fork
    (contributor),
  - **Pull requests: Read and write** on the upstream marketplace when you use
    **Submit as a pull request**.

A classic PAT with `public_repo` works for public repositories; `repo` also
covers private ones.

The token is stored in `~/.qah/git_marketplace.json` with mode `0600` on
Linux/macOS. On Windows it relies on the user-profile ACL. Never commit that
file.

Environment overrides (handy for CI):

```text
QAH_GIT_MARKETPLACE_REPO=owner/repo
QAH_GIT_MARKETPLACE_BRANCH=main
QAH_GIT_MARKETPLACE_TOKEN=...
QAH_GIT_MARKETPLACE_CONFIG=/path/to/config.json
QAH_GIT_MARKETPLACE_CACHE=/path/to/cache.json
```

### Initialize an empty repository

The repository must exist on GitHub and have a branch (an empty repo is also
supported). Then:

```powershell
py -3 git_marketplace_cli.py init --name "QAH Git Marketplace"
```

or use **Initialize repository** in Settings. This creates `index.json` and
`README.md` in one commit and refuses to overwrite an existing catalog.

---

## Browse, install, update

GUI: search, category filter, **Refresh**, **Update All**, details pane with all
versions and changelogs, **Install**, **Update**, **Uninstall**, **Info**, and
right-click **Delete from marketplace**.

CLI:

```powershell
py -3 git_marketplace_cli.py list
py -3 git_marketplace_cli.py info wheel_plugin_manager
py -3 git_marketplace_cli.py install wheel_plugin_manager
py -3 git_marketplace_cli.py install wheel_plugin_manager --version 1.1.0
py -3 git_marketplace_cli.py updates
```

Installation downloads the ZIP, verifies its SHA256 against `index.json`,
extracts it (stripping a single wrapper folder), checks that the manifest `id`
matches, then swaps the plugin directory atomically. Existing installs are
backed up and restored if the swap fails.

Plugins are installed into QAH's classic plugin directory:

```text
%USERPROFILE%\QAH\plugins\python_plugins\<id>\
~/QAH/plugins/python_plugins/<id>/
```

Bundled/system plugins are shown as installed but cannot be uninstalled from the
marketplace.

---

## Themes and Sentinel addons

Use the **Plugins / Themes / Addons** filter above the list.

### Themes

Themes install flat into `%USERPROFILE%\QAH\themes\<id>.json` + `<id>.css`, so
QAH's existing Theme Manager sees them without a restart. Existing `theme.json`
files and their CSS keep working.

```powershell
py -3 git_marketplace_cli.py list-themes
py -3 git_marketplace_cli.py install-theme studio_aurora
py -3 git_marketplace_cli.py publish-theme "C:\path\to\theme" --changelog "Aurora palette"
```

### Sentinel addons

Addons are `.qah` source packages with `addon.json` + a Python entry point. They
are **not** QAH plugins: they run only in Plugin Sentinel's Addons tab, in an
isolated process. The marketplace shows declared capabilities and API version
before installation.

Addons install into:

```text
%USERPROFILE%\QAH\plugin_sentinel\addons\<id>\
```

and get a `.qah_install.json` marker with the archive SHA256. Sentinel pins the
installed folder hash automatically after a marketplace install.

```powershell
py -3 git_marketplace_cli.py list-addons
py -3 git_marketplace_cli.py install-addon dft_output_checks
py -3 git_marketplace_cli.py uninstall-addon dft_output_checks
py -3 git_marketplace_cli.py publish-addon "C:\path\to\addon" --changelog "First release"
```

Required `addon.json` shape:

```json
{
  "format": "qah-sentinel-addon",
  "id": "dft_output_checks",
  "name": "DFT Output Checks",
  "version": "1.0.0",
  "api_version": 1,
  "author": "You",
  "description": "Checks DFT output files",
  "main": "main.py",
  "entry": "run",
  "capabilities": ["read-files", "findings", "report"]
}
```

---

## Self-update safety

Git Plugin Marketplace refuses to install, downgrade or uninstall
`git_plugin_marketplace` from its own running UI/process. It also excludes
itself from **Update all**.

To update it safely:

- use QAH's system Plugin Marketplace,
- use QAH's manual ZIP importer, or
- replace it with QAH closed.

Other plugins, themes and Sentinel addons update normally. The installer still
uses staging + backup + atomic replace, so a failed extraction restores the
previous folder.

---

## Publish a plugin

GUI: **Publish Plugin…** → choose the folder → manifest fields are filled in →
edit version/changelog → Publish.

CLI:

```powershell
py -3 git_marketplace_cli.py publish "C:\Users\HP\QAH\plugin_projects\wheel_plugin_manager" `
    --changelog "Windows-safe wheel installer, validate/fix commands"
```

What happens:

1. the folder is validated (`manifest.json`, `__init__.py`, valid `id`),
2. a `.qplugin.zip` is built with the manifest at the archive root; `.git`,
   `__pycache__`, `dist`, `target`, `.venv`, `*.pyc`, `*.qplugin.zip` and
   editor folders are excluded,
3. SHA256 and size are computed,
4. `index.json`, `plugins/<id>/manifest.json`, optional `README.md` and the ZIP
   are written in **one Git commit** using the GitHub Git Data API,
5. an existing version with the same number is replaced; other versions stay.

### Submit as a pull request

For a protected/public catalog where only the owner merges:

GUI: **Publish Plugin…** → tick **Submit as a pull request (fork + PR)**. It is
pre-selected automatically when your token does not have write access to the
upstream repository.

CLI:

```powershell
py -3 git_marketplace_cli.py submit "C:\path\to\plugin" `
    --changelog "What changed"
```

The plugin:

1. builds and validates the ZIP exactly like `publish`,
2. identifies your GitHub account,
3. creates (or reuses) your fork of the marketplace,
4. creates a branch from the upstream head,
5. commits `index.json`, manifest, README and ZIP to **your fork**,
6. opens a pull request against the upstream base branch.

Nothing changes in the upstream catalog until the owner merges. CI (`validate`)
runs on the PR. Failures delete the temporary branch. Add `--draft` for a draft
PR.

Build locally without uploading:

```powershell
py -3 git_marketplace_cli.py validate "C:\path\to\plugin"
py -3 git_marketplace_cli.py build "C:\path\to\plugin" --out dist
```

---

## Delete

GUI: right-click a plugin → **Delete from marketplace…** → delete the current
version or all versions.

```powershell
py -3 git_marketplace_cli.py delete my_plugin --version 1.0.0
py -3 git_marketplace_cli.py delete my_plugin --all
```

Deletion removes the entry and files from the branch tip. Git history keeps the
old objects, so this is not a secure erase. Force-pushing/history rewriting is
outside the plugin.

---

## Publishing to the public catalog

The default catalog (`ADOBApps/qah-git-marketplace`) is **public read, pull-request
write**:

- anyone can browse/install without a token;
- `master` is protected; contributions go through a fork and a PR;
- CI validates `index.json` and every ZIP (`validate` check);
- only the owner merges and deletes.

See the catalog's
[CONTRIBUTING.md](https://github.com/ADOBApps/qah-git-marketplace/blob/master/CONTRIBUTING.md).
The plugin can open the PR automatically: tick **Submit as a pull request** in
the Publish dialog (or run `git_marketplace_cli.py submit`). It forks, commits to
a branch and opens the PR; only the owner merges.

---

## How it works

- **Reads** use the GitHub Contents API. With a token it works for private
  repositories; without one only public repositories work.
- **Writes** use the Git Data API: read branch head → create blobs → create tree
  → create commit → update ref. If the branch moved between read and update, the
  whole operation is retried once.
- **Caching**: the catalog is cached in
  `~/.qah/git_marketplace_cache.json` for `cache_ttl` seconds. **Refresh** in
  the UI forces a re-read. A publish/delete updates the cache immediately.
- **Integrity**: every version stores a SHA256; installs fail closed on a
  mismatch.
- **ZIP safety**: absolute paths, `..`, symlinks and `__MACOSX` entries are
  rejected.

### Limits

- GitHub rejects files larger than **100 MB**. The plugin refuses larger ZIPs.
- Every version stays in Git history, so the repository grows over time. For
  large/binary plugins prefer `"url"` entries pointing at GitHub Releases (the
  plugin supports them; uploading release assets is manual for now).
- GitHub API rate limits apply; the catalog cache reduces reads.

---

## CLI reference

```text
doctor                      configuration + connection test
config [--owner --repo-name --branch --token --api-base --cache-ttl]
                            save settings (--show to print)
list [--refresh]            list catalog plugins
info <id>                   full JSON for one plugin
install <id> [--version]    download, verify and install
uninstall <id>              remove from the user plugin folder
publish <folder> [--version] [--changelog] [--homepage]
                            [--name] [--author] [--category] [--description]
submit  <folder> [--version] [--changelog] [--homepage] [--draft]
                            [--name] [--author] [--category] [--description]
delete <id> [--version|--all]
init [--name] [--description]
updates                     compare installed vs catalog
list-themes                 list theme assets
install-theme <id>          install a theme
uninstall-theme <id>        remove an installed theme
publish-theme <folder>      package and publish a theme
list-addons                 list Sentinel addon assets
install-addon <id>          install a Sentinel addon
uninstall-addon <id>        remove an installed Sentinel addon
publish-addon <folder>      package and publish a Sentinel addon
build <folder> [--out]      build a .qplugin.zip locally
validate <folder>           build + print id/version/sha256
```

Global `--repo owner/name` and `--branch name` override the saved settings for
one command.

---

## Differences and limitations

- No payment processing, license activation, subscriptions or trials. `price`
  fields are display metadata only.
- No server-side moderation. Repository permissions are the access control.
- A publish is a normal Git commit; use branch protection/review if you need
  approval before changes reach `main`.
- `index.json` is generated; editing it by hand is possible but the GUI/CLI
  always rewrite it from the current catalog.
- The UI deliberately mirrors the Firebase marketplace (search, category,
  list/details, install/update/uninstall, publish, delete, update-all) but adds
  a Settings dialog, an Activity log and version selection.

---

## Development

```powershell
py -3 -m unittest discover -s tests -v
py -3 git_marketplace_cli.py validate "C:\path\to\plugin"
```

Files:

```text
manifest.json                 QAH plugin manifest
__init__.py                   QAH entry point (Plugin class)
git_marketplace_core.py       Qt-free catalog, GitHub API, install/publish/delete
marketplace_widget.py         PySide6 main view
settings_dialog.py            repository/token configuration
publish_dialog.py             publish form
git_marketplace_cli.py        standalone CLI (no Qt)
icon.svg                      plugin icon
tests/test_core.py            unit tests (no network)
```
