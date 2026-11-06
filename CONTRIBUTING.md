# Contributing a plugin

Uploads to the QAH Git Marketplace are **pull requests**. Direct pushes to
`master` are blocked for everyone except the owner; merges and deletions are
owner-only.

## Rules

1. Only submit plugins you own or have permission to redistribute.
2. The public repository exposes the ZIP contents, including Python source.
   Do not submit private, paid or NDA-covered code here.
3. Use a new semantic version for every change. Never reuse or move a version.
4. Do not edit another plugin's files in the same PR unless you own it.
5. Do not commit tokens, credentials or private keys.
6. The validation workflow must pass; the owner reviews and merges.

## 1. Fork the repository

On GitHub: **Fork** → `YOUR_USER/qah-git-marketplace`.

## 2. Build and publish to your fork

### CLI (recommended)

You need a token that can write to **your fork**:

- Classic PAT: `public_repo` scope.
- Fine-grained PAT: repository access to your fork, **Contents: Read and
  write**.

```powershell
$cli = "C:\path\to\git_plugin_marketplace\git_marketplace_cli.py"

$env:QAH_GIT_MARKETPLACE_TOKEN = "YOUR_FORK_TOKEN"
py -3 $cli --repo YOUR_USER/qah-git-marketplace --branch master `
    publish "C:\path\to\your_plugin" `
    --changelog "Describe this release"
```

This writes `index.json`, `plugins/<id>/manifest.json`, the optional README and
the ZIP to **your fork** in one commit. It does not touch the upstream
repository.

### GUI

1. **Git Plugin Marketplace → Settings**
2. Owner: `YOUR_USER`, Repository: `qah-git-marketplace`, Branch: `master`
3. Token: your fork token
4. **Publish Plugin…**, then switch the settings back to `ADOBApps` afterwards.

## 3. Open the pull request

On GitHub, open a PR from `YOUR_USER:master` to `ADOBApps:master`.

CI runs `.github/validate_marketplace.py`, which checks:

- valid `index.json` and schema,
- unique plugin ids/versions,
- ZIP exists, size and SHA256 match,
- `manifest.json` at the ZIP root with matching `id` and `version`,
- no unsafe paths,
- the catalog's `version` is the highest non-yanked version.

Fix any failure by publishing again to your fork (same version replaces it),
then the PR updates automatically.

## 4. Review and merge

The owner (`@ADOBApps`) is the code owner. Only the owner merges. After a merge,
users click **Refresh** in the marketplace and see the new release.

## Updating an existing plugin

Publish a new version to your fork with the same plugin id and open a PR. The
catalog keeps older versions, so users can still install them.

## Deleting

Only the repository owner can delete. Contributors may open a PR that removes an
entry, but it cannot be merged without the owner. The plugin's **Delete from
marketplace** action requires a write token and fails with 403 for read-only
users.

## Private or unreleased plugins

Do not put them in this public repository. Use a separate private staging
repository and only publish approved ZIPs here.

## Questions

Open an issue or contact [@ADOBApps](https://github.com/ADOBApps).

<!-- CI smoke test; not merged. -->

