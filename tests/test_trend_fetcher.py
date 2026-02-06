"""
Tests for the trend_fetcher skill.

Goals:
- Validate input model constraints (required fields, ranges, defaults)
- Verify output model structure
- Keep execution contract test failing/skipped until implementation exists

Run with:  pytest tests/test_trend_fetcher.py -v
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from skills.trend_fetcher.interface import (
    TrendFetcherInput,
    TrendFetcherOutput,
    TrendItem,
)

# Try to import real implementation
try:
    from skills.trend_fetcher.impl import run_trend_fetcher
except ImportError:
    run_trend_fetcher = None


# Enable asyncio support
pytestmark = pytest.mark.asyncio


# ────────────────────────────────────────────────
# Input model validation (these should PASS)
# ────────────────────────────────────────────────

def test_trend_fetcher_input_minimal_valid():
    """Minimal valid input should pass"""
    inp = TrendFetcherInput(
        agent_id="chimera-eth-fashion-001",
        niche="Ethiopian streetwear",
    )
    assert inp.agent_id == "chimera-eth-fashion-001"
    assert inp.niche == "Ethiopian streetwear"
    assert inp.lookback_hours == 24
    assert inp.max_items == 10
    assert inp.language == "en"
    assert inp.mcp_resources is None


def test_trend_fetcher_input_full_valid():
    """Full input with custom values"""
    inp = TrendFetcherInput(
        agent_id="agent-trend-777",
        niche="crypto memecoins",
        lookback_hours=96,
        max_items=30,
        language="am",
        mcp_resources=["news://crypto", "twitter://trends/memecoins"]
    )
    assert inp.lookback_hours == 96
    assert inp.max_items == 30
    assert inp.language == "am"
    assert len(inp.mcp_resources) == 2


def test_trend_fetcher_input_missing_required():
    """Missing agent_id or niche → ValidationError"""
    with pytest.raises(ValidationError):
        TrendFetcherInput(niche="fashion")  # missing agent_id

    with pytest.raises(ValidationError):
        TrendFetcherInput(agent_id="agent-123")  # missing niche


def test_trend_fetcher_input_invalid_ranges():
    """Out-of-range values should fail"""
    with pytest.raises(ValidationError):
        TrendFetcherInput(
            agent_id="agent-123",
            niche="test",
            lookback_hours=0   # too small
        )

    with pytest.raises(ValidationError):
        TrendFetcherInput(
            agent_id="agent-123",
            niche="test",
            lookback_hours=500   # too large
        )

    # max_items should be capped by validator
    inp = TrendFetcherInput(
        agent_id="agent-123",
        niche="test",
        max_items=100
    )
    assert inp.max_items == 50, "max_items should be capped at 50"


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_trend_fetcher_output_minimal():
    """Minimal valid output structure"""
    item = TrendItem(
        title="Top 10 Streetwear Trends Ethiopia 2026",
        source="Addis Fashion Blog",
        relevance_score=0.89
    )

    out = TrendFetcherOutput(
        trends=[item],
        summary="Strong interest in local prints and bold colors",
        item_count=1,
        sources_used=1
    )
    assert len(out.trends) == 1
    assert out.summary.startswith("Strong")
    assert out.item_count == 1
    assert isinstance(out.fetched_at, datetime)


def test_trend_fetcher_output_no_results():
    """Should allow empty trends list (no matches case)"""
    out = TrendFetcherOutput(
        trends=[],
        summary="No relevant trends found in the last 48 hours",
        item_count=0,
        sources_used=3
    )
    assert out.trends == []
    assert out.item_count == 0


# ────────────────────────────────────────────────
# Execution contract (should FAIL or be skipped)
# ────────────────────────────────────────────────

@pytest.mark.skipif(
    run_trend_fetcher is None,
    reason="run_trend_fetcher is not implemented yet"
)
async def test_trend_fetcher_execution_contract():
    """
    Defines the full contract the skill must eventually satisfy.
    Should fail until the stub is replaced with real logic.
    """
    input_data = TrendFetcherInput(
        agent_id="test-agent-trend",
        niche="Ethiopian fashion",
        lookback_hours=48,
        max_items=10
    )

    result = await run_trend_fetcher(input_data)

    assert isinstance(result, TrendFetcherOutput)
    assert isinstance(result.trends, list)
    assert isinstance(result.summary, str)
    assert len(result.summary) >= 15
    assert isinstance(result.item_count, int)
    assert result.item_count == len(result.trends)
    assert isinstance(result.fetched_at, datetime)

    if result.trends:
        first = result.trends[0]
        assert isinstance(first.title, str)
        assert len(first.title) >= 5
        assert isinstance(first.relevance_score, float)
        assert 0.0 <= first.relevance_score <= 1.0