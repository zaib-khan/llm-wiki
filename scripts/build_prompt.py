#!/usr/bin/env python3
"""Assemble the distributed prompt from its thematic Markdown sources."""

import argparse
from pathlib import Path
import re
import sys


SOURCES = {
    "01-principles.md": ("intro", "1", "2", "3", "4", "17"),
    "02-structure.md": ("5", "6"),
    "03-setup.md": ("7", "8", "15", "16"),
    "04-ingest.md": ("9", "9.1", "9.2", "10"),
    "05-query.md": ("9.3", "12"),
    "06-maintenance.md": ("9.4", "9.5", "9.6", "11"),
    "07-integrations.md": ("13", "14"),
}
ORDER = (
    "intro", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "10", "11",
    "12", "13", "14", "15", "16", "17",
)
OUTPUT = "zaib-khan-llm-wiki.md"


def split_sections(text):
    """Keep every character, ignoring section-like headings in code fences."""
    sections = {}
    key = "intro"
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) +
                            r"{" + str(len(fence)) + r",}[ \t]*\r?\n?", line):
                fence = None
            lines.append(line)
            continue
        opening = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if opening:
            fence = opening.group(1)
            lines.append(line)
            continue
        heading = re.match(r"^## (\d+)\. ", line) or re.match(r"^### (9\.\d+) ", line)
        if heading:
            if lines:
                sections[key] = "".join(lines)
            key = heading.group(1)
            if key in sections:
                raise ValueError(f"Duplicate section: {key}")
            lines = []
        lines.append(line)
    if fence:
        raise ValueError("Unclosed code fence")
    if lines:
        sections[key] = "".join(lines)
    return sections


def assemble(root):
    sections = {}
    for filename, expected in SOURCES.items():
        path = root / "prompt" / filename
        found = split_sections(path.read_bytes().decode("utf-8"))
        missing = set(expected) - found.keys()
        extra = found.keys() - set(expected)
        if missing or extra:
            raise ValueError(f"{filename}: missing sections {sorted(missing)}; "
                             f"unexpected sections {sorted(extra)}")
        sections.update(found)
    return "".join(sections[key] for key in ORDER).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Fail if the distributed prompt differs; do not write files.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output = root / OUTPUT
    try:
        content = assemble(root)
        if args.check:
            if not output.exists() or output.read_bytes() != content:
                print(f"{OUTPUT} is out of date. Run python3 scripts/build_prompt.py.",
                      file=sys.stderr)
                return 1
            print(f"{OUTPUT} is up to date.")
        else:
            output.write_bytes(content)
            print(f"Built {OUTPUT} from {len(SOURCES)} source files.")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Cannot build prompt: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
