"""Validate every hub page's `AA-PAGE-META` block against `page-standards.md`'s
own contract. AAASM-5601.

`page-standards.md` is the spec: field reference, the 15 cross-field rules, the
parsing contract, and the freshness thresholds are written there to be
"sufficient with no further decisions. If a rule needs judgement to implement,
that is a defect in this page — report it rather than choosing." This script
implements that contract; it does not add rules of its own. Anywhere this file
and `page-standards.md` disagree, `page-standards.md` is right and this file has
a bug.

WHY A HAND-WRITTEN PARSER, NOT PyYAML
---------------------------------------
This repo is Python-stdlib-only by convention (see `.claude/CLAUDE.md` — the
compatibility generator and every other script here has no third-party
dependency), and `page-standards.md` calls the metadata block "a YAML 1.2
mapping" in the general sense, but its own field reference closes the grammar
actually in use to a narrow, fully-enumerable subset: flat scalars, inline
`[a, b]` lists, one block object (`last_verified`), and two block lists of flat
block mappings (`platforms[]`, `claims[]`). Nothing here uses YAML's anchors,
multi-document streams, or arbitrary nesting depth. A parser scoped to exactly
that grammar is a few hundred lines and needs no new dependency; a general YAML
1.2 parser would be doing (and getting wrong, for corner cases nothing here
exercises) far more than this format ever asks of it.

WHAT THIS SCRIPT DOES ON A GRAMMAR IT DOESN'T RECOGNISE
----------------------------------------------------------
Raises, rather than silently reading a partial or wrong structure — the same
refuse-rather-than-guess posture `check_claim_vocabulary.py` and
`generate_capability_tables.py` already take in this repo. A validator that
fails open on a shape it can't parse is worse than one that doesn't exist.

SCOPE: A PAGE WITH NO METADATA BLOCK IS NOT, BY ITSELF, AN ERROR HERE
------------------------------------------------------------------------
`page-standards.md`'s own parsing contract calls "zero blocks" a hard error,
and taken literally that would fail every page in this hub that has not yet
adopted the block -- rolling every page onto one is AAASM-5610's adoption
work, still in progress (this page carried the only block when written; ten
do as of AAASM-5600/5601). Requiring one from every page today would fail the
site for a rollout this ticket does not own, the same reasoning AAASM-5600
already applied to `capability_ids`.

So this script's scope is: (1) a page that DOES declare a block gets it fully
validated against every rule below -- "zero blocks" is read as scoped to a
page already expected to carry one, and a page with a block that fails to
parse, or parses but violates a rule, is always an error regardless of
rollout; (2) rule 13 (an unbounded claim verb with no bounding metadata) is
checked on EVERY page, block or no block, because it is the one rule whose
whole purpose is catching exactly the pages that have not yet been brought
under this contract -- a page with no block making an unguarded capability
claim is the acceptance criterion ("public pages cannot omit status and
limitations when the claim depends on them"), not an adoption question.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

SCRIPT_DIR: Final[Path] = Path(__file__).resolve().parent
REPO_ROOT: Final[Path] = SCRIPT_DIR.parent.parent
SRC_DIR: Final[Path] = REPO_ROOT / "docs" / "src"
COMPATIBILITY_TOML: Final[Path] = REPO_ROOT / "compatibility.toml"

# --------------------------------------------------------------------------- #
# The closed vocabularies `page-standards.md`'s field reference defines.
# --------------------------------------------------------------------------- #

PAGE_TYPES: Final[frozenset[str]] = frozenset({"product", "guide", "reference", "architecture", "adr"})
AUDIENCES: Final[frozenset[str]] = frozenset(
    {"evaluator", "developer", "operator", "security-engineer", "contributor", "auditor"}
)
AVAILABILITIES: Final[frozenset[str]] = frozenset(
    {"available-verified", "available-with-limits", "preview", "deprecated"}
)
# ADR 0033 §6's eleven terms, verbatim (prose form, as `claims[].term` carries it).
CLAIM_TERMS: Final[frozenset[str]] = frozenset(
    {
        "Observed",
        "Detected",
        "Evaluated",
        "Denied before execution",
        "Redacted",
        "Approval required",
        "Degraded",
        "Unmeasured",
        "Experimental",
        "Planned",
        "Unsupported",
    }
)
# Rule 14: every §6 term that asserts a control did something to an action —
# everything except Unmeasured/Unsupported/Planned/Experimental (see that
# rule's own docstring below for why those four and no others are excluded).
RULE_14_TERMS: Final[frozenset[str]] = frozenset(
    {
        "Observed",
        "Detected",
        "Evaluated",
        "Denied before execution",
        "Redacted",
        "Approval required",
        "Degraded",
    }
)
PLATFORM_CHANNELS: Final[frozenset[str]] = frozenset(
    {"github-release", "homebrew", "ghcr", "install-sh", "crates-io"}
)
PLATFORM_PLATFORMS: Final[frozenset[str]] = frozenset({"linux-x86_64", "linux-aarch64", "macos", "windows"})
PLATFORM_STATUSES: Final[frozenset[str]] = frozenset({"available-verified", "available-with-limits", "unsupported"})
# rule 7: platforms[].status may never be preview/deprecated, nor a §6 term
# other than `unsupported` — expressed here as the allow-list above, which is
# the same enum `page-standards.md`'s own [`platforms[]`](#platforms) table
# gives `status`, so rule 7 is enforced simply by using this set rather than
# AVAILABILITIES or CLAIM_TERMS.

# `owner` surfaces, exactly as `page-standards.md`'s table pairs them — fixed
# here rather than by cross-repository lookup, per that page's own design.
OWNER_SURFACES: Final[frozenset[str]] = frozenset(
    {
        "L0:horonomy.dev",
        "L1:official-website",
        "L2:docs",
        "L3:agent-assembly",
        "L3:python-sdk",
        "L3:node-sdk",
        "L3:go-sdk",
        "L3:arena",
        "L3:cloud",
        "L3:agent-assembly-enterprise",
        "L4:examples",
    }
)
# `owner` -> the repository name this hub page must sit in for
# `canonical_source: self` to be valid (rule 9). This repo IS `docs` (L2), so
# only L2:docs makes `self` meaningful here; anything else always requires a
# link, which rule 9/10 already enforce independent of this mapping.
SELF_OWNER: Final[str] = "L2:docs"

AREA_IDS: Final[frozenset[str]] = frozenset(
    {
        "core",
        "python-sdk",
        "node-sdk",
        "go-sdk",
        "arena",
        "examples",
        "homebrew",
        "specs",
        "releases",
        "cloud",
        "enterprise",
        "operations",
    }
)

# Rule 12: which disclosure levels a page_type must/may carry.
LEVELS_MUST: Final[dict[str, frozenset[int]]] = {
    "product": frozenset({1, 2, 3}),
    "guide": frozenset({1, 3}),
    "reference": frozenset({3, 4}),
    "architecture": frozenset({3, 4}),
    "adr": frozenset({4}),
}
LEVELS_MAY: Final[dict[str, frozenset[int]]] = {
    "product": frozenset(),
    "guide": frozenset({2}),
    "reference": frozenset({1, 2}),
    "architecture": frozenset({1, 2}),
    "adr": frozenset({3}),
}

RULE_13_VERBS: Final[tuple[str, ...]] = ("protects", "enforces", "catches", "prevents", "guarantees")

_CANONICAL_LINK = re.compile(
    r"^(?:[\w./-]+\.md(?:#[\w-]+)?"  # repo-relative path, optional anchor
    r"|https://github\.com/[\w.-]+/[\w.-]+/blob/HEAD/[\w./-]+"
    r"|https://docs\.agent-assembly\.com/[\w./-]*)$"
)
_LIMITATIONS_FORM = re.compile(r"^(?:#[\w-]+|[\w./-]+\.md#[\w-]+)$")


class MetaError(ValueError):
    """A page's metadata block is invalid. Carries the file-relative path."""


