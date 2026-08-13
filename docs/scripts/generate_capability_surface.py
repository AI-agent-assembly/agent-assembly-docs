"""Render the two Docs Hub evaluator guides from ``capability-surface.toml``.

``docs/src/what-ships-today.md`` and ``docs/src/choose-your-enforcement-path.md``
are capability-claim surfaces: every row on them is a statement about what the
product does to an action. None of those rows is hand-written. They are rendered
here from ``capability-surface.toml`` — the pinned projection of AAASM-5531's
capability manifest that ``extract_capability_surface.py`` produces — and spliced
between ``<!-- BEGIN GENERATED:capability-surface:<key> -->`` /
``<!-- END GENERATED:capability-surface:<key> -->`` markers, leaving the
hand-written prose around them untouched.

Run with no arguments to regenerate in place; run with ``--check`` to verify the
committed pages already match the extract. This mirrors
``generate_hub_components.py`` and ``generate_compatibility.py`` exactly, including
the marker shape and the ``--check`` contract, so the three gates behave the same
way for a contributor and in CI.

Checks that run before anything is rendered, each failing loudly rather than
emitting a page:

1. **Every value of every rendered vocabulary has a label**, checked against the
   key set of the mapping that renders it — see ``VOCABULARIES``. An
   order-list drops what it cannot label *silently*, which publishes an absence the
   manifest never stated, so an unlabelled value must stop the build. ``coverage``
   is the strictest case: it must map to one of ADR 0033 §6's eleven terms
   verbatim, because §6 owns that vocabulary and a twelfth value is the ADR's to
   add, never this table's.
2. **Every census accounts for every row it summarises**, so a breakdown can never
   print beside a row count it does not sum to. The platform table gets the same
   treatment per *row* rather than per *value*, in both directions — see the
   conservation block in ``validate``. Labelability alone is not enough there,
   because that table renders a strict subset of ``PLATFORM_LABEL`` and selects its
   rows by domain.
3. **Every capability id named in a path definition exists in the extract.** A
   renamed or retired id would otherwise silently shrink a path.
4. **No capability id appears in two path definitions**, and the ids not in any
   path are rendered rather than dropped.
5. **Exactly one marker pair exists per key** — see ``splice``.

Scope of what ``--check`` proves, stated because the stronger reading is the
tempting one: **the generated tables match the extract.** Prose outside the markers
is not checked, and nothing here proves the extract matches the upstream manifest
(AAASM-5600).

See AAASM-5609 (Epic AAASM-3659).
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
SRC_DIR: Final[Path] = REPO_ROOT / "docs" / "src"

SHIPS_PATH: Final[Path] = SRC_DIR / "what-ships-today.md"
PATHS_PATH: Final[Path] = SRC_DIR / "choose-your-enforcement-path.md"

# Ticket references are plain text, never links. The tracker is not publicly
# readable, so a link reaches a login wall — which a link checker scores as
# reachable, making the reference look verified when it is not. Six hub pages state
# this convention explicitly; this generator follows it.

# --------------------------------------------------------------------------
# ADR 0033 §6's eleven claim terms, in §6's own table order.
#
# The keys are the manifest's `coverage` enum; the values are §6's terms spelled
# exactly as §6 spells them. This table is a *transliteration*, not a definition:
# no meaning is attached here, and every page that prints a term links to §6 for
# what it means. `approval_required` and `planned` have no manifest row today and
# are carried anyway, so the page can show that they are absent rather than let
# their absence look like an omission.
# --------------------------------------------------------------------------
SIX_TERMS: Final[tuple[tuple[str, str], ...]] = (
    ("observed", "Observed"),
    ("detected", "Detected"),
    ("evaluated", "Evaluated"),
    ("denied_before_execution", "Denied before execution"),
    ("redacted", "Redacted"),
    ("approval_required", "Approval required"),
    ("degraded", "Degraded"),
    ("unmeasured", "Unmeasured"),
    ("experimental", "Experimental"),
    ("planned", "Planned"),
    ("unsupported", "Unsupported"),
)
TERM_ORDER: Final[list[str]] = [key for key, _ in SIX_TERMS]
TERM_LABEL: Final[dict[str, str]] = dict(SIX_TERMS)

# The manifest's `domain` enum, with the reader-facing wording used on the page.
# The raw enum value is printed beside it so the mapping is visible rather than
# implied — a display name is the easiest place for a silent rename to hide.
DOMAIN_LABEL: Final[dict[str, str]] = {
    "sdk": "SDK and framework seams",
    "network": "Network traffic",
    "mcp": "MCP",
    "host_action": "Host actions",
    "devtool_launch": "Developer-tool launch",
    "credentials": "Credentials",
    "identity": "Identity and attribution",
    "degraded_mode": "Degraded and failure modes",
    "platform": "Platform host-level interception",
}
DOMAIN_ORDER: Final[list[str]] = list(DOMAIN_LABEL)

CHANNEL_LABEL: Final[dict[str, str]] = {
    "github_release": "GitHub Release assets",
    "homebrew": "Homebrew tap",
    "install_script": "Install script",
    "crates_io": "crates.io",
    "pypi": "PyPI",
    "npm": "npm",
    "go_modules": "Go modules",
    "ghcr": "GHCR container images",
    "not_applicable": "No distribution question",
}
CHANNEL_ORDER: Final[list[str]] = list(CHANNEL_LABEL)

PLATFORM_LABEL: Final[dict[str, str]] = {
    "linux_x86_64": "Linux x86_64",
    "linux_aarch64": "Linux aarch64",
    "macos": "macOS",
    "windows": "Windows",
    "not_applicable": "No platform question",
}
PLATFORM_ORDER: Final[list[str]] = list(PLATFORM_LABEL)

# The platform table has a row for each of these and for nothing else. It is a
# STRICT SUBSET of PLATFORM_LABEL: `not_applicable` is labelable but is not a
# platform, so it gets no row. That gap between "labelable" and "rendered" is where
# the Windows bug survived a per-value guard, so the set is named once here and read
# by both `validate` and `render_platforms` rather than being re-derived in each.
RENDERED_PLATFORMS: Final[list[str]] = [
    p for p in PLATFORM_ORDER if p != "not_applicable"
]

TIMING_LABEL: Final[dict[str, str]] = {
    "pre": "before the action takes effect",
    "in_line": "in line with the request",
    "post": "after the action",
    "none": "no decision point",
}

POSTURE_LABEL: Final[dict[str, str]] = {
    "fail_closed": "fail closed",
    "fail_open": "fail open",
    "fail_open_silent": "fail open, and silently",
    "silent_truncation": "silent truncation",
    "not_applicable": "no failure posture",
}

REACHABILITY_LABEL: Final[dict[str, str]] = {
    "shipped": "shipped",
    "shipped_with_platform_exception": "shipped, with a platform exception",
    "shipped_crates_io_only": "shipped on crates.io only",
    "absent_mechanism": "no mechanism exists",
    "dead_code": "present but unreachable",
}

# The manifest's own words for what stands behind a row.
EVIDENCE_LABEL: Final[dict[str, str]] = {
    "test": "a located test",
    "test_unlocated": "a test asserted but not locatable from the manifest's repository",
    "gap": "a recorded gap — no test",
}

RUNS_LABEL: Final[dict[str, str]] = {
    "standing": "It runs on every push to `main`",
    "path_gated_with_schedule": "It is path-gated, with a schedule",
    "none": "It does not run",
}

DEFAULT_STATE_ORDER: Final[list[str]] = [
    "on", "off", "open", "closed", "mixed", "not_applicable",
]

ABSENCE_STATUS: Final[frozenset[str]] = frozenset({"not_published", "not_surveyed"})

# --------------------------------------------------------------------------
# Every manifest vocabulary this script renders through an order-list.
#
# An order-list renders the values it knows and SILENTLY DROPS the rest, so an
# unlisted value does not raise — it disappears, and the page then publishes an
# absence the manifest never stated. That failure already happened once here: the
# platform table keyed on `released_platforms`, and P4 (Windows, Unsupported) fell
# out of it, so the page said "no platform-area row" where the manifest said
# Unsupported.
#
# Fixing that one row left the CLASS open. This table closes it: every field below
# is checked against the exact key set of the mapping that renders it, so a value
# the renderer cannot display stops the build instead of vanishing from a table.
#
# The trigger is not hypothetical. `PLATFORM_LABEL` has no key `linux`, and `linux`
# appears on 68 of the manifest's 80 rows in the `platform` field. One upstream
# revision normalising a `platform`-domain row to that spelling is enough.
#
# `only_domain` scopes a check to the rows whose values are actually rendered.
# It is set for exactly one field, and the reason is measured rather than assumed:
# `platform` is rendered ONLY for `platform`-domain rows (the per-platform
# host-adapter answer). Across all 80 rows that field also carries the coarser
# `linux` (68 rows), `macos` (69) and `windows` (39) — spellings PLATFORM_LABEL has
# no key for and deliberately should not, since they are not table rows. Checking
# the field unscoped would fail the build on data that renders correctly today.
#
# Every other field IS rendered across all rows, so every other check is unscoped —
# which is the strict direction, and the right one: a value that cannot be
# displayed should stop the build rather than vanish from a table.
#
# (value_field, allowed_keys, is_list, only_domain)
# --------------------------------------------------------------------------
VOCABULARIES: Final[tuple[tuple[str, frozenset[str], bool, str | None], ...]] = (
    ("coverage", frozenset(TERM_LABEL), False, None),
    ("domain", frozenset(DOMAIN_LABEL), False, None),
    ("decision_timing", frozenset(TIMING_LABEL), False, None),
    ("failure_posture", frozenset(POSTURE_LABEL), False, None),
    ("reachability", frozenset(REACHABILITY_LABEL), False, None),
    ("default_state", frozenset(DEFAULT_STATE_ORDER), False, None),
    ("evidence_runs_on_main", frozenset(RUNS_LABEL), False, None),
    ("platform", frozenset(PLATFORM_LABEL), True, "platform"),
    ("released_platforms", frozenset(PLATFORM_LABEL), True, None),
    ("released_channels", frozenset(CHANNEL_LABEL), True, None),
    ("evidence_kinds", frozenset(EVIDENCE_LABEL), True, None),
)

# --------------------------------------------------------------------------
# Path definitions.
#
# THIS IS THE ONE EDITORIAL TABLE IN THIS FILE, and it is here rather than in the
# extract because the extract is machine-generated and must not be hand-edited.
#
# Each path is one of the roles ADR 0033 §1 names, and the ids attached to it are the
# manifest rows whose `interception_component` is that role's implementation as §1's
# "Implemented today by" column names it. The grouping is this page's; every per-row
# fact rendered under it is the manifest's.
#
# The roles are named rather than numbered on purpose. ADR 0033 §1 labels them E1-E6,
# but `product-promise.md` on this same hub already uses E1-E7 for the AAASM-5528
# evidence blocks. Printing an element code here would put two meanings of `E2` one
# click apart, so this page uses the role names and cites §1 for the mapping.
#
# Deliberately NOT a partition of all 80 rows: forcing every row into a path would
# put identity, credential and control-plane rows under an interception element
# they do not implement. The unattached remainder is rendered by
# `render_unattached`, so nothing is dropped by being left out.
# --------------------------------------------------------------------------
PATHS: Final[tuple[dict[str, object], ...]] = (
    {
        "key": "checkpoints",
        "title": "Managed execution checkpoints",
        "implemented_by": (
            "the SDK seams, `aa-runtime`'s `handle_policy_query`, `aa-sdk-client` "
            "and `aa-sandbox`"
        ),
        "ids": (
            "S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12 S13 H5 G1 G2 G5"
        ).split(),
    },
    {
        "key": "transport",
        "title": "Protocol and transport mediation",
        "implemented_by": "`aa-proxy`",
        "ids": (
            "N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 "
            "M1 M2 M3 M4 M5 M6 M7 M8 M9 C1 C2 C4 G3 G4"
        ).split(),
    },
    {
        "key": "host",
        "title": "Platform-specific host-level interception adapters",
        "implemented_by": (
            "Linux eBPF via `aa-ebpf-loaderd`; on macOS and Windows, no adapter"
        ),
        "ids": "P1 P2 P3 P4 H2 H3 H4 N13 I4 G6 G7".split(),
    },
)

# Not an interception element. ADR 0033 §6 rules that a developer-tool config write
# is "Not a data-path claim at all" — it is the route by which a tool is placed onto
# a path above, which is why these rows are rendered separately from the three.
LAUNCH_IDS: Final[list[str]] = "L1 L2 L3 L4 L5 L6 L7 L8 H8 M10".split()


def _marker(key: str, kind: str) -> str:
    """Return the exact BEGIN/END marker string for a generated block."""
    return f"<!-- {kind} GENERATED:capability-surface:{key} -->"


def load_extract(path: Path) -> dict[str, object]:
    """Read and parse the pinned extract."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _rows(extract: dict[str, object]) -> list[dict[str, object]]:
    rows = extract["capability"]
    if not isinstance(rows, list):
        raise TypeError("extract key 'capability' must be an array of tables")
    return rows


