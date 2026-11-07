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

Version: 3.7.0
Author: Acxel Orozco
Created: 2026-02-07