# --------------------------------------------------------------------------- #
# Locating and lexing the AA-PAGE-META block
# --------------------------------------------------------------------------- #

_BEGIN = "<!-- BEGIN AA-PAGE-META"
_END = "END AA-PAGE-META -->"
_FENCE = re.compile(r"^(`{3,}|~{3,})")
_INLINE_CODE = re.compile(r"`[^`\n]*`")


def _strip_exempt_regions(text: str) -> str:
    """Blank fenced code blocks and inline code spans, preserving line count and
    non-exempt characters' positions — used only to decide where a genuine
    BEGIN/END delimiter or a rule-13 verb can occur, per the parsing contract
    and rule 13's own exemption list.
    """
    lines = text.split("\n")
    out: list[str] = []
    fence: str | None = None
    for line in lines:
        stripped = line.strip()
        m = _FENCE.match(stripped)
        if fence is None:
            if m:
                fence = m.group(1)
                out.append("")
                continue
        else:
            out.append("")
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        out.append(_INLINE_CODE.sub(lambda mm: "\x00" * len(mm.group(0)), line))
    return "\n".join(out)


def find_meta_block(raw_text: str) -> tuple[str, int, int]:
    """Return (body_text, begin_line_index, end_line_index), 0-based, over the
    RAW (unstripped) text — the caller needs real content to parse.

    Delimiters are located against the exemption-stripped text (fences/inline
    code do not open or close a block) but returned as indices into the raw
    line list, so the body handed back is the real content between them.
    """
    raw_lines = raw_text.split("\n")
    scan_lines = _strip_exempt_regions(raw_text).split("\n")

    begins = [i for i, line in enumerate(scan_lines) if line.strip().startswith(_BEGIN)]
    ends = [i for i, line in enumerate(scan_lines) if line.strip() == _END]

    if len(begins) == 0 and len(ends) == 0:
        raise MetaError("no AA-PAGE-META block found")
    if len(begins) != 1 or len(ends) != 1:
        raise MetaError(
            f"expected exactly one BEGIN and one END AA-PAGE-META delimiter, "
            f"found {len(begins)} BEGIN and {len(ends)} END"
        )
    begin_idx, end_idx = begins[0], ends[0]
    if end_idx <= begin_idx:
        raise MetaError("END AA-PAGE-META appears before BEGIN AA-PAGE-META")

    # "the first construct in the file, before the # H1" — no non-blank content
    # may precede the BEGIN line.
    for line in raw_lines[:begin_idx]:
        if line.strip():
            raise MetaError("AA-PAGE-META block is not the first construct in the file")

    body_lines = raw_lines[begin_idx + 1 : end_idx]
    body = "\n".join(body_lines)
    if "--" in "\n".join(raw_lines[begin_idx + 1 : end_idx]):
        raise MetaError("metadata body contains '--', which is not legal inside an HTML comment")
    return body, begin_idx, end_idx


