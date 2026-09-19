# Agentic Data Analyst

> Governed agentic analytics reference architecture for turning
> natural-language questions into controlled analytical workflows.

**Focus:** Agentic AI · Text-to-SQL · Tool Use · Governance · Data Analytics

## Architecture

```text
                     USER
                      │
                      ▼
             Natural Language Query
                      │
                      ▼
              ┌──────────────┐
              │    Planner   │
              └──────┬───────┘
                     │
                     ▼
              Schema Discovery
                     │
                     ▼
               LLM Provider
                     │
                     ▼
               Proposed SQL
                     │
                     ▼
             ┌───────────────┐
             │ Policy Engine │
             └───────┬───────┘
                     │
                ALLOW / BLOCK
                     │
                     ▼
            Read-Only Database
                     │
                     ▼
               Result Limit
                     │
                     ▼
              Agent Synthesis
                     │
                     ▼
           Structured Response
                     │
                     ▼
                Audit Trail
```

The language model proposes actions; it does not own authorization. SQL passes through deterministic application policy before execution, and the database is opened with read-only access. This creates separate reasoning, authorization, and execution boundaries.

## Key Engineering Areas

- Explicit agent planning
- Schema-aware SQL generation
- Deterministic SQL validation
- Read-only database execution
- Tool-level authorization boundaries
- Structured agent state
- Auditable execution
- Provider-independent LLM interface