def validate(extract: dict[str, object]) -> None:
    """Fail before rendering if the extract and the path table disagree."""
    rows = _rows(extract)
    by_id = {str(r["id"]): r for r in rows}

    for field, allowed, is_list, only_domain in VOCABULARIES:
        present: set[str] = set()
        for row in rows:
            if only_domain is not None and str(row["domain"]) != only_domain:
                continue
            value = row[field]
            if is_list:
                present.update(str(v) for v in value)
            else:
                present.add(str(value))
        unknown = sorted(present - allowed)
        if not unknown:
            continue
        if field == "coverage":
            raise ValueError(
                "coverage value(s) with no ADR 0033 §6 term: "
                + ", ".join(unknown)
                + " — §6 owns this vocabulary; extend §6 first, never this table"
            )
        scope = f" (on {only_domain}-domain rows)" if only_domain else ""
        raise ValueError(
            f"{field} value(s) this script cannot render{scope}: "
            f"{', '.join(unknown)}. An unlisted value is dropped silently by the "
            "order-list that renders it, so the page would publish an absence the "
            "manifest never stated. Add the value to its label mapping, deliberately."
        )

    # ---------------------------------------------------------------
    # Per-ROW conservation for the platform table.
    #
    # The vocabulary loop above is per-VALUE: it proves every value can be
    # labelled. That is necessary and not sufficient, because this table renders a
    # strictly smaller set than PLATFORM_LABEL and selects its rows by domain. Two
    # ways a platform-domain row silently leaves the table while every value it
    # carries is labelable:
    #
    #   * it carries `platform = ["not_applicable"]` — labelable, but no row is
    #     rendered for it. Not exotic: P4 already carries exactly that in
    #     `released_platforms`, for the same stated reason, so one editor
    #     propagating that reasoning one field across reproduces the Windows bug.
    #   * it is re-tagged out of the `platform` domain — then the platform it was
    #     the answer for has no row covering it, and macOS or Windows simply
    #     vanishes from the table.
    #
    # Both print "— *no `platform`-area row*" against a manifest that says
    # `unsupported`, at exit 0, and a regenerate then freezes that forever.
    # ---------------------------------------------------------------
    covered: set[str] = set()
    for row in rows:
        if str(row["domain"]) != "platform":
            continue
        for value in row["platform"]:
            if str(value) not in RENDERED_PLATFORMS:
                raise ValueError(
                    f"platform-domain row {row['id']} carries platform "
                    f"{str(value)!r}, which the platform table renders no row for. "
                    "The row's answer would be dropped silently. Use one of: "
                    + ", ".join(RENDERED_PLATFORMS)
                )
            covered.add(str(value))
    uncovered = [p for p in RENDERED_PLATFORMS if p not in covered]
    if uncovered:
        raise ValueError(
            "the platform table renders row(s) no platform-domain capability "
            f"covers: {', '.join(uncovered)}. Each would print as "
            "'no platform-area row' regardless of what the manifest says about it."
        )

    for absence in extract.get("channel_absence", []):
        channel = str(absence["channel"])
        status = str(absence["status"])
        if channel not in CHANNEL_LABEL:
            raise ValueError(f"channel_absence names unrenderable channel {channel!r}")
        if status not in ABSENCE_STATUS:
            raise ValueError(
                f"channel_absence status {status!r} is neither not_published nor "
                "not_surveyed; the channel table counts only those two, so any "
                "other value would be silently uncounted"
            )

    seen: dict[str, str] = {}
    for group_key, ids in [(str(p["key"]), list(p["ids"])) for p in PATHS] + [
        ("launch", LAUNCH_IDS)
    ]:
        for cap_id in ids:
            if cap_id not in by_id:
                raise ValueError(f"path {group_key!r} names unknown capability id {cap_id!r}")
            if cap_id in seen:
                raise ValueError(
                    f"capability id {cap_id!r} is in both {seen[cap_id]!r} and {group_key!r}"
                )
            seen[cap_id] = group_key


