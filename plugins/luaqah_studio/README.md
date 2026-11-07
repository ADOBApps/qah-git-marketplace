# LuaQAH Studio 2.1

A visual programming studio for **Lua** inside Quantum Analysis Helper (QAH).
Build programs by dropping blocks on a canvas, connect typed sockets, generate
clean Lua, and run it without leaving QAH.

This plugin is part of QAH and is free software under the GNU General Public
License (GPL-3.0-or-later).

Copyright (C) [2026] Acxel David Orozco Baldomero

---

## What is new in 2.1

- **New SVG icon** and a cleaner, theme-aware studio layout.
- **Connection persistence**: saved `.blockproj` files now keep block links.
- **Connection-aware code generation**: one clean file, no duplicated action
  blocks, no literal `{placeholder}` leaks, and smarter defaults.
- **Fixed variable blocks**: Set/Get/Increment/Decrement now use the variable
  name and connected value correctly.
- **Undo / redo** for adding, deleting, connecting and arranging blocks.
- **Searchable block library** with category counts, tooltips and empty-category
  filtering.
- **Syntax-highlighted Lua preview**.
- **Auto Arrange** and a dotted grid canvas with cursor-centred zoom.
- **Project workflow**: New/Open/Save/Save As, dirty-state tracking, drag-and-drop
  `.blockproj` and `.lua` files, and a richer project list.
- **Better Run**: the generated program is created on demand, executed in the
  Lua bridge, and errors are shown in the output panel.

## Features

| Area | Details |
|---|---|
| Blocks | Events, control flow, variables, math, strings, tables, file I/O, input/output, quantum helpers |
| Canvas | Typed sockets, curved connections, selection, grid, zoom, fit view, auto arrange |
| Code | Connection-aware Lua generation, syntax highlighting, export to `.lua` |
| Projects | `.blockproj` JSON with blocks, connections, engine settings and metadata |
| Editing | Undo/redo, duplicate block, delete, context menu, double-click editor |
| Terminal | Interactive Lua terminal with history and multi-line input |
| Runtime | Lua bridge when available; demo mode otherwise |

## Installation

1. Import `luaqah_studio.qplugin.zip` through
   **Plugins → Import** in QAH, or copy this folder to:
   - Windows: `%USERPROFILE%\QAH\plugins\python_plugins\luaqah_studio\`
   - Linux: `~/QAH/plugins/python_plugins/luaqah_studio/`
2. Restart QAH.
3. Open **Plugins → LuaQAH Studio**.

## Quick start

1. Click **On Start** in the block library.
2. Add **Set Variable**, **Add**, **Print**, or any other block.
3. Connect an output socket to an input socket (click one, then the other).
4. Press **Generate Code** (`Ctrl+G`).
5. Press **Run** (`F5`).
6. Save the project with `Ctrl+S` (`.blockproj`) and export Lua with
   **Export .lua**.

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New project |
| `Ctrl+O` | Open project |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+G` | Generate Lua |
| `F5` | Run |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` / `Ctrl+Shift+Z` | Redo |
| `Ctrl++` / `Ctrl+-` | Zoom in/out |
| `Ctrl+0` | Fit view |
| `Del` | Delete selected blocks |
| `Ctrl+F` | Focus the block search field |

## Project format

`.blockproj` is a readable JSON document:

```json
{
  "version": "2.0",
  "plugin_version": "2.1.0",
  "blocks": [
    {
      "type": "event",
      "id": "a1b2c3d4",
      "title": "On Start",
      "position": {"x": 100, "y": 100},
      "sockets": {"trigger": {"type": "execution", "direction": "output", "data_type": "any"}},
      "lua_code": "print(\"Program started\")",
      "data": {}
    }
  ],
  "connections": [
    {
      "from_block": "a1b2c3d4",
      "from_socket": "trigger",
      "to_block": "e5f6a7b8",
      "to_socket": "exec_in"
    }
  ],
  "engine_settings": {"engine": "lua", "memory_limit": 256, "debug_mode": false}
}
```

## Block model

- **Event** blocks are entry points (`On Start`, `On Timer`, `On Click`).
- **Control** blocks hold a condition and a loop/if body.
- **Variable** blocks store `var_name` and optional `value` in `data`.
- **Operator** and **function** blocks produce values and expose a `result`
  output socket.
- **Action** blocks use `exec_in`/`exec_out` for execution order.
- Socket data types are colour-coded: number, string, boolean, table, function,
  execution.

## Development

The plugin is plain PySide6 and does not need a separate build step. The main
files are:

| File | Purpose |
|---|---|
| `__init__.py` | Plugin entry point, icon and lazy widget loading |
| `plugin_ui.py` | Studio window, project I/O, undo/redo, run integration |
| `block_components.py` | Blocks, sockets, connections, scene, view, library, preview |
| `enhanced_terminal.py` | Interactive Lua terminal |
| `code_generator.py` | Optional advanced code generator helper |
| `analyzer.py` | Block analysis/validation helpers |
| `file_manager.py` | Export/project helpers |
| `icon.svg` | Plugin icon |

Run a quick import check with QAH's Python:

```bash
python -c "import luaqah_studio; print(luaqah_studio.__version__)"
```

## License

GPL-3.0-or-later. See the QAH project for the full license text.
