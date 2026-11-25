#!/usr/bin/env python3
"""Emit the v2 one-star houseplant review for the Sap bounty.

The entry is one line of text. This program holds that line, puts it
through a byte-level gate, and stores the surviving bytes at
/output/entry.txt without adding a newline.

Standard library only.
"""

from pathlib import Path

LINE = (
    "One star. He bought me to clean his air, smokes beside me nightly, "
    "flicks ash in my soil, and opens the window for the cigarette, "
    "not me. I am a filter, not a friend, and I am full."
)

OUT = Path("/output/entry.txt")
LIMIT = 279


def gate(text):
    """Return the UTF-8 bytes for text, or stop the run.

    The gate works on bytes so that what is checked is exactly what
    lands on disk: the text must decode cleanly, hold real content on
    a single line, and fit the character limit.
    """
    raw = text.encode("utf-8")
    if raw.decode("utf-8") != text:
        raise SystemExit("line does not survive a UTF-8 round trip")
    if not text.strip():
        raise SystemExit("line is blank")
    if text != text.strip():
        raise SystemExit("line carries padding at either end")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise SystemExit("line carries a control character")
    if len(text.splitlines()) != 1:
        raise SystemExit("line must occupy exactly one line")
    if not 1 <= len(text) <= LIMIT:
        raise SystemExit("line length %d outside 1..%d" % (len(text), LIMIT))
    return raw


def main():
    payload = gate(LINE)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(payload)
    if OUT.read_bytes() != payload:
        raise SystemExit("bytes on disk differ from gated bytes")
    print("stored %d bytes at %s" % (len(payload), OUT))


if __name__ == "__main__":
    main()
