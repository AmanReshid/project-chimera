# Database Schema – Project Chimera

**File status**  
- Version: 0.2  
- Status: Draft → Planning  
- Last updated: 2026-02-06  
- Owner: Architecture Lead  

## 1. Purpose of this document

This file defines the **logical database schema** for Project Chimera — both the **transactional PostgreSQL database** and the **semantic memory layer (Weaviate)**.

It serves as:

- the single source of truth for data modeling decisions
- reference for developers writing migrations, queries, or ORM models
- foundation for audit, compliance, and observability requirements

## 2. Design Goals & Principles

1. **Strong audit trail** — every published post, generated asset, and financial movement must be traceable
2. **Multi-tenancy from day one** — strict logical separation via `tenant_id`
3. **Performance for dashboard & analytics** — reasonable indexing for common queries
4. **Simplicity first** — avoid premature optimization and complex partitioning
5. **Compliance readiness** — support for EU AI Act (provenance, transparency)
6. **Cost-awareness** — track generation costs and link to transactions
7. **Separation of concerns**  
   - PostgreSQL: structured, relational, audit-critical data  
   - Weaviate: semantic memory, long-term RAG, trend clustering

## 3. PostgreSQL – Main Tables

### 3.1 agents (virtual influencers)

```sql
CREATE TABLE agents (
    id              TEXT PRIMARY KEY,               -- e.g. "chimera-eth-fashion-001"
    tenant_id       TEXT NOT NULL,                  -- multi-tenant isolation
    display_name    TEXT NOT NULL,
    description     TEXT,
    wallet_address  TEXT UNIQUE NOT NULL,           -- non-custodial Coinbase wallet
    status          TEXT NOT NULL DEFAULT 'active', -- active | paused | error | archived
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_active_at  TIMESTAMPTZ,
    last_heartbeat  TIMESTAMPTZ,

    CONSTRAINT valid_status CHECK (status IN ('active', 'paused', 'error', 'archived'))
);