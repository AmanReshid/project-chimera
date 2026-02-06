"""
Tests for the content_generate_image skill.

Goals:
- Validate that ImageGenerationInput enforces all constraints
  (required fields, string lengths, literal enums, budget guardrail)
- Verify ImageGenerationOutput has the expected structure
- Define (but keep failing/skipped) the real execution contract until impl.py is finished

Run with:  pytest tests/test_content_generate_image.py -v
"""

import pytest
from pydantic import ValidationError
from typing import Any

from skills.content_generate_image.interface import (
    ImageGenerationInput,
    ImageGenerationOutput,
)

# Try to import the real implementation function
try:
    from skills.content_generate_image.impl import run_content_generate_image
except ImportError:
    run_content_generate_image = None


# Enable asyncio support for this file
pytestmark = pytest.mark.asyncio


# ────────────────────────────────────────────────
# Input model validation tests (these should PASS)
# ────────────────────────────────────────────────

def test_image_generation_input_minimal_valid():
    """Minimal valid input should pass validation"""
    inp = ImageGenerationInput(
        agent_id="chimera-eth-fashion-001",
        prompt="A confident young woman in vibrant Ethiopian streetwear, Addis Ababa market, golden hour lighting",
        character_reference_id="eth-fashion-v1-lora-001"
    )
    assert inp.agent_id == "chimera-eth-fashion-001"
    assert len(inp.prompt) > 10
    assert inp.character_reference_id == "eth-fashion-v1-lora-001"
    assert inp.style_preset == "photorealistic"  # default
    assert inp.aspect_ratio == "1:1"             # default
    assert inp.model == "ideogram-2.0"           # default
    assert inp.max_cost_usd is None


def test_image_generation_input_full_valid():
    """Full input with all optional fields"""
    inp = ImageGenerationInput(
        agent_id="agent-img-456",
        prompt="Futuristic cyberpunk portrait of an Ethiopian model, neon lights, dramatic pose",
        negative_prompt="blurry, low quality, extra limbs, deformed face",
        character_reference_id="eth-cyber-v2-ref-003",
        style_preset="cinematic",
        aspect_ratio="9:16",
        model="flux-1.1",
        max_cost_usd=0.45
    )
    assert inp.style_preset == "cinematic"
    assert inp.aspect_ratio == "9:16"
    assert inp.model == "flux-1.1"
    assert inp.max_cost_usd == 0.45
    assert inp.negative_prompt is not None


def test_image_generation_input_missing_required_fields():
    """Missing required fields should raise ValidationError"""
    # Missing prompt
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            character_reference_id="ref-1"
        )

    # Missing character_reference_id
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            prompt="test prompt"
        )


def test_image_generation_input_invalid_values():
    """Invalid enum values, too short prompt, negative budget → should fail"""
    # Invalid style_preset
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            prompt="long enough prompt here",
            character_reference_id="ref-1",
            style_preset="invalid-style"     # not in Literal
        )

    # Invalid aspect_ratio
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            prompt="test",
            character_reference_id="ref-1",
            aspect_ratio="7:13"              # not allowed
        )

    # Negative budget
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            prompt="test prompt",
            character_reference_id="ref-1",
            max_cost_usd=-0.1
        )

    # Prompt too short
    with pytest.raises(ValidationError):
        ImageGenerationInput(
            agent_id="agent-123",
            prompt="short",                  # < 10 chars
            character_reference_id="ref-1"
        )


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_image_generation_output_success_shape():
    """Minimal success case structure"""
    out = ImageGenerationOutput(
        success=True,
        image_url="https://cdn.aiqem.tech/gen/abc123-4567.png",
        thumbnail_url="https://cdn.aiqem.tech/thumbs/abc123.jpg",
        width=1024,
        height=1024,
        seed=92837465,
        generation_time_ms=4200,
        cost_estimate_usd=0.045,
        metadata={
            "model": "ideogram-2.0",
            "character_ref_id": "eth-fashion-v1",
            "prompt_hash": "a1b2c3d4"
        }
    )
    assert out.success is True
    assert out.image_url is not None
    assert out.metadata["model"] == "ideogram-2.0"


def test_image_generation_output_failure_shape():
    """Minimal failure case structure"""
    out = ImageGenerationOutput(
        success=False,
        error_message="Generation timeout after 45s",
        metadata={"attempted_model": "ideogram-2.0"}
    )
    assert out.success is False
    assert out.image_url is None
    assert out.error_message is not None


# ────────────────────────────────────────────────
# Real execution contract (should FAIL right now)
# ────────────────────────────────────────────────

@pytest.mark.skipif(
    run_content_generate_image is None,
    reason="run_content_generate_image is not implemented yet"
)
async def test_content_generate_image_execution_contract():
    """
    This test defines what the full skill execution must return.
    It should FAIL until you replace the NotImplementedError stub.
    """
    input_data = ImageGenerationInput(
        agent_id="test-agent-image",
        prompt="A stylish young woman in modern Ethiopian streetwear, standing in a vibrant Addis Ababa market, golden hour lighting, highly detailed",
        character_reference_id="eth-fashion-v1-lora-001",
        aspect_ratio="3:4",
        style_preset="photorealistic",
        max_cost_usd=0.60
    )

    result = await run_content_generate_image(input_data)

    # Contract assertions
    assert isinstance(result, ImageGenerationOutput)
    assert isinstance(result.success, bool)

    if result.success:
        assert isinstance(result.image_url, str)
        assert "http" in result.image_url
        assert result.width is not None and result.width > 0
        assert result.height is not None and result.height > 0
        assert result.generation_time_ms is not None and result.generation_time_ms > 0
        assert result.metadata is not None
        assert "model" in result.metadata
    else:
        assert result.error_message is not None
        assert isinstance(result.error_message, str)
        assert len(result.error_message) > 0