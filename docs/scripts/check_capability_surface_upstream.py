"""Prove `capability-surface.toml` still matches the live upstream manifest.
AAASM-5600.

`hub-metadata-check.yml`'s own header comment states the gap this closes: CI's
`generate_capability_surface.py --check` proves the two evaluator guides match
the *committed extract*; it "does NOT prove the extract matches the upstream
manifest — that needs a cross-repository check, which is AAASM-5600's."

    pip install pyyaml   # same requirement extract_capability_surface.py has
    python3 docs/scripts/check_capability_surface_upstream.py \
        --manifest ../agent-assembly/governance/capability-manifest.yaml

WHY THIS REUSES `extract_capability_surface.build()` RATHER THAN COMPARING FIELDS
------------------------------------------------------------------------------------
Re-deriving a fresh projection with the exact function that produced the
committed one, then comparing text, means there is exactly one place that knows
how to turn a manifest row into a projected row. A hand-written field-by-field
comparator here would be a second, divergent copy of that logic — the two would
silently drift from each other the next time either script's projection changes,
which is the same class of defect this whole check exists to catch one layer up.

The only expected difference between a fresh build and the committed file is the
`[pin].source_commit` line: it records *when the extract was taken*, not a fact
about the manifest, so a fresh run always disagrees with it even on an
unchanged manifest. Both texts are compared with that one line normalised out.

WHY THIS IS NOT WIRED INTO CI
-------------------------------
Same reasoning `official-website/scripts/trust-evidence.py`'s `upstream` mode
already documents for the identical shape of check: this repository's CI makes
no network calls to another repository, and whether it ever should is a
cross-repo policy question AAASM-5587 deferred and this ticket does not reopen.
Run this by hand — after any change to `capability-surface.toml`, and
periodically to catch upstream manifest drift the extract hasn't picked up yet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Final

SCRIPT_DIR: Final[Path] = Path(__file__).resolve().parent
REPO_ROOT: Final[Path] = SCRIPT_DIR.parent.parent
EXTRACT_PATH: Final[Path] = REPO_ROOT / "capability-surface.toml"

sys.path.insert(0, str(SCRIPT_DIR))
import extract_capability_surface as extract  # noqa: E402

_SOURCE_COMMIT_LINE = re.compile(r'^source_commit = ".*"$', re.MULTILINE)
_PLACEHOLDER_SHA: Final[str] = "0" * 40


def _normalise(text: str) -> str:
    """Blank out the `[pin].source_commit` line — the one field a fresh build
    is expected to disagree with the committed file on even when nothing else
    has changed (see module docstring)."""
    return _SOURCE_COMMIT_LINE.sub(f'source_commit = "{_PLACEHOLDER_SHA}"', text, count=1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="path to the upstream governance/capability-manifest.yaml",
    )
    args = parser.parse_args(argv)

    try:
        import yaml
    except ImportError:
        sys.stderr.write("This script needs PyYAML: pip install pyyaml\n")
        return 2

    with args.manifest.open("rb") as handle:
        manifest = yaml.safe_load(handle)

    fresh = _normalise(extract.build(manifest, _PLACEHOLDER_SHA))
    committed = _normalise(EXTRACT_PATH.read_text(encoding="utf-8"))

    if fresh == committed:
        print(
            f"check_capability_surface_upstream: {EXTRACT_PATH.name} matches "
            f"the manifest at {args.manifest} (ignoring the source_commit pin)."
        )
        return 0

    sys.stderr.write(
        f"{EXTRACT_PATH.name} has drifted from the upstream manifest at "
        f"{args.manifest}. Regenerate with:\n"
        f"  python3 docs/scripts/extract_capability_surface.py "
        f"--manifest {args.manifest} --source-commit <sha>\n"
        f"  python3 docs/scripts/generate_capability_surface.py\n"
        f"  python3 docs/scripts/generate_capability_tables.py\n"
    )
    fresh_lines = fresh.splitlines()
    committed_lines = committed.splitlines()
    shown = 0
    for i, (a, b) in enumerate(zip(committed_lines, fresh_lines)):
        if a != b:
            sys.stderr.write(f"  line {i + 1}:\n    committed: {a}\n    fresh:     {b}\n")
            shown += 1
            if shown >= 20:
                sys.stderr.write("  ... (further differences omitted)\n")
                break
    if len(fresh_lines) != len(committed_lines):
        sys.stderr.write(
            f"  line counts differ: committed {len(committed_lines)}, fresh {len(fresh_lines)}\n"
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
