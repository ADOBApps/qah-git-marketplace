# QAH SSH

Enhanced Cluster Connector with folder upload/download

## Installation
1. Download the plugin ZIP file
2. In Quantum Analyzer Helper, go to Plugins → Import Plugin...
3. Select the ZIP file
4. The plugin will appear in the Plugins menu

## Usage
1. Open the plugin from the Plugins menu
2. Use the interface to interact with the plugin
3. Configure settings as needed

## Configuration
Edit the `manifest.json` file to change plugin settings.

## Development
This plugin was created with the Plugin Maker tool.

### Key Changes
1. **Centralized Python Utilities**: All shared Python code moved to `plugins.libs.python_utils`
2. **Unified Plugin Management**: All plugin-related utilities in `plugins.libs`
3. **Better Separation**: Core libraries vs. individual plugins
4. **Easier Maintenance**: Shared code updates affect all plugins

## Compressed downloads

The file browser can create a single `tar.gz` archive on the cluster, download
it and extract it locally. This is much faster than transferring many small
files individually.

- **Compress on server (tar.gz)** is checked by default next to **Download**.
- Select one or more files/folders → **Download**.
- Or right-click → **Download compressed (tar.gz)**.
- Uncheck the box for files that are already compressed (`.zip`, `.gz`,
  `.xz`, large binary data).
- The remote temporary archive is deleted after the transfer.
- Extraction rejects absolute paths, `..` traversal, symlinks and device files.
- A missing `tar`/`gzip` on the cluster produces a clear error; disable the
  option to use the normal per-file download.

Large archives still use the chunked transfer path, so multi-GB downloads keep
flat memory use and progress reporting.

## Transfer queue

The plugin includes a separate **Transfer Queue** tab, next to **SSH Browser**
and **Text Editor**. It runs uploads and downloads one at a time, so you can
select several transfers and let them finish without waiting between dialogs.

Queued transfers run in a **background worker with their own SFTP channel**, so
the SSH Browser stays usable while a transfer is running. You can navigate,
refresh, and open other tabs. The queue is still sequential: one transfer runs
at a time. Immediate transfers launched from the SSH Browser without the queue
checkbox remain foreground operations.

Add jobs from **SSH Browser** using **Upload File**, **Upload Folder** or
**Download**. **Queue transfers** is checked by default, so transfers run in the
background queue. Uncheck it only when you deliberately want a foreground
transfer. If **Compress on server (tar.gz)** is checked, the queued download
also compresses, downloads and extracts the archive. Compressed downloads
always use the background queue, even if **Queue transfers** is unchecked.

The **Transfer Queue** tab is for control only:

- **Pause / Resume**: let the current transfer finish, then wait before the next
  job.
- **Stop current**: cancel the active transfer. Waiting jobs remain queued.
- **Stop all**: cancel the active transfer and every waiting job.
- **Retry**: requeue the selected finished, failed or canceled job.
- **Clear**: remove finished, failed and canceled rows.

Queue jobs capture their source and destination when added, so navigating to
another remote folder does not move an already queued upload or download.

## Credential manager

**Use in Form** fills the connection fields from a saved credential.

- New credentials store the encrypted token inside the credential index, so the
  manager works even if `shh_info_history.json` is deleted.
- If the password token is missing (entries created before 3.8.1, or a lost
  history file), host, port and user are still filled and a warning asks you to
  enter the password once. The next successful connection stores it again.
- Export/import bundles include both the key files and the encrypted tokens.

## Command auto-complete

The terminal command box has a completion popup powered by:

- your saved command history,
- a built-in list of common Linux/HPC commands (`sbatch`, `squeue`, `module`,
  `vasp`, `pw.x`, ...),
- command names fetched from the cluster with `compgen -c` when you connect.

Start typing and pick a suggestion; use Up/Down inside the popup, then Enter/Tab.
Up/Down outside the popup still navigates command history. Use the refresh
button in the terminal toolbar to fetch the cluster command list again.

## Plugin Structure

### Core Plugin Files in `plugins.libs/`

| File | Purpose |
|------|---------|
| `base_plugin.py` | Abstract base classes for all plugins |
| `lua_bridge.py` | Lua 5.4+ integration bridge |
| `luajit_bridge.py` | LuaJIT (Lua 5.1) integration bridge |
| `plugin_manager.py` | Main plugin lifecycle management |
| `import_manager.py` | Plugin import/export functionality |
| `import_dialog.py` | UI for plugin import operations |
| `one_click_importer.py` | Simplified plugin installation |
| `debug_plugin_import.py` | Debug utilities for plugin loading |

Version: 3.11.1
Author: Acxel Orozco
Created: 2026-02-07
