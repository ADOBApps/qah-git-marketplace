# LaTeX Studio

Category: **Tools**

A QAH-native LaTeX paper workspace with:

- project and file management (`main.tex`, `sections/`, `figures/`, `.bib`);
- syntax-highlighted editor with line numbers, find/replace and auto-indent;
- `latexmk` or direct `pdflatex`/`xelatex`/`lualatex` builds;
- build log and optional first-page PDF preview (PyMuPDF);
- a **Git relay** for asynchronous collaboration: commit, pull, push, sync, auto-pull and conflict handling;
- no separate collaboration server: the shared Git remote is the relay.

## Install

Install from the Git Plugin Marketplace, or use **Plugins → Tools → LaTeX Studio**.

External requirements:

- `git` on `PATH`;
- a LaTeX distribution with `latexmk` (recommended), or `pdflatex`/`xelatex`/`lualatex` and `bibtex`;
- optional: PyMuPDF (`fitz`) for inline PDF preview.

## Quick start

1. Press **New…** and choose a template (`article`, `report` or `beamer`).
2. Edit the files in the left tree.
3. Open **Build**, choose the main file and engine, and press **Build**.
4. Use **Open PDF** or the preview pane.

## Git relay collaboration

1. Create an empty private repository on GitHub/GitLab or use any Git remote.
2. Open **Git relay**, paste the remote URL and branch (`main`).
3. Press **Save config**, then **Initialize repo** (new project) or **Clone…** (existing paper).
4. Commit locally, then **Push**.
5. Collaborators press **Pull**, or enable **Auto-pull**.

Git is asynchronous. Pull before a writing session, make small commits, and push often. If a pull conflicts:

1. Open the conflicted files from the Git status.
2. Resolve the `<<<<<<<`, `=======`, `>>>>>>>` markers.
3. Save and press **Continue**, or **Abort** to return to the previous state.

Tokens are stored in the local QAH LaTeX Studio settings, not in the repository. Prefer SSH keys or the system Git credential manager when possible.

## Optional Google Drive relay

The Google Drive backend uses the `drive.file` scope: the plugin creates a
`LaTeX Studio` folder in Drive and syncs source snapshots. It is file-level
sync, not Git; conflicting files are saved as `.conflict-...` copies.

Install the optional Google libraries with Wheel Plugin Manager, into the
private `latex_studio` target:

```powershell
$wpm = "C:\Users\HP\QAH\plugins\python_plugins\wheel_plugin_manager\qah_wheel_cli.py"
py -3 $wpm inject google-api-python-client google-auth google-auth-oauthlib --target latex_studio
py -3 $wpm deps-verify latex_studio google-api-python-client
py -3 $wpm deps-verify latex_studio google-auth-oauthlib
```

Linux:

```bash
python3 "$HOME/QAH/plugins/python_plugins/wheel_plugin_manager/qah_wheel_cli.py" \
  inject google-api-python-client google-auth google-auth-oauthlib --target latex_studio
```

Create a Google Cloud **OAuth Desktop app** client, paste its client ID and
secret into **Google Drive**, press **Authorize**, then **Create / find
folder**. Share the Drive folder with collaborators. Because `drive.file` only
grants per-app access, collaborators may need to select/open the shared folder
in Drive or use Drive for Desktop; this is a Google scope limitation, not a
plugin bug.

## Notes

- Builds run in the project folder; auxiliary files and PDFs are ignored by the default `.gitignore`.
- Embedded preview is optional; **Open PDF** works without PyMuPDF.
- This plugin is an editor and collaboration shell; it does not replace a full LaTeX IDE or a Git client.

## License

GPL-3.0-or-later.
