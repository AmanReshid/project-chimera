"""
Tests for the content_publish skill.

Goals:
- Validate that ContentPublishInput enforces all constraints (enums, lengths, required fields)
- Verify ContentPublishOutput has the expected structure
- Define (but keep failing) the real execution contract test until impl.py is finished

Run with:  pytest tests/test_content_publish.py -v
"""

import pytest
from pydantic import ValidationError

from skills.content_publish.interface import (
    ContentPublishInput,
    ContentPublishOutput,
)

# Attempt to import the real implementation function
try:
    from skills.content_publish.impl import run_content_publish
except ImportError:
    run_content_publish = None


# ===============================================
# Enable asyncio support for this file
# ===============================================

# Option A: marker on the module level (works with pytest-asyncio)
pytestmark = pytest.mark.asyncio

# Option B: register marker explicitly (prevents warning even without config)
def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as requiring async support")


# ────────────────────────────────────────────────
# Input model validation tests (these should PASS)
# ────────────────────────────────────────────────

def test_content_publish_input_minimal_valid():
    """Minimal valid input should be accepted"""
    inp = ContentPublishInput(
        agent_id="chimera-eth-001",
        platform="twitter",
        text_content="Just a simple test post 🚀",
    )
    assert inp.agent_id == "chimera-eth-001"
    assert inp.platform == "twitter"
    assert inp.text_content == "Just a simple test post 🚀"
    assert inp.media_urls == []
    assert inp.disclosure_level == "automated"
    assert inp.reply_to_post_id is None
    assert inp.scheduled_at is None


def test_content_publish_input_with_media_and_reply():
    """Full input with media, reply, and scheduling should be valid"""
    inp = ContentPublishInput(
        agent_id="agent-fashion-123",
        platform="instagram",
        text_content="New drop alert! 🔥 #EthiopiaFashion",
        media_urls=[
            "https://cdn.aiqem.tech/gen/abc123.jpg",
            "https://cdn.aiqem.tech/gen/video456.mp4"
        ],
        reply_to_post_id="1791234567890123456",
        disclosure_level="automated",
        scheduled_at="2026-02-10T18:00:00Z"
    )
    assert len(inp.media_urls) == 2
    assert inp.reply_to_post_id == "1791234567890123456"
    assert inp.scheduled_at == "2026-02-10T18:00:00Z"


def test_content_publish_input_invalid_platform():
    """Platform not in allowed list → should fail with Pydantic v2 message"""
    with pytest.raises(ValidationError) as exc_info:
        ContentPublishInput(
            agent_id="agent-xyz",
            platform="facebook",          # ← not allowed
            text_content="test"
        )

    error_str = str(exc_info.value)
    assert "platform" in error_str
    assert "type=literal_error" in error_str
    assert "facebook" in error_str
    assert "twitter" in error_str or "instagram" in error_str  # at least one valid option shown


def test_content_publish_input_missing_required_fields():
    """Missing platform or text_content → ValidationError"""
    with pytest.raises(ValidationError):
        ContentPublishInput(
            agent_id="agent-123",
            # platform missing
            text_content="hello"
        )

    with pytest.raises(ValidationError):
        ContentPublishInput(
            agent_id="agent-123",
            platform="twitter"
            # text_content missing
        )


def test_content_publish_input_text_too_short():
    """text_content must be at least 1 character"""
    with pytest.raises(ValidationError):
        ContentPublishInput(
            agent_id="agent-123",
            platform="twitter",
            text_content=""             # empty string
        )


def test_content_publish_input_invalid_disclosure_level():
    """disclosure_level must be one of the allowed literals"""
    with pytest.raises(ValidationError):
        ContentPublishInput(
            agent_id="agent-123",
            platform="twitter",
            text_content="test post",
            disclosure_level="secret"   # not allowed
        )


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_content_publish_output_success_shape():
    """Minimal success case shape"""
    out = ContentPublishOutput(
        success=True,
        external_post_id="1789456123789012345",
        platform_url="https://x.com/user/status/1789456123789012345",
        posted_at="2026-02-06T14:35:22Z",
        audit_log_reference="publish-log-abc123"
    )
    assert out.success is True
    assert out.external_post_id is not None
    assert out.audit_log_reference == "publish-log-abc123"


def test_content_publish_output_failure_shape():
    """Minimal failure case shape"""
    out = ContentPublishOutput(
        success=False,
        error_message="Platform rate limit exceeded",
        audit_log_reference="log-err-20260206-xyz"
    )
    assert out.success is False
    assert out.external_post_id is None
    assert out.error_message is not None
    assert out.audit_log_reference.startswith("log-err")


# ────────────────────────────────────────────────
# Real execution contract (should FAIL with NotImplementedError)
# ────────────────────────────────────────────────

async def test_content_publish_execution_contract():
    """
    This test defines what the full skill execution should return.
    It should FAIL until you replace the NotImplementedError stub in impl.py.
    """
    input_data = ContentPublishInput(
        agent_id="test-agent-publish",
        platform="twitter",
        text_content="Automated test post from Chimera",
        media_urls=["https://example.com/test.jpg"]
    )

    result = await run_content_publish(input_data)

    assert isinstance(result, ContentPublishOutput)
    assert isinstance(result.success, bool)

    if result.success:
        assert isinstance(result.external_post_id, str)
        assert result.external_post_id != ""
        assert result.platform_url is not None
        assert result.posted_at is not None
        assert result.audit_log_reference.startswith("publish-")
        assert result.media_ids == [] or all(isinstance(id_, str) for id_ in result.media_ids)
    else:
        assert result.error_message is not None
        assert result.audit_log_reference.startswith("error-")