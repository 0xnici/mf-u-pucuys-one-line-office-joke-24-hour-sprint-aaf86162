"""Write this entry's one-line office joke to the make.fun grader output.

Grader contract:
    The harness runs this script and then reads ``entry.txt`` from the
    directory named by MAKEFUN_OUTPUT_DIR (default ``/output``). That file
    must hold one UTF-8 line: 1 to 200 characters, not whitespace-only, with
    no embedded newline. The joke itself lives in ``joke.txt`` next to this
    script, so the answer can be reviewed without running any code. This
    program only creates the output directory if it is missing and writes
    the single ``entry.txt`` file; it never deletes or clears /output.
"""

import os
from pathlib import Path

MAX_LENGTH = 200


def load_joke_bytes(source: Path) -> tuple[str, bytes]:
    """Read joke.txt and return (validated_joke_string, original_bytes).

    Validation rules:
        * 1 to 200 characters after stripping a single trailing LF/CRLF
        * not blank
        * no embedded LF, CR, or NUL
    """
    raw = source.read_bytes()
    if not raw:
        raise ValueError("joke.txt is empty")
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"joke.txt is not valid UTF-8: {e}")

    # Strip exactly one trailing LF or CRLF (the conventional single newline).
    if decoded.endswith("\r\n"):
        joke = decoded[:-2]
    elif decoded.endswith("\n"):
        joke = decoded[:-1]
    else:
        joke = decoded

    if not 1 <= len(joke) <= MAX_LENGTH:
        raise ValueError(f"joke must be 1 to {MAX_LENGTH} characters")
    if not joke.strip():
        raise ValueError("joke must not be blank")
    if any(ch in joke for ch in ("\n", "\r", "\x00")):
        raise ValueError("joke must be a single line with no control characters")

    return joke, raw


def main() -> None:
    source = Path(__file__).with_name("joke.txt")
    _, original = load_joke_bytes(source)

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_bytes(original)


if __name__ == "__main__":
    main()