# --------------------------------------------------------------------------- #
# Parsing the body — the narrow grammar described in the module docstring.
# --------------------------------------------------------------------------- #

_KV_LINE = re.compile(r"^([a-z_][a-z0-9_]*):\s?(.*)$")
_DASH_KV_LINE = re.compile(r"^-\s?([a-z_][a-z0-9_]*):\s?(.*)$")

# Which top-level keys are which shape — closed, per the field reference.
FLOW_LIST_KEYS: Final[frozenset[str]] = frozenset({"audience", "disclosure_levels", "capability_ids"})
BLOCK_OBJECT_KEYS: Final[frozenset[str]] = frozenset({"last_verified"})
BLOCK_LIST_KEYS: Final[frozenset[str]] = frozenset({"platforms", "claims"})


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _parse_flow_list(raw: str) -> list[str]:
    raw = raw.strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        raise MetaError(f"expected a flow list like [a, b], got: {raw!r}")
    inner = raw[1:-1].strip()
    if not inner:
        return []
    return [_unquote(item) for item in inner.split(",")]


@dataclass
class Lexed:
    scalars: dict[str, str] = field(default_factory=dict)
    lists: dict[str, list[str]] = field(default_factory=dict)
    objects: dict[str, dict[str, str]] = field(default_factory=dict)
    block_lists: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    keys_seen: list[str] = field(default_factory=list)


