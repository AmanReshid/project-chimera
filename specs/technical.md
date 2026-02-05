# Technical Specification – Core Contracts & Data Models

## 1. Core Task Message (Planner → Worker)

```json
{
  "task_id":          "uuidv4",
  "parent_task_id":   "uuidv4 | null",
  "task_type":        "string enum",
  "priority":         "high | medium | low",
  "created_at":       "ISO8601",
  "status":           "pending | assigned | working | completed | failed | cancelled",
  "context": {
    "agent_id":           "string",
    "campaign_id":        "string | null",
    "goal_summary":       "string",
    "persona_summary":    "object (name, voice_traits, directives)",
    "required_resources": ["array<mcp://uri>"],
    "required_tools":     ["array<tool_name>"],
    "max_cost_usdc":      "number | null",
    "soft_deadline":      "ISO8601 | null"
  },
  "input_artifact_ids":  ["array<previous task_ids>"],
  "assigned_worker_id":  "string | null"
}