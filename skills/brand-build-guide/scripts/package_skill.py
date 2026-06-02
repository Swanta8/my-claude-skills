#!/usr/bin/env python3
"""
Package a generated brand skill into an upload-ready .zip.

Usage:
    python package_skill.py <path/to/brand-skill-folder> [output-dir]

- Runs validate_brand_skill.py first; refuses to package on errors.
- Produces <folder-name>.zip with the skill folder at the TOP LEVEL of the archive.
- Excludes .DS_Store, __pycache__, *.pyc, node_modules, dotfiles.
- Writes the zip directly (no temp-file rename) so it also works inside synced
  folders. If your environment still blocks it, target /tmp and copy the file out.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_NAMES = {".DS_Store"}


def excluded(rel: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return True
    if any(part.startswith(".") for part in rel.parts):  # dotfiles/dotdirs
        return True
    if rel.name in EXCLUDE_NAMES or rel.suffix == ".pyc":
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("usage: package_skill.py <skill-folder> [output-dir]")
        return 2
    skill = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not (skill / "SKILL.md").exists():
        print(f"❌ SKILL.md not found in {skill}")
        return 1

    # Validate first (same folder as this script).
    validator = Path(__file__).with_name("validate_brand_skill.py")
    if validator.exists():
        print("🔍 Validating before packaging...")
        rc = subprocess.run([sys.executable, str(validator), str(skill)]).returncode
        if rc != 0:
            print("\n❌ Validation failed — fix the errors above before packaging.")
            return 1

    zip_path = out_dir / f"{skill.name}.zip"
    base = skill.parent
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(skill.rglob("*")):
            rel = p.relative_to(base)            # includes the top-level folder name
            rel_inside = p.relative_to(skill)    # for exclusion checks
            if excluded(rel_inside):
                continue
            if p.is_file():
                zf.write(p, rel.as_posix())
                count += 1

    print(f"\n✅ {zip_path}  ({count} bestanden)")
    print("   Upload via: organizational skills → Upload skill → drag the .zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
