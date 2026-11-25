#!/usr/bin/env python3
"""Entry point for news-image-20261125.

Copies the bundled front-page image to $MAKEFUN_OUTPUT_DIR/entry.png.
Standard library only; no network; deterministic: the same bytes every run.
"""
import hashlib
import os
import struct
import sys

EXPECTED_SHA256 = "9080dc59e8de61d38f59e62e50b24a052d989e0a503f8c22a505d0b9c559c26a"
MAX_BYTES = 1048576
MAX_DIM = 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("entry.png exceeds 1024x1024")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch")
    if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
        sys.exit("entry.png is truncated (no IEND)")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)
    print(f"wrote entry.png ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
