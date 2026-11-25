#!/usr/bin/env python3
"""One-star houseplant review for the make.fun "One Star, Written in Sap" bounty.

The whole entry is a single review line, held in REVIEW. Running this
file checks the line against the house gate (plain UTF-8 text, 1 to 279
characters, one line, more than blank) and writes it unchanged, with no
trailing newline, to /output/entry.txt.

Only the Python standard library is used.
"""

from pathlib import Path

REVIEW = "One star. He bought me as a basil plant, so every leaf I grow ends up in his pasta. I am not a garnish. I am lunch with a view."

TARGET = Path("/output/entry.txt")
MAX_CHARS = 279


def check(line: str) -> str:
    """Return the line if it passes the gate, else fail loudly."""
    text = line.strip()
    if not text:
        raise SystemExit("review is empty")
    if "\n" in text or "\r" in text:
        raise SystemExit("review must be a single line")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "review is %d chars, over the %d limit" % (len(text), MAX_CHARS)
        )
    return text


def main() -> None:
    ready = check(REVIEW)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(ready, encoding="utf-8")
    print("wrote %d chars to %s" % (len(ready), TARGET))


if __name__ == "__main__":
    main()
