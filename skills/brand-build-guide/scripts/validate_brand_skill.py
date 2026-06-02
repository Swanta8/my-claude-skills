#!/usr/bin/env python3
"""
Validate a GENERATED brand skill before packaging/upload.

Usage:
    python validate_brand_skill.py <path/to/brand-skill-folder>

Checks (stdlib only, no third-party deps):
  - exactly one SKILL.md, at the folder root
  - frontmatter has name + description (single-line description)
  - description <= 1024 characters (hard upload limit)
  - name matches the folder name (warning)
  - no leftover {{PLACEHOLDER}} in any text file (error); <vul ... in> data
    placeholders are allowed and reported
  - assets/design-tokens.json is present and valid JSON
  - the default reference set is present (warning if a file is missing)
  - report-scaffold.html / email-scaffold.html present and free of {{...}}

Exit code 0 = OK (warnings allowed), 1 = errors found.
"""
import json
import re
import sys
from pathlib import Path

TEXT_EXT = {".md", ".html", ".json", ".css", ".txt"}
DEFAULT_REFS = ["design-tokens.md", "voice-and-tone.md", "html-reports.md", "email.md"]
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
DATA_PLACEHOLDER_RE = re.compile(r"<vul[^>]*>", re.IGNORECASE)


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    return fm


def main():
    if len(sys.argv) < 2:
        print("usage: validate_brand_skill.py <skill-folder>")
        return 2
    root = Path(sys.argv[1]).resolve()
    errors, warnings, notes = [], [], []

    if not root.is_dir():
        print(f"ERROR: not a folder: {root}")
        return 1

    # SKILL.md presence / uniqueness
    skill_md = root / "SKILL.md"
    all_skill_md = [p for p in root.rglob("SKILL.md")
                    if "__pycache__" not in p.parts]
    if not skill_md.exists():
        errors.append("SKILL.md not found at folder root")
    if len(all_skill_md) > 1:
        extra = [str(p.relative_to(root)) for p in all_skill_md if p != skill_md]
        errors.append(f"multiple SKILL.md found (upload rejects this): {extra}")

    # Frontmatter + description length
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if not fm:
            errors.append("no valid YAML frontmatter in SKILL.md")
        else:
            if not fm.get("name"):
                errors.append("frontmatter missing 'name'")
            elif fm["name"] != root.name:
                warnings.append(f"name '{fm['name']}' != folder '{root.name}'")
            desc = fm.get("description", "")
            if not desc:
                errors.append("frontmatter missing 'description'")
            else:
                n = len(desc)
                if n > 1024:
                    errors.append(f"description is {n} chars (>1024 upload limit) — trim it")
                else:
                    notes.append(f"description length OK ({n}/1024)")

    # design-tokens.json
    tokens = root / "assets" / "design-tokens.json"
    if not tokens.exists():
        warnings.append("assets/design-tokens.json missing")
    else:
        try:
            json.loads(tokens.read_text(encoding="utf-8"))
            notes.append("design-tokens.json is valid JSON")
        except Exception as e:
            errors.append(f"design-tokens.json invalid JSON: {e}")

    # default reference set
    refs_dir = root / "references"
    for r in DEFAULT_REFS:
        if not (refs_dir / r).exists():
            warnings.append(f"reference missing (ok if not in coverage): references/{r}")

    # leftover placeholders + scaffolds
    leftover = {}
    data_ph = {}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and "__pycache__" not in p.parts:
            content = p.read_text(encoding="utf-8", errors="replace")
            hits = PLACEHOLDER_RE.findall(content)
            if hits:
                leftover[str(p.relative_to(root))] = sorted(set(hits))[:8]
            d = DATA_PLACEHOLDER_RE.findall(content)
            if d:
                data_ph[str(p.relative_to(root))] = sorted(set(d))[:8]

    for scf in ["assets/report-scaffold.html", "assets/email-scaffold.html"]:
        if not (root / scf).exists():
            warnings.append(f"scaffold missing: {scf}")
    if leftover:
        for f, hs in leftover.items():
            errors.append(f"leftover {{...}} placeholder in {f}: {hs}")
    if data_ph:
        flat = sorted({x for v in data_ph.values() for x in v})
        notes.append(f"data placeholders to complete before sending: {flat}")

    # report
    print(f"\n=== Validatie: {root.name} ===")
    for n in notes:
        print(f"  • {n}")
    for w in warnings:
        print(f"  ⚠️  {w}")
    for e in errors:
        print(f"  ❌ {e}")
    if errors:
        print(f"\n{len(errors)} fout(en), {len(warnings)} waarschuwing(en). NIET upload-klaar.")
        return 1
    print(f"\n✅ Upload-klaar. {len(warnings)} waarschuwing(en).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
