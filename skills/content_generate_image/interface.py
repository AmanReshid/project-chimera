from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal


class ImageGenerationInput(BaseModel):
    """Parameters for generating a consistent image"""
    agent_id: str = Field(..., min_length=3)
    prompt: str = Field(..., min_length=10, max_length=2000)
    negative_prompt: Optional[str] = None
    character_reference_id: str = Field(
        ..., 
        description="Persistent ID / LoRA / face reference to maintain consistency"
    )
    style_preset: Optional[Literal[
        "photorealistic", "anime", "cinematic", "digital_art", "illustration", "vibrant"
    ]] = "photorealistic"
    aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4"] = "1:1"
    model: Literal["ideogram-2.0", "flux-1.1", "sd3-medium", "dall-e-3"] = "ideogram-2.0"
    max_cost_usd: Optional[float] = Field(None, ge=0.0, description="Budget guardrail")


class ImageGenerationOutput(BaseModel):
    """Result of image generation"""
    success: bool
    image_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    width: Optional[int] = None
    height: Optional[int] = None
    seed: Optional[int] = None
    generation_time_ms: Optional[int] = None
    cost_estimate_usd: Optional[float] = None
    error_message: Optional[str] = None
    metadata: dict = Field(default_factory=dict)  # model, ref_id, prompt_hash, etc.