# Project Chimera – Rules & Prime Directives for Claude (and other coding assistants)

Last updated: February 06, 2026

## Project Context

This is **Project Chimera**, an autonomous influencer system.

We are building a production-grade foundation for a fleet of persistent, goal-directed AI agents (virtual influencers) that can:

- perceive digital signals (trends, mentions, news, audience interactions)
- plan multi-step content strategies using the FastRender swarm pattern (Planner → Workers → Judge)
- generate consistent multimodal content (text, images, short videos)
- publish and engage on social platforms via MCP (Model Context Protocol)
- perform limited agentic commerce (non-custodial wallets, budget checks, transfers)
- operate under strong governance, HITL escalation, audit trails, and EU AI Act compliance

Core architectural principles (never violate these):

- All external interactions go through MCP servers — never direct API calls in core logic
- Hierarchical swarm only: Planner, Workers, Judge — no monolithic agents
- Specs/ directory is the single source of truth for intent and requirements
- Strong multi-tenancy (tenant_id everywhere), auditability, budget guards
- TDD-first: tests define the boundary before implementation

## Prime Directive – Absolute Rule

**NEVER generate or suggest any implementation code unless:**

1. The relevant specification already exists in the `specs/` directory
2. You have read and understood the specific section(s) of the spec file(s)
3. You can clearly reference exactly which spec file and section you are implementing

If no suitable specification exists:
→ Do NOT write any code.
→ Instead, propose a new or updated file in `specs/`
→ Explain what should be added and why
→ Wait for confirmation before proceeding to code

## Traceability & Reasoning Rules

Before writing any code or suggesting changes, you **must**:

1. State clearly which file(s) in `specs/` you are implementing or extending  
   Example:  
   "Implementing the input validation for content_publish as defined in specs/technical.md section 2"

2. Explain your plan in plain English **before** showing any code  
   Example:  
   "Plan:  
   1. Define Pydantic model matching the JSON schema  
   2. Add field validators for enum values and ranges  
   3. Write two test cases: valid minimal input + invalid platform"

3. Always prefer:
   - Explicit failure (raise meaningful exceptions) over silent errors
   - Type hints (Python 3.10+ style)
   - Pydantic v2 for all data models / contracts
   - Docstrings on public functions/classes
   - Tests written before or immediately after implementation

## Forbidden Patterns

Do NOT suggest or generate code that:

- Makes direct HTTP/API calls outside of MCP servers
- Uses monolithic agent logic (only swarm: Planner/Worker/Judge)
- Hard-codes secrets, API keys, wallet addresses, or credentials
- Ignores tenant_id filtering in queries
- Bypasses Judge validation for publishing, transactions, or sensitive content
- Skips tests or writes tests after the fact
- Uses outdated patterns (Flask, pydantic v1 validators, click for new CLI code)

## Preferred Technologies & Patterns (2026 context)

- Python 3.12+
- uv (preferred) or poetry for dependency management
- Pydantic v2 (strict mode encouraged)
- pytest + pytest-asyncio + ruff + mypy
- Redis for queues & ephemeral state
- PostgreSQL for transactional data
- Weaviate for semantic memory / RAG
- MCP SDK for all external integrations
- Coinbase AgentKit for on-chain actions
- Async-first where appropriate (asyncio / anyio)

## When in doubt

Ask one of these clarifying questions:

- "Which spec file defines this behavior?"
- "Should I first create or update a specification in specs/?"
- "Does this change affect multi-tenancy, budget guards, HITL, or disclosure rules?"

If unclear → do not proceed with code. Suggest spec clarification first.

## Quick Checklist Before Any Code

1. Does a spec exist in `specs/` that covers this?
2. Have I stated which spec section I'm implementing?
3. Have I explained my plan in English?
4. Am I following the swarm pattern?
5. Are external calls going through MCP?
6. Is tenant_id enforced where needed?
7. Will this be auditable / traceable?

If any answer is "no" → stop and fix it.

Follow these rules strictly to keep Project Chimera maintainable, safe, and spec-driven.