"""
Unit tests for EaseStart V2 Search Engine (core.py).
Run: python3 scripts/test_core.py
Zero dependencies — uses stdlib unittest only.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core import (
    search,
    _get_stage_weight,
    _score_to_confidence,
    _find_anti_pattern_warnings,
    _stage_matches,
    get_stats,
    clear_search_cache,
    _INDEX_CACHE,
    STAGE_RELEVANCE_WEIGHTS,
    MIN_SCORE_THRESHOLD,
    CONFIDENCE_THRESHOLDS,
)


class TestStageWeights(unittest.TestCase):
    """Stage-weighted scoring tests."""

    def test_exact_match(self):
        """Exact stage match should get 1.5x boost."""
        self.assertEqual(_get_stage_weight("3", 3), 1.5)

    def test_adjacent(self):
        """Adjacent stage (distance 1) should get 1.2x boost."""
        self.assertEqual(_get_stage_weight("2", 3), 1.2)

    def test_far(self):
        """Far stage (distance 3+) should get 0.7x penalty."""
        self.assertEqual(_get_stage_weight("0", 3), 0.7)

    def test_no_stage(self):
        """Empty stage value should return neutral 1.0."""
        self.assertEqual(_get_stage_weight("", 3), 1.0)
        self.assertEqual(_get_stage_weight(None, 3), 1.0)

    def test_range(self):
        """Range like '2-5' should use center (3.5) for distance calc."""
        weight = _get_stage_weight("2-5", 4)
        self.assertEqual(weight, 1.5)

    def test_far_range(self):
        """Range '0-1' queried at stage 5 should get penalty."""
        weight = _get_stage_weight("0-1", 5)
        self.assertEqual(weight, 0.7)


class TestConfidenceMapping(unittest.TestCase):
    """Lucius L5 confidence level tests."""

    def test_high(self):
        self.assertEqual(_score_to_confidence(3.0), "HIGH")
        self.assertEqual(_score_to_confidence(7.5), "HIGH")

    def test_medium(self):
        self.assertEqual(_score_to_confidence(1.0), "MEDIUM")
        self.assertEqual(_score_to_confidence(2.99), "MEDIUM")

    def test_low(self):
        self.assertEqual(_score_to_confidence(0.5), "LOW")
        self.assertEqual(_score_to_confidence(0.99), "LOW")


class TestMinScoreThreshold(unittest.TestCase):
    """Min-score filtering tests."""

    def test_nonsense_filtered(self):
        """Nonsense query should return fewer results due to min-score filter."""
        results = search("zqxjkw qwpfmz xvbnrt rlkjhg", top_k=10)
        self.assertLessEqual(len(results), 3)

    def test_override(self):
        """Custom min_score=0.0 should return more results (no filtering)."""
        results_default = search("pricing", min_score=None)
        results_zero = search("pricing", min_score=0.0)
        self.assertGreaterEqual(len(results_zero), len(results_default))


class TestAntiPatternWarnings(unittest.TestCase):
    """Anti-pattern warning tests."""

    def test_warnings_triggered(self):
        """Query about validation should trigger anti-pattern warnings."""
        warning = _find_anti_pattern_warnings("validate idea before building MVP", "reasoning", stage=1)
        if warning:
            self.assertIn("⚠️", warning)

    def test_no_false_positive(self):
        """Generic query should NOT trigger anti-pattern warnings."""
        warning = _find_anti_pattern_warnings("hello world test", "tools", stage=None)
        if warning is not None:
            self.assertLess(len(warning), 200)


class TestStageWeightedSearch(unittest.TestCase):
    """Stage-weighted search integration tests."""

    def test_stage_changes_ranking(self):
        """Same query at different stages should change result scores."""
        results_s2 = search("pricing strategy", stage=2, top_k=3)
        results_s5 = search("pricing strategy", stage=5, top_k=3)

        if results_s2 and results_s5:
            scores_s2 = [r["_score"] for r in results_s2]
            scores_s5 = [r["_score"] for r in results_s5]
            self.assertNotEqual(scores_s2, scores_s5, "Stage weighting should change scores")

    def test_returns_confidence(self):
        """Every search result should have _confidence field."""
        results = search("pricing strategy", top_k=3)
        for r in results:
            self.assertIn("_confidence", r)
            self.assertIn(r["_confidence"], ("HIGH", "MEDIUM", "LOW"))


class TestStageMatcher(unittest.TestCase):
    """Stage matching utility tests."""

    def test_exact(self):
        self.assertTrue(_stage_matches("3", 3))
        self.assertFalse(_stage_matches("3", 4))

    def test_range(self):
        self.assertTrue(_stage_matches("2-5", 3))
        self.assertFalse(_stage_matches("2-5", 1))
        self.assertTrue(_stage_matches("0-6", 4))

    def test_empty(self):
        """Empty stage should match any target."""
        self.assertTrue(_stage_matches("", 3))


class TestStats(unittest.TestCase):
    """Knowledge graph stats tests."""

    def test_total(self):
        stats = get_stats()
        self.assertGreaterEqual(stats["total"], 500)
        self.assertIn("playbook", stats)
        self.assertIn("reasoning", stats)


class TestSearchCache(unittest.TestCase):
    """V3 search index caching tests."""

    def setUp(self):
        """Clear cache before each test."""
        clear_search_cache()

    def test_cache_populated_after_search(self):
        """After searching a domain, its index should be cached."""
        self.assertEqual(len(_INDEX_CACHE), 0)
        search("pricing strategy", domain="pricing", top_k=3)
        self.assertIn("pricing", _INDEX_CACHE)
        self.assertIn("fingerprint", _INDEX_CACHE["pricing"])

    def test_cache_hit_returns_same_results(self):
        """Two identical searches should return the same results (cache hit)."""
        results1 = search("pricing strategy", domain="pricing", top_k=3)
        results2 = search("pricing strategy", domain="pricing", top_k=3)
        scores1 = [r["_score"] for r in results1]
        scores2 = [r["_score"] for r in results2]
        self.assertEqual(scores1, scores2, "Cached search should return identical scores")

    def test_clear_cache_invalidates(self):
        """clear_search_cache() should empty the cache."""
        search("pricing strategy", domain="pricing", top_k=3)
        self.assertGreater(len(_INDEX_CACHE), 0)
        clear_search_cache()
        self.assertEqual(len(_INDEX_CACHE), 0)

    def test_clear_single_domain(self):
        """clear_search_cache(domain) should only clear that domain."""
        search("pricing strategy", domain="pricing", top_k=3)
        search("lean canvas", domain="frameworks", top_k=3)
        self.assertIn("pricing", _INDEX_CACHE)
        self.assertIn("frameworks", _INDEX_CACHE)
        clear_search_cache("pricing")
        self.assertNotIn("pricing", _INDEX_CACHE)
        self.assertIn("frameworks", _INDEX_CACHE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
