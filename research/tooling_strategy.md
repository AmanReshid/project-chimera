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

## 5. Next Steps

1. Install & configure `filesystem-mcp` and `git-mcp` locally
2. Document exact endpoints/tools in `docs/developer_mcp_setup.md`
3. Test basic workflow: AI proposes spec change → writes file → commits