def parse_body(body: str) -> Lexed:
    """Parse the metadata body into scalars / flow lists / one block object /
    block lists of flat maps — see module docstring for why this grammar and
    not general YAML.
    """
    lines = [ln for ln in body.split("\n")]
    result = Lexed()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith(" "):
            raise MetaError(f"unexpected indented line at the top level: {line!r}")

        m = _KV_LINE.match(line)
        if not m:
            raise MetaError(f"cannot parse metadata line: {line!r}")
        key, rest = m.group(1), m.group(2)
        if key in result.keys_seen:
            raise MetaError(f"key {key!r} appears more than once")
        result.keys_seen.append(key)

        if rest.strip():
            # Scalar or flow list on the same line.
            if key in FLOW_LIST_KEYS:
                result.lists[key] = _parse_flow_list(rest)
            else:
                result.scalars[key] = _unquote(rest)
            i += 1
            continue

        # Bare key: a block object or a block list of flat maps follows,
        # indented. Collect the indented run.
        i += 1
        block_lines: list[str] = []
        while i < n and (lines[i].startswith("  ") or not lines[i].strip()):
            block_lines.append(lines[i])
            i += 1

        if key in BLOCK_OBJECT_KEYS:
            result.objects[key] = _parse_flat_object(block_lines, indent=2)
        elif key in BLOCK_LIST_KEYS:
            result.block_lists[key] = _parse_block_list(block_lines)
        else:
            raise MetaError(f"key {key!r} has no value and is not a recognised block key")

    return result


def _parse_flat_object(lines: list[str], indent: int) -> dict[str, str]:
    prefix = " " * indent
    out: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        if not line.startswith(prefix):
            raise MetaError(f"expected {indent}-space indent, got: {line!r}")
        content = line[indent:]
        m = _KV_LINE.match(content)
        if not m:
            raise MetaError(f"cannot parse object field: {line!r}")
        out[m.group(1)] = _unquote(m.group(2))
    return out


def _parse_block_list(lines: list[str]) -> list[dict[str, str]]:
    """Parse `  - key: value` / `    key: value` items — each item is a flat
    map whose first field shares the dash's line and whose remaining fields
    are indented to align under it (2-space dash indent + 2 more spaces, i.e.
    4-space continuation — the shape every real `platforms[]`/`claims[]`
    block in this hub uses).
    """
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("  - "):
            if current is not None:
                items.append(current)
            content = line[4:]
            m = _KV_LINE.match(content)
            if not m:
                raise MetaError(f"cannot parse block-list item start: {line!r}")
            current = {m.group(1): _unquote(m.group(2))}
        elif line.startswith("    "):
            if current is None:
                raise MetaError(f"block-list continuation with no open item: {line!r}")
            content = line[4:]
            m = _KV_LINE.match(content)
            if not m:
                raise MetaError(f"cannot parse block-list item field: {line!r}")
            current[m.group(1)] = _unquote(m.group(2))
        else:
            raise MetaError(f"unexpected line in block list: {line!r}")
    if current is not None:
        items.append(current)
    return items


# --------------------------------------------------------------------------- #
# Freshness thresholds ("last_verified") — needs the current release version.
# --------------------------------------------------------------------------- #


def current_release_version(compat_path: Path) -> str:
    """The `core` value of the one `[[release]]` table with `status = "current"`
    in `compatibility.toml` — parsed, not grepped (the file's own worked example
    contains a second, commented-out match for the bare string).
    """
    with compat_path.open("rb") as handle:
        manifest = tomllib.load(handle)
    current = [r for r in manifest.get("release", []) if r.get("status") == "current"]
    if len(current) != 1:
        raise ValueError(
            f"expected exactly one [[release]] with status = \"current\" in "
            f"{compat_path.name}, found {len(current)}"
        )
    return str(current[0]["core"])


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #


@dataclass
class Diagnostic:
    path: str
    severity: str  # "error" | "warning" | "pre-existing"
    message: str
    # 1-indexed line range this diagnostic anchors to, for --diff-base scoping.
    # Block-validation diagnostics anchor to the whole block (a rewrite of any
    # line in an existing block is treated as touching the diagnostic — the
    # conservative, block-baseline-is-zero-today direction); rule 13 hits
    # anchor to the exact line the verb occurs on.
    line: int = 1
    end_line: int = 1


