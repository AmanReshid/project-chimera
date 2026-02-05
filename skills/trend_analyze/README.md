# Skill: trend_analyze

## Purpose

Analyzes recent trends, news, or social signals relevant to the agent's niche/persona.  
This skill is typically used by the Planner or a dedicated perception Worker to inform content planning.

## Responsibilities

- Fetch data via MCP Resources (news, social mentions, trend APIs)
- Filter and rank items by relevance
- Produce a concise summary + opportunity suggestions

## Input / Output Contract

Defined in `interface.py`

- **Input**: `TrendAnalyzeInput`
- **Output**: `TrendAnalyzeOutput` (or raises `SkillError`)

## Usage Example (pseudo-code)

```python
from skills.trend_analyze.interface import TrendAnalyzeInput, TrendAnalyzeOutput
from skills.trend_analyze.impl import run_trend_analyze

input_data = TrendAnalyzeInput(
    agent_id="chimera-eth-fashion-001",
    niche="Ethiopian streetwear",
    time_window_hours=48,
    max_results=12
)

result: TrendAnalyzeOutput = await run_trend_analyze(input_data)
print(result.summary)