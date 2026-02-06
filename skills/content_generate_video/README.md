# Skill: content_generate_video

## Purpose

Generate a short video clip (typically 5–30 seconds) from text prompt, image, or existing media using text-to-video or image-to-video models via MCP.

## Responsibilities

- Enforce character/style consistency using persistent reference
- Support tiered generation: cheap (image-to-video motion) vs premium (full text-to-video)
- Call the appropriate MCP video generation tool
- Return video URL + metadata (duration, resolution, cost)

## Safety & Governance Notes

- **Must be called only after Judge approval**
- Character consistency validation is done by Judge (vision model or metadata check)
- Generation cost must be checked against task/campaign budget
- Tier selection (cheap vs premium) is decided by Planner based on priority & budget

## Input / Output Contract

See `interface.py`

## Status

- Interface: complete
- Implementation: stub
- Tests: `tests/test_content_generate_video.py`