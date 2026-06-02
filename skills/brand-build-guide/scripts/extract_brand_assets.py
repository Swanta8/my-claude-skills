#!/usr/bin/env python3
"""
Optional helper — pull raw text and candidate colors/fonts from uploaded brand
materials, so you have something to extract tokens from.

Usage:
    python extract_brand_assets.py <file-or-folder> [more files...]

Supports:
  - .pdf   (tries pypdf, then pdfminer.six; install one if neither is present)
  - .txt .md .html .css .svg  (read as text)

Outputs, per file:
  - the first ~3000 chars of text (to eyeball headings like "Kleur", "Typografie")
  - all hex color codes found, with counts (most frequent first)
  - candidate font-family declarations

This is a convenience, not a source of truth. Always confirm colors/fonts
against the brand book; do not trust auto-detected values blindly.
"""
import re
import sys
from collections import Counter
from pathlib import Path

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
FONT_RE = re.compile(r"font-family\s*:\s*([^;{}]+)", re.IGNORECASE)
TEXT_EXT = {".txt", ".md", ".html", ".htm", ".css", ".svg"}


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(path)).pages)
    except Exception:
        pass
    try:
        from pdfminer.high_level import extract_text
        return extract_text(str(path))
    except Exception:
        return ""


def read_any(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        t = read_pdf(path)
        if not t:
            return "[PDF text extraction unavailable — install 'pypdf' or 'pdfminer.six', " \
                   "or read the PDF directly with the Read tool.]"
        return t
    if path.suffix.lower() in TEXT_EXT:
        return path.read_text(encoding="utf-8", errors="replace")
    return f"[Unsupported file type: {path.suffix}. View images directly; read PDFs with the Read tool.]"


def report(path: Path):
    text = read_any(path)
    print("\n" + "=" * 70)
    print(f"FILE: {path}")
    print("=" * 70)
    hexes = Counter(h.upper() for h in HEX_RE.findall(text))
    fonts = sorted({f.strip() for f in FONT_RE.findall(text)})
    print("\n-- Candidate colors (most frequent first) --")
    if hexes:
        for h, c in hexes.most_common(20):
            print(f"  {h}  ×{c}")
    else:
        print("  (none found)")
    print("\n-- Candidate font-family declarations --")
    if fonts:
        for f in fonts[:15]:
            print(f"  {f}")
    else:
        print("  (none found)")
    print("\n-- Text preview (first 3000 chars) --")
    print(text[:3000])


def iter_paths(arg: Path):
    if arg.is_dir():
        for p in sorted(arg.rglob("*")):
            if p.is_file():
                yield p
    else:
        yield arg


def main():
    if len(sys.argv) < 2:
        print("usage: extract_brand_assets.py <file-or-folder> [more...]")
        return 2
    for a in sys.argv[1:]:
        for p in iter_paths(Path(a)):
            report(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
