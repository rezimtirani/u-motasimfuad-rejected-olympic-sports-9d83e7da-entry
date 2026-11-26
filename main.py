"""Rejected Olympic Sports — make.fun entry.

Writes one single-line rejected Olympic sport to
$MAKEFUN_OUTPUT_DIR/entry.txt. Pure standard library, no network,
no third-party imports: the grader runs in a bare sandbox.
"""

import os
from pathlib import Path


LINE = (
    "Competitive pretending to listen: athletes nod for four hours "
    "while their partners talk; the first to say 'huh?' is disqualified."
)


def entry_text() -> str:
    """Return the entry line with any stray whitespace trimmed."""
    return LINE.strip()


def output_path() -> Path:
    """Resolve the entry output file from the environment."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not directory:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    return Path(directory) / "entry.txt"


def verify_written(target: Path, expected: str) -> None:
    """Read the file back and confirm it holds exactly the entry.

    A mismatch here means the sandbox wrote something else, so fail
    loudly instead of letting a wrong line reach the judge.
    """
    written = target.read_text(encoding="utf-8")
    if written != expected:
        raise SystemExit(
            f"entry.txt mismatch: wrote {len(written)} characters, "
            f"expected {len(expected)}"
        )
    if "\n" in written:
        raise SystemExit("entry.txt must be a single line")


def main() -> None:
    text = entry_text()
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry is {len(text)} characters, must be 1-200")
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    verify_written(target, text)


if __name__ == "__main__":
    main()
