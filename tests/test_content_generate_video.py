"""
Tests for the content_generate_video skill.

Goals:
- Validate input model constraints (required fields, enums, ranges, budget guard)
- Verify output model structure
- Keep execution contract test failing/skipped until impl.py is implemented

Run with: pytest tests/test_content_generate_video.py -v
"""

import pytest
from pydantic import ValidationError

from skills.content_generate_video.interface import (
    VideoGenerationInput,
    VideoGenerationOutput,
)

# Try to import real implementation
try:
    from skills.content_generate_video.impl import run_content_generate_video
except ImportError:
    run_content_generate_video = None


# Enable asyncio support
pytestmark = pytest.mark.asyncio


# ────────────────────────────────────────────────
# Input model validation (these should PASS)
# ────────────────────────────────────────────────

def test_video_input_minimal_valid():
    """Minimal valid input (cheap tier, image-to-video)"""
    inp = VideoGenerationInput(
        agent_id="chimera-eth-fashion-001",
        prompt="A young woman in vibrant Ethiopian streetwear dancing in Addis market, golden hour lighting, smooth camera move",
        character_reference_id="eth-fashion-v1-lora-001",
        input_image_url="https://cdn.aiqem.tech/reference/eth-look-001.jpg",
        duration_seconds=8,
        tier="cheap"
    )
    assert inp.agent_id == "chimera-eth-fashion-001"
    assert inp.tier == "cheap"
    assert inp.duration_seconds == 8
    assert inp.model == "runway-gen3"  # default


def test_video_input_premium_valid():
    """Full premium text-to-video input"""
    inp = VideoGenerationInput(
        agent_id="agent-video-999",
        prompt="Cinematic shot: Ethiopian model walking through futuristic Addis Ababa at night, neon lights, dramatic camera pan",
        negative_prompt="blurry, low quality, artifacts, text overlay",
        character_reference_id="eth-cinematic-v2-ref-004",
        tier="premium",
        duration_seconds=15,
        resolution="1080p",
        fps=30,
        model="luma-dream-machine",
        max_cost_usd=1.20
    )
    assert inp.tier == "premium"
    assert inp.resolution == "1080p"
    assert inp.max_cost_usd == 1.20


def test_video_input_missing_required():
    """Missing prompt or character reference → fail"""
    with pytest.raises(ValidationError):
        VideoGenerationInput(
            agent_id="agent-123",
            character_reference_id="ref-1",
            duration_seconds=10,
            tier="cheap"
            # prompt missing
        )

    with pytest.raises(ValidationError):
        VideoGenerationInput(
            agent_id="agent-123",
            prompt="test prompt",
            duration_seconds=10,
            tier="cheap"
            # character_reference_id missing
        )


def test_video_input_invalid_values():
    """Invalid enum, out-of-range duration, negative budget → fail"""
    with pytest.raises(ValidationError):
        VideoGenerationInput(
            agent_id="agent-123",
            prompt="long enough prompt",
            character_reference_id="ref-1",
            tier="invalid-tier"           # not allowed
        )

    with pytest.raises(ValidationError):
        VideoGenerationInput(
            agent_id="agent-123",
            prompt="test",
            character_reference_id="ref-1",
            duration_seconds=60           # too long
        )

    with pytest.raises(ValidationError):
        VideoGenerationInput(
            agent_id="agent-123",
            prompt="test",
            character_reference_id="ref-1",
            max_cost_usd=-0.5             # negative
        )


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_video_output_success_shape():
    """Minimal success case"""
    out = VideoGenerationOutput(
        success=True,
        video_url="https://cdn.aiqem.tech/video/gen/abc123.mp4",
        thumbnail_url="https://cdn.aiqem.tech/thumbs/abc123.jpg",
        duration_seconds=12,
        width=1280,
        height=720,
        fps=30,
        generation_time_ms=18500,
        estimated_cost_usd=0.85,
        metadata={"model": "runway-gen3", "tier": "premium"}
    )
    assert out.success is True
    assert out.video_url is not None
    assert out.duration_seconds == 12


def test_video_output_failure_shape():
    """Failure case shape"""
    out = VideoGenerationOutput(
        success=False,
        error_message="Generation timeout after 60s",
        metadata={"attempted_model": "luma-dream-machine"}
    )
    assert out.success is False
    assert out.video_url is None
    assert out.error_message is not None


# ────────────────────────────────────────────────
# Execution contract (should FAIL right now)
# ────────────────────────────────────────────────

@pytest.mark.skipif(
    run_content_generate_video is None,
    reason="run_content_generate_video is not implemented yet"
)
async def test_content_generate_video_execution_contract():
    """
    Defines the full contract the skill must eventually satisfy.
    Should fail until the stub is replaced with real logic.
    """
    input_data = VideoGenerationInput(
        agent_id="test-agent-video",
        prompt="A stylish Ethiopian model walking through a vibrant market at sunset, cinematic camera pan",
        character_reference_id="eth-fashion-v1-lora-001",
        tier="cheap",
        duration_seconds=10,
        max_cost_usd=0.40
    )

    result = await run_content_generate_video(input_data)

    assert isinstance(result, VideoGenerationOutput)
    assert isinstance(result.success, bool)
    assert result.success == (result.error_message is None)

    if result.success:
        assert isinstance(result.video_url, str)
        assert "http" in result.video_url
        assert result.duration_seconds is not None and 5 <= result.duration_seconds <= 30
        assert result.estimated_cost_usd is not None and result.estimated_cost_usd >= 0
        assert "model" in result.metadata
    else:
        assert result.error_message is not None