# Skill: content_generate_image

## Purpose

Generates a consistent, persona-aligned image using a text-to-image model via MCP.  
Ensures character consistency across all visual content using reference IDs / LoRAs.

## Responsibilities

- Construct prompt using persona traits and campaign context
- Include mandatory character/style reference
- Call image generation MCP tool (Ideogram, Flux, Midjourney, etc.)
- Validate basic output quality (size, format)
- Return image URL + metadata

## Safety & Governance Notes

- **Must be called only after Judge approval**
- Character consistency check should happen in Judge (vision model or metadata check)
- Generation cost must be estimated and checked against budget

## Input / Output Contract

Defined in `interface.py`

## Status

- Interface: defined
- Implementation: stub (awaiting MCP integration)
- Tests: contract validation only