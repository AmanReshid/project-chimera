"""
Tests for the trend_analyze skill.

Goals:
- Validate that TrendAnalyzeInput enforces all constraints (required fields, ranges, enums)
- Verify TrendAnalyzeOutput has the expected structure
- Define (but keep failing/skipped) the real execution contract test until impl.py is finished

Run with:  pytest tests/test_trend_analyze.py -v
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from skills.trend_analyze.interface import (
    TrendAnalyzeInput,
    TrendAnalyzeOutput,
    TrendItem,
)

# Attempt to import the real implementation function
try:
    from skills.trend_analyze.impl import run_trend_analyze
except ImportError:
    run_trend_analyze = None


# Enable asyncio support for this file (if/when we test async execution)
pytestmark = pytest.mark.asyncio


# ────────────────────────────────────────────────
# Input model validation tests (these should PASS)
# ────────────────────────────────────────────────

def test_trend_analyze_input_minimal_valid():
    """Minimal valid input should be accepted"""
    inp = TrendAnalyzeInput(
        agent_id="chimera-eth-fashion-001",
        niche="Ethiopian streetwear",
    )
    assert inp.agent_id == "chimera-eth-fashion-001"
    assert inp.niche == "Ethiopian streetwear"
    assert inp.time_window_hours == 24
    assert inp.max_results == 10
    assert inp.language == "en"
    assert inp.mcp_resources is None


def test_trend_analyze_input_full_valid():
    """Full input with custom values should be valid"""
    inp = TrendAnalyzeInput(
        agent_id="agent-trend-777",
        niche="crypto memecoins",
        time_window_hours=72,
        max_results=25,
        language="en",
        mcp_resources=[
            "news://crypto/latest",
            "twitter://trends/memecoins"
        ]
    )
    assert inp.time_window_hours == 72
    assert inp.max_results == 25
    assert len(inp.mcp_resources) == 2


def test_trend_analyze_input_missing_required_fields():
    """Missing agent_id or niche → should fail"""
    with pytest.raises(ValidationError):
        TrendAnalyzeInput(
            niche="fashion",
            # agent_id missing
        )

    with pytest.raises(ValidationError):
        TrendAnalyzeInput(
            agent_id="agent-123"
            # niche missing
        )


def test_trend_analyze_input_invalid_ranges():
    """Values outside allowed ranges should fail"""
    # time_window_hours too small
    with pytest.raises(ValidationError):
        TrendAnalyzeInput(
            agent_id="agent-123",
            niche="test",
            time_window_hours=0
        )

    # time_window_hours too large
    with pytest.raises(ValidationError):
        TrendAnalyzeInput(
            agent_id="agent-123",
            niche="test",
            time_window_hours=300
        )

    # max_results too high (validator should cap it)
    inp = TrendAnalyzeInput(
        agent_id="agent-123",
        niche="test",
        max_results=100
    )
    assert inp.max_results == 50, "Validator should have capped max_results at 50"


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_trend_analyze_output_minimal_valid():
    """Minimal valid output structure"""
    item = TrendItem(
        title="Top 10 Streetwear Trends 2026",
        source="Vogue Ethiopia",
        relevance_score=0.92
    )

    out = TrendAnalyzeOutput(
        trends=[item],
        summary="Rising interest in bold colors and local prints",
        source_count=1
    )
    assert len(out.trends) == 1
    assert out.summary.startswith("Rising")
    assert out.source_count == 1
    assert isinstance(out.execution_timestamp, datetime)


def test_trend_analyze_output_empty_trends():
    """Output should allow empty trends list (no results found case)"""
    out = TrendAnalyzeOutput(
        trends=[],
        summary="No significant trends detected in the last 24 hours",
        source_count=0
    )
    assert out.trends == []
    assert out.source_count == 0


# ────────────────────────────────────────────────
# Real execution contract (should FAIL right now)
# ────────────────────────────────────────────────

@pytest.mark.skipif(
    run_trend_analyze is None,
    reason="run_trend_analyze is not implemented yet"
)
async def test_trend_analyze_execution_contract():
    """
    This test defines what the full skill execution should return.
    It should FAIL until you replace the NotImplementedError stub in impl.py.
    """
    input_data = TrendAnalyzeInput(
        agent_id="test-agent-trend",
        niche="Ethiopian streetwear",
        time_window_hours=48,
        max_results=8
    )

    result = await run_trend_analyze(input_data)

    # Contract assertions
    assert isinstance(result, TrendAnalyzeOutput)
    assert isinstance(result.trends, list)
    assert isinstance(result.summary, str)
    assert len(result.summary) >= 20
    assert isinstance(result.source_count, int)
    assert isinstance(result.execution_timestamp, datetime)

    # Optional but nice to check
    if result.trends:
        first = result.trends[0]
        assert isinstance(first, TrendItem)
        assert isinstance(first.title, str)
        assert len(first.title) >= 5
        assert isinstance(first.relevance_score, float)
        assert 0.0 <= first.relevance_score <= 1.0