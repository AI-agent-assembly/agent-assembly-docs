"""Tests for `content_audit.py` (AAASM-5603)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_audit as ca  # noqa: E402


class ParseGradedFindingsTest(unittest.TestCase):
    def test_parses_error_and_warning_and_pre_existing(self) -> None:
        stdout = (
            "some preamble\n"
            "docs/src/a.md:3: error: rule 13: bad\n"
            "docs/src/b.md:5: warning: rule 11: stale, evidence is 200 days old\n"
            "docs/src/c.md:7: pre-existing: rule 13: bad, tracked on AAASM-5610\n"
            "validate_page_metadata: 3 page(s) checked\n"
        )
        findings = ca.parse_graded_findings("page-metadata", stdout)
        self.assertEqual(len(findings), 3)
        self.assertEqual([f.severity for f in findings], ["error", "warning", "pre-existing"])

    def test_no_graded_lines_returns_empty(self) -> None:
        self.assertEqual(ca.parse_graded_findings("page-metadata", "all clean\n"), [])


class AuditResultMetricsTest(unittest.TestCase):
    def test_p0_counts_errors_orphans_and_duplicate_claims(self) -> None:
        result = ca.AuditResult(
            findings=[
                ca.Finding("page-metadata", "error", "e1"),
                ca.Finding("page-metadata", "warning", "w1"),
                ca.Finding("page-metadata", "pre-existing", "p1"),
            ],
            orphan_pages=["docs/src/orphan.md"],
            duplicate_claims={"S1": ["docs/src/a.md", "docs/src/b.md"]},
        )
        self.assertEqual(result.p0_count, 1 + 1 + 1)  # 1 error + 1 orphan + 1 dup group
        self.assertEqual(result.p1_count, 1)

    def test_stale_evidence_count_matches_days_substring(self) -> None:
        result = ca.AuditResult(
            findings=[
                ca.Finding("page-metadata", "warning", "docs/src/a.md:1: warning: evidence is 200 days old"),
                ca.Finding("page-metadata", "error", "docs/src/b.md:2: error: rule 13: unbounded verb"),
            ]
        )
        self.assertEqual(result.stale_evidence_count, 1)


class OrphanPageTest(unittest.TestCase):
    def test_page_not_linked_from_summary_is_an_orphan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "src"
            src.mkdir()
            (src / "SUMMARY.md").write_text("# Summary\n\n- [Linked](linked.md)\n", encoding="utf-8")
            (src / "linked.md").write_text("# Linked\n", encoding="utf-8")
            (src / "orphan.md").write_text("# Orphan\n", encoding="utf-8")

            old_root, old_src, old_summary = ca.REPO_ROOT, ca.SRC_DIR, ca.SUMMARY_MD
            try:
                ca.REPO_ROOT, ca.SRC_DIR, ca.SUMMARY_MD = root, src, src / "SUMMARY.md"
                orphans = ca.find_orphan_pages()
            finally:
                ca.REPO_ROOT, ca.SRC_DIR, ca.SUMMARY_MD = old_root, old_src, old_summary

        self.assertEqual([Path(o).name for o in orphans], ["orphan.md"])


class RenderReportTest(unittest.TestCase):
    def test_render_report_includes_metrics_and_provenance(self) -> None:
        result = ca.AuditResult(findings=[ca.Finding("repo-names", "error", "bad name found")])
        report = ca.render_report(result, date="2026-08-20", git_sha="deadbeef")
        self.assertIn("2026-08-20", report)
        self.assertIn("deadbeef", report)
        self.assertIn("Unresolved P0 findings: 1", report)

    def test_render_json_is_valid_json_with_metrics(self) -> None:
        import json

        result = ca.AuditResult(findings=[ca.Finding("repo-names", "error", "bad name found")])
        payload = json.loads(ca.render_json(result, date="2026-08-20", git_sha="deadbeef"))
        self.assertEqual(payload["metrics"]["p0_count"], 1)
        self.assertEqual(payload["date"], "2026-08-20")


if __name__ == "__main__":
    unittest.main()
