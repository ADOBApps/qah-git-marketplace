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

- *Repository access*: the marketplace repository (and any repo you publish
  from, if it is private),
- *Permissions*: **Contents: Read and write**.

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
The GUI/CLI publish action commits directly, so contributors point it at their
own fork first and then open the PR.

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
delete <id> [--version|--all]
init [--name] [--description]
updates                     compare installed vs catalog
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
