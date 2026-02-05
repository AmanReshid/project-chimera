
### `skills/trend_analyze/interface.py`


from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class TrendItem(BaseModel):
    """Single trend/news/mention item"""
    title: str = Field(..., min_length=5)
    source: str
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    summary: str = Field(default="", description="Short description or excerpt")


class TrendAnalyzeInput(BaseModel):
    """Input parameters for trend analysis skill"""
    agent_id: str = Field(..., min_length=3)
    niche: str = Field(..., min_length=3, description="Main topic/focus area")
    time_window_hours: int = Field(24, ge=1, le=168)
    max_results: int = Field(10, ge=5, le=50)
    language: str = Field("en", min_length=2, max_length=5)
    mcp_resources: Optional[List[str]] = Field(
        default=None,
        description="Specific MCP resource URIs to query (optional)"
    )

    @validator("max_results")
    def limit_max_results(cls, v):
        return min(v, 50)


class TrendAnalyzeOutput(BaseModel):
    """Result of trend analysis"""
    trends: List[TrendItem]
    summary: str = Field(..., min_length=20, description="Concise overview")
    detected_opportunities: List[str] = Field(
        default_factory=list,
        description="Suggested content angles or actions"
    )
    execution_timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_count: int
    processing_duration_ms: Optional[int] = None