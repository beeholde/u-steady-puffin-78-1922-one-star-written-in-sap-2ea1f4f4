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
    """Return the line if it passes the gate, else fail loudly.

    The gate keeps the entry honest: one plain line of text, long enough
    to say something, short enough to fit the bounty limit, with no
    control characters smuggled in.
    """
    text = line.strip()
    if not text:
        raise SystemExit("review is empty")
    if len(text) < 10:
        raise SystemExit("review is %d chars, too short to say anything" % len(text))
    if "\n" in text or "\r" in text:
        raise SystemExit("review must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("review contains control characters")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "review is %d chars, over the %d limit" % (len(text), MAX_CHARS)
        )
    return text


def main() -> None:
    ready = check(REVIEW)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(ready, encoding="utf-8")
    # Round-trip: what landed on disk must be exactly what passed the gate.
    written = TARGET.read_text(encoding="utf-8")
    if written != ready:
        raise SystemExit("wrote %d chars but read back %d" % (len(ready), len(written)))
    print("wrote %d chars to %s" % (len(ready), TARGET))


if __name__ == "__main__":
    main()
