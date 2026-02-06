# Tooling & MCP Developer Tools Strategy  
Project Chimera – Research & Planning Document

Last updated: 2026-02-06

## 1. Purpose

This document outlines the **developer-facing MCP servers** that help the engineering team (and AI assistants) work efficiently inside the codebase.

These are **not** runtime tools for Chimera agents — they are development productivity tools.

## 2. Selected Developer MCP Servers

| MCP Server Name       | Purpose                                      | Transport     | Status       | Notes / Source |
|-----------------------|----------------------------------------------|---------------|--------------|----------------|
| `filesystem-mcp`      | Read, write, list, search files in workspace | stdio / local | Planned      | Essential for IDE agents to edit files |
| `git-mcp`             | Git operations: status, diff, commit, branch, push | stdio / local | Planned      | Enables AI to propose commits & branches |
| `grep-mcp`            | Search codebase with grep-like patterns      | stdio         | Planned      | Fast way to find existing implementations |
| `shell-mcp`           | Run safe shell commands (make, uv, pytest…)  | stdio         | Planned (restricted) | Limited to whitelisted commands |
| `cursor-mcp`          | Interact with Cursor IDE features (if available) | stdio      | Optional     | May not be needed if using native Cursor rules |
| `weaviate-mcp`        | Query project documentation & specs (Weaviate) | http/sse   | Nice-to-have | Useful for semantic search over specs/ & docs/ |

## 3. Recommended Initial Setup (MVP)

Start with these three core developer MCP servers:

1. **`filesystem-mcp`**  
   - Allows reading and writing files safely within the project root  
   - Critical for AI agents to propose spec updates or code changes

2. **`git-mcp`**  
   - Operations: `status`, `diff`, `add`, `commit`, `branch`, `push`  
   - Security: only allow commits with conventional commit messages  
   - Branch naming convention: `ai/feature/<description>`

3. **`grep-mcp`** or **`search-mcp`**  
   - Quick codebase search (filename, content)  
   - Helps AI assistants find existing patterns before suggesting new code

## 4. Security & Safety Rules for Developer MCPs

- **No destructive commands** by default (rm, git reset --hard, etc.)
- **All write operations** must be confirmed by human or follow strict naming rules
- **Rate limiting** on heavy operations (e.g., full-text search)
- **Logging** of all MCP calls made by AI agents

## 5. Developer Tooling & MCP Servers Strategy  
Project Chimera – Development Environment


This document lists the **MCP servers** that are useful **during development** — i.e. tools that help the developer (human + AI coding assistant) work efficiently inside the codebase.

These are **not** the runtime MCP servers that Chimera agents will use to interact with Twitter, image generation, wallets, etc.  
Those will be documented separately (most likely in `specs/mcp_servers_runtime.md` or similar).

## Selected Developer MCP Servers

| Server name          | Purpose                                                                 | Priority | Recommended implementation / notes                               | Status      |
|----------------------|-------------------------------------------------------------------------|----------|-------------------------------------------------------------------|-------------|
| `filesystem-mcp`     | Read, write, list, search, create/delete files in the workspace         | ★★★★★    | Essential. Restrict to project root only.                         | Must-have   |
| `git-mcp`            | Git operations: status, diff, add, commit, branch, push, log            | ★★★★☆    | Enables AI to propose commits / branches without manual copy-paste | High        |
| `search-mcp` / `grep-mcp` | Fast full-text / filename search across the codebase                | ★★★★     | Helps AI find existing code patterns, similar functions, etc.     | High        |
| `tree-mcp`           | Show directory structure (like `tree` or `ls -R`)                       | ★★★      | Very useful when AI loses track of folder layout                  | Medium      |
| `shell-mcp`          | Run whitelisted shell commands (make, pytest, uv, ruff, git status…)    | ★★★      | Restricted whitelist only – no rm, pip install, sudo, etc.        | Medium      |
| `pytest-mcp`         | Run specific pytest commands / markers / files                          | ★★       | Nice-to-have for TDD workflows                                    | Optional    |

**Minimum recommended set to start (MVP):**

1. `filesystem-mcp`  
2. `git-mcp`  
3. `search-mcp` / `grep-mcp`

These three give the biggest productivity boost for AI-assisted development.

## Recommended Setup & Configuration (early 2026)

### 1. filesystem-mcp (highest priority)

- **Purpose**: Let the AI read specs/, write to skills/, create test files, etc.
- **Security constraints**:
  - Root path = current project directory only
  - No writes outside the repo
  - Optional: block writes to `.git/`, `venv/`, `__pycache__/`
- **Typical launch command**:
  ```bash
  mcp-server-filesystem --root .