"""Validate every page's `capability_ids` metadata field against the real
capability manifest. AAASM-5600.

`page-standards.md`'s field reference marks `capability_ids` "reserved — pending
AAASM-5531. Shape not validated in v1: the key is accepted and ignored." AAASM-5531
has since landed (`governance/capability-manifest.yaml` in `agent-assembly`), so
this script closes that hand-off: a page that declares `capability_ids` now gets
each id resolved against a real capability row, and an id that does not resolve
fails CI.

WHY THIS READS `capability-surface.toml`, NOT THE UPSTREAM MANIFEST DIRECTLY
------------------------------------------------------------------------------
The manifest lives in another repository. `capability-surface.toml` is already
the pinned, committed projection of it (AAASM-5609's `extract_capability_surface.py`
+ `generate_capability_surface.py`), read with the standard-library `tomllib` and
carrying an `id` for every projected row. Every id that has ever existed in the
manifest is present here (the projection carries every row, not a curated
subset), so this is a complete and CI-safe (no network) set of known ids — the
same reuse decision `generate_capability_tables.py` makes for the same reason.
Fetching the manifest a second, separate way here would be a second path to the
same fact.

WHY THIS IS NARROWER THAN THE FULL METADATA VALIDATOR
------------------------------------------------------
`page-standards.md` defines validation rules for the WHOLE `AA-PAGE-META` block
(schema_version, page_type, audience, owner, cross-field rules 1-15, etc.) — that
general validator is AAASM-5601's ticket, not built yet. This script does not
duplicate it: it only extracts and resolves `capability_ids`, ignoring every
other key in the block. When AAASM-5601's validator lands, it can subsume this
narrow check or call it as a sub-step; either way there is exactly one place
that knows how to resolve a capability id, not two.

WHY NOT REQUIRE THE FIELD
--------------------------
`page-standards.md`'s hand-off says `capability_ids` "becomes validated and
required, at schema_version: 2" — but rolling every hub page to schema_version 2
is AAASM-5610's rollout, not this ticket's. As of this script, zero pages declare
`capability_ids`, so requiring it here would fail every page in the hub for a
field this ticket does not own the rollout of. This script validates the field
INSTEAD wherever it is already present, which satisfies AAASM-5600's own
acceptance criterion ("unknown capability IDs fail CI") without pre-empting
AAASM-5601/5610's separate scope.

PARSING THE METADATA BLOCK
---------------------------
`docs/src/` has no front-matter (mdBook has none); `page-standards.md`'s block is
an HTML comment, `<!-- BEGIN AA-PAGE-META ... END AA-PAGE-META -->`, holding a
flat run of `key: value` / `key:` + indented list lines — a YAML *fragment*.
`capability_ids` is always a simple `[a, b]`-or-list-of-scalars field (never a
list of objects, unlike `platforms[]`/`claims[]`), so this script's parser
handles only that one field's two spellings and ignores everything else in the
block, rather than growing into a second full parser for the same grammar
AAASM-5601 will need to write anyway.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path
from typing import Final

SCRIPT_DIR: Final[Path] = Path(__file__).resolve().parent
REPO_ROOT: Final[Path] = SCRIPT_DIR.parent.parent
SRC_DIR: Final[Path] = REPO_ROOT / "docs" / "src"
EXTRACT_PATH: Final[Path] = REPO_ROOT / "capability-surface.toml"

_META_BLOCK = re.compile(r"<!--\s*BEGIN AA-PAGE-META(.*?)END AA-PAGE-META\s*-->", re.DOTALL)
# `capability_ids: [A1, B2]` (flow form) or `capability_ids:` followed by
# `  - A1` / `  - B2` lines (block form) — `page-standards.md` uses flow form
# for other short lists (`audience: [contributor]`, `disclosure_levels: [3, 4]`),
# so both spellings are accepted rather than assuming one.
_FLOW_FIELD = re.compile(r"^capability_ids:\s*\[(.*?)\]\s*$", re.MULTILINE)
_BLOCK_FIELD = re.compile(r"^capability_ids:\s*$", re.MULTILINE)
_BLOCK_ITEM = re.compile(r"^\s*-\s*(\S+)\s*$")


def extract_capability_ids(block_text: str) -> list[str]:
    """Return the `capability_ids` list declared in one metadata block's inner
    text, or `[]` if the field is absent. Raises `ValueError` on a shape this
    parser does not recognise, rather than silently reading nothing — a
    validator that can't tell "absent" from "present but unparsed" is worse
    than no validator.
    """
    flow = _FLOW_FIELD.search(block_text)
    if flow:
        raw = flow.group(1).strip()
        if not raw:
            return []
        return [item.strip().strip("'\"") for item in raw.split(",") if item.strip()]

    block = _BLOCK_FIELD.search(block_text)
    if not block:
        return []
    # Block form: collect indented `- item` lines immediately following the key,
    # stopping at the first line that isn't a list item (the next key, or the
    # end of the comment).
    lines = block_text[block.end():].splitlines()
    ids: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        item = _BLOCK_ITEM.match(line)
        if item:
            ids.append(item.group(1).strip("'\""))
            continue
        break
    return ids


def pages_with_capability_ids(src_dir: Path) -> list[tuple[Path, list[str]]]:
    """Return `(page_path, capability_ids)` for every page that declares the
    field, over every `.md` file under `src_dir`.
    """
    results: list[tuple[Path, list[str]]] = []
    for path in sorted(src_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        block = _META_BLOCK.search(text)
        if not block:
            continue
        ids = extract_capability_ids(block.group(1))
        if ids:
            results.append((path, ids))
    return results


def known_ids(extract_path: Path) -> tuple[set[str], str]:
    """Return the full set of `id`s in `capability-surface.toml`, plus its
    manifest version (for the summary line)."""
    with extract_path.open("rb") as handle:
        doc = tomllib.load(handle)
    rows = doc.get("capability", [])
    if not isinstance(rows, list) or len(rows) < 40:
        raise ValueError(
            f"expected at least 40 [[capability]] rows in {extract_path.name}, found "
            f"{len(rows) if isinstance(rows, list) else 'none'}"
        )
    return {row["id"] for row in rows}, str(doc.get("pin", {}).get("manifest_version", "?"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    del args

    ids, manifest_version = known_ids(EXTRACT_PATH)

    pages = pages_with_capability_ids(SRC_DIR)
    errors: list[str] = []
    for path, declared in pages:
        rel = path.relative_to(REPO_ROOT)
        unknown = [i for i in declared if i not in ids]
        if unknown:
            errors.append(
                f"{rel}: capability_ids references {unknown} — not in "
                f"{EXTRACT_PATH.name} (manifest {manifest_version})"
            )

    if errors:
        for e in errors:
            sys.stderr.write(e + "\n")
        return 1

    print(
        f"validate_capability_ids: {len(pages)} page(s) declare capability_ids, "
        f"all resolve against manifest {manifest_version} ({len(ids)} rows)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
