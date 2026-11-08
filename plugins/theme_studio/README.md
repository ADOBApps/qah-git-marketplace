# Theme Studio

Advanced visual theme builder for QAH with **legacy Theme Manager compatibility**.

Exports the original contract:

```text
theme.json
theme.css
```

plus optional extended metadata (`id`, `tokens`, `font_family`, `radius`,
`preview.svg`). Older Theme Manager versions ignore the extra keys.

---

## Tabs

- **Design** — metadata, color tokens, typography, radius, import existing theme.
- **Advanced CSS** — edit generated QSS; regenerate from tokens or preserve custom CSS.
- **Preview** — live sample form, buttons, table and tabs.
- **Export & Publish** — write a folder, `.qtheme.zip`, or publish to Git Marketplace.
- **Documentation** — format, compatibility and install layout.

## Export formats

### Legacy folder

```text
my_theme/
  theme.json
  theme.css
  preview.svg
  README.md
```

### Marketplace package

```text
my_theme-1.0.0.qtheme.zip
  theme.json
  theme.css
  preview.svg
  README.md
```

## Marketplace themes

Git Plugin Marketplace treats themes as first-class assets:

```text
themes/<id>/<version>/<id>-<version>.qtheme.zip
```

They install flat into:

```text
%USERPROFILE%\QAH\themes\
  <id>.json
  <id>.css
```

Theme Manager reads `*.json` from that folder, so installation does not require
a QAH restart. The marketplace refreshes Theme Manager after installing a
theme.

CLI:

```powershell
py -3 git_marketplace_cli.py list-themes
py -3 git_marketplace_cli.py install-theme my_theme
py -3 git_marketplace_cli.py uninstall-theme my_theme
py -3 git_marketplace_cli.py publish-theme path\to\my_theme
```

## Backward compatibility

- Existing themes still load unchanged.
- Old catalogs without a `themes` list are accepted.
- Old marketplace clients ignore the new `themes` section.
- Generated `theme.json` still contains `name`, `author`, `version`,
  `description`, `css_file` and `preview_color`.
- Generated CSS is plain QSS.

## Limitations

- The builder is a token/QSS editor, not a full visual scene editor.
- Custom CSS overrides generated tokens until regenerated.
- Marketplace publishing uses the configured Git Marketplace token/repository.

---

Version: 1.0.0  
Author: Acxel Orozco