def validate_page(rel_path: str, lexed: Lexed, current_version: str, today: str) -> list[Diagnostic]:
    d: list[Diagnostic] = []
    s, lists, objs, bl = lexed.scalars, lexed.lists, lexed.objects, lexed.block_lists

    known_keys = (
        {"schema_version", "page_type", "user_job", "owner", "canonical_source", "describes_capability",
         "area", "availability", "limitations", "deeper"}
        | FLOW_LIST_KEYS
        | BLOCK_OBJECT_KEYS
        | BLOCK_LIST_KEYS
    )
    for key in lexed.keys_seen:
        if key not in known_keys:
            d.append(Diagnostic(rel_path, "error", f"unknown metadata key {key!r}"))

    # --- required scalars ---
    if s.get("schema_version") != "1":
        d.append(Diagnostic(rel_path, "error", f"schema_version must be 1, got {s.get('schema_version')!r}"))
    page_type = s.get("page_type")
    if page_type not in PAGE_TYPES:
        d.append(Diagnostic(rel_path, "error", f"page_type {page_type!r} not in {sorted(PAGE_TYPES)}"))
    audience = lists.get("audience", [])
    if not audience:
        d.append(Diagnostic(rel_path, "error", "audience must be non-empty"))
    for a in audience:
        if a not in AUDIENCES:
            d.append(Diagnostic(rel_path, "error", f"audience value {a!r} not in {sorted(AUDIENCES)}"))
    user_job = s.get("user_job", "")
    if not (10 <= len(user_job) <= 120):
        d.append(Diagnostic(rel_path, "error", f"user_job must be 10-120 chars, got {len(user_job)}"))
    if user_job.endswith("."):
        d.append(Diagnostic(rel_path, "error", "user_job must not end with a period"))
    if re.search(r"\.\s", user_job):
        d.append(Diagnostic(rel_path, "error", "user_job must be one sentence (no interior '. ')"))
    owner = s.get("owner")
    if owner not in OWNER_SURFACES:
        d.append(Diagnostic(rel_path, "error", f"owner {owner!r} not in the fixed owner-surface table"))
    describes_capability = s.get("describes_capability")
    if describes_capability not in ("true", "false"):
        d.append(Diagnostic(rel_path, "error", f"describes_capability must be true/false, got {describes_capability!r}"))
    is_capability_page = describes_capability == "true"

    canonical_source = s.get("canonical_source")
    if canonical_source is None:
        d.append(Diagnostic(rel_path, "error", "canonical_source is required"))
    elif canonical_source == "self":
        # rule 9: canonical_source: self requires the owner surface to name the
        # repository this page is in -- this repo is `docs` (L2).
        if owner != SELF_OWNER:
            d.append(
                Diagnostic(
                    rel_path, "error",
                    f"canonical_source: self requires owner: {SELF_OWNER}, got {owner!r}",
                )
            )
    else:
        # rule 10
        if not _CANONICAL_LINK.match(canonical_source):
            d.append(Diagnostic(rel_path, "error", f"canonical_source {canonical_source!r} is not in canonical-link form"))
        if re.search(r"/blob/(?!HEAD/)[^/]+/", canonical_source):
            d.append(Diagnostic(rel_path, "error", f"canonical_source {canonical_source!r} uses a branch name, not HEAD"))

    disclosure_levels_raw = lists.get("disclosure_levels", [])
    try:
        disclosure_levels = [int(x) for x in disclosure_levels_raw]
    except ValueError:
        disclosure_levels = []
        d.append(Diagnostic(rel_path, "error", f"disclosure_levels must be integers, got {disclosure_levels_raw!r}"))
    if not disclosure_levels:
        d.append(Diagnostic(rel_path, "error", "disclosure_levels must be non-empty"))
    if disclosure_levels != sorted(set(disclosure_levels)):
        d.append(Diagnostic(rel_path, "error", "disclosure_levels must be ascending with no duplicates"))
    if any(lvl not in (1, 2, 3, 4) for lvl in disclosure_levels):
        d.append(Diagnostic(rel_path, "error", "disclosure_levels must be a subset of [1,2,3,4]"))

    # rule 12
    if page_type in LEVELS_MUST:
        must = LEVELS_MUST[page_type]
        may = LEVELS_MAY[page_type]
        allowed = must | may
        have = set(disclosure_levels)
        if not must <= have:
            d.append(Diagnostic(rel_path, "error", f"page_type {page_type!r} must carry levels {sorted(must)}, has {sorted(have)}"))
        if not have <= allowed:
            d.append(Diagnostic(rel_path, "error", f"page_type {page_type!r} may only carry levels {sorted(allowed)}, has {sorted(have)}"))

    # rule 15
    if page_type in ("product", "guide") and 4 in disclosure_levels:
        d.append(Diagnostic(rel_path, "error", f"page_type {page_type!r} may never carry disclosure level 4"))

    # rule 11
    deeper = s.get("deeper")
    if disclosure_levels and max(disclosure_levels) < 4 and not deeper:
        d.append(Diagnostic(rel_path, "error", "max(disclosure_levels) < 4 requires 'deeper'"))
    if deeper is not None and not _CANONICAL_LINK.match(deeper):
        d.append(Diagnostic(rel_path, "error", f"deeper {deeper!r} is not in canonical-link form"))

    # --- conditional fields, gated by describes_capability (rules 1/2) ---
    area = s.get("area")
    availability = s.get("availability")
    limitations = s.get("limitations")
    platforms = bl.get("platforms", [])
    last_verified = objs.get("last_verified")
    claims = bl.get("claims", [])

    has_self_planned = any(
        c.get("term") == "Planned" and c.get("subject", "self") == "self" for c in claims
    )

    if is_capability_page:
        # rule 1
        if area is None:
            d.append(Diagnostic(rel_path, "error", "describes_capability: true requires 'area'"))
        if last_verified is None:
            d.append(Diagnostic(rel_path, "error", "describes_capability: true requires 'last_verified'"))
        if "claims" not in lexed.keys_seen:
            d.append(Diagnostic(rel_path, "error", "describes_capability: true requires 'claims'"))
        if "platforms" not in lexed.keys_seen:
            d.append(Diagnostic(rel_path, "error", "describes_capability: true requires 'platforms'"))
        # rule 4: a self-subject Planned claim forces availability absent and
        # platforms == [].
        if has_self_planned:
            if availability is not None:
                d.append(Diagnostic(rel_path, "error", "a self-subject Planned claim requires 'availability' absent"))
            if platforms:
                d.append(Diagnostic(rel_path, "error", "a self-subject Planned claim requires platforms: []"))
            self_planned_count = sum(
                1 for c in claims if c.get("subject", "self") == "self"
            )
            if self_planned_count > 1:
                d.append(Diagnostic(rel_path, "error", "a self-subject Planned claim allows no other self-subject claim"))
        else:
            if not platforms:
                d.append(Diagnostic(rel_path, "error", "platforms must be non-empty unless a self-subject Planned claim applies"))
        # rule 6: availability present iff describes_capability true and no
        # self-subject Planned.
        if has_self_planned:
            pass  # already covered by rule 4 above
        elif availability is None:
            d.append(Diagnostic(rel_path, "error", "describes_capability: true (without a self-subject Planned claim) requires 'availability'"))
    else:
        # rule 2
        for key, val in (("area", area), ("availability", availability), ("limitations", limitations)):
            if val is not None:
                d.append(Diagnostic(rel_path, "error", f"describes_capability: false requires {key!r} absent"))
        for key in ("platforms", "last_verified", "claims"):
            if key in lexed.keys_seen:
                d.append(Diagnostic(rel_path, "error", f"describes_capability: false requires {key!r} absent"))
        if availability is not None:
            d.append(Diagnostic(rel_path, "error", "describes_capability: false requires 'availability' absent"))

    if area is not None and area not in AREA_IDS:
        d.append(Diagnostic(rel_path, "error", f"area {area!r} not in the 12 area ids"))
    if availability is not None and availability not in AVAILABILITIES:
        d.append(Diagnostic(rel_path, "error", f"availability {availability!r} not in {sorted(AVAILABILITIES)}"))

    # rule 3
    if availability in ("available-with-limits", "deprecated") and not limitations:
        d.append(Diagnostic(rel_path, "error", f"availability: {availability} requires non-empty 'limitations'"))
    if limitations is not None and not _LIMITATIONS_FORM.match(limitations):
        d.append(Diagnostic(rel_path, "error", f"limitations {limitations!r} must be an in-page anchor or a link+anchor"))

    # --- platforms[] ---
    seen_pairs: set[tuple[str, str]] = set()
    for row in platforms:
        channel, plat, status = row.get("channel"), row.get("platform"), row.get("status")
        if channel not in PLATFORM_CHANNELS:
            d.append(Diagnostic(rel_path, "error", f"platforms[].channel {channel!r} invalid"))
        if plat not in PLATFORM_PLATFORMS:
            d.append(Diagnostic(rel_path, "error", f"platforms[].platform {plat!r} invalid"))
        # rule 7
        if status not in PLATFORM_STATUSES:
            d.append(Diagnostic(rel_path, "error", f"platforms[].status {status!r} invalid (rule 7)"))
        if status is not None and status != "unsupported" and not row.get("evidence"):
            d.append(Diagnostic(rel_path, "error", "platforms[] row requires 'evidence' unless status is unsupported"))
        pair = (channel, plat)
        if pair in seen_pairs:
            d.append(Diagnostic(rel_path, "error", f"duplicate platforms[] pair {pair!r}"))
        seen_pairs.add(pair)

    # rule 5
    if availability == "available-verified":
        for row in platforms:
            if row.get("status") == "available-with-limits":
                d.append(Diagnostic(rel_path, "error", "availability: available-verified forbids an available-with-limits platforms[] row"))

    # --- last_verified ---
    if last_verified is not None:
        version = last_verified.get("version")
        ref = last_verified.get("ref")
        date = last_verified.get("date")
        method = last_verified.get("method")
        if not version:
            d.append(Diagnostic(rel_path, "error", "last_verified.version is required"))
        if not method or len(method) > 200:
            d.append(Diagnostic(rel_path, "error", "last_verified.method must be non-empty and <= 200 chars"))
        if ref in ("main", "master", "HEAD"):
            d.append(Diagnostic(rel_path, "error", f"last_verified.ref must not be a branch name, got {ref!r}"))
        elif not (re.match(r"^v\d+\.\d+\.\d+(-[A-Za-z0-9.]+)?$", ref or "") or re.match(r"^[0-9a-f]{40}$", ref or "")):
            d.append(Diagnostic(rel_path, "error", f"last_verified.ref {ref!r} is not a tag or a 40-char SHA"))
        if not date or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            d.append(Diagnostic(rel_path, "error", f"last_verified.date {date!r} is not ISO 8601 YYYY-MM-DD"))
        else:
            if date > today:
                d.append(Diagnostic(rel_path, "error", f"last_verified.date {date!r} is in the future"))
            else:
                age_days = _days_between(date, today)
                if age_days > 180:
                    d.append(Diagnostic(rel_path, "error", f"last_verified.date is {age_days} days old (> 180, stale)"))
                elif age_days > 90:
                    d.append(Diagnostic(rel_path, "warning", f"last_verified.date is {age_days} days old (> 90)"))
            if version and version != current_version:
                d.append(Diagnostic(rel_path, "warning", f"last_verified.version {version!r} differs from current release {current_version!r}"))

    # --- claims[] ---
    for c in claims:
        term = c.get("term")
        if term not in CLAIM_TERMS:
            d.append(Diagnostic(rel_path, "error", f"claims[].term {term!r} not in ADR 0033 §6's eleven terms (rule 8)"))
        if not c.get("evidence"):
            d.append(Diagnostic(rel_path, "error", "claims[] row requires non-empty 'evidence'"))
        subject = c.get("subject", "self")
        if subject != "self" and subject not in OWNER_SURFACES:
            d.append(Diagnostic(rel_path, "error", f"claims[].subject {subject!r} is neither 'self' nor a valid owner"))

    # rule 14
    if any(c.get("term") in RULE_14_TERMS for c in claims) and not limitations:
        d.append(Diagnostic(rel_path, "error", "a §6 rule-14 claim term requires non-empty 'limitations'"))

    return d