def _pick(extract: dict[str, object], ids: list[str]) -> list[dict[str, object]]:
    """Return the extract rows for ``ids``, in the extract's own order."""
    wanted = set(ids)
    return [r for r in _rows(extract) if str(r["id"]) in wanted]


def _census(rows: list[dict[str, object]], key: str, order: list[str]) -> list[tuple[str, int]]:
    """Return ``(value, count)`` for ``key`` across ``rows``, in ``order``.

    Asserts the census accounts for every row. ``order`` filters as well as sorts,
    so a value missing from it is dropped rather than raised — which prints a
    breakdown summing to less than the row count stated beside it, with no error.
    ``validate`` should already have made that impossible; this is the second lock,
    because the failure is silent and the two numbers sit in the same table.
    """
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row[key])] = counts.get(str(row[key]), 0) + 1
    census = [(value, counts.get(value, 0)) for value in order if counts.get(value, 0)]
    total = sum(count for _, count in census)
    if total != len(rows):
        dropped = sorted(set(counts) - set(order))
        raise ValueError(
            f"census of {key!r} accounts for {total} of {len(rows)} rows; "
            f"value(s) missing from the order list: {', '.join(dropped)}"
        )
    return census


def _terms_phrase(rows: list[dict[str, object]]) -> str:
    """Render the outcome census of ``rows`` as ``Term n · Term n``."""
    parts = [
        f"{TERM_LABEL[value]} {count}"
        for value, count in _census(rows, "coverage", TERM_ORDER)
    ]
    return " · ".join(parts) if parts else "—"


