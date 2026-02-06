# Skill: wallet_check_balance

## Purpose

Retrieve the current balance of the agent's non-custodial wallet (primarily USDC on Base or Ethereum).  
Used as a safety gate before any cost-incurring action (image/video generation, publishing, transfers).

## Responsibilities

- Query wallet balance via Coinbase AgentKit / MCP
- Convert/format balances if multiple tokens are tracked
- Return usable confirmed balance + optional pending amount

## Safety & Governance Notes

- **Read-only** skill — safe to call frequently
- Should be cached short-term (Redis) to reduce API calls
- Low balance should trigger Planner to pause expensive workflows
- Never exposes private keys or signs transactions

## Input / Output Contract

See `interface.py`

## Status

- Interface: complete
- Implementation: stub
- Tests: in `tests/test_wallet_check_balance.py`