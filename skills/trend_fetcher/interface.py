
### `skills/trend_fetcher/interface.py`

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class TrendItem(BaseModel):
    """Single trend/news/signal item"""
    title: str = Field(..., min_length=5, description="Headline or main phrase")
    source: str = Field(..., min_length=2)
    url: Optional[str] = Field(None, description="Link to original source")
    published_at: Optional[datetime] = None
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="0–1 relevance to agent's niche")
    snippet: str = Field(default="", description="Short excerpt or summary sentence")


class TrendFetcherInput(BaseModel):
    """Input parameters for fetching trends"""
    agent_id: str = Field(..., min_length=3, description="Unique agent identifier")
    niche: str = Field(..., min_length=3, description="Main topic/focus area")
    lookback_hours: int = Field(24, ge=1, le=168, description="How far back to look")
    max_items: int = Field(10, ge=5, le=50, description="Maximum number of items to return")
    language: str = Field("en", min_length=2, max_length=5, description="Preferred language")
    mcp_resources: Optional[List[str]] = Field(
        default=None,
        description="Specific MCP resource URIs to query (optional)"
    )

    @validator("max_items")
    def cap_max_items(cls, v):
        return min(v, 50)


class TrendFetcherOutput(BaseModel):
    """Result of trend fetching"""
    trends: List[TrendItem] = Field(default_factory=list)
    summary: str = Field(..., min_length=15, description="One-sentence overview of results")
    item_count: int = Field(..., ge=0, description="Number of returned items")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    sources_used: int = Field(0, description="How many different sources contributed")
    processing_duration_ms: Optional[int] = None