def _ids(rows: list[dict[str, object]]) -> str:
    return " ".join(f"`{r['id']}`" for r in rows) if rows else "—"


# ---------------------------------------------------------------------------
# what-ships-today.md
# ---------------------------------------------------------------------------


def render_pin(extract: dict[str, object]) -> str:
    """Render the provenance line both pages carry."""
    pin = extract["pin"]
    commit = str(pin["source_commit"])
    return "\n".join(
        [
            f"> Every table below is generated from [`{pin['source_path']}`]"
            f"(https://github.com/{pin['source_repository']}/blob/HEAD/{pin['source_path']}) "
            f"in the `{pin['source_repository']}` repository — the capability and evidence "
            f"manifest defined by {pin['manifest_ticket']} — through the pinned extract "
            "`capability-surface.toml` in this repository.",
            ">",
            f"> **Manifest version** `{pin['manifest_version']}` · "
            f"**{pin['row_count']} capability rows** · "
            f"**taken at commit** [`{commit[:9]}`]"
            f"(https://github.com/{pin['source_repository']}/commit/{commit}) · "
            f"**the manifest's own evidence tree** `{str(pin['evidence_tree'])[:9]}`, "
            f"dated {pin['evidence_date']} · "
            f"**declared fix version** {pin['fix_version']}.",
            ">",
            "> The extract is refreshed by hand, so it can lag the manifest. What this "
            "repository's CI proves is that **the generated tables** on these pages "
            "match the extract — prose outside the generated blocks is not checked, "
            "and proving the extract itself matches the manifest needs a "
            "cross-repository check, which is AAASM-5600.",
        ]
    )


