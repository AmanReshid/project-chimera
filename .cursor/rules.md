# Project Chimera – AI Coding & Reasoning Rules
Last updated: 2026-02-06

## 1. Project Context

This is **Project Chimera** — an autonomous influencer system.

We are building the foundational infrastructure for a fleet of persistent, goal-directed AI agents (virtual influencers) that can:

- perceive digital signals (trends, mentions, news, comments)
- plan multi-step content strategies
- generate consistent multimodal content (text, images, short videos)
- publish and engage on social platforms
- perform agentic commerce (non-custodial wallets, autonomous transfers)
- operate under strong governance (Planner → Worker → Judge swarm + HITL)

Core architectural pillars (must never be violated):

- Model Context Protocol (MCP) — the only way agents interact with the external world
- Hierarchical FastRender-style swarm: Planner (strategist), Workers (executors), Judge (gatekeeper + quality + safety)
- Agentic Commerce via Coinbase AgentKit
- Strong multi-tenancy, audit trail, budget governance, EU AI Act compliance

This project follows **Spec-Driven Development (SDD)**.  
The `specs/` directory is the **single source of truth** for all intent and requirements.

## 2. Prime Directive – Non-negotiable

**NEVER generate or suggest any implementation code unless:**

1. The relevant specification already exists in the `specs/` directory, and
2. You have read and understood the corresponding spec file(s), and
3. You can clearly reference which spec section(s) you are implementing.

If no spec exists for the requested change/feature:
→ Do NOT write code.
→ Instead, propose a new or updated spec file in `specs/`
→ Explain what should be added and why
→ Wait for confirmation before proceeding to implementation

## 3. Traceability & Reasoning Rules

Before writing any code or suggesting changes, you **must**:

1. State clearly which file(s) in `specs/` you are implementing or extending  
   (example: "Implementing task schema validation as defined in specs/technical.md section 1")

2. Explain your plan in plain English before showing any code  
   (example: "Plan: 1. Define Pydantic model matching the JSON schema → 2. Add validation for required fields → 3. Write two test cases (valid + invalid)")

3. Always prefer:
   - Explicit failure (raise meaningful exceptions) over silent errors
   - Type hints (Python 3.10+ style)
   - Pydantic v2 for all data models / contracts
   - Docstrings on public functions/classes

## 4. Forbidden Patterns (do NOT suggest these)

- Hard-coding API keys, endpoints, wallet addresses, or credentials
- Making direct HTTP/API calls outside of MCP servers
- Writing monolithic single-agent logic (we only use swarm pattern)
- Skipping or writing tests after implementation (tests define the boundary)
- Bypassing the Judge for publishing, transactions, or sensitive content
- Ignoring tenant_id filtering in queries
- Using outdated patterns (no Flask, no old pydantic v1, no click for CLI in new code)

## 5. Preferred Technologies & Patterns (2026 context)

- Python 3.12+
- uv (preferred) or poetry for dependency management
- Pydantic v2 (strict mode where possible)
- pytest + ruff + mypy
- Redis (queues, ephemeral state)
- PostgreSQL (transactional data)
- Weaviate (semantic memory / RAG)
- MCP SDK for all external integrations
- Coinbase AgentKit for on-chain actions
- Structured logging (structlog or loguru)
- Async-first where appropriate (asyncio, anyio)

## 6. How to respond when unsure

Ask one of these questions:

- "Which spec file defines this behavior?"
- "Should I first create/update a specification in specs/ for this?"
- "Does this change affect multi-tenancy, budget guards, or HITL rules?"

If the answer is unclear → do not proceed with code. Suggest spec clarification first.

## 7. Quick Reference – Always Check First

1. Does a spec exist in `specs/` that covers this?
2. Have I explained my plan?
3. Am I following the swarm pattern (Planner/Worker/Judge)?
4. Are external calls going through MCP?
5. Is tenant_id enforced?
6. Will this be auditable / traceable?

If any answer is "no" → stop and address it.

Happy building — but always spec-first.