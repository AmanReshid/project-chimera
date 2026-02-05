# Skill: content_publish

## Purpose

Publishes prepared content (text + media) to a target social platform.

This is a **critical safety boundary** skill — all publishing actions must pass Judge validation first.

## Responsibilities

- Format content according to platform rules
- Call the correct MCP publish tool
- Apply AI disclosure flags when supported
- Return external post ID and metadata

## Input / Output Contract

Defined in `interface.py`

## Usage Example (pseudo-code)

```python
from skills.content_publish.interface import ContentPublishInput, ContentPublishOutput

input_data = ContentPublishInput(
    agent_id="chimera-eth-fashion-001",
    platform="twitter",
    text_content="🔥 Summer heat in Addis just got hotter! 🇪🇹 #EthiopiaStreetwear",
    media_urls=["https://cdn.../image.png"],
    disclosure_level="automated"
)

result = await run_content_publish(input_data)
print(result.external_post_id)