def render_terms(extract: dict[str, object]) -> str:
    """Render the census of ADR 0033 §6 terms across every manifest row."""
    rows = _rows(extract)
    lines = [
        "| ADR 0033 §6 term | Rows | Areas | Capability ids |",
        "|---|---|---|---|",
    ]
    for key in TERM_ORDER:
        matching = [r for r in rows if str(r["coverage"]) == key]
        if not matching:
            lines.append(
                f"| **{TERM_LABEL[key]}** | 0 | — | "
                "— *no row in the manifest carries this term* |"
            )
            continue
        areas = sorted({DOMAIN_LABEL[str(r["domain"])] for r in matching})
        lines.append(
            f"| **{TERM_LABEL[key]}** | {len(matching)} | {', '.join(areas)} | "
            f"{_ids(matching)} |"
        )
    lines.append(f"| *Total* | {len(rows)} | | |")
    return "\n".join(lines)


def render_areas(extract: dict[str, object]) -> str:
    """Render, per manifest area, which outcomes its rows reach."""
    rows = _rows(extract)
    lines = [
        "| Area | Rows | Outcomes its rows reach today |",
        "|---|---|---|",
    ]
    for domain in DOMAIN_ORDER:
        matching = [r for r in rows if str(r["domain"]) == domain]
        lines.append(
            f"| {DOMAIN_LABEL[domain]} (`{domain}`) | {len(matching)} | "
            f"{_terms_phrase(matching)} |"
        )
    return "\n".join(lines)


