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

## Notes

- Builds run in the project folder; auxiliary files and PDFs are ignored by the default `.gitignore`.
- Embedded preview is optional; **Open PDF** works without PyMuPDF.
- This plugin is an editor and collaboration shell; it does not replace a full LaTeX IDE or a Git client.

## License

GPL-3.0-or-later.
