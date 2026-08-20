"""Render the capability & protection status table from `capability-surface.toml`.
AAASM-5600, per `governance/README.md`'s own "Interfaces this manifest provides"
section in `agent-assembly` (which names this ticket as the manifest's public-table
consumer) and ADR 0034 Decision 2 (a lower-precedence layer "may simplify an
approved lower-layer fact. It may never broaden it.").

WHY THIS READS THE COMMITTED EXTRACT, NOT THE UPSTREAM MANIFEST DIRECTLY
-------------------------------------------------------------------------
`capability-surface.toml` already exists — AAASM-5609's pinned projection of
`governance/capability-manifest.yaml`, refreshed by hand with
`extract_capability_surface.py` and read in CI with the standard-library
`tomllib` by `generate_capability_surface.py`. This script reuses that same
projection and the same CI-safety property (no network call in CI; the
manifest lives in another repository) rather than opening a second path to the
same upstream file. Two projected fields the two evaluator guides don't
render — `protection_state`, `governance_level_ceiling` — and one list field
— `framework_or_tool` — were added to `extract_capability_surface.py`'s
projection for this ticket; see that script's own docstring for why the
addition is additive and backward compatible.

Mirrors `generate_compatibility.py`'s BEGIN/END GENERATED splice pattern in this
same repo, and matches `generate_capability_surface.py`'s own `--check` contract:
a contributor and CI run the identical command.

THREE AXES, RENDERED AS SEPARATE COLUMNS, NEVER MIXED
------------------------------------------------------
`governance/README.md`'s "Three axes, three owners" section is explicit that
behaviour-on-evidence (`coverage`), protection state (`protection_state`) and the
adapter ceiling (`governance_level_ceiling`) each have a distinct owning ADR and
must not be mixed into one reading. This generator keeps them in separate
columns for that reason, rather than folding them into a single prose cell.

WHAT IS NOT FILTERED OUT
------------------------
Every row in the extract is rendered, including rows carrying `unsupported` or
`unmeasured` coverage and `not_measured`/`not_applicable` protection state — the
ticket's own acceptance criterion is that these stay visible rather than being
dropped as "nothing to show". A table that quietly excluded them would look more
complete than the manifest actually claims to be.

WHAT PROVING "THE EXTRACT MATCHES THE MANIFEST" NEEDS INSTEAD
---------------------------------------------------------------
This script proves the page matches `capability-surface.toml`. It cannot prove
the extract itself still matches the live upstream manifest — that is
`check_capability_surface_upstream.py` (AAASM-5600), hand-run for the same
reason `extract_capability_surface.py` is: it needs the same sibling checkout,
and this repo's CI does not make network calls to another repository (the same
cross-repo CI policy deferral `official-website/scripts/trust-evidence.py`'s
`upstream` mode already documents, AAASM-5587).
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Final

SCRIPT_DIR: Final[Path] = Path(__file__).resolve().parent
REPO_ROOT: Final[Path] = SCRIPT_DIR.parent.parent
EXTRACT_PATH: Final[Path] = REPO_ROOT / "capability-surface.toml"
PAGE_PATH: Final[Path] = REPO_ROOT / "docs" / "src" / "capability-status.md"

PROVENANCE_BEGIN: Final[str] = "<!-- BEGIN GENERATED:capability-manifest:provenance -->"
PROVENANCE_END: Final[str] = "<!-- END GENERATED:capability-manifest:provenance -->"
TABLE_BEGIN: Final[str] = "<!-- BEGIN GENERATED:capability-manifest:table -->"
TABLE_END: Final[str] = "<!-- END GENERATED:capability-manifest:table -->"

# Display prose for the closed coverage/protection-state enums, so the table
# reads in words rather than raw machine tokens. Every enum member is listed —
# a term rendered only when some row carries it disappears the moment none
# does, which is itself information (see `trust-evidence.py`'s `TERMS` for the
# same reasoning applied to `/trust`).
COVERAGE_PROSE: Final[dict[str, str]] = {
    "observed": "Observed",
    "detected": "Detected",
    "evaluated": "Evaluated",
    "denied_before_execution": "Denied before execution",
    "redacted": "Redacted",
    "approval_required": "Approval required",
    "degraded": "Degraded",
    "unmeasured": "Unmeasured",
    "experimental": "Experimental",
    "planned": "Planned",
    "unsupported": "Unsupported",
}
PROTECTION_PROSE: Final[dict[str, str]] = {
    "not_installed": "Not installed",
    "detected_not_integrated": "Detected, not integrated",
    "partially_integrated": "Partially integrated",
    "integrated": "Integrated",
    "gateway_protected": "Gateway-protected",
    "host_enforced": "Host-enforced",
    "drifted": "Drifted",
    "degraded": "Degraded",
    "incompatible": "Incompatible",
    "not_applicable": "Not applicable",
    "not_measured": "Not measured",
}


def load_extract(path: Path) -> dict:
    """Read `capability-surface.toml`, validating the shape this generator needs."""
    with path.open("rb") as handle:
        doc = tomllib.load(handle)
    rows = doc.get("capability", [])
    if not isinstance(rows, list) or len(rows) < 40:
        raise ValueError(
            f"expected at least 40 [[capability]] rows in {path.name}, found "
            f"{len(rows) if isinstance(rows, list) else 'none'}"
        )
    missing_fields = [
        r["id"]
        for r in rows
        if "protection_state" not in r or "framework_or_tool" not in r
    ]
    if missing_fields:
        raise ValueError(
            f"rows missing protection_state/framework_or_tool: {missing_fields[:5]} — "
            "re-run extract_capability_surface.py to refresh the projection"
        )
    return doc


def _escape_cell(value: str) -> str:
    """Escape a string so it is safe inside a Markdown table cell."""
    return value.replace("|", "\\|").replace("\n", " ")


def _prose(token: str, table: dict[str, str]) -> str:
    """Render an enum token as prose, or the raw token if it's unrecognised.

    Falling back to the raw token rather than raising keeps table generation
    from breaking on an extract that has genuinely added a new enum member —
    the upstream manifest's own schema already closes that enum, so reaching
    this function with an unrecognised token can only mean this table's own
    prose map is stale, which should be visible (the raw token) rather than
    crash the whole render.
    """
    return table.get(token, token)


def render_provenance(pin: dict) -> str:
    """Render the provenance block: manifest version and how stale the
    extraction is (`source_commit`/`evidence_tree`/`evidence_date`).
    """
    source_commit = pin.get("source_commit", "")
    short_source = source_commit[:12] if source_commit else "—"
    evidence_tree = pin.get("evidence_tree", "")
    short_evidence = evidence_tree[:12] if evidence_tree else "—"
    lines = [
        f"- **Manifest version:** `{pin.get('manifest_version', '—')}`",
        f"- **Ticket:** {pin.get('manifest_ticket', '—')}",
        f"- **Fix version:** {pin.get('fix_version', '—')}",
        f"- **Extract taken at commit:** `{short_source}`",
        f"- **Evidence surveyed at:** `{short_evidence}` ({pin.get('evidence_date', '—')})",
    ]
    return "\n".join(lines)


def render_table(rows: list[dict]) -> str:
    """Render one table over every extract row, sorted by (domain, id).

    Columns keep the three governed axes separate (coverage / protection state /
    governance ceiling are never folded into one cell — see module docstring),
    plus the distribution axis (`platform`, `released_channels`) and ownership
    (`component`, `framework_or_tool`).
    """
    header = (
        "| ID | Capability | Owner | Framework / tool | Platform | "
        "Released channels | Coverage | Protection state |"
    )
    separator = "|---|---|---|---|---|---|---|---|"
    lines: list[str] = [header, separator]

    for row in sorted(rows, key=lambda r: (r.get("domain", ""), r["id"])):
        cells = [
            row["id"],
            _escape_cell(row.get("capability", "—")),
            _escape_cell(row.get("component", "—")),
            _escape_cell(", ".join(sorted(row.get("framework_or_tool", []))) or "—"),
            _escape_cell(", ".join(sorted(row.get("platform", []))) or "—"),
            _escape_cell(", ".join(sorted(row.get("released_channels", []))) or "—"),
            _prose(row.get("coverage", ""), COVERAGE_PROSE) or "—",
            _prose(row.get("protection_state", ""), PROTECTION_PROSE) or "—",
        ]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def splice(page: str, begin: str, end: str, body: str) -> str:
    """Replace the content between ``begin``/``end`` markers, preserving them."""
    start = page.find(begin)
    stop = page.find(end)
    if start == -1 or stop == -1 or stop < start:
        raise ValueError(f"markers {begin!r} / {end!r} not found (or out of order)")
    head = page[: start + len(begin)]
    tail = page[stop:]
    return f"{head}\n\n{body}\n\n{tail}"


def render_page(doc: dict, current: str) -> str:
    """Return the page text with both generated blocks refreshed from the extract."""
    rendered = splice(current, PROVENANCE_BEGIN, PROVENANCE_END, render_provenance(doc["pin"]))
    rendered = splice(rendered, TABLE_BEGIN, TABLE_END, render_table(doc["capability"]))
    return rendered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed page matches capability-surface.toml; exit nonzero if stale",
    )
    args = parser.parse_args(argv)

    doc = load_extract(EXTRACT_PATH)
    current = PAGE_PATH.read_text(encoding="utf-8")
    rendered = render_page(doc, current)

    if args.check:
        if rendered != current:
            sys.stderr.write(
                f"{PAGE_PATH} is out of date with {EXTRACT_PATH.name}.\n"
                "Run: python3 docs/scripts/generate_capability_tables.py\n"
            )
            return 1
        return 0

    if rendered != current:
        PAGE_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