def render_platforms(extract: dict[str, object]) -> str:
    """Render the per-platform position, host-level interception first."""
    rows = _rows(extract)
    # Key the host-adapter answer on each `platform`-domain row's own `platform`
    # list — the platforms the row is ABOUT — not on `released_platforms`, which is
    # where an artifact ships. The two differ, and the difference is not cosmetic:
    # P4 (Windows mediation, Unsupported) carries `released_platforms:
    # [not_applicable]` because no artifact ships for it, so keying on distribution
    # silently drops the one row whose whole content is that Windows is Unsupported.
    by_platform: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        if str(row["domain"]) != "platform":
            continue
        for value in row["platform"]:
            by_platform.setdefault(str(value), []).append(row)

    lines = [
        "| Platform | Capability rows released on it | "
        "Host-level interception today | Reachability of that row |",
        "|---|---|---|---|",
    ]
    for platform in RENDERED_PLATFORMS:
        released = [r for r in rows if platform in r["released_platforms"]]
        host = by_platform.get(platform, [])
        if host:
            term = " · ".join(
                sorted({TERM_LABEL[str(r["coverage"])] for r in host})
            )
            reach = " · ".join(
                sorted({REACHABILITY_LABEL[str(r["reachability"])] for r in host})
            )
            term = f"{term} ({_ids(host)})"
        else:
            term = "— *no `platform`-area row*"
            reach = "—"
        lines.append(
            f"| **{PLATFORM_LABEL[platform]}** | {len(released)} | {term} | {reach} |"
        )
    return "\n".join(lines)


def render_channels(extract: dict[str, object]) -> str:
    """Render the distribution-channel position, absences included."""
    rows = _rows(extract)
    absences = extract.get("channel_absence", [])
    lines = [
        "| Channel | Rows delivered on it | Rows recorded as not published there | "
        "Rows recorded as not surveyed |",
        "|---|---|---|---|",
    ]
    for channel in CHANNEL_ORDER:
        delivered = sum(1 for r in rows if channel in r["released_channels"])
        not_published = sum(
            len(a["ids"])
            for a in absences
            if str(a["channel"]) == channel and str(a["status"]) == "not_published"
        )
        not_surveyed = sum(
            len(a["ids"])
            for a in absences
            if str(a["channel"]) == channel and str(a["status"]) == "not_surveyed"
        )
        lines.append(
            f"| {CHANNEL_LABEL[channel]} (`{channel}`) | {delivered} | "
            f"{not_published or '— *not recorded*'} | "
            f"{not_surveyed or '— *not recorded*'} |"
        )
    pin = extract["pin"]
    surveyed = [str(c) for c in pin["channels_surveyed"]]
    lines.append("")
    lines.append(
        f"Channels the manifest surveyed: {', '.join(f'`{c}`' for c in surveyed)}. "
        f"Channels it did not survey: "
        + (
            ", ".join(f"`{c}`" for c in pin["channels_not_surveyed"])
            or "none."
        )
    )
    return "\n".join(lines)


