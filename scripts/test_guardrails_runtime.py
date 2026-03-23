#!/usr/bin/env python3
"""Tests for guardrails_runtime.py — Guard Layer."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.guardrails_runtime import (
    detect_query_domains,
    evaluate_guardrails,
    format_violations,
    parse_state_md,
)


class TestDomainDetection(unittest.TestCase):
    def test_growth_keywords(self):
        domains = detect_query_domains("growth hacking strategy")
        self.assertIn("growth", domains)

    def test_fundraising_keywords(self):
        domains = detect_query_domains("how to raise a seed round from VC")
        self.assertIn("fundraising", domains)

    def test_hiring_keywords(self):
        domains = detect_query_domains("hire a full-time developer")
        self.assertIn("hiring", domains)

    def test_equity_keywords(self):
        domains = detect_query_domains("co-founder equity split vesting")
        self.assertIn("equity", domains)

    def test_no_match(self):
        domains = detect_query_domains("explain what a lean canvas is")
        self.assertEqual(len(domains), 0)

    def test_multiple_domains(self):
        domains = detect_query_domains("hire someone to grow our marketing channels")
        self.assertIn("hiring", domains)
        self.assertIn("growth", domains)


class TestParseStateMd(unittest.TestCase):
    def test_parse_real_format(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# STATE.md — Test\n\n")
            f.write("**Project:** TestProject\n")
            f.write("**Stage:** 2 — Validation\n")
            f.write("**Current Focus:** Testing\n")
            f.write("**Last Update:** 2026-03-18\n")
            f.name

        state = parse_state_md(Path(f.name))
        self.assertEqual(state["stage"], 2)
        self.assertEqual(state["project"], "TestProject")
        Path(f.name).unlink()

    def test_missing_file(self):
        state = parse_state_md(Path("/nonexistent/path.md"))
        self.assertEqual(state["stage"], 0)


class TestGuardrailEvaluation(unittest.TestCase):
    def test_growth_blocked_at_stage_1(self):
        violations = evaluate_guardrails(
            query="growth hacking tactics",
            stage_override=1,
        )
        block_violations = [v for v in violations if v["type"] == "BLOCK"]
        self.assertGreater(len(block_violations), 0, "Should block growth at stage 1")

    def test_growth_allowed_at_stage_4(self):
        violations = evaluate_guardrails(
            query="growth hacking tactics",
            stage_override=4,
        )
        # At stage 4, growth BLOCK rules (which check stage < 2) should not fire
        block_violations = [
            v for v in violations
            if v["type"] == "BLOCK" and v["domain"] == "growth"
        ]
        self.assertEqual(len(block_violations), 0, "Growth should not be blocked at stage 4")

    def test_fundraising_blocked_early(self):
        violations = evaluate_guardrails(
            query="raise money from investors VC",
            stage_override=2,
        )
        block_ids = [v["id"] for v in violations if v["type"] == "BLOCK"]
        self.assertIn("G-003", block_ids, "G-003 should block fundraising at stage 2")

    def test_hiring_blocked_early(self):
        violations = evaluate_guardrails(
            query="hire a full-time developer",
            stage_override=3,
        )
        block_ids = [v["id"] for v in violations if v["type"] == "BLOCK"]
        self.assertIn("G-004", block_ids, "G-004 should block hiring at stage 3")

    def test_no_violations_for_neutral_query(self):
        violations = evaluate_guardrails(
            query="explain what a lean canvas is",
            stage_override=1,
        )
        self.assertEqual(len(violations), 0, "Neutral query should have no violations")

    def test_equity_domain_detected(self):
        """G-010 uses intent-level condition (equity_agreement AND NOT vesting_clause) 
        that can't be evaluated from query text alone. Verify domain is at least detected."""
        domains = detect_query_domains("split equity with co-founder")
        self.assertIn("equity", domains, "Should detect equity domain")

    def test_paid_ads_blocked_before_stage_5(self):
        violations = evaluate_guardrails(
            query="run paid ads campaign on facebook",
            stage_override=3,
        )
        block_ids = [v["id"] for v in violations if v["type"] == "BLOCK"]
        self.assertIn("G-002", block_ids, "G-002 should block paid ads before stage 5")


class TestFormatViolations(unittest.TestCase):
    def test_no_violations(self):
        output = format_violations([])
        self.assertIn("No guardrail violations", output)

    def test_block_display(self):
        violations = [{"type": "BLOCK", "message": "❌ Test block", "rationale": "Bad"}]
        output = format_violations(violations)
        self.assertIn("BLOCKED", output)
        self.assertIn("Test block", output)

    def test_warn_display(self):
        violations = [{"type": "WARN", "message": "⚠️ Test warn", "rationale": "Caution"}]
        output = format_violations(violations)
        self.assertIn("WARNINGS", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
