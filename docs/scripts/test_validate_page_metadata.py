"""Tests for `validate_page_metadata.py` (AAASM-5601).

One positive and one negative case per rule where practical, plus the parsing
contract's own trickiest cases (delimiter exemptions, quote-pairing, the "--"
ban) and the freshness thresholds. Stdlib `unittest` only, matching this
repo's convention (`test_check_repo_names.py`). Run with:
`python3 docs/scripts/test_validate_page_metadata.py`.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_page_metadata as vpm  # noqa: E402


def _wrap(body: str) -> str:
    return f"<!-- BEGIN AA-PAGE-META\n{body}\nEND AA-PAGE-META -->\n\n# Title\n\nBody text.\n"


BASE_FIELDS = (
    "schema_version: 1\n"
    "page_type: reference\n"
    "audience: [contributor]\n"
    "user_job: Do a thing that is between ten and one twenty chars long\n"
    "owner: L2:docs\n"
    "canonical_source: self\n"
    "describes_capability: false\n"
    "disclosure_levels: [3, 4]"
)


class ParsingContractTest(unittest.TestCase):
    def test_finds_single_block(self) -> None:
        body, b, e = vpm.find_meta_block(_wrap(BASE_FIELDS))
        self.assertIn("schema_version: 1", body)
        self.assertEqual(b, 0)

    def test_zero_blocks_raises(self) -> None:
        with self.assertRaises(vpm.MetaError):
            vpm.find_meta_block("# Title\n\nNo block here.\n")

    def test_two_begins_is_an_error(self) -> None:
        text = _wrap(BASE_FIELDS).replace(
            "END AA-PAGE-META -->", "END AA-PAGE-META -->\n<!-- BEGIN AA-PAGE-META\nEND AA-PAGE-META -->"
        )
        with self.assertRaises(vpm.MetaError):
            vpm.find_meta_block(text)

    def test_block_not_first_construct_is_an_error(self) -> None:
        text = "Some text first.\n\n" + _wrap(BASE_FIELDS)
        with self.assertRaises(vpm.MetaError):
            vpm.find_meta_block(text)

    def test_delimiter_inside_fence_does_not_open_a_block(self) -> None:
        # The fenced mention comes AFTER the real block: a genuine block must
        # be the first construct, so a fenced false-BEGIN before it would fail
        # for that reason regardless of the exemption -- this isolates the
        # exemption itself.
        text = _wrap(BASE_FIELDS) + "\n```\n<!-- BEGIN AA-PAGE-META\n```\n"
        body, b, e = vpm.find_meta_block(text)
        self.assertIn("schema_version: 1", body)

    def test_delimiter_inside_inline_code_does_not_open_a_block(self) -> None:
        # The real block is still the only one found even though the literal
        # BEGIN string also appears inside a code span before it -- but a
        # block must be the FIRST construct, so put the inline mention after.
        text = _wrap(BASE_FIELDS) + "\nSee `<!-- BEGIN AA-PAGE-META` for the syntax.\n"
        body, b, e = vpm.find_meta_block(text)
        self.assertIn("schema_version: 1", body)

    def test_double_hyphen_in_body_is_an_error(self) -> None:
        text = _wrap(BASE_FIELDS + "\nuser_job: A job -- with a double hyphen in it")
        with self.assertRaises(vpm.MetaError):
            vpm.find_meta_block(text)

    def test_duplicate_key_is_an_error(self) -> None:
        with self.assertRaises(vpm.MetaError):
            vpm.parse_body(BASE_FIELDS + "\nschema_version: 1")

    def test_unknown_key_is_an_error(self) -> None:
        lexed = vpm.parse_body(BASE_FIELDS + "\nfrobnicate: true")
        diags = vpm.validate_page("t.md", lexed, "v0.0.1-rc.6", "2026-08-20")
        self.assertTrue(any("unknown metadata key" in d.message for d in diags))


class FieldReferenceTest(unittest.TestCase):
    def _diags(self, body: str) -> list[vpm.Diagnostic]:
        lexed = vpm.parse_body(body)
        return vpm.validate_page("t.md", lexed, "v0.0.1-rc.6", "2026-08-20")

    def test_clean_minimal_page_has_no_errors(self) -> None:
        self.assertEqual(self._diags(BASE_FIELDS), [])

    def test_bad_page_type_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("page_type: reference", "page_type: bogus"))
        self.assertTrue(any("page_type" in d.message for d in diags))

    def test_empty_audience_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("audience: [contributor]", "audience: []"))
        self.assertTrue(any("audience must be non-empty" in d.message for d in diags))

    def test_user_job_too_short_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace(
            "user_job: Do a thing that is between ten and one twenty chars long",
            "user_job: Too short",
        ))
        self.assertTrue(any("user_job must be 10-120" in d.message for d in diags))

    def test_user_job_trailing_period_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace(
            "user_job: Do a thing that is between ten and one twenty chars long",
            "user_job: Do a thing that ends with a period.",
        ))
        self.assertTrue(any("must not end with a period" in d.message for d in diags))

    def test_bad_owner_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("owner: L2:docs", "owner: L9:nowhere"))
        self.assertTrue(any("owner" in d.message for d in diags))

    def test_disclosure_levels_out_of_order_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("disclosure_levels: [3, 4]", "disclosure_levels: [4, 3]"))
        self.assertTrue(any("ascending" in d.message for d in diags))

    def test_disclosure_levels_duplicate_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("disclosure_levels: [3, 4]", "disclosure_levels: [3, 3]"))
        self.assertTrue(any("ascending" in d.message for d in diags))


class CrossFieldRuleTest(unittest.TestCase):
    def _diags(self, body: str) -> list[vpm.Diagnostic]:
        lexed = vpm.parse_body(body)
        return vpm.validate_page("t.md", lexed, "v0.0.1-rc.6", "2026-08-20")

    CAPABILITY_PAGE = (
        "schema_version: 1\n"
        "page_type: guide\n"
        "audience: [evaluator]\n"
        "user_job: Find out whether this capability is available to me today\n"
        "owner: L3:agent-assembly\n"
        "canonical_source: https://docs.agent-assembly.com/core/\n"
        "describes_capability: true\n"
        "area: core\n"
        "availability: available-with-limits\n"
        "limitations: \"#limits\"\n"
        "platforms:\n"
        "  - channel: github-release\n"
        "    platform: linux-x86_64\n"
        "    status: available-verified\n"
        "    evidence: some evidence string\n"
        "last_verified:\n"
        "  version: v0.0.1-rc.6\n"
        "  ref: v0.0.1-rc.6\n"
        "  date: 2026-08-13\n"
        "  method: read the manifest by hand\n"
        "claims:\n"
        "  - term: Evaluated\n"
        "    evidence: some evidence link\n"
        "disclosure_levels: [1, 3]\n"
        "deeper: https://docs.agent-assembly.com/core/"
    )

    def test_rule1_capability_page_clean(self) -> None:
        self.assertEqual(self._diags(self.CAPABILITY_PAGE), [])

    def test_rule1_missing_area_on_capability_page_is_an_error(self) -> None:
        body = self.CAPABILITY_PAGE.replace("area: core\n", "")
        diags = self._diags(body)
        self.assertTrue(any("requires 'area'" in d.message for d in diags))

    def test_rule2_non_capability_page_with_area_is_an_error(self) -> None:
        diags = self._diags(BASE_FIELDS + "\narea: core")
        self.assertTrue(any("describes_capability: false requires 'area' absent" in d.message for d in diags))

    def test_rule3_available_with_limits_needs_limitations(self) -> None:
        body = self.CAPABILITY_PAGE.replace('limitations: "#limits"\n', "")
        diags = self._diags(body)
        self.assertTrue(any("requires non-empty 'limitations'" in d.message for d in diags))

    def test_rule4_self_planned_forces_empty_platforms(self) -> None:
        body = self.CAPABILITY_PAGE.replace(
            "claims:\n  - term: Evaluated\n    evidence: some evidence link\n",
            "claims:\n  - term: Planned\n    evidence: AAASM-9999\n",
        )
        diags = self._diags(body)
        self.assertTrue(any("platforms: []" in d.message for d in diags))
        self.assertTrue(any("'availability' absent" in d.message for d in diags))

    def test_rule4_foreign_subject_planned_does_not_fire(self) -> None:
        # The worked control from page-standards.md's own rule-4 section.
        body = self.CAPABILITY_PAGE.replace(
            "claims:\n  - term: Evaluated\n    evidence: some evidence link\n",
            "claims:\n"
            "  - term: Evaluated\n"
            "    evidence: some evidence link\n"
            "  - term: Planned\n"
            "    evidence: AAASM-9999\n"
            "    subject: L3:python-sdk\n",
        )
        diags = self._diags(body)
        self.assertEqual([d for d in diags if "rule 4" in d.message.lower() or "platforms" in d.message], [])

    def test_rule5_available_verified_forbids_limited_platform_row(self) -> None:
        body = self.CAPABILITY_PAGE.replace("availability: available-with-limits", "availability: available-verified")
        body = body.replace("status: available-verified", "status: available-with-limits")
        diags = self._diags(body)
        self.assertTrue(any("forbids an available-with-limits" in d.message for d in diags))

    def test_rule6_capability_page_without_availability_is_an_error(self) -> None:
        body = self.CAPABILITY_PAGE.replace("availability: available-with-limits\n", "")
        diags = self._diags(body)
        self.assertTrue(any("requires 'availability'" in d.message for d in diags))

    def test_rule7_platform_status_cannot_be_preview(self) -> None:
        body = self.CAPABILITY_PAGE.replace("status: available-verified", "status: preview")
        diags = self._diags(body)
        self.assertTrue(any("rule 7" in d.message for d in diags))

    def test_rule8_claim_term_must_be_a_section6_term(self) -> None:
        body = self.CAPABILITY_PAGE.replace("term: Evaluated", "term: Bogus")
        diags = self._diags(body)
        self.assertTrue(any("rule 8" in d.message for d in diags))

    def test_rule9_canonical_source_self_requires_l2_docs_owner(self) -> None:
        body = BASE_FIELDS.replace("owner: L2:docs", "owner: L3:agent-assembly")
        diags = self._diags(body)
        self.assertTrue(any("canonical_source: self requires owner" in d.message for d in diags))

    def test_rule10_branch_name_blob_url_is_rejected(self) -> None:
        body = self.CAPABILITY_PAGE.replace(
            "canonical_source: https://docs.agent-assembly.com/core/",
            "canonical_source: https://github.com/ai-agent-assembly/agent-assembly/blob/main/governance/README.md",
        )
        diags = self._diags(body)
        self.assertTrue(any("branch name" in d.message for d in diags))

    def test_rule11_max_level_below_4_requires_deeper(self) -> None:
        diags = self._diags(BASE_FIELDS)  # disclosure_levels: [3, 4] already has 4
        self.assertEqual([d for d in diags if "requires 'deeper'" in d.message], [])
        diags2 = self._diags(BASE_FIELDS.replace("disclosure_levels: [3, 4]", "disclosure_levels: [3]"))
        self.assertTrue(any("requires 'deeper'" in d.message for d in diags2))

    def test_rule12_reference_page_must_carry_3_and_4(self) -> None:
        diags = self._diags(BASE_FIELDS.replace("disclosure_levels: [3, 4]", "disclosure_levels: [1, 3]"))
        self.assertTrue(any("must carry levels" in d.message for d in diags))

    def test_rule14_bounded_claim_term_requires_limitations(self) -> None:
        body = self.CAPABILITY_PAGE.replace('limitations: "#limits"\n', "")
        diags = self._diags(body)
        self.assertTrue(any("rule-14" in d.message for d in diags))

    def test_rule15_product_page_forbids_level_4(self) -> None:
        body = BASE_FIELDS.replace("page_type: reference", "page_type: product")
        body = body.replace("disclosure_levels: [3, 4]", "disclosure_levels: [1, 2, 3, 4]")
        diags = self._diags(body)
        self.assertTrue(any("may never carry disclosure level 4" in d.message for d in diags))


class Rule13Test(unittest.TestCase):
    def test_bare_verb_is_a_hit(self) -> None:
        hits = vpm.find_rule13_hits("Agent Assembly enforces the policy.\n")
        self.assertEqual([v for v, _ in hits], ["enforces"])

    def test_verb_in_fenced_code_is_exempt(self) -> None:
        hits = vpm.find_rule13_hits("```\nAgent Assembly enforces the policy.\n```\n")
        self.assertEqual(hits, [])

    def test_verb_in_inline_code_is_exempt(self) -> None:
        hits = vpm.find_rule13_hits("See `enforces` in the glossary.\n")
        self.assertEqual(hits, [])

    def test_verb_in_straight_quotes_is_exempt(self) -> None:
        hits = vpm.find_rule13_hits('The banned phrase is "it enforces everything".\n')
        self.assertEqual(hits, [])

    def test_verb_in_typographic_quotes_is_exempt(self) -> None:
        hits = vpm.find_rule13_hits("The banned phrase is “it enforces everything”.\n")
        self.assertEqual(hits, [])

    def test_common_noun_blocks_is_not_matched(self) -> None:
        # Rule 13's verb list is deliberately narrow; "blocks" (the noun, as in
        # code blocks) is not one of the five and must never fire.
        hits = vpm.find_rule13_hits("See the fenced code blocks below.\n")
        self.assertEqual(hits, [])

    def test_odd_quote_count_is_an_error(self) -> None:
        with self.assertRaises(vpm.MetaError):
            vpm.find_rule13_hits('One quote: " and no closing pair.\n')

    def test_wrapped_quotation_spans_two_lines(self) -> None:
        hits = vpm.find_rule13_hits('"it enforces\neverything"\n')
        self.assertEqual(hits, [])


class FreshnessTest(unittest.TestCase):
    def _last_verified_diags(self, date: str, ref: str = "v0.0.1-rc.6", version: str = "v0.0.1-rc.6") -> list[vpm.Diagnostic]:
        body = CrossFieldRuleTest.CAPABILITY_PAGE
        body = body.replace("ref: v0.0.1-rc.6", f"ref: {ref}")
        body = body.replace("version: v0.0.1-rc.6", f"version: {version}")
        body = body.replace("date: 2026-08-13", f"date: {date}")
        lexed = vpm.parse_body(body)
        return vpm.validate_page("t.md", lexed, "v0.0.1-rc.6", "2026-08-20")

    def test_fresh_date_is_clean(self) -> None:
        diags = self._last_verified_diags("2026-08-13")
        self.assertEqual([d for d in diags if "stale" in d.message or "days old" in d.message], [])

    def test_91_days_is_a_warning(self) -> None:
        diags = self._last_verified_diags("2026-05-21")  # 91 days before 2026-08-20
        warn = [d for d in diags if d.severity == "warning" and "days old" in d.message]
        self.assertTrue(warn)

    def test_181_days_is_an_error(self) -> None:
        diags = self._last_verified_diags("2026-02-20")  # 181 days before 2026-08-20
        err = [d for d in diags if d.severity == "error" and "stale" in d.message]
        self.assertTrue(err)

    def test_future_date_is_an_error(self) -> None:
        diags = self._last_verified_diags("2026-12-25")
        self.assertTrue(any("in the future" in d.message for d in diags))

    def test_branch_name_ref_is_an_error(self) -> None:
        diags = self._last_verified_diags("2026-08-13", ref="main")
        self.assertTrue(any("branch name" in d.message for d in diags))

    def test_version_mismatch_is_a_warning(self) -> None:
        diags = self._last_verified_diags("2026-08-13", version="v0.0.1-rc.1")
        self.assertTrue(any(d.severity == "warning" and "differs from current release" in d.message for d in diags))


if __name__ == "__main__":
    unittest.main()
