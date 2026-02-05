# Project Chimera – Meta Specification

## 1. Project Vision

Project Chimera is an infrastructure platform designed to operate a scalable fleet of **autonomous AI-driven virtual influencers**.

These agents should be capable of:

- perceiving digital signals (trends, audience reactions, news, mentions)
- reasoning about campaign goals and current context
- planning multi-step content strategies
- generating consistent multimodal content (text, images, short-form video)
- publishing and engaging across social platforms
- performing limited economic actions (receiving payments, paying for services, transferring funds)

The system is intentionally built around three strong architectural foundations:

1. Model Context Protocol (MCP) – universal interface for all external data and actions
2. Hierarchical FastRender-style swarm (Planner → parallel Workers → Judge)
3. Agentic Commerce via non-custodial wallets and budget-aware governance

## 2. Core Constraints (Non-negotiable)

- **All external interactions** (social platforms, databases, blockchains, generation models) **MUST** go through MCP servers — never directly from core agent logic.
- **Strong separation** between perception, planning, execution, and validation.
- **Human safety override** remains mandatory for:
  - content confidence < 0.70
  - sensitive topic detection (politics, health advice, financial/legal claims)
  - budget limit violations
  - character consistency validation failures
- **Full disclosure**: All published content must use platform-native AI labels when available. Agents must clearly state they are AI when directly asked.
- **Economic safety**: Every cost-incurring action requires prior balance check + budget guardrail enforcement.
- **Multi-tenancy isolation**: Memory, wallets, content history, and campaigns are strictly separated per agent/tenant.

## 3. Scale & Performance Targets (MVP → v1)

- Support 1,000+ concurrently active agents
- High-priority interaction latency ≤ 10 seconds (excluding HITL time)
- Tolerate social API rate limiting, temporary outages, and model degradation gracefully

## 4. Development & Governance Rules

- This `specs/` directory is the **single source of truth** for intent.
- No implementation code should be written without a corresponding, up-to-date specification.
- All public interfaces **must** be described with JSON schemas or Pydantic-style models.
- Tests must exist (and fail) before implementation begins (TDD boundary).
- Every change should improve **traceability**, **safety**, or **scalability**.

