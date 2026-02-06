# Skill: trend_fetcher

## Purpose

Fetches and filters recent trends, news items, or social signals relevant to the agent's niche/persona.  
Typically used by the Planner or a perception Worker to gather input data for content planning.

## Responsibilities

- Query MCP Resources (news feeds, trend APIs, social mentions, etc.)
- Apply basic filtering and relevance scoring
- Return a ranked list of trend items + a short summary

## Input / Output Contract

Defined in `interface.py`

- **Input**: `TrendFetcherInput`
- **Output**: `TrendFetcherOutput` (or raises exception on failure)

## Usage Example (pseudo-code)

```python
from skills.trend_fetcher.interface import TrendFetcherInput, TrendFetcherOutput
from skills.trend_fetcher.impl import run_trend_fetcher

input_data = TrendFetcherInput(
    agent_id="chimera-eth-fashion-001",
    niche="Ethiopian streetwear",
    lookback_hours=48,
    max_items=12
)

result: TrendFetcherOutput = await run_trend_fetcher(input_data)
print(result.summary)
print(f"Found {len(result.trends)} relevant trends")