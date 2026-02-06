from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal


class VideoGenerationInput(BaseModel):
    """Parameters for generating a short video clip"""
    agent_id: str = Field(..., min_length=3, description="Unique agent identifier")
    prompt: str = Field(..., min_length=10, max_length=3000, description="Main text prompt for video")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Elements to avoid")

    # Consistency & style
    character_reference_id: str = Field(..., description="Persistent character/style reference (LoRA/face ID)")

    # Optional input source (one should be provided in real usage)
    input_image_url: Optional[HttpUrl] = Field(None, description="Start from static image (motion animation)")
    input_video_url: Optional[HttpUrl] = Field(None, description="Extend or restyle existing short clip")

    # Generation settings
    tier: Literal["cheap", "premium"] = Field("cheap", description="cheap = image-to-video motion, premium = full text-to-video")
    duration_seconds: int = Field(..., ge=5, le=30, description="Target video length")
    resolution: Literal["480p", "720p", "1080p"] = "720p"
    fps: int = Field(24, ge=15, le=60)
    model: Literal[
        "runway-gen3",
        "luma-dream-machine",
        "pika-1.5",
        "kling-1.5"
    ] = "runway-gen3"

    # Governance & cost control
    max_cost_usd: Optional[float] = Field(None, ge=0.0, description="Hard budget limit")


class VideoGenerationOutput(BaseModel):
    """Result of short video generation"""
    success: bool
    video_url: Optional[HttpUrl] = Field(None, description="Public/CDN URL to generated video")
    thumbnail_url: Optional[HttpUrl] = None
    duration_seconds: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[int] = None
    seed: Optional[int] = None
    generation_time_ms: Optional[int] = None
    estimated_cost_usd: Optional[float] = None
    error_message: Optional[str] = None
    metadata: dict = Field(default_factory=dict)  # model, tier, ref_id, prompt_hash, etc.