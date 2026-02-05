
### `skills/content_publish/interface.py`


from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal


class ContentPublishInput(BaseModel):
    """Input for publishing content to a social platform"""
    agent_id: str = Field(..., min_length=3)
    platform: Literal["twitter", "instagram", "threads", "tiktok", "youtube_shorts"]
    text_content: str = Field(..., min_length=1, max_length=5000)
    media_urls: List[HttpUrl] = Field(default_factory=list)
    reply_to_post_id: Optional[str] = None
    disclosure_level: Literal["automated", "assisted", "none"] = "automated"
    scheduled_at: Optional[str] = None  # ISO8601 if future scheduling supported


class ContentPublishOutput(BaseModel):
    """Result of publish operation"""
    success: bool
    external_post_id: Optional[str] = None
    platform_url: Optional[str] = None
    posted_at: Optional[str] = None  # ISO8601
    media_ids: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    audit_log_reference: str = Field(..., description="Reference to log entry")