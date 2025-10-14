#!/usr/bin/env python3
"""Pre-commit check for .txt files under data/.

Checks:
- No line ends with a space character.
- No duplicate (exact) lines within the same file.

Exits with code 1 on any failure and prints diagnostics.
"""

import sys
from pathlib import Path


def check_file(path: Path) -> int:
    errors = 0
    seen = {}
    with path.open("r", encoding="utf-8") as f:
        for i, raw in enumerate(f, 1):
            # Keep the raw line for trailing space check, but remove trailing newline for duplicate detection
            if raw.endswith(" \n") or raw.endswith(" "):
                print(f"{path}: line {i} ends with a space")
                errors += 1

            line = raw.rstrip("\r\n")
            if line in seen:
                first = seen[line]
                print(
                    f"{path}: duplicate line {i} (first occurrence at line {first}): {line}"
                )
                errors += 1
            else:
                seen[line] = i

    return errors


def main() -> int:
    data_dir = Path("data")
    if not data_dir.exists():
        print("No data/ directory; nothing to check.")
        return 0

    total_errors = 0
    for txt in sorted(data_dir.glob("*.txt")):
        total_errors += check_file(txt)

    if total_errors:
        print(f"Found {total_errors} issue(s) in data/*.txt")
        return 1

    print("All data/*.txt checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
