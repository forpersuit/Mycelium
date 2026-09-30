"""Validation test harness for Study Library Adaptive RAG benchmark.

Verifies that the benchmark specifications are valid, complete,
and ready for regression testing once the execution engine is built.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

BENCHMARK_FILE = Path(__file__).parent / "study_library_scenarios.json"


def test_study_library_benchmark_contract():
    """Verify that the validation benchmark file exists and is strictly valid."""
    assert BENCHMARK_FILE.exists(), "study_library_scenarios.json must exist"

    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["benchmark_name"] == "StudyLibraryAdaptiveRAGBenchmark"
    scenarios = data.get("scenarios", [])
    assert len(scenarios) == 5, "Expected 5 core validation scenarios"

    scenario_ids = [s["id"] for s in scenarios]
    assert scenario_ids == [
        "SCENARIO-01",
        "SCENARIO-02",
        "SCENARIO-03",
        "SCENARIO-04",
        "SCENARIO-05",
    ]

    for s in scenarios:
        assert "query" in s or "session_turns" in s, f"{s['id']} must provide query or session_turns"
        assert "expected_routing" in s, f"{s['id']} must declare expected_routing"
        assert "evaluation_metrics" in s, f"{s['id']} must declare evaluation_metrics"
        assert "ground_truth_assertion" in s, f"{s['id']} must declare ground_truth_assertion"


@pytest.mark.parametrize(
    "expected_tier",
    [
        "Tier1_FTS_Macro_Filter",
        "Tier1_Small_To_Big",
        "Tier2_Lazy_KV_Cache",
        "Tier1_Layout_Window_Fallback",
        "Tier4_Multimodal_Page_Dispatch",
    ],
)
def test_all_expected_tiers_covered(expected_tier: str):
    """Verify that every architectural routing tier is explicitly tested."""
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    active_tiers = {s["expected_routing"] for s in data["scenarios"]}
    assert expected_tier in active_tiers, f"Tier {expected_tier} must have a dedicated test scenario"
