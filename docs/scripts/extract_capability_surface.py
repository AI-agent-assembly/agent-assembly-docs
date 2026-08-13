"""Extract ``capability-surface.toml`` from the upstream capability manifest.

The Docs Hub publishes two evaluator guides — *What Ships Today* and *Choose your
enforcement path* — whose every row is a capability claim. AAASM-5531 defines the
machine-readable source those claims must come from:
``governance/capability-manifest.yaml`` in the ``agent-assembly`` repository.

That manifest is **in another repository**, so a Docs Hub CI job cannot read it.
This script is the bridge, run by hand when the upstream manifest changes:

    pip install pyyaml   # the only script here needing a third-party module
    python3 docs/scripts/extract_capability_surface.py \
        --manifest ../agent-assembly/governance/capability-manifest.yaml \
        --source-commit <40-hex sha of the agent-assembly commit read>

It writes ``capability-surface.toml`` at the repo root: a **pinned projection** of
the manifest carrying only the fields the two guides render, plus a ``[pin]`` table
recording exactly which upstream commit it was taken from. The pin is published on
the page rather than kept in the tooling, so a reader can see how old the extract is.

Division of labour, and why it is split this way:

* This script needs PyYAML and network-free access to a sibling checkout, so it is
  **not** run in CI.
* ``generate_capability_surface.py`` reads only the committed TOML with the
  standard-library ``tomllib`` and **is** run in CI with ``--check``, matching the
  existing ``generate_hub_components.py`` / ``generate_compatibility.py`` gates.

The consequence is stated rather than hidden: CI proves the *generated tables* on
those pages match the *extract*. It does not check prose outside the markers, and it
cannot prove the extract matches the *upstream manifest*. Closing that second gap
needs a cross-repository check, which is AAASM-5600's.

See AAASM-5609 (Epic AAASM-3659) and ADR 0033 §6 for the claim vocabulary.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Final

SCRIPT_DIR: Final[Path] = Path(__file__).resolve().parent
REPO_ROOT: Final[Path] = SCRIPT_DIR.parent.parent
OUTPUT_PATH: Final[Path] = REPO_ROOT / "capability-surface.toml"

SHA_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{40}$")

# The per-capability keys projected into the extract. Everything else in the
# upstream row — free-text notes, target_level prose, per-row bypass narratives —
# is deliberately left behind: a projection that carries prose invites the page to
# quote it, and quoting a manifest's prose is how a second copy of a claim starts.
SCALAR_KEYS: Final[tuple[str, ...]] = (
    "domain",
    "capability",
    "coverage",
    "decision_timing",
    "observe_or_enforce",
    "sync_or_best_effort",
    "failure_posture",
    "reachability",
    "default_state",
    "launch_path",
    "evidence_runs_on_main",
)
LIST_KEYS: Final[tuple[str, ...]] = (
    "platform",
    "released_platforms",
    "released_channels",
)


def _toml_escape(value: str) -> str:
    """Return ``value`` as a TOML basic string, escaped."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", " ").replace("\r", " ")
    return f'"{escaped}"'


def _toml_array(values: list[str]) -> str:
    """Return a single-line TOML array of strings."""
    return "[" + ", ".join(_toml_escape(v) for v in values) + "]"


def _evidence_kinds(row: dict[str, Any]) -> list[str]:
    """Return the sorted unique ``evidence[].kind`` values for one row.

    The manifest distinguishes three kinds — ``test`` (a located test),
    ``test_unlocated`` (asserted to exist but unverifiable from the manifest's own
    repository) and ``gap`` (no test, with the reason recorded). Collapsing them
    would erase the distinction the guides most need to publish.
    """
    kinds = {str(entry["kind"]) for entry in row.get("evidence", [])}
    return sorted(kinds)


def _preconditions(row: dict[str, Any]) -> list[str]:
    """Return one ``kind:name`` token per declared precondition.

    A path's prerequisites are what an evaluator most needs before choosing it, and
    the manifest states them per row as ``{kind, name, required_value}``. Only kind
    and name are projected — ``required_value`` is frequently the placeholder
    ``<set>``, which carries no information a page can publish.
    """
    tokens: list[str] = []
    for entry in row.get("preconditions", []) or []:
        kind = str(entry.get("kind", "")).strip()
        name = str(entry.get("name", "")).strip()
        tokens.append(f"{kind}:{name}" if kind else name)
    return tokens


