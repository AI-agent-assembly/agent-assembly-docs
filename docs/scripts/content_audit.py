"""Recurring full-hub content audit. AAASM-5603.

Runs every existing claim/metadata/drift checker this hub already has
(`check_repo_names.py`, `validate_page_metadata.py` in full-tree mode,
`validate_capability_ids.py`, `generate_compatibility.py --check`) as
subprocesses and aggregates their findings into one dated, provenance-stamped
report, plus a small set of metrics AAASM-5603's own scope calls for that no
existing script computes: orphan pages (tracked under `docs/src/` but not
reachable from `SUMMARY.md`) and duplicate canonical claims (two or more pages
declaring the same `capability_ids` entry as their own -- a page's block does
not currently say "this is MY canonical claim" vs "I merely reference this
capability", so this is a coarse proxy: any id claimed by more than one page is
reported, not asserted to be wrong).

WHY AGGREGATE RATHER THAN ADD A SECOND VALIDATION PATH: every one of the
existing checkers already IS the audit for its own area; this script does not
re-implement any of their rules, it runs them and reads their output. The only
new logic here is orphan-page and duplicate-claim detection, which nothing
else in this repo computes, and the report/metrics rendering.

WHY THIS DOES NOT FAIL THE BUILD: this is a scheduled audit, not a PR gate --
`validate_page_metadata.py`'s own rule 13 backlog (~30 pre-existing unbounded-
verb findings, tracked on AAASM-5610) makes a full-tree run of that checker
exit non-zero on every run until that backlog is cleared, which is expected
and not this script's problem to fix. The workflow that calls this reports and
labels findings; it does not gate anything (see `.github/workflows/
content-audit.yml`'s header comment for why a required check would be the
wrong mechanism here).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
SUMMARY_MD = SRC_DIR / "SUMMARY.md"

# (label, argv, severity-when-nonzero). validate_page_metadata.py grades its
# own findings (error/warning/pre-existing) via `_parse_graded_lines`; the
# other three are pass/fail checks with no internal grading, so a nonzero exit
# is reported as a single P0 finding for that tool.
CHECKS = [
    ("repo-names", [sys.executable, str(SCRIPTS_DIR / "check_repo_names.py")], False),
    ("page-metadata", [sys.executable, str(SCRIPTS_DIR / "validate_page_metadata.py")], True),
    ("capability-ids", [sys.executable, str(SCRIPTS_DIR / "validate_capability_ids.py")], False),
    ("compatibility-drift", [sys.executable, str(SCRIPTS_DIR / "generate_compatibility.py"), "--check"], False),
]

_GRADED_LINE = re.compile(r"^(?P<path>[^:]+):(?P<line>\d+): (?P<severity>error|warning|pre-existing): (?P<msg>.*)$")


@dataclass
class Finding:
    tool: str
    severity: str  # "error" (P0) | "warning" (P1) | "pre-existing" (tracked, non-blocking)
    detail: str


@dataclass
class AuditResult:
    findings: list = field(default_factory=list)
    orphan_pages: list = field(default_factory=list)
    duplicate_claims: dict = field(default_factory=dict)  # capability_id -> [pages]
    tool_exit_codes: dict = field(default_factory=dict)

    @property
    def p0_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error") + len(self.orphan_pages) + len(
            [1 for pages in self.duplicate_claims.values() if len(pages) > 1]
        )

    @property
    def p1_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")

    @property
    def stale_evidence_count(self) -> int:
        # `validate_page_metadata.py` rule 11 (freshness) findings mention
        # "days" in the message; this is a substring match on its own wording,
        # not a second implementation of the threshold logic.
        return sum(1 for f in self.findings if f.severity in ("error", "warning") and "days" in f.detail)


def run_check(argv: list) -> tuple:
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def parse_graded_findings(tool: str, stdout: str) -> list:
    findings = []
    for line in stdout.splitlines():
        m = _GRADED_LINE.match(line)
        if m:
            findings.append(Finding(tool=tool, severity=m.group("severity"), detail=line))
    return findings


def find_orphan_pages() -> list:
    """Pages tracked under docs/src/*.md that SUMMARY.md never links to.

    A coarse reachability check: any relative `.md` link anywhere in
    SUMMARY.md counts a page as reachable, regardless of nesting depth. It
    does not follow links transitively through other pages -- SUMMARY.md is
    mdBook's own table of contents, so a page absent from it is, by
    definition, not in the book's navigation even if some other page happens
    to link to it in prose.
    """
    if not SUMMARY_MD.exists():
        return []
    summary_text = SUMMARY_MD.read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(([^)#]+\.md)\)", summary_text))
    linked_names = {Path(p).name for p in linked}
    linked_names.add("SUMMARY.md")

    orphans = []
    for md_file in sorted(SRC_DIR.rglob("*.md")):
        if md_file.name in linked_names:
            continue
        orphans.append(str(md_file.relative_to(REPO_ROOT)))
    return orphans


def find_duplicate_claims() -> dict:
    """Pages that declare the same `capability_ids` entry as each other.

    Reuses `validate_capability_ids.py`'s own `pages_with_capability_ids`
    extraction rather than a second metadata parser -- see that script for why
    a full YAML parse is not used here either.
    """
    from validate_capability_ids import pages_with_capability_ids  # local import: script dir is on sys.path

    claim_owners: dict = {}
    for page_path, cap_ids in pages_with_capability_ids(SRC_DIR):
        for cap_id in cap_ids:
            claim_owners.setdefault(cap_id, []).append(str(page_path.relative_to(REPO_ROOT)))
    return {cap_id: pages for cap_id, pages in claim_owners.items() if len(pages) > 1}


def run_audit() -> AuditResult:
    result = AuditResult()
    sys.path.insert(0, str(SCRIPTS_DIR))

    for label, argv, graded in CHECKS:
        code, stdout, _stderr = run_check(argv)
        result.tool_exit_codes[label] = code
        if graded:
            result.findings.extend(parse_graded_findings(label, stdout))
        elif code != 0:
            result.findings.append(Finding(tool=label, severity="error", detail=stdout.strip() or f"{label} exited {code}"))

    result.orphan_pages = find_orphan_pages()
    result.duplicate_claims = find_duplicate_claims()
    return result


def render_report(result: AuditResult, *, date: str, git_sha: str) -> str:
    lines = [
        f"# Content audit — {date}",
        "",
        f"Provenance: commit `{git_sha}`, generated by `scripts/content_audit.py` (AAASM-5603).",
        "",
        "## Metrics",
        "",
        f"- Unresolved P0 findings: {result.p0_count}",
        f"- Unresolved P1 findings: {result.p1_count}",
        f"- Stale-evidence findings: {result.stale_evidence_count}",
        f"- Orphan pages: {len(result.orphan_pages)}",
        f"- Duplicate canonical claims: {len([p for p in result.duplicate_claims.values() if len(p) > 1])}",
        "",
        "## Tool results",
        "",
    ]
    for label, code in result.tool_exit_codes.items():
        lines.append(f"- `{label}`: exit {code}")
    lines.append("")

    if result.findings:
        lines.append("## Findings")
        lines.append("")
        for f in result.findings:
            lines.append(f"- [{f.severity}] ({f.tool}) {f.detail}")
        lines.append("")

    if result.orphan_pages:
        lines.append("## Orphan pages (not reachable from SUMMARY.md)")
        lines.append("")
        for p in result.orphan_pages:
            lines.append(f"- {p}")
        lines.append("")

    if result.duplicate_claims:
        lines.append("## Duplicate canonical claims")
        lines.append("")
        for cap_id, pages in result.duplicate_claims.items():
            lines.append(f"- `{cap_id}`: {', '.join(pages)}")
        lines.append("")

    return "\n".join(lines)


def render_json(result: AuditResult, *, date: str, git_sha: str) -> str:
    payload = {
        "date": date,
        "git_sha": git_sha,
        "metrics": {
            "p0_count": result.p0_count,
            "p1_count": result.p1_count,
            "stale_evidence_count": result.stale_evidence_count,
            "orphan_page_count": len(result.orphan_pages),
            "duplicate_claim_count": len([p for p in result.duplicate_claims.values() if len(p) > 1]),
        },
        "tool_exit_codes": result.tool_exit_codes,
        "findings": [{"tool": f.tool, "severity": f.severity, "detail": f.detail} for f in result.findings],
        "orphan_pages": result.orphan_pages,
        "duplicate_claims": result.duplicate_claims,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list = None) -> int:
    import argparse
    import datetime

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None, help="override the report date (testing only)")
    parser.add_argument("--git-sha", default=None, help="override the reported commit sha (testing only)")
    args = parser.parse_args(argv)

    date = args.date or datetime.date.today().isoformat()
    # The date becomes a filename component below. Restricted to the ISO
    # calendar-date shape it's documented to be, rather than trusted as-is --
    # `--out-dir` used to be a second CLI-controlled path fragment here too;
    # dropped in favour of always writing under the fixed `audit-reports/`
    # directory, so this is the only place left that turns an argument into
    # part of a filesystem path.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise SystemExit(f"--date must be an ISO calendar date (YYYY-MM-DD), got {date!r}")

    git_sha = args.git_sha
    if git_sha is None:
        try:
            git_sha = subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT, check=True
            ).stdout.strip()
        except Exception:
            git_sha = "unknown"

    result = run_audit()

    out_dir = REPO_ROOT / "audit-reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{date}.md").write_text(render_report(result, date=date, git_sha=git_sha), encoding="utf-8")
    (out_dir / "latest.json").write_text(render_json(result, date=date, git_sha=git_sha), encoding="utf-8")

    print(f"content_audit: P0={result.p0_count} P1={result.p1_count} orphans={len(result.orphan_pages)} "
          f"duplicate_claims={len([p for p in result.duplicate_claims.values() if len(p) > 1])}")
    # Report-only: never fails the invoking workflow. See module docstring.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
