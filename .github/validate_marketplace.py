#!/usr/bin/env python3
"""Validate the QAH Git Marketplace catalog and every plugin archive.

Runs in GitHub Actions for pull requests and pushes to master. Only the Python
standard library is used, so no install step is required.

Checks:
  * index.json is valid JSON with schema 1
  * plugin ids are unique and safe
  * every version has a valid path or URL
  * local ZIP files exist, match size and SHA256, and are readable
  * every ZIP has manifest.json at the root with matching id/version
  * no duplicate versions and no path traversal
  * the catalog "version" equals the highest non-yanked version
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.json"
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ERRORS: List[str] = []


def error(message: str) -> None:
    ERRORS.append(message)
    print(f"ERROR: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_key(value: str) -> Tuple:
    text = str(value or "").strip().lstrip("vV")
    numbers = [int(part) for part in re.findall(r"\d+", text)][:4]
    base = tuple(numbers + [0] * (4 - len(numbers)))
    prerelease = bool(re.search(r"(?:a|b|rc|alpha|beta|pre|dev|nightly)", text, re.I))
    return base + (0 if prerelease else 1,)


def safe_relative(path_text: str) -> Optional[Path]:
    if not path_text:
        return None
    path = PurePosixPath(path_text.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        error(f"unsafe path {path_text!r}")
        return None
    return ROOT.joinpath(*path.parts)


def check_zip(plugin_id: str, version: str, path: Path) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad is not None:
                error(f"{path}: corrupt ZIP member {bad!r}")
                return
            names = archive.namelist()
            if "manifest.json" not in names:
                error(f"{path}: manifest.json is not at the archive root")
                return
            for name in names:
                member = PurePosixPath(name.replace("\\", "/"))
                if member.is_absolute() or ".." in member.parts:
                    error(f"{path}: unsafe member {name!r}")
            manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            if str(manifest.get("id")) != plugin_id:
                error(
                    f"{path}: manifest id {manifest.get('id')!r} != {plugin_id!r}"
                )
            if str(manifest.get("version")) != version:
                error(
                    f"{path}: manifest version {manifest.get('version')!r} "
                    f"!= {version!r}"
                )
            for field in ("name", "author", "description", "category"):
                if not str(manifest.get(field) or "").strip():
                    error(f"{path}: manifest is missing {field!r}")
    except Exception as exc:  # noqa: BLE001 - CI wants a readable failure
        error(f"{path}: cannot read ZIP: {exc}")


def main() -> int:
    if not INDEX.is_file():
        error("index.json is missing")
        return 1
    try:
        catalog = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"index.json is not valid JSON: {exc}")
        return 1

    if catalog.get("schema") != 1:
        error(f"unsupported schema: {catalog.get('schema')!r}")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        error("index.json has no plugins list")
        return 1

    seen_ids = set()
    for plugin in plugins:
        if not isinstance(plugin, dict):
            error("plugin entry is not an object")
            continue
        plugin_id = str(plugin.get("id") or "").strip()
        if not ID_RE.match(plugin_id):
            error(f"invalid plugin id {plugin_id!r}")
            continue
        if plugin_id in seen_ids:
            error(f"duplicate plugin id {plugin_id!r}")
        seen_ids.add(plugin_id)

        for field in ("name", "author", "description", "category"):
            if not str(plugin.get(field) or "").strip():
                error(f"{plugin_id}: missing {field!r}")

        versions = plugin.get("versions")
        if not isinstance(versions, list) or not versions:
            error(f"{plugin_id}: no versions")
            continue

        seen_versions = set()
        usable: List[Dict[str, Any]] = []
        for version_entry in versions:
            if not isinstance(version_entry, dict):
                error(f"{plugin_id}: version entry is not an object")
                continue
            version = str(version_entry.get("version") or "").strip()
            if not version:
                error(f"{plugin_id}: version entry without a version")
                continue
            if version in seen_versions:
                error(f"{plugin_id}: duplicate version {version!r}")
            seen_versions.add(version)

            path_text = str(version_entry.get("path") or "").strip()
            url = str(version_entry.get("url") or "").strip()
            if not path_text and not url:
                error(f"{plugin_id} {version}: no path or url")
                continue
            if path_text:
                path = safe_relative(path_text)
                if path is None:
                    continue
                if not path.is_file():
                    error(f"{plugin_id} {version}: missing {path_text}")
                    continue
                expected_size = version_entry.get("size")
                if expected_size is not None and int(expected_size) != path.stat().st_size:
                    error(
                        f"{plugin_id} {version}: size {path.stat().st_size} "
                        f"!= catalog {expected_size}"
                    )
                expected_hash = str(version_entry.get("sha256") or "").lower()
                if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                    error(f"{plugin_id} {version}: invalid sha256")
                elif sha256(path) != expected_hash:
                    error(f"{plugin_id} {version}: sha256 mismatch")
                check_zip(plugin_id, version, path)
            elif not url.startswith("https://"):
                error(f"{plugin_id} {version}: url must use https")

            if not version_entry.get("yanked"):
                usable.append(version_entry)

            declared = str(plugin.get("version") or "")
            if declared and version_key(version) > version_key(declared):
                error(
                    f"{plugin_id}: catalog version {declared} is lower than "
                    f"version {version}"
                )

        if usable:
            latest = max(usable, key=lambda item: version_key(str(item["version"])))
            if str(plugin.get("version")) != str(latest["version"]):
                error(
                    f"{plugin_id}: catalog version {plugin.get('version')!r} "
                    f"!= latest {latest['version']!r}"
                )

        manifest_rel = Path("plugins") / plugin_id / "manifest.json"
        if not (ROOT / manifest_rel).is_file():
            error(f"{plugin_id}: {manifest_rel.as_posix()} is missing")

    if ERRORS:
        print()
        print(f"FAILED: {len(ERRORS)} error(s)")
        return 1
    print(f"OK: {len(plugins)} plugin(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
