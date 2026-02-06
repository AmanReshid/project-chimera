# Project Chimera

**Agent factory for autonomous AI influencers**  
Persistent digital agents that perceive trends, plan content strategies, generate multimodal assets, publish across social platforms, and perform lightweight **on-chain commerce**.

Built on:

- **Model Context Protocol (MCP)** — universal interface to the external world  
- **Hierarchical swarm orchestration** (Planner / Worker / Judge pattern)  
- **Strict spec-driven governance** for safe, scalable multi-agent systems

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourusername/project-chimera/actions/workflows/main.yml/badge.svg)](https://github.com/yourusername/project-chimera/actions)

## What is Project Chimera?

Chimera is infrastructure for creating and running **autonomous AI influencers** — persistent, goal-directed digital entities that operate 24/7 without constant human scripting.

These agents can:

- Perceive real-time trends, mentions, news and audience signals  
- Plan multi-channel content strategies using hierarchical swarms  
- Generate consistent text captions, images and short videos  
- Publish, reply and engage natively on social platforms  
- Handle basic **on-chain commerce** (receive payments, pay for generation, transfer revenue)

The project is deliberately built around **three pillars**:

1. **MCP** — all external communication goes through Model Context Protocol servers  
2. **Swarm pattern** — Planner decomposes goals → Workers execute in parallel → Judge validates & enforces rules  
3. **Spec-driven governance** — `specs/` is the single source of truth; no code without a spec reference

## Current State (February 2026)

- Core runtime skills defined with strict Pydantic interfaces  
- TDD contract tests in place (model validation passes, execution tests intentionally fail/skipped)  
- Spec-Driven Development enforced  
- Basic CI (tests + linting on push/PR)  
- Makefile + Docker for reproducible environment  
- Developer tooling strategy outlined (MCP servers for dev productivity)
