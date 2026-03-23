#!/usr/bin/env python3
"""Tests for compliance_checker.py — Guard Layer."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.compliance_checker import (
    CheckResult,
    ComplianceReport,
    check_artifact_exists,
    check_phase_dependencies,
    check_review_gate,
    check_status_md,
    run_full_check,
    run_phase_check,
    PHASE_ARTIFACTS,
    SPECS_DIR,
)


class TestCheckResult(unittest.TestCase):
    def test_passed_check(self):
        r = CheckResult("test", True, "OK")
        self.assertTrue(r.passed)

    def test_failed_check(self):
        r = CheckResult("test", False, "fail", severity="BLOCK")
        self.assertFalse(r.passed)
        self.assertEqual(r.severity, "BLOCK")


class TestComplianceReport(unittest.TestCase):
    def test_empty_report_passes(self):
        report = ComplianceReport("test-feature")
        self.assertTrue(report.passed)

    def test_all_passed(self):
        report = ComplianceReport("test-feature")
        report.add(CheckResult("a", True, "OK"))
        report.add(CheckResult("b", True, "OK"))
        self.assertTrue(report.passed)
        self.assertEqual(report.block_count, 0)

    def test_block_fails(self):
        report = ComplianceReport("test-feature")
        report.add(CheckResult("a", True, "OK"))
        report.add(CheckResult("b", False, "fail", "BLOCK"))
        self.assertFalse(report.passed)
        self.assertEqual(report.block_count, 1)

    def test_warn_fails(self):
        report = ComplianceReport("test-feature")
        report.add(CheckResult("a", False, "warn", "WARN"))
        self.assertFalse(report.passed)
        self.assertEqual(report.warn_count, 1)

    def test_to_dict(self):
        report = ComplianceReport("test-feature", phase=1)
        report.add(CheckResult("a", True, "OK"))
        d = report.to_dict()
        self.assertEqual(d["feature_id"], "test-feature")
        self.assertEqual(d["phase"], 1)
        self.assertTrue(d["passed"])


class TestArtifactChecks(unittest.TestCase):
    """Test with real temp dirs."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_missing_artifact(self):
        artifact = PHASE_ARTIFACTS[1]
        result = check_artifact_exists(self.tmpdir, artifact)
        self.assertFalse(result.passed)
        self.assertEqual(result.severity, "BLOCK")

    def test_existing_artifact(self):
        artifact = PHASE_ARTIFACTS[1]
        filepath = self.tmpdir / artifact["file"]
        # Write enough content with required sections
        filepath.write_text(
            "# Press Release\nThis is a great product.\n\n## User Stories\nAs a user, I want X.\n" * 5,
            encoding="utf-8",
        )
        result = check_artifact_exists(self.tmpdir, artifact)
        self.assertTrue(result.passed)

    def test_too_small_artifact(self):
        artifact = PHASE_ARTIFACTS[1]
        filepath = self.tmpdir / artifact["file"]
        filepath.write_text("tiny", encoding="utf-8")
        result = check_artifact_exists(self.tmpdir, artifact)
        self.assertFalse(result.passed)
        self.assertEqual(result.severity, "WARN")

    def test_missing_sections(self):
        artifact = PHASE_ARTIFACTS[1]
        filepath = self.tmpdir / artifact["file"]
        filepath.write_text("# Something Else\n" * 50, encoding="utf-8")
        result = check_artifact_exists(self.tmpdir, artifact)
        self.assertFalse(result.passed)
        self.assertIn("Missing sections", result.message)

    def test_status_md_present(self):
        (self.tmpdir / "STATUS.md").write_text("status: specced\n", encoding="utf-8")
        result = check_status_md(self.tmpdir)
        self.assertTrue(result.passed)

    def test_status_md_missing(self):
        result = check_status_md(self.tmpdir)
        self.assertFalse(result.passed)

    def test_status_md_no_status_field(self):
        (self.tmpdir / "STATUS.md").write_text("# Feature\nSome text\n", encoding="utf-8")
        result = check_status_md(self.tmpdir)
        self.assertFalse(result.passed)

    def test_phase_deps_phase2(self):
        # Phase 2 requires phase 1 artifact
        results = check_phase_dependencies(self.tmpdir, 2)
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].passed)

        # Create phase 1 artifact
        (self.tmpdir / "brainstorm.md").write_text("content", encoding="utf-8")
        results = check_phase_dependencies(self.tmpdir, 2)
        self.assertTrue(results[0].passed)

    def test_review_gate_no_indicators(self):
        result = check_review_gate(self.tmpdir)
        self.assertFalse(result.passed)

    def test_review_gate_with_report(self):
        (self.tmpdir / "review-report.md").write_text("Review passed", encoding="utf-8")
        result = check_review_gate(self.tmpdir)
        self.assertTrue(result.passed)

    def test_review_gate_via_status(self):
        (self.tmpdir / "STATUS.md").write_text("status: review passed\n", encoding="utf-8")
        result = check_review_gate(self.tmpdir)
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
