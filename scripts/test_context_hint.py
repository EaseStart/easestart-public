#!/usr/bin/env python3
"""Tests for context_hint.py — Hint Layer."""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts import context_hint


class TestParseDate(unittest.TestCase):
    def test_iso_format(self):
        d = context_hint.parse_date("2026-03-18")
        self.assertEqual(d.year, 2026)
        self.assertEqual(d.month, 3)
        self.assertEqual(d.day, 18)

    def test_invalid_format(self):
        d = context_hint.parse_date("not a date")
        self.assertIsNone(d)


class TestSessionHints(unittest.TestCase):
    def test_empty_hints(self):
        hints = context_hint.SessionHints()
        md = hints.to_markdown()
        self.assertIn("all clear", md)

    def test_add_hint(self):
        hints = context_hint.SessionHints()
        hints.add("Test", "🔴", "Something important", priority=1)
        md = hints.to_markdown()
        self.assertIn("Something important", md)
        self.assertIn("Test", md)

    def test_priority_sorting(self):
        hints = context_hint.SessionHints()
        hints.add("Low", "📌", "Low priority", priority=10)
        hints.add("High", "🔴", "High priority", priority=1)
        result = hints.to_dict()
        self.assertEqual(result[0]["category"], "High")
        self.assertEqual(result[1]["category"], "Low")


class TestGenerateHints(unittest.TestCase):
    """Test hint generation with mocked state files."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.pm_dir = self.tmpdir / "pm"
        self.pm_dir.mkdir()
        self.specs_dir = self.tmpdir / "plans" / "specs"
        self.specs_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    @patch.object(context_hint, "STATE_FILE")
    @patch.object(context_hint, "TASKBOARD_FILE")
    @patch.object(context_hint, "STATE_JSON_FILE")
    @patch.object(context_hint, "BROADCAST_FILE")
    @patch.object(context_hint, "SPECS_DIR")
    def test_missing_state(self, mock_specs, mock_broadcast, mock_agent, mock_tb, mock_state):
        mock_state.__class__ = Path
        mock_state.exists = lambda: False
        mock_tb.__class__ = Path
        mock_tb.exists = lambda: False
        mock_agent.__class__ = Path
        mock_agent.exists = lambda: False
        mock_broadcast.__class__ = Path
        mock_broadcast.exists = lambda: False
        mock_specs.__class__ = Path
        mock_specs.exists = lambda: False

        # Use a non-existent path
        nonexistent = self.tmpdir / "nonexistent" / "STATE.md"
        with patch.object(context_hint, "STATE_FILE", nonexistent):
            with patch.object(context_hint, "TASKBOARD_FILE", self.tmpdir / "nonexistent" / "tb.json"):
                with patch.object(context_hint, "STATE_JSON_FILE", self.tmpdir / "nonexistent" / "s.json"):
                    with patch.object(context_hint, "BROADCAST_FILE", self.tmpdir / "nonexistent" / "b.md"):
                        with patch.object(context_hint, "SPECS_DIR", self.tmpdir / "nonexistent" / "specs"):
                            hints = context_hint.generate_hints()
                            md = hints.to_markdown()
                            self.assertIn("STATE.md not found", md)

    def test_stale_state_generates_warning(self):
        # Create a STATE.md with old date
        state_file = self.pm_dir / "STATE.md"
        old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        state_file.write_text(
            f"**Project:** Test\n**Stage:** 2\n**Current Focus:** Testing\n"
            f"**Active Blockers:** None\n**Last Update:** {old_date}\n"
        )

        with patch.object(context_hint, "STATE_FILE", state_file):
            with patch.object(context_hint, "TASKBOARD_FILE", self.tmpdir / "nonexistent.json"):
                with patch.object(context_hint, "STATE_JSON_FILE", self.tmpdir / "nonexistent2.json"):
                    with patch.object(context_hint, "BROADCAST_FILE", self.tmpdir / "nonexistent3.md"):
                        with patch.object(context_hint, "SPECS_DIR", self.specs_dir):
                            hints = context_hint.generate_hints()
                            md = hints.to_markdown()
                            self.assertIn("days old", md)

    def test_active_sprint_hint(self):
        # Create STATE.md
        state_file = self.pm_dir / "STATE.md"
        today = datetime.now().strftime("%Y-%m-%d")
        state_file.write_text(
            f"**Project:** Test\n**Stage:** 3\n**Current Focus:** MVP\n"
            f"**Active Blockers:** None\n**Last Update:** {today}\n"
        )

        # Create taskboard with active sprint
        tb_file = self.pm_dir / "taskboard.json"
        tb_file.write_text(json.dumps({
            "active_sprint": "sprint-build",
            "tasks": [
                {"status": "complete"},
                {"status": "in_progress"},
                {"status": "blocked"},
            ],
        }))

        with patch.object(context_hint, "STATE_FILE", state_file):
            with patch.object(context_hint, "TASKBOARD_FILE", tb_file):
                with patch.object(context_hint, "STATE_JSON_FILE", self.tmpdir / "nonexistent.json"):
                    with patch.object(context_hint, "BROADCAST_FILE", self.tmpdir / "nonexistent.md"):
                        with patch.object(context_hint, "SPECS_DIR", self.specs_dir):
                            hints = context_hint.generate_hints()
                            md = hints.to_markdown()
                            self.assertIn("sprint-build", md)
                            self.assertIn("1/3", md)

    def test_stage_guard_early_stage(self):
        state_file = self.pm_dir / "STATE.md"
        today = datetime.now().strftime("%Y-%m-%d")
        state_file.write_text(
            f"**Project:** Test\n**Stage:** 1\n**Current Focus:** Ideation\n"
            f"**Active Blockers:** None\n**Last Update:** {today}\n"
        )

        with patch.object(context_hint, "STATE_FILE", state_file):
            with patch.object(context_hint, "TASKBOARD_FILE", self.tmpdir / "x.json"):
                with patch.object(context_hint, "STATE_JSON_FILE", self.tmpdir / "y.json"):
                    with patch.object(context_hint, "BROADCAST_FILE", self.tmpdir / "z.md"):
                        with patch.object(context_hint, "SPECS_DIR", self.specs_dir):
                            hints = context_hint.generate_hints()
                            md = hints.to_markdown()
                            self.assertIn("BLOCKED", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