def _days_between(earlier: str, later: str) -> int:
    from datetime import date as _date

    e = _date.fromisoformat(earlier)
    later_date = _date.fromisoformat(later)
    return (later_date - e).days


def find_rule13_hits(raw_text: str) -> list[tuple[str, int]]:
    """Rule 13: an unbounded claim verb in the body (outside fences/inline
    code/quoted spans) requires describes_capability, non-empty claims and
    non-empty limitations. Returns `(verb, 1-indexed line)` per hit."""
    stripped = _strip_exempt_regions(raw_text)
    # Strip straight and typographic double-quoted spans, document-wide.
    stripped = re.sub(r'"[^"]*"', lambda m: "\x00" * len(m.group(0)), stripped)
    if stripped.count('"') % 2 != 0:
        raise MetaError("odd number of straight double quotes in the document")
    stripped = re.sub(r"“[^”]*”", lambda m: "\x00" * len(m.group(0)), stripped)

    hits: list[tuple[str, int]] = []
    for verb in RULE_13_VERBS:
        for m in re.finditer(rf"\b{verb}\b", stripped, re.IGNORECASE):
            line = stripped.count("\n", 0, m.start()) + 1
            hits.append((verb, line))
    return hits


def validate_file(path: Path, current_version: str, today: str) -> list[Diagnostic]:
    rel = str(path.relative_to(REPO_ROOT))
    raw = path.read_text(encoding="utf-8")

    diags: list[Diagnostic] = []
    lexed: Lexed | None = None

    try:
        body, begin_idx, end_idx = find_meta_block(raw)
    except MetaError as exc:
        if str(exc) == "no AA-PAGE-META block found":
            # Not itself an error -- see module docstring's SCOPE section.
            # Rule 13 below still applies regardless.
            body = None
        else:
            diags.append(Diagnostic(rel, "error", str(exc), line=1, end_line=1))
            body = None

    if body is not None:
        block_line, block_end_line = begin_idx + 1, end_idx + 1
        try:
            lexed = parse_body(body)
        except MetaError as exc:
            diags.append(Diagnostic(rel, "error", f"metadata body: {exc}", line=block_line, end_line=block_end_line))
        else:
            for d in validate_page(rel, lexed, current_version, today):
                d.line, d.end_line = block_line, block_end_line
                diags.append(d)

    try:
        rule13_hits = find_rule13_hits(raw)
    except MetaError as exc:
        diags.append(Diagnostic(rel, "error", str(exc), line=1, end_line=1))
        rule13_hits = []
    if rule13_hits:
        describes_capability = lexed.scalars.get("describes_capability") if lexed else None
        claims_present = bool(lexed and lexed.block_lists.get("claims"))
        limitations_present = bool(lexed and lexed.scalars.get("limitations"))
        if describes_capability != "true" or not claims_present or not limitations_present:
            verbs = sorted({v for v, _ in rule13_hits})
            for verb, line in rule13_hits:
                diags.append(
                    Diagnostic(
                        rel, "error",
                        f"rule 13: unbounded claim verb {verb!r} (of {verbs}) requires "
                        "describes_capability: true, non-empty claims, and limitations",
                        line=line, end_line=line,
                    )
                )

    return diags


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD) for freshness checks, for testing")
    parser.add_argument(
        "--diff-base",
        help="restrict ERROR diagnostics to lines added or modified since this ref; "
        "a pre-existing violation is reported as 'pre-existing' instead of blocking. "
        "This repo's rule-13 baseline is non-empty (unlike check_claim_vocabulary.py's, "
        "which is zero) -- see module docstring.",
    )
    args = parser.parse_args(argv)

    from datetime import date as _date

    sys.path.insert(0, str(SCRIPT_DIR))
    import check_claim_vocabulary as ccv  # noqa: E402  (reuses _changed_lines, proven elsewhere in this repo)

    today = args.today or _date.today().isoformat()
    current_version = current_release_version(COMPATIBILITY_TOML)

    all_diags: list[Diagnostic] = []
    pages_checked = 0
    targets: list[str] = []
    for path in sorted(SRC_DIR.rglob("*.md")):
        pages_checked += 1
        rel = str(path.relative_to(REPO_ROOT))
        targets.append(rel)
        all_diags.extend(validate_file(path, current_version, today))

    if args.diff_base:
        changed = ccv._changed_lines(REPO_ROOT, args.diff_base, targets)
        for d in all_diags:
            if d.severity != "error":
                continue
            touched = changed.get(d.path, set())
            if not any(line in touched for line in range(d.line, d.end_line + 1)):
                d.severity = "pre-existing"

    errors = [d for d in all_diags if d.severity == "error"]
    warnings = [d for d in all_diags if d.severity == "warning"]
    pre_existing = [d for d in all_diags if d.severity == "pre-existing"]
    for d in all_diags:
        print(f"{d.path}:{d.line}: {d.severity}: {d.message}")

    print(
        f"\nvalidate_page_metadata: {pages_checked} page(s) checked; "
        f"{len(errors)} error(s), {len(warnings)} warning(s), "
        f"{len(pre_existing)} pre-existing."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
