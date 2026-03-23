#!/usr/bin/env python3
"""Tests for telemetry.py — Track Layer."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts import telemetry


class TestLogEvent(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.telemetry_file = self.tmpdir / "telemetry.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_log_creates_file(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="feature-dev", agent="mvp-agent")
        self.assertTrue(self.telemetry_file.exists())

    def test_log_appends(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="feature-dev")
            telemetry.log_event("gate_pass", workflow="feature-dev", details="Phase 1")

        lines = self.telemetry_file.read_text().strip().split("\n")
        self.assertEqual(len(lines), 2)

    def test_log_event_structure(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            event = telemetry.log_event(
                "gate_fail",
                workflow="review-gate",
                agent="orchestrator",
                details="Score 5/10",
            )

        self.assertEqual(event["type"], "gate_fail")
        self.assertEqual(event["workflow"], "review-gate")
        self.assertIn("timestamp", event)

    def test_log_with_metadata(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            event = telemetry.log_event(
                "compliance_check",
                metadata={"feature_id": "test-feat", "passed": True},
            )

        self.assertIn("metadata", event)
        self.assertEqual(event["metadata"]["feature_id"], "test-feat")


class TestReadEvents(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.telemetry_file = self.tmpdir / "telemetry.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_read_empty(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            events = telemetry.read_events()
        self.assertEqual(len(events), 0)

    def test_read_logged_events(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="a")
            telemetry.log_event("gate_pass", workflow="a")
            telemetry.log_event("workflow_complete", workflow="a")
            events = telemetry.read_events()

        self.assertEqual(len(events), 3)

    def test_read_with_day_filter(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="today")
            events = telemetry.read_events(last_days=1)

        self.assertEqual(len(events), 1)


class TestGenerateReport(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.telemetry_file = self.tmpdir / "telemetry.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_empty_report(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            report = telemetry.generate_report()
        self.assertEqual(report["total_events"], 0)

    def test_healthy_report(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            # Log some events simulating a healthy workflow
            for _ in range(3):
                telemetry.log_event("workflow_start", workflow="feature-dev", agent="mvp-agent")
                telemetry.log_event("gate_pass", workflow="feature-dev")
                telemetry.log_event("gate_pass", workflow="feature-dev")
                telemetry.log_event("workflow_complete", workflow="feature-dev")

            report = telemetry.generate_report()

        self.assertEqual(report["workflows_started"], 3)
        self.assertEqual(report["workflows_completed"], 3)
        self.assertEqual(report["completion_rate"], "100%")
        self.assertEqual(report["gate_passes"], 6)
        self.assertEqual(report["gate_fails"], 0)
        self.assertEqual(report["compliance_rate"], "100%")
        self.assertIn("HEALTHY", report["health"])

    def test_unhealthy_report(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="a")
            telemetry.log_event("gate_fail", workflow="a")
            telemetry.log_event("gate_fail", workflow="a")
            telemetry.log_event("gate_pass", workflow="a")
            telemetry.log_event("audit_skip", workflow="a")

            report = telemetry.generate_report()

        self.assertEqual(report["compliance_rate"], "33%")
        self.assertIn("CRITICAL", report["health"])
        self.assertEqual(report["audit_skips"], 1)

    def test_format_report(self):
        with patch.object(telemetry, "TELEMETRY_FILE", self.telemetry_file):
            telemetry.log_event("workflow_start", workflow="test")
            telemetry.log_event("gate_pass", workflow="test")
            report = telemetry.generate_report()

        output = telemetry.format_report(report)
        self.assertIn("Compliance Report", output)
        self.assertIn("Gate Compliance", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