def render_evidence(extract: dict[str, object]) -> str:
    """Render what stands behind the rows, and whether it runs."""
    rows = _rows(extract)
    located = [r for r in rows if "test" in r["evidence_kinds"]]
    asserted = [
        r
        for r in rows
        if "test" not in r["evidence_kinds"] and "test_unlocated" in r["evidence_kinds"]
    ]
    gap_only = [
        r
        for r in rows
        if "test" not in r["evidence_kinds"] and "test_unlocated" not in r["evidence_kinds"]
    ]
    lines = [
        "| What stands behind the row | Rows |",
        "|---|---|",
        f"| At least {EVIDENCE_LABEL['test']} | {len(located)} |",
        f"| No located test, but {EVIDENCE_LABEL['test_unlocated']} | {len(asserted)} |",
        f"| {EVIDENCE_LABEL['gap'][0].upper() + EVIDENCE_LABEL['gap'][1:]} | {len(gap_only)} |",
        "",
        "| Does that evidence run? | Rows |",
        "|---|---|",
    ]
    for value, count in _census(
        rows, "evidence_runs_on_main", list(RUNS_LABEL)
    ):
        lines.append(f"| {RUNS_LABEL[value]} | {count} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# choose-your-enforcement-path.md
# ---------------------------------------------------------------------------


def render_paths_overview(extract: dict[str, object]) -> str:
    """Render one row per path: what it reaches, and how much it excludes."""
    lines = [
        "| Path | Implemented today by | Rows | Outcomes its rows reach | "
        "Rows at Unmeasured or Unsupported |",
        "|---|---|---|---|---|",
    ]
    for path in PATHS:
        rows = _pick(extract, list(path["ids"]))
        excluded = [
            r for r in rows if str(r["coverage"]) in {"unmeasured", "unsupported"}
        ]
        lines.append(
            f"| [{path['title']}](#path-{str(path['key'])}) | "
            f"{path['implemented_by']} | "
            f"{len(rows)} | {_terms_phrase(rows)} | "
            f"{len(excluded)} of {len(rows)} |"
        )
    return "\n".join(lines)


def render_path(extract: dict[str, object], path: dict[str, object]) -> str:
    """Render one path: prerequisites, posture, and its own exclusions."""
    rows = _pick(extract, list(path["ids"]))
    preconditions = sorted({p for r in rows for p in r["preconditions"]})
    launch_paths = sorted({str(r["launch_path"]) for r in rows})
    defaults = _census(rows, "default_state", DEFAULT_STATE_ORDER)

    lines = [
        "| | |",
        "|---|---|",
        f"| **Implemented today by** | {path['implemented_by']} |",
        f"| **Manifest rows** | {len(rows)} — {_ids(rows)} |",
        f"| **Outcomes its rows reach** | {_terms_phrase(rows)} |",
        "| **Decision timing** | "
        + " · ".join(
            f"{TIMING_LABEL[v]} {c}"
            for v, c in _census(rows, "decision_timing", list(TIMING_LABEL))
        )
        + " |",
        "| **Failure posture** | "
        + " · ".join(
            f"{POSTURE_LABEL[v]} {c}"
            for v, c in _census(rows, "failure_posture", list(POSTURE_LABEL))
        )
        + " |",
        "| **Reachability** | "
        + " · ".join(
            f"{REACHABILITY_LABEL[v]} {c}"
            for v, c in _census(rows, "reachability", list(REACHABILITY_LABEL))
        )
        + " |",
        "| **Default state of its controls** | "
        + " · ".join(f"`{v}` {c}" for v, c in defaults)
        + " |",
        "| **Declared preconditions** | "
        + (" · ".join(f"`{p}`" for p in preconditions) if preconditions else "none declared")
        + " |",
        "| **Launch paths that reach it** | "
        + " · ".join(f"`{lp}`" for lp in launch_paths)
        + " |",
    ]

    excluded = [r for r in rows if str(r["coverage"]) in {"unmeasured", "unsupported"}]
    lines.append("")
    if excluded:
        lines.append("**What this path does not cover.** Every row below is one the")
        lines.append("manifest records at *Unmeasured* or *Unsupported* — nothing is known")
        lines.append("about the action, or the mechanism is not available at all.")
        lines.append("")
        lines.append("| Id | What it is | ADR 0033 §6 term | Reachability |")
        lines.append("|---|---|---|---|")
        for row in excluded:
            lines.append(
                f"| `{row['id']}` | {row['capability']} | "
                f"{TERM_LABEL[str(row['coverage'])]} | "
                f"{REACHABILITY_LABEL[str(row['reachability'])]} |"
            )
    else:
        lines.append(
            "**What this path does not cover.** No row attached to this path sits at "
            "*Unmeasured* or *Unsupported*."
        )
    return "\n".join(lines)


def render_launch(extract: dict[str, object]) -> str:
    """Render the launch and settings rows, which are not an interception path."""
    rows = _pick(extract, LAUNCH_IDS)
    lines = [
        "| Id | Route | ADR 0033 §6 term | Decision timing | Failure posture |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['id']}` | {row['capability']} | "
            f"{TERM_LABEL[str(row['coverage'])]} | "
            f"{TIMING_LABEL[str(row['decision_timing'])]} | "
            f"{POSTURE_LABEL[str(row['failure_posture'])]} |"
        )
    return "\n".join(lines)


def render_unattached(extract: dict[str, object]) -> str:
    """Render every row that no path above claims, grouped by area."""
    attached = {i for p in PATHS for i in p["ids"]} | set(LAUNCH_IDS)
    rows = [r for r in _rows(extract) if str(r["id"]) not in attached]
    lines = [
        "| Area | Rows | Outcomes they reach | Capability ids |",
        "|---|---|---|---|",
    ]
    for domain in DOMAIN_ORDER:
        matching = [r for r in rows if str(r["domain"]) == domain]
        if not matching:
            continue
        lines.append(
            f"| {DOMAIN_LABEL[domain]} (`{domain}`) | {len(matching)} | "
            f"{_terms_phrase(matching)} | {_ids(matching)} |"
        )
    lines.append(f"| *Total* | {len(rows)} | | |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Splice + orchestration
# ---------------------------------------------------------------------------


def splice(page: str, begin: str, end: str, body: str) -> str:
    """Replace the content between ``begin`` and ``end`` markers in ``page``."""
    # A duplicate marker pair is a forgery vector, not a typo. ``find`` returns the
    # FIRST pair, so a second hand-written block carrying the same key is never
    # rewritten and never compared — it survives --check at exit 0 while wearing the
    # "generated, do not hand-edit" provenance of the block above it. Counting the
    # markers is what makes "the generated tables match the extract" true of ALL of
    # them rather than of the first one.
    if page.count(begin) != 1 or page.count(end) != 1:
        raise ValueError(
            f"expected exactly one {begin!r} / {end!r} pair, found "
            f"{page.count(begin)} / {page.count(end)}; a duplicate block would be "
            "left unchecked by the splice below"
        )
    start = page.find(begin)
    stop = page.find(end)
    if start == -1 or stop == -1 or stop < start:
        raise ValueError(f"markers {begin!r} / {end!r} not found (or out of order)")
    head = page[: start + len(begin)]
    tail = page[stop:]
    return f"{head}\n\n{body}\n\n{tail}"


def _render_page_blocks(page: Path, blocks: list[tuple[str, str]]) -> tuple[str, str]:
    """Return ``(current, rendered)`` for a page carrying several blocks."""
    current = page.read_text(encoding="utf-8")
    rendered = current
    for key, body in blocks:
        rendered = splice(rendered, _marker(key, "BEGIN"), _marker(key, "END"), body)
    return current, rendered


def render_all(extract: dict[str, object]) -> list[tuple[Path, str, str]]:
    """Return ``(path, current, rendered)`` for both managed pages."""
    path_blocks: list[tuple[str, str]] = [("pin", render_pin(extract))]
    path_blocks.append(("paths-overview", render_paths_overview(extract)))
    for path in PATHS:
        path_blocks.append((f"path-{path['key']}", render_path(extract, path)))
    path_blocks.append(("launch", render_launch(extract)))
    path_blocks.append(("unattached", render_unattached(extract)))

    return [
        (
            SHIPS_PATH,
            *_render_page_blocks(
                SHIPS_PATH,
                [
                    ("pin", render_pin(extract)),
                    ("terms", render_terms(extract)),
                    ("areas", render_areas(extract)),
                    ("platforms", render_platforms(extract)),
                    ("channels", render_channels(extract)),
                    ("evidence", render_evidence(extract)),
                ],
            ),
        ),
        (PATHS_PATH, *_render_page_blocks(PATHS_PATH, path_blocks)),
    ]


def main(argv: list[str] | None = None) -> int:
    """Entry point: regenerate the pages, or with ``--check`` verify freshness."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed pages match the extract; exit nonzero if stale",
    )
    args = parser.parse_args(argv)

    extract = load_extract(EXTRACT_PATH)
    validate(extract)
    results = render_all(extract)

    if args.check:
        stale = [path for path, current, rendered in results if current != rendered]
        if stale:
            sys.stderr.write(
                "Evaluator guides are out of date with "
                f"{EXTRACT_PATH.relative_to(REPO_ROOT)}:\n"
            )
            for path in stale:
                sys.stderr.write(f"  - {path.relative_to(REPO_ROOT)}\n")
            sys.stderr.write("Run: python3 docs/scripts/generate_capability_surface.py\n")
            return 1
        return 0

    for path, current, rendered in results:
        if rendered != current:
            path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