def build(manifest: dict[str, Any], source_commit: str) -> str:
    """Render the whole ``capability-surface.toml`` body as text."""
    meta = manifest["meta"]
    rows = manifest["capabilities"]

    out: list[str] = [
        "# capability-surface.toml — a pinned projection of the upstream capability",
        "# manifest, and the source of every generated row in the two Docs Hub",
        "# evaluator guides (AAASM-5609).",
        "#",
        "# DO NOT HAND-EDIT. Regenerate with:",
        "#   python3 docs/scripts/extract_capability_surface.py \\",
        "#       --manifest ../agent-assembly/governance/capability-manifest.yaml \\",
        "#       --source-commit <sha>",
        "#",
        "# Then re-render the pages with:",
        "#   python3 docs/scripts/generate_capability_surface.py",
        "",
        "[pin]",
        f"source_repository = {_toml_escape('ai-agent-assembly/agent-assembly')}",
        f"source_path = {_toml_escape('governance/capability-manifest.yaml')}",
        f"source_commit = {_toml_escape(source_commit)}",
        f"manifest_version = {_toml_escape(str(manifest['manifest_version']))}",
        f"manifest_ticket = {_toml_escape(str(meta['ticket']))}",
        f"fix_version = {_toml_escape(str(meta['fix_version']))}",
        f"evidence_tree = {_toml_escape(str(meta['evidence_tree']))}",
        f"evidence_date = {_toml_escape(str(meta['evidence_date']))}",
        f"row_count = {len(rows)}",
    ]

    # Kept inside [pin] rather than at top level: TOML assigns a bare key after a
    # table header to that table, so a "top-level" key written here would silently
    # become pin.channels_surveyed anyway. Writing it where it lands is honest.
    surveyed = [str(c) for c in meta.get("channels_surveyed", [])]
    out.append(f"channels_surveyed = {_toml_array(surveyed)}")
    not_surveyed = [str(c) for c in meta.get("channels_not_surveyed", [])]
    out.append(f"channels_not_surveyed = {_toml_array(not_surveyed)}")
    out.append("")

    # Channel absences are the manifest's way of saying "this row's artifact is not
    # published on this channel" as distinct from "the question does not apply".
    # AAASM-5680 exists because losing that distinction is exactly what a
    # hand-written channel matrix does.
    for absence in meta.get("channel_absences", []):
        out.append("[[channel_absence]]")
        out.append(f"channel = {_toml_escape(str(absence['channel']))}")
        out.append(f"status = {_toml_escape(str(absence['status']))}")
        out.append(f"ticket = {_toml_escape(str(absence.get('ticket', '')))}")
        out.append(f"ids = {_toml_array([str(i) for i in absence['ids']])}")
        out.append("")

    for row in rows:
        out.append("[[capability]]")
        out.append(f"id = {_toml_escape(str(row['id']))}")
        out.append(f"component = {_toml_escape(str(row['owner']['component']))}")
        out.append(f"repository = {_toml_escape(str(row['owner']['repository']))}")
        for key in SCALAR_KEYS:
            out.append(f"{key} = {_toml_escape(str(row[key]))}")
        for key in LIST_KEYS:
            values = row[key]
            if not isinstance(values, list):
                values = [values]
            out.append(f"{key} = {_toml_array([str(v) for v in values])}")
        out.append(f"evidence_kinds = {_toml_array(_evidence_kinds(row))}")
        out.append(f"preconditions = {_toml_array(_preconditions(row))}")
        out.append("")

    return "\n".join(out).rstrip("\n") + "\n"


def main(argv: list[str] | None = None) -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="path to the upstream governance/capability-manifest.yaml",
    )
    parser.add_argument(
        "--source-commit",
        required=True,
        help="40-character hex SHA of the agent-assembly commit the manifest was read at",
    )
    args = parser.parse_args(argv)

    if not SHA_RE.match(args.source_commit):
        sys.stderr.write(
            "--source-commit must be a 40-character lowercase hex SHA; a branch "
            "name does not identify what was read.\n"
        )
        return 2

    try:
        import yaml
    except ImportError:  # pragma: no cover - documented operator step
        sys.stderr.write("This script needs PyYAML: pip install pyyaml\n")
        return 2

    with args.manifest.open("rb") as handle:
        manifest = yaml.safe_load(handle)

    OUTPUT_PATH.write_text(build(manifest, args.source_commit), encoding="utf-8")
    sys.stderr.write(
        f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} "
        f"({len(manifest['capabilities'])} rows) from {args.source_commit[:9]}